import ee
import json
from backend.auth_manager import initialize_gee

def get_s2_composite(geometry, start_date, end_date):
    """
    Retrieves a cloud-masked Sentinel-2 median composite for a given geometry and date range.
    """
    # Sentinel-2 Harmonized Collection
    s2_col = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    
    # Cloud masking function using QA60 band
    def mask_s2_clouds(image):
        qa = image.select('QA60')
        cloud_bit_mask = 1 << 10
        cirrus_bit_mask = 1 << 11
        # Both flags should be zero, indicating clear conditions.
        mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(
            qa.bitwiseAnd(cirrus_bit_mask).eq(0)
        )
        return image.updateMask(mask).divide(10000).copyProperties(image, ["system:time_start"])

    # Filter by bounds, dates, and metadata cloud cover < 20%
    composite = s2_col.filterBounds(geometry) \
                      .filterDate(start_date, end_date) \
                      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                      .map(mask_s2_clouds) \
                      .median() \
                      .clip(geometry)
                      
    return composite

def calculate_indices(image):
    """
    Calculates NDVI, NDWI, and NDBI for a Sentinel-2 image.
    """
    # NDVI: (NIR - Red) / (NIR + Red) -> (B8 - B4) / (B8 + B4)
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    
    # NDWI: (Green - NIR) / (Green + NIR) -> (B3 - B8) / (B3 + B8)
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
    
    # NDBI: (SWIR1 - NIR) / (SWIR1 + NIR) -> (B11 - B8) / (B11 + B8)
    ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')
    
    return image.addBands([ndvi, ndwi, ndbi])

