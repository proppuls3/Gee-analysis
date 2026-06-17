import json
from datetime import datetime

# Expanded database covering every major villa cluster in the UAE and their Developers
COMMUNITIES = {
    # --- DUBAI ---
    "Arabian Ranches (Dubai)": {
        "center": [25.044, 55.280],
        "zoom": 14,
        "developer": "Emaar Properties",
        "description": "Premium established suburban villa community. Characterized by spacious plots, pool additions, and roof extensions.",
        "stats": {
            "total_villas": 4120,
            "detected_renovations_3yr": 284,
            "avg_pool_roi": 86.6,
            "avg_extension_roi": 77.1,
            "avg_value_lift_aed": 850000,
            "top_renovation_type": "Pool & Landscaping"
        },
        "leads": [
            {
                "id": "AR-VILLA-382",
                "address": "Saheel Street 3, Villa 42",
                "coordinates": [25.0465, 55.2810],
                "renovation_type": "Pool Addition",
                "gee_detected_date": "2023-11-12",
                "gee_confidence": 0.94,
                "timeline": {
                    "purchase_dld": { "date": "2021-04-18", "price_aed": 4200000, "price_per_sqft": 875, "bua_sqft": 4800, "plot_sqft": 7500 },
                    "permit": { "id": "DM-2023-P8829", "date": "2023-08-05", "type": "Private Swimming Pool Construction", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2023-11-12", "description": "NDWI index spike from -0.15 to +0.48. High certainty of water body addition." },
                    "resale_dld": { "date": "2025-02-14", "price_aed": 5850000, "price_per_sqft": 1218, "market_gain_baseline_pct": 22.0, "actual_gain_pct": 39.3, "renovation_value_lift_aed": 726000, "estimated_renovation_cost_aed": 150000, "net_renovation_profit_aed": 576000, "renovation_roi_pct": 384.0 }
                }
            },
            {
                "id": "AR-VILLA-112",
                "address": "Alvorada Street 1, Villa 15",
                "coordinates": [25.0425, 55.2785],
                "renovation_type": "Structural Extension",
                "gee_detected_date": "2022-05-24",
                "gee_confidence": 0.89,
                "timeline": {
                    "purchase_dld": { "date": "2020-09-15", "price_aed": 5500000, "price_per_sqft": 948, "bua_sqft": 5800, "plot_sqft": 9200 },
                    "permit": { "id": "DM-2022-B1293", "date": "2021-12-10", "type": "Villa Extension - Additional Room & Pergola", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2022-05-24", "description": "NDBI index increase from 0.05 to 0.32. Increase in concrete built-up surface area." },
                    "resale_dld": { "date": "2024-10-08", "price_aed": 8200000, "price_per_sqft": 1413, "market_gain_baseline_pct": 28.0, "actual_gain_pct": 49.1, "renovation_value_lift_aed": 1160000, "estimated_renovation_cost_aed": 350000, "net_renovation_profit_aed": 810000, "renovation_roi_pct": 231.4 }
                }
            }
        ]
    },
    "Palm Jumeirah (Dubai)": {
        "center": [25.120, 55.135],
        "zoom": 14,
        "developer": "Nakheel",
        "description": "World-famous luxury man-made island. High-density beachfront frond villas undergoing ultra-luxury rebuilds and modern pool deck upgrades.",
        "stats": {
            "total_villas": 1850,
            "detected_renovations_3yr": 168,
            "avg_pool_roi": 140.0,
            "avg_extension_roi": 216.7,
            "avg_value_lift_aed": 4200000,
            "top_renovation_type": "Structural Extension & Facade Rebuild"
        },
        "leads": [
            {
                "id": "PJ-VILLA-042",
                "address": "Frond B, Beach Villa 14",
                "coordinates": [25.1238, 55.1345],
                "renovation_type": "Structural Extension",
                "gee_detected_date": "2023-06-18",
                "gee_confidence": 0.95,
                "timeline": {
                    "purchase_dld": { "date": "2020-11-12", "price_aed": 18500000, "price_per_sqft": 2720, "bua_sqft": 6800, "plot_sqft": 12000 },
                    "permit": { "id": "DM-2022-EXT-883", "date": "2022-09-02", "type": "Full Facade Modification & Ground+First Floor Extension", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2023-06-18", "description": "NDBI jump from 0.12 to 0.45. Structural modifications indicating complete demolition of the rear wall and addition of 120 sqm BUA." },
                    "resale_dld": { "date": "2024-12-20", "price_aed": 34000000, "price_per_sqft": 5000, "market_gain_baseline_pct": 35.0, "actual_gain_pct": 83.8, "renovation_value_lift_aed": 9025000, "estimated_renovation_cost_aed": 1500000, "net_renovation_profit_aed": 7525000, "renovation_roi_pct": 501.7 }
                }
            },
            {
                "id": "PJ-VILLA-108",
                "address": "Frond D, Beach Villa 28",
                "coordinates": [25.1205, 55.1378],
                "renovation_type": "Pool Addition",
                "gee_detected_date": "2022-08-04",
                "gee_confidence": 0.93,
                "timeline": {
                    "purchase_dld": { "date": "2021-02-28", "price_aed": 16200000, "price_per_sqft": 2571, "bua_sqft": 6300, "plot_sqft": 10500 },
                    "permit": { "id": "DM-2021-P9901", "date": "2021-12-14", "type": "Infinity Pool Construction and Beach Retaining Wall", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2022-08-04", "description": "NDWI spike from -0.11 to +0.55. High reflection matching water profile." },
                    "resale_dld": { "date": "2024-04-12", "price_aed": 26500000, "price_per_sqft": 4206, "market_gain_baseline_pct": 40.0, "actual_gain_pct": 63.6, "renovation_value_lift_aed": 3820000, "estimated_renovation_cost_aed": 300000, "net_renovation_profit_aed": 3520000, "renovation_roi_pct": 1173.3 }
                }
            }
        ]
    },
    "Jumeirah Islands (Dubai)": {
        "center": [25.068, 55.145],
        "zoom": 14,
        "developer": "Nakheel",
        "description": "Prestigious self-contained community of 50 islands. Expat-favorite characterized by significant plot size upgrades and landscaping modifications.",
        "stats": {
            "total_villas": 736,
            "detected_renovations_3yr": 82,
            "avg_pool_roi": 95.0,
            "avg_extension_roi": 145.5,
            "avg_value_lift_aed": 2400000,
            "top_renovation_type": "Full Villa Modernization"
        },
        "leads": [
            {
                "id": "JI-VILLA-012",
                "address": "Cluster 4, Villa 12",
                "coordinates": [25.0685, 55.1448],
                "renovation_type": "Structural Extension",
                "gee_detected_date": "2023-03-15",
                "gee_confidence": 0.92,
                "timeline": {
                    "purchase_dld": { "date": "2021-01-20", "price_aed": 8500000, "price_per_sqft": 1545, "bua_sqft": 5500, "plot_sqft": 10200 },
                    "permit": { "id": "DM-2022-JI-443", "date": "2022-10-18", "type": "Internal Modification and Extension of Living Area", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2023-03-15", "description": "NDBI build-up increase. High concrete reflectivity. ~65 sqm extension detected." },
                    "resale_dld": { "date": "2024-09-10", "price_aed": 14200000, "price_per_sqft": 2581, "market_gain_baseline_pct": 32.0, "actual_gain_pct": 67.1, "renovation_value_lift_aed": 2984000, "estimated_renovation_cost_aed": 600000, "net_renovation_profit_aed": 2384000, "renovation_roi_pct": 397.3 }
                }
            }
        ]
    },
    "Dubai Hills Estate (Dubai)": {
        "center": [25.101, 55.265],
        "zoom": 13,
        "developer": "Emaar Properties & Meraas",
        "description": "Modern master development. Features luxury shell-and-core villa plots in Parkway Hills & Parkway Vistas where owners customize massive mansions.",
        "stats": {
            "total_villas": 2100,
            "detected_renovations_3yr": 192,
            "avg_pool_roi": 110.0,
            "avg_extension_roi": 180.0,
            "avg_value_lift_aed": 3100000,
            "top_renovation_type": "Mansion Fit-out"
        },
        "leads": [
            {
                "id": "DH-VILLA-088",
                "address": "Parkway Vistas, Villa 18",
                "coordinates": [25.1032, 55.2685],
                "renovation_type": "Pool Addition",
                "gee_detected_date": "2024-02-18",
                "gee_confidence": 0.96,
                "timeline": {
                    "purchase_dld": { "date": "2022-05-12", "price_aed": 19000000, "price_per_sqft": 2375, "bua_sqft": 8000, "plot_sqft": 12500 },
                    "permit": { "id": "DM-2023-DH-093", "date": "2023-09-01", "type": "Swimming Pool Construction and Pergola Fitout", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2024-02-18", "description": "NDWI rise matching standard private pool profile. NDVI vegetation drop during pool excavation." },
                    "resale_dld": { "date": "2025-04-30", "price_aed": 25500000, "price_per_sqft": 3187, "market_gain_baseline_pct": 20.0, "actual_gain_pct": 34.2, "renovation_value_lift_aed": 2700000, "estimated_renovation_cost_aed": 400000, "net_renovation_profit_aed": 2300000, "renovation_roi_pct": 575.0 }
                }
            }
        ]
    },
    "Jumeirah 1 (Commercial Villas)": {
        "center": [25.215, 55.258],
        "zoom": 14,
        "developer": "Private / DM Zoning",
        "description": "High-traffic district. Major hub for residential-to-commercial villa conversions (clinics, salons, restaurants).",
        "stats": {
            "total_villas": 1150,
            "detected_renovations_3yr": 105,
            "avg_pool_roi": 0.0,
            "avg_extension_roi": 280.0,
            "avg_value_lift_aed": 5500000,
            "top_renovation_type": "Commercial Fit-Out & Facade"
        },
        "leads": [
            {
                "id": "JUM1-COM-88",
                "address": "Al Wasl Road, Villa 412",
                "coordinates": [25.2178, 55.2612],
                "renovation_type": "Commercial Conversion",
                "gee_detected_date": "2024-02-14",
                "gee_confidence": 0.98,
                "timeline": {
                    "purchase_dld": { "date": "2023-01-10", "price_aed": 12000000, "price_per_sqft": 1500, "bua_sqft": 8000, "plot_sqft": 10000 },
                    "permit": { "id": "DM-2023-COM-99", "date": "2023-08-05", "type": "Change of Use: Residential to Commercial (Clinic)", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2024-02-14", "description": "NDBI spike indicating major facade reconstruction and expanded parking area." },
                    "ded_license": { "date": "2024-04-01", "name": "Aesthetics Dental Clinic LLC", "activity": "Specialized Medical Clinic", "license_no": "DED-883921" },
                    "google_maps_pin": { "date": "2024-05-15", "name": "Aesthetics Dental Clinic", "rating": "New", "url": "https://maps.google.com" },
                    "resale_dld": { "date": "2025-01-20", "price_aed": 22000000, "price_per_sqft": 2750, "market_gain_baseline_pct": 15.0, "actual_gain_pct": 83.3, "renovation_value_lift_aed": 8200000, "estimated_renovation_cost_aed": 2500000, "net_renovation_profit_aed": 5700000, "renovation_roi_pct": 228.0 }
                }
            }
        ]
    },
    "Jumeirah Golf Estates (Dubai)": {
        "center": [25.025, 55.195],
        "zoom": 14,
        "developer": "Jumeirah Golf Estates / Nakheel",
        "description": "High-end residential golf community. Characterized by customizable luxury villas backing onto world-class golf courses (Earth & Fire).",
        "stats": {
            "total_villas": 1500,
            "detected_renovations_3yr": 94,
            "avg_pool_roi": 75.0,
            "avg_extension_roi": 120.0,
            "avg_value_lift_aed": 1900000,
            "top_renovation_type": "Backyard Golf-View Landscaping"
        },
        "leads": [
            {
                "id": "JGE-VILLA-209",
                "address": "Whispering Pines, Villa 4",
                "coordinates": [25.0235, 55.1968],
                "renovation_type": "Landscaping Overhaul",
                "gee_detected_date": "2023-09-12",
                "gee_confidence": 0.85,
                "timeline": {
                    "purchase_dld": { "date": "2021-08-04", "price_aed": 6800000, "price_per_sqft": 1416, "bua_sqft": 4800, "plot_sqft": 8200 },
                    "permit": { "id": "DM-2023-JGE-882", "date": "2023-04-10", "type": "Golf Course Facing External Landscaping & BBQ Area", "issuer": "Dubai Municipality" },
                    "gee_change": { "date": "2023-09-12", "description": "NDVI shift indicating lawn modifications. NDBI slight increase representing a brick barbecue patio structure." },
                    "resale_dld": { "date": "2025-01-20", "price_aed": 9200000, "price_per_sqft": 1916, "market_gain_baseline_pct": 25.0, "actual_gain_pct": 35.3, "renovation_value_lift_aed": 700000, "estimated_renovation_cost_aed": 250000, "net_renovation_profit_aed": 450000, "renovation_roi_pct": 180.0 }
                }
            }
        ]
    },

    # --- ABU DHABI ---
    "Yas Island (Abu Dhabi)": {
        "center": [24.498, 54.605],
        "zoom": 13,
        "developer": "Aldar Properties",
        "description": "Abu Dhabi's entertainment hub. Subdivisions like Yas Acres feature premium modern townhouses and villas popular for extension additions.",
        "stats": {
            "total_villas": 2800,
            "detected_renovations_3yr": 142,
            "avg_pool_roi": 65.4,
            "avg_extension_roi": 105.0,
            "avg_value_lift_aed": 650000,
            "top_renovation_type": "Garden Pools"
        },
        "leads": [
            {
                "id": "YAS-VILLA-042",
                "address": "Yas Acres, Royal Oak Villa 21",
                "coordinates": [24.5015, 54.6088],
                "renovation_type": "Pool Addition",
                "gee_detected_date": "2024-04-05",
                "gee_confidence": 0.91,
                "timeline": {
                    "purchase_dld": { "date": "2022-01-15", "price_aed": 3900000, "price_per_sqft": 928, "bua_sqft": 4200, "plot_sqft": 6800 },
                    "permit": { "id": "ADM-2023-YAS-4412", "date": "2023-11-20", "type": "Villa Swimming Pool License", "issuer": "Abu Dhabi Municipality" },
                    "gee_change": { "date": "2024-04-05", "description": "NDWI rise. Successful pool signature overlay. NDVI reduction in southern quadrant." },
                    "resale_dld": { "date": "2025-10-18", "price_aed": 5300000, "price_per_sqft": 1261, "market_gain_baseline_pct": 18.0, "actual_gain_pct": 35.9, "renovation_value_lift_aed": 698000, "estimated_renovation_cost_aed": 140000, "net_renovation_profit_aed": 558000, "renovation_roi_pct": 398.6 }
                }
            }
        ]
    },
    "Khalifa City (Abu Dhabi)": {
        "center": [24.415, 54.575],
        "zoom": 13,
        "developer": "Private / Various Master Developers",
        "description": "Massive residential zone with huge plots. Very common for Emirati families to construct supplementary outbuildings, driver rooms, or majlises.",
        "stats": {
            "total_villas": 6200,
            "detected_renovations_3yr": 418,
            "avg_pool_roi": 45.0,
            "avg_extension_roi": 92.5,
            "avg_value_lift_aed": 750000,
            "top_renovation_type": "Supplementary Outbuilding/Majlis"
        },
        "leads": [
            {
                "id": "KC-VILLA-809",
                "address": "Khalifa City Sector 12, Villa 105",
                "coordinates": [24.4172, 54.5785],
                "renovation_type": "Structural Extension",
                "gee_detected_date": "2023-01-20",
                "gee_confidence": 0.88,
                "timeline": {
                    "purchase_dld": { "date": "2020-03-10", "price_aed": 4800000, "price_per_sqft": 600, "bua_sqft": 8000, "plot_sqft": 15000 },
                    "permit": { "id": "ADM-2022-KC-992", "date": "2022-07-15", "type": "License for External Majlis and Boundary Modification", "issuer": "Abu Dhabi Municipality" },
                    "gee_change": { "date": "2023-01-20", "description": "NDBI built-up index increase representing addition of a 90 sqm external majlis structure in the yard." },
                    "resale_dld": { "date": "2024-05-14", "price_aed": 6600000, "price_per_sqft": 825, "market_gain_baseline_pct": 15.0, "actual_gain_pct": 37.5, "renovation_value_lift_aed": 1080000, "estimated_renovation_cost_aed": 280000, "net_renovation_profit_aed": 800000, "renovation_roi_pct": 285.7 }
                }
            }
        ]
    },
    "Saadiyat Island (Abu Dhabi)": {
        "center": [24.535, 54.435],
        "zoom": 13,
        "developer": "Aldar Properties",
        "description": "Ultra-exclusive beachfront cultural district. Saadiyat Beach Villas feature massive beachfront custom estates with luxury garden upgrades.",
        "stats": {
            "total_villas": 1200,
            "detected_renovations_3yr": 74,
            "avg_pool_roi": 120.0,
            "avg_extension_roi": 195.0,
            "avg_value_lift_aed": 3800000,
            "top_renovation_type": "Beachfront Landscape Rebuild"
        },
        "leads": [
            {
                "id": "SAD-VILLA-015",
                "address": "Saadiyat Beach Villas, Block C, Villa 8",
                "coordinates": [24.5385, 54.4392],
                "renovation_type": "Structural Extension",
                "gee_detected_date": "2023-08-30",
                "gee_confidence": 0.94,
                "timeline": {
                    "purchase_dld": { "date": "2021-06-18", "price_aed": 14500000, "price_per_sqft": 2071, "bua_sqft": 7000, "plot_sqft": 14000 },
                    "permit": { "id": "ADM-2022-SAD-091", "date": "2022-12-05", "type": "Internal Modification and Beach-Facing Room Extension", "issuer": "Abu Dhabi Municipality" },
                    "gee_change": { "date": "2023-08-30", "description": "NDBI building edge expansion of ~80 sqm. High concrete reflectance." },
                    "resale_dld": { "date": "2025-03-24", "price_aed": 22500000, "price_per_sqft": 3214, "market_gain_baseline_pct": 28.0, "actual_gain_pct": 55.2, "renovation_value_lift_aed": 3940000, "estimated_renovation_cost_aed": 950000, "net_renovation_profit_aed": 2990000, "renovation_roi_pct": 314.7 }
                }
            }
        ]
    },

    # --- SHARJAH ---
    "Al Zahia (Sharjah)": {
        "center": [25.312, 55.485],
        "zoom": 14,
        "developer": "Sharjah Holding (Majid Al Futtaim)",
        "description": "Sharjah's first gated community. Expat-friendly modern design language with standardized villa formats and high-intent pool conversions.",
        "stats": {
            "total_villas": 1900,
            "detected_renovations_3yr": 84,
            "avg_pool_roi": 55.0,
            "avg_extension_roi": 72.8,
            "avg_value_lift_aed": 350000,
            "top_renovation_type": "Plunge Pool Installation"
        },
        "leads": [
            {
                "id": "ZAH-VILLA-122",
                "address": "Lilac Lilies Street, Villa 84",
                "coordinates": [25.3142, 55.4882],
                "renovation_type": "Pool Addition",
                "gee_detected_date": "2023-07-14",
                "gee_confidence": 0.89,
                "timeline": {
                    "purchase_dld": { "date": "2021-03-12", "price_aed": 2400000, "price_per_sqft": 685, "bua_sqft": 3500, "plot_sqft": 5200 },
                    "permit": { "id": "SM-2022-ZAH-0839", "date": "2022-11-04", "type": "Private Plunge Pool Building Permit", "issuer": "Sharjah Municipality" },
                    "gee_change": { "date": "2023-07-14", "description": "NDWI rise in backyard area. Minor NDVI drop." },
                    "resale_dld": { "date": "2024-11-05", "price_aed": 3200000, "price_per_sqft": 914, "market_gain_baseline_pct": 18.0, "actual_gain_pct": 33.3, "renovation_value_lift_aed": 368000, "estimated_renovation_cost_aed": 950000, "net_renovation_profit_aed": -582000, "renovation_roi_pct": -61.3 } # Low margin in Sharjah standard
                }
            }
        ]
    },
    "Al Rahmaniya (Sharjah)": {
        "center": [25.395, 55.545],
        "zoom": 13,
        "developer": "Sharjah Directorate of Housing / Various",
        "description": "Large family-oriented residential community in Sharjah. Large plot sizes with frequent additions of parking shelters and landscaping updates.",
        "stats": {
            "total_villas": 3500,
            "detected_renovations_3yr": 126,
            "avg_pool_roi": 30.0,
            "avg_extension_roi": 45.0,
            "avg_value_lift_aed": 220000,
            "top_renovation_type": "Car Parking Shelter / Garden Upgrades"
        },
        "leads": [
            {
                "id": "RAH-VILLA-405",
                "address": "Rahmaniya 5, Villa 12",
                "coordinates": [25.3978, 55.5482],
                "renovation_type": "Landscaping Overhaul",
                "gee_detected_date": "2024-01-10",
                "gee_confidence": 0.81,
                "timeline": {
                    "purchase_dld": { "date": "2022-09-02", "price_aed": 1900000, "price_per_sqft": 475, "bua_sqft": 4000, "plot_sqft": 9000 },
                    "permit": { "id": "SM-2023-RAH-102", "date": "2023-08-14", "type": "Internal Modification and Front Garden Re-Remodeling", "issuer": "Sharjah Municipality" },
                    "gee_change": { "date": "2024-01-10", "description": "NDVI drop in front courtyard representing lawn removal." },
                    "resale_dld": { "date": "2025-06-18", "price_aed": 2250000, "price_per_sqft": 562, "market_gain_baseline_pct": 12.0, "actual_gain_pct": 18.4, "renovation_value_lift_aed": 122000, "estimated_renovation_cost_aed": 60000, "net_renovation_profit_aed": 62000, "renovation_roi_pct": 103.3 }
                }
            }
        ]
    },

    # --- RAS AL KHAIMAH ---
    "Al Hamra Village (Ras Al Khaimah)": {
        "center": [25.688, 55.778],
        "zoom": 14,
        "developer": "Al Hamra Real Estate Development",
        "description": "Seaside resort-style community. Expat enclave with golf courses and marina. High renovation rate of older beach townhouses.",
        "stats": {
            "total_villas": 1400,
            "detected_renovations_3yr": 92,
            "avg_pool_roi": 48.0,
            "avg_extension_roi": 64.0,
            "avg_value_lift_aed": 280000,
            "top_renovation_type": "Beach Townhouse Deck & Pools"
        },
        "leads": [
            {
                "id": "AH-VILLA-055",
                "address": "Marina Townhouses Phase 2, Villa 5",
                "coordinates": [25.6892, 55.7798],
                "renovation_type": "Pool Addition",
                "gee_detected_date": "2023-05-18",
                "gee_confidence": 0.88,
                "timeline": {
                    "purchase_dld": { "date": "2021-07-28", "price_aed": 1650000, "price_per_sqft": 550, "bua_sqft": 3000, "plot_sqft": 4500 },
                    "permit": { "id": "RAKM-2022-P993", "date": "2022-12-10", "type": "Private swimming pool and landscape license", "issuer": "RAK Municipality" },
                    "gee_change": { "date": "2023-05-18", "description": "NDWI rise. Liquid body overlay confirmed. NDVI drop." },
                    "resale_dld": { "date": "2024-10-14", "price_aed": 2200000, "price_per_sqft": 733, "market_gain_baseline_pct": 15.0, "actual_gain_pct": 33.3, "renovation_value_lift_aed": 302000, "estimated_renovation_cost_aed": 110000, "net_renovation_profit_aed": 192000, "renovation_roi_pct": 174.5 }
                }
            }
        ]
    },

    # --- AJMAN ---
    "Al Yasmeen (Ajman)": {
        "center": [25.405, 55.535],
        "zoom": 14,
        "developer": "Ajman Properties / Private",
        "description": "Affordable residential cluster. Characterized by new build expansions and adding car port roofing on the plot boundaries.",
        "stats": {
            "total_villas": 1200,
            "detected_renovations_3yr": 68,
            "avg_pool_roi": 22.0,
            "avg_extension_roi": 35.8,
            "avg_value_lift_aed": 110000,
            "top_renovation_type": "Boundary Wall & Roof Additions"
        },
        "leads": [
            {
                "id": "YAS-VILLA-012",
                "address": "Al Yasmeen Sector 2, Villa 15",
                "coordinates": [25.4072, 55.5385],
                "renovation_type": "Structural Extension",
                "gee_detected_date": "2024-03-24",
                "gee_confidence": 0.83,
                "timeline": {
                    "purchase_dld": { "date": "2022-04-18", "price_aed": 1250000, "price_per_sqft": 357, "bua_sqft": 3500, "plot_sqft": 5000 },
                    "permit": { "id": "AM-2023-YAS-089", "date": "2023-10-15", "type": "Permit for Additional Room above Garage", "issuer": "Ajman Municipality" },
                    "gee_change": { "date": "2024-03-24", "description": "NDBI index rise. Reflectivity matches concrete garage roofing conversion." },
                    "resale_dld": { "date": "2025-05-10", "price_aed": 1500000, "price_per_sqft": 428, "market_gain_baseline_pct": 10.0, "actual_gain_pct": 20.0, "renovation_value_lift_aed": 125000, "estimated_renovation_cost_aed": 80000, "net_renovation_profit_aed": 45000, "renovation_roi_pct": 56.3 }
                }
            }
        ]
    }
}

def get_communities_list():
    """Returns a list of available communities and basic metadata."""
    return [
        {
            "name": name,
            "center": info["center"],
            "zoom": info["zoom"],
            "developer": info["developer"],
            "description": info["description"],
            "stats": info["stats"]
        }
        for name, info in COMMUNITIES.items()
    ]

def get_community_data(name):
    """Returns all data associated with a single community."""
    return COMMUNITIES.get(name)

def get_all_leads():
    """Flattens all leads across all communities."""
    all_leads = []
    for comm_name, info in COMMUNITIES.items():
        for lead in info["leads"]:
            lead_copy = lead.copy()
            lead_copy["community"] = comm_name
            lead_copy["developer"] = info["developer"]
            all_leads.append(lead_copy)
    return all_leads