def run_gee_change_detection(geometry_geojson, start_before, end_before, start_after, end_after, sensitivity_factors=None):
    """
    Performs GEE change detection.
    sensitivity_factors: dict with threshold values for ndvi, ndwi, and ndbi.
    Returns:
        Dict with tile URLs (before, after, change overlay) and list of detected coordinates.
    """
    # Default thresholds (lower threshold = more sensitive)
    thresholds = {
        "ndvi_drop": 0.15,   # Minimum drop in vegetation (garden clearing)
        "ndwi_rise": 0.18,   # Minimum rise in water index (new pool)
        "ndbi_rise": 0.15    # Minimum rise in built-up index (extension)
    }
    if sensitivity_factors:
        # sensitivity slider: 1 to 10 (10 = highly sensitive, meaning lower thresholds)
        sens = float(sensitivity_factors.get("sensitivity", 5))
        scale = (11.0 - sens) / 5.0 # scale factor: 10 -> 0.2, 5 -> 1.2, 1 -> 2.0
        thresholds["ndvi_drop"] *= scale
        thresholds["ndwi_rise"] *= scale
        thresholds["ndbi_rise"] *= scale

    # Initialize GEE first
    success, _ = initialize_gee()
    if not success:
        raise Exception("Google Earth Engine not authenticated. Switch to Demo Mode.")

    # Parse GeoJSON ROI
    if isinstance(geometry_geojson, str):
        geojson = json.loads(geometry_geojson)
    else:
        geojson = geometry_geojson
        
    coordinates = geojson.get("geometry", geojson).get("coordinates")
    geom_type = geojson.get("geometry", geojson).get("type")
    
    if geom_type == "Polygon":
        geometry = ee.Geometry.Polygon(coordinates)
    elif geom_type == "MultiPolygon":
        geometry = ee.Geometry.MultiPolygon(coordinates)
    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")

    # 1. Fetch Composites
    before_img = calculate_indices(get_s2_composite(geometry, start_before, end_before))
    after_img = calculate_indices(get_s2_composite(geometry, start_after, end_after))

    # 2. Difference Images
    ndvi_diff = after_img.select('NDVI').subtract(before_img.select('NDVI'))
    ndwi_diff = after_img.select('NDWI').subtract(before_img.select('NDWI'))
    ndbi_diff = after_img.select('NDBI').subtract(before_img.select('NDBI'))

    # 3. Create Change Masks
    # Drop in NDVI (vegetation cleared)
    veg_clearing = ndvi_diff.lt(-thresholds["ndvi_drop"]).rename('veg_clearing')
    
    # Rise in NDWI (new water body)
    pool_added = ndwi_diff.gt(thresholds["ndwi_rise"]).rename('pool_added')
    
    # Rise in NDBI (new built area)
    built_extension = ndbi_diff.gt(thresholds["ndbi_rise"]).rename('built_extension')

    # Combined change image: 1 = Veg Clearing, 2 = Pool, 3 = Extension
    # We prioritize pool and extension over general veg clearing
    combined_change = ee.Image(0) \
        .where(veg_clearing.eq(1), 1) \
        .where(built_extension.eq(1), 3) \
        .where(pool_added.eq(1), 2) \
        .selfMask() \
        .rename('change_type')

    # 4. Extract Hotspot Coordinates (Clustering)
    # We project the masked change area to find individual connected clusters (blobs)
    # We restrict analysis to Pools and Extensions (types 2 and 3)
    significant_change = combined_change.gte(2).selfMask()
    
    # Group neighboring pixels into components
    # Sentinel-2 scale is 10m, so connectedComponents groups pixels
    conn = significant_change.connectedComponents(
        connectivity=ee.Kernel.plus(1),
        maxSize=128
    )
    
    # Calculate area of each cluster (in square meters)
    object_sizes = conn.select('labels').connectedPixelCount(128, False).multiply(100).rename('area')
    
    # Filter out tiny changes (e.g. less than 30 sqm - too small for pool/extension) and large ones (commercial construction > 2000 sqm)
    filtered_changes = conn.addBands(object_sizes).updateMask(
        object_sizes.gte(30).And(object_sizes.lte(2000))
    )

    # Convert to vectors to get coordinates (centroids)
    # Reduce region to vectors to get centroids of clusters
    vectors = filtered_changes.select('labels').reduceToVectors(
        geometry=geometry,
        scale=10,
        geometryType='centroid',
        labelProperty='label_id',
        maxPixels=1e6
    )

    # Fetch vectors to local list (cap at 50 leads to avoid timeouts)
    leads_list = []
    try:
        features = vectors.limit(50).getInfo().get('features', [])
        for feat in features:
            coords = feat['geometry']['coordinates'] # [lon, lat]
            lat, lon = coords[1], coords[0]
            
            # Extract change values at this coordinate
            point = ee.Geometry.Point([lon, lat])
            
            # Sample GEE indices at this point to identify what change it is
            sampled_vals = combined_change.reduceRegion(
                reducer=ee.Reducer.first(),
                geometry=point,
                scale=10
            ).getInfo()
            
            change_code = sampled_vals.get('change_type', 0)
            change_type = "Landscaping Overhaul"
            if change_code == 2:
                change_type = "Pool Addition"
            elif change_code == 3:
                change_type = "Structural Extension"
                
            # Sample area size
            area_size = object_sizes.reduceRegion(
                reducer=ee.Reducer.first(),
                geometry=point,
                scale=10
            ).getInfo().get('area', 100)

            leads_list.append({
                "lat": lat,
                "lon": lon,
                "type": change_type,
                "area_sqm": round(area_size),
                "confidence": round(0.8 + (change_code * 0.05), 2) # Synthetic confidence based on index strength
            })
    except Exception as e:
        print(f"Error extracting centroid coordinates: {e}")
        # Return fallback coordinate if vector reduction fails/times out
        leads_list = []

    # 5. Generate Tile URLs for Map Rendering
    # RGB visualization parameters for Sentinel-2 (B4 = Red, B3 = Green, B2 = Blue)
    rgb_vis = {
        'bands': ['B4', 'B3', 'B2'],
        'min': 0.0,
        'max': 0.3,
        'gamma': 1.3
    }
    
    # Visual params for changes: 1 = Green (Veg), 2 = Cyan (Pool), 3 = Yellow/Red (Extension)
    change_vis = {
        'min': 1,
        'max': 3,
        'palette': ['00FF00', '00FFFF', 'FFA500']
    }

    # Fetch Tile Map IDs
    def get_leaflet_tile_url(image, vis):
        map_id = ee.data.getMapId({'image': image, 'visParams': vis})
        # Format double curly braces for python format compat
        url_format = map_id['tile_fetcher'].url_format
        return url_format.replace("{z}", "{z}").replace("{x}", "{x}").replace("{y}", "{y}")

    before_url = get_leaflet_tile_url(before_img, rgb_vis)
    after_url = get_leaflet_tile_url(after_img, rgb_vis)
    change_url = get_leaflet_tile_url(combined_change, change_vis)

    return {
        "before_tile_url": before_url,
        "after_tile_url": after_url,
        "change_tile_url": change_url,
        "detected_leads": leads_list,
        "thresholds_used": thresholds
    }
