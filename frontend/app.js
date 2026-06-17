let map;
let drawControl;
let drawnItems;
let activeROIGeometry = null;
let currentCommunity = null;
let beforeTileLayer = null;
let afterTileLayer = null;
let changeTileLayer = null;
let leadMarkers = [];
let allLeads = [];
let selectedLeadId = null;

// CSS colors matching legend
const CHANGE_COLORS = {
    "Pool Addition": "#00FFFF",        // Cyan
    "Structural Extension": "#FFA500",  // Orange/Amber
    "Landscaping Overhaul": "#00FF00"  // Emerald Green
};

document.addEventListener("DOMContentLoaded", () => {
    initMap();
    checkConnectionStatus();
    loadCommunities();
    setupEventHandlers();
});

// 1. Initialize Map
function initMap() {
    // Center of Dubai
    map = L.map("map", {
        zoomControl: true,
        attributionControl: false
    }).setView([25.07, 55.15], 11);

    // Premium Dark Base Map (CartoDB Dark Matter)
    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        maxZoom: 20
    }).addTo(map);

    // Setup Leaflet Draw for Custom ROI
    drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            remove: true
        },
        draw: {
            polygon: {
                allowIntersection: false,
                showArea: true,
                drawError: {
                    color: '#ef4444',
                    message: '<strong>Error:</strong> Polygons cannot intersect!'
                },
                shapeOptions: {
                    color: '#06b6d4'
                }
            },
            rectangle: {
                shapeOptions: {
                    color: '#06b6d4'
                }
            },
            circle: false,
            polyline: false,
            marker: false,
            circlemarker: false
        }
    });
    map.addControl(drawControl);

    // Capture Drawn Shapes
    map.on(L.Draw.Event.CREATED, (e) => {
        drawnItems.clearLayers();
        const layer = e.layer;
        drawnItems.addLayer(layer);
        
        // Save GeoJSON geometry
        const geojson = layer.toGeoJSON();
        activeROIGeometry = geojson.geometry;
        
        // Update Selector UI
        document.getElementById("select-community").value = "";
        currentCommunity = null;
        
        // Show message
        showToast("Custom region of interest captured.");
    });

    map.on(L.Draw.Event.DELETED, () => {
        activeROIGeometry = null;
    });
}

// 2. Fetch Earth Engine Connection Status
async function checkConnectionStatus() {
    const badge = document.getElementById("connection-badge");
    try {
        const response = await fetch("/api/status");
        const status = await response.json();
        
        if (status.authenticated && status.api_active) {
            badge.className = "badge badge-success";
            badge.innerHTML = `<i class="fa-solid fa-circle-check"></i> Live GEE Mode`;
            showToast("Google Earth Engine Connected.");
        } else {
            badge.className = "badge badge-warning";
            badge.innerHTML = `<i class="fa-solid fa-circle-info"></i> Demo Mode`;
        }
    } catch (e) {
        badge.className = "badge badge-danger";
        badge.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Connection Error`;
    }
}

// 3. Load Communities from Backend
async function loadCommunities() {
    const selector = document.getElementById("select-community");
    try {
        const response = await fetch("/api/communities");
        const communities = await response.json();
        
        selector.innerHTML = `<option value="" disabled selected>-- Select a Community --</option>`;
        communities.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.name;
            opt.textContent = c.name;
            selector.appendChild(opt);
        });
        
        // Auto-select first community as default
        if (communities.length > 0) {
            selector.value = communities[0].name;
            onCommunityChange(communities[0].name, communities);
        }
        
        // Save list for handling changes
        selector.addEventListener("change", (e) => {
            onCommunityChange(e.target.value, communities);
        });
        
    } catch (e) {
        console.error("Failed to load communities", e);
    }
}

function onCommunityChange(name, communitiesList) {
    // Clear drawn items if user selects default community
    drawnItems.clearLayers();
    activeROIGeometry = null;
    
    currentCommunity = communitiesList.find(c => c.name === name);
    if (currentCommunity) {
        map.setView(currentCommunity.center, currentCommunity.zoom);
    }
}

// 4. Setup Event Listeners
function setupEventHandlers() {
    // Run Analysis Button
    const btnRun = document.getElementById("btn-run-analysis");
    btnRun.addEventListener("click", runAnalysis);

    // Layer Controls
    document.getElementById("btn-layer-before").addEventListener("click", (e) => setActiveLayer("before", e.target));
    document.getElementById("btn-layer-after").addEventListener("click", (e) => setActiveLayer("after", e.target));
    document.getElementById("btn-layer-change").addEventListener("click", (e) => setActiveLayer("change", e.target));

    // Opacity Slider
    const opacitySlider = document.getElementById("layer-opacity");
    opacitySlider.addEventListener("input", (e) => {
        const opacity = e.target.value / 100;
        if (changeTileLayer) changeTileLayer.setOpacity(opacity);
    });

    // Sensitivity Slider
    const sensitivitySlider = document.getElementById("range-sensitivity");
    sensitivitySlider.addEventListener("input", (e) => {
        document.getElementById("sensitivity-value").textContent = e.target.value;
    });

    // Export CSV
    document.getElementById("btn-export-csv").addEventListener("click", exportLeadsCSV);

    // Modal Control
    const modal = document.getElementById("settings-modal");
    const btnSettings = document.getElementById("btn-settings");
    const spanClose = document.querySelector(".close-modal");
    
    btnSettings.onclick = () => {
        modal.classList.remove("hidden");
        loadSavedKeyPlaceholder();
    };
    spanClose.onclick = () => modal.classList.add("hidden");
    window.onclick = (e) => {
        if (e.target === modal) modal.classList.add("hidden");
    };

    // Save GEE SA Key
    document.getElementById("btn-save-key").addEventListener("click", saveCredentials);
    document.getElementById("btn-clear-key").addEventListener("click", clearCredentials);
    
    // Timeline Close
    document.getElementById("btn-close-timeline").addEventListener("click", () => {
        document.getElementById("timeline-card").classList.add("hidden");
        // Deselect table row
        const selectedRow = document.querySelector("#leads-tbody tr.selected");
        if (selectedRow) selectedRow.classList.remove("selected");
    });
}

// 5. Save Credentials
async function saveCredentials() {
    const keyInput = document.getElementById("sa-key-input").value.trim();
    const statusText = document.getElementById("modal-status");
    
    if (!keyInput) {
        statusText.style.color = "#ef4444";
        statusText.textContent = "Please paste key content first.";
        return;
    }
    
    statusText.style.color = "var(--text-secondary)";
    statusText.textContent = "Authenticating...";
    
    try {
        const response = await fetch("/api/authenticate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key_content: keyInput })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            statusText.style.color = "var(--color-success)";
            statusText.textContent = "Success! GEE Connected.";
            checkConnectionStatus();
            setTimeout(() => {
                document.getElementById("settings-modal").classList.add("hidden");
                statusText.textContent = "";
            }, 1500);
        } else {
            statusText.style.color = "#ef4444";
            statusText.textContent = result.detail || "Authentication failed.";
        }
    } catch (e) {
        statusText.style.color = "#ef4444";
        statusText.textContent = "Failed to communicate with server.";
    }
}

async function clearCredentials() {
    document.getElementById("sa-key-input").value = "";
    document.getElementById("modal-status").textContent = "Saved key cleared locally (Demo mode active).";
    // Check status again to reset to demo mode
    await checkConnectionStatus();
}

function loadSavedKeyPlaceholder() {
    // Just a basic check to show they have something saved if auth is active
    const badge = document.getElementById("connection-badge");
    if (badge.textContent.includes("Live GEE")) {
        document.getElementById("sa-key-input").placeholder = "Earth Engine service key active. Paste a new JSON key to overwrite.";
    }
}

// 6. Run Google Earth Engine Analysis
async function runAnalysis() {
    const btn = document.getElementById("btn-run-analysis");
    const communityName = document.getElementById("select-community").value;
    
    if (!communityName && !activeROIGeometry) {
        showToast("Please select a community or draw an ROI polygon.");
        return;
    }

    // Toggle loading
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Processing GEE...`;
    
    const requestData = {
        community_name: communityName || "Custom ROI",
        geometry: activeROIGeometry,
        start_before: document.getElementById("before-start").value,
        end_before: document.getElementById("before-end").value,
        start_after: document.getElementById("after-start").value,
        end_after: document.getElementById("after-end").value,
        sensitivity: parseFloat(document.getElementById("range-sensitivity").value)
    };

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            renderAnalysisResults(data, requestData.community_name);
        } else {
            showToast("Analysis error: " + data.detail);
        }
        
    } catch (e) {
        console.error(e);
        showToast("Server communication error.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-play"></i> Run GEE Analysis`;
    }
}

// 7. Render GEE Map layers and Lead markers
function renderAnalysisResults(data, communityName) {
    // Clear previous GEE map layers
    if (beforeTileLayer) map.removeLayer(beforeTileLayer);
    if (afterTileLayer) map.removeLayer(afterTileLayer);
    if (changeTileLayer) map.removeLayer(changeTileLayer);

    // Clear previous lead markers
    leadMarkers.forEach(m => map.removeLayer(m));
    leadMarkers = [];
    
    allLeads = data.leads;
    
    // Add GEE Image layers if present (in Live Mode)
    if (data.tile_urls && data.tile_urls.before && data.tile_urls.change) {
        beforeTileLayer = L.tileLayer(data.tile_urls.before, { maxZoom: 20 });
        afterTileLayer = L.tileLayer(data.tile_urls.after, { maxZoom: 20 });
        
        const opacity = document.getElementById("layer-opacity").value / 100;
        changeTileLayer = L.tileLayer(data.tile_urls.change, { 
            maxZoom: 20,
            opacity: opacity 
        });

        // Add layers to map (after and changes by default)
        afterTileLayer.addTo(map);
        changeTileLayer.addTo(map);
        setActiveTabUI("after");
    } else {
        // Fallback for Demo mode
        setActiveTabUI("after");
    }

    // Plot Lead Markers (Centroids of changes)
    allLeads.forEach(lead => {
        const color = CHANGE_COLORS[lead.renovation_type] || "#ffffff";
        
        const marker = L.circleMarker(lead.coordinates, {
            radius: 8,
            fillColor: color,
            color: "#ffffff",
            weight: 1.5,
            opacity: 0.9,
            fillOpacity: 0.8
        }).addTo(map);

        marker.bindTooltip(`<strong>${lead.id}</strong>: ${lead.renovation_type}`, {
            direction: 'top',
            offset: [0, -5]
        });

        marker.on("click", () => {
            selectLead(lead.id);
            // Fly to marker
            map.setView(lead.coordinates, 17);
        });

        leadMarkers.push(marker);
    });

    // Fit map bounds to leads if custom ROI was used
    if (leadMarkers.length > 0 && activeROIGeometry) {
        const group = new L.featureGroup(leadMarkers);
        map.fitBounds(group.getBounds().pad(0.1));
    }

    // Update Sidebar Stats
    document.getElementById("stat-developer").textContent = currentCommunity ? currentCommunity.developer : "Multiple / Custom";
    document.getElementById("stat-prospects").textContent = data.stats.detected_renovations_3yr;
    
    // Average ROI
    const activeCommName = communityName === "Custom ROI" ? "Arabian Ranches" : communityName;
    const avgROI = activeCommName === "Palm Jumeirah" ? "55.4%" : "22.8%";
    document.getElementById("stat-roi").textContent = avgROI;
    
    // Estimated Value
    const formattedVal = (data.stats.avg_value_lift_aed / 1000).toFixed(0) + "k AED";
    document.getElementById("stat-value").textContent = formattedVal;

    // Render Breakdown Section
    renderBreakdown(activeCommName);

    // Populate Leads Table
    renderLeadsTable(allLeads);

    // Generate Ad Copy
    generateAdCopy(activeCommName, data.stats);

    showToast(`Analysis complete: ${allLeads.length} leads loaded.`);
}

function renderBreakdown(communityName) {
    const container = document.getElementById("roi-breakdown-container");
    container.innerHTML = "";

    // Preloaded details mapping
    const summaries = {
        "Arabian Ranches": [
            { type: "Structural Extension", roi: "77.1%", cost: "350k AED", lift: "620k AED", isNeg: false },
            { type: "Pool Addition", roi: "86.6%", cost: "150k AED", lift: "280k AED", isNeg: false },
            { type: "Landscaping Overhaul", roi: "-25%", cost: "80k AED", lift: "60k AED", isNeg: true }
        ],
        "Palm Jumeirah": [
            { type: "Structural Extension", roi: "216.7%", cost: "1.2M AED", lift: "3.8M AED", isNeg: false },
            { type: "Pool Addition", roi: "140.0%", cost: "250k AED", lift: "600k AED", isNeg: false },
            { type: "Landscaping Overhaul", roi: "50%", cost: "300k AED", lift: "450k AED", isNeg: false }
        ]
    };

    const commList = summaries[communityName] || summaries["Arabian Ranches"];
    commList.forEach(item => {
        const card = document.createElement("div");
        card.className = "roi-item";
        card.innerHTML = `
            <div class="roi-header">
                <span class="roi-title">${item.type}</span>
                <span class="roi-pct-badge ${item.isNeg ? 'negative' : ''}">ROI: ${item.roi}</span>
            </div>
            <div class="roi-details">
                <span>Est. Cost: ${item.cost}</span>
                <span>Value Added: ${item.lift}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

function renderLeadsTable(leads) {
    const tbody = document.getElementById("leads-tbody");
    tbody.innerHTML = "";

    if (leads.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="table-placeholder">No modifications detected in this area/time range. Try lowering sensitivity.</td></tr>`;
        return;
    }

    leads.forEach(lead => {
        const row = document.createElement("tr");
        row.id = `row-${lead.id}`;
        
        const purchasePrice = (lead.timeline.purchase_dld.price_aed / 1000000).toFixed(1) + "M AED";
        const resalePrice = (lead.timeline.resale_dld.price_aed / 1000000).toFixed(1) + "M AED";
        
        const roiVal = lead.timeline.resale_dld.renovation_roi_pct;
        const roiColor = roiVal > 100 ? "var(--color-success)" : (roiVal < 0 ? "var(--color-danger)" : "var(--color-warning)");
        
        row.innerHTML = `
            <td style="font-weight:700; color:var(--color-primary);">${lead.id}</td>
            <td>${lead.address}</td>
            <td style="font-family:monospace; font-size:0.75rem;">${lead.coordinates[0].toFixed(5)}, ${lead.coordinates[1].toFixed(5)}</td>
            <td>
                <span style="display:inline-flex; align-items:center; gap:0.25rem;">
                    <span style="width:8px; height:8px; border-radius:50%; background-color:${CHANGE_COLORS[lead.renovation_type]};"></span>
                    ${lead.renovation_type}
                </span>
            </td>
            <td>${purchasePrice}</td>
            <td>${resalePrice}</td>
            <td style="font-weight:700; color:${roiColor}">${roiVal > 0 ? '+' : ''}${roiVal}%</td>
            <td>${Math.round(lead.gee_confidence * 100)}%</td>
            <td>
                <a href="https://www.google.com/maps/search/?api=1&query=${lead.coordinates[0]},${lead.coordinates[1]}" 
                   target="_blank" class="btn btn-secondary btn-sm" style="display:inline-flex;" title="Verify on Google Maps satellite imagery">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> Google Satellite
                </a>
            </td>
        `;

        row.addEventListener("click", () => selectLead(lead.id));
        tbody.appendChild(row);
    });
}

// 8. Lead selection and Detail Timeline
function selectLead(leadId) {
    selectedLeadId = leadId;
    
    // Highlight table row
    document.querySelectorAll("#leads-tbody tr").forEach(r => r.classList.remove("selected"));
    const row = document.getElementById(`row-${leadId}`);
    if (row) {
        row.classList.add("selected");
        row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    const lead = allLeads.find(l => l.id === leadId);
    if (!lead) return;

    // Populate Detailed Timeline
    document.getElementById("timeline-title").textContent = lead.address;
    
    // Purchase Event
    document.getElementById("timeline-p-date").textContent = lead.timeline.purchase_dld.date;
    document.getElementById("timeline-p-price").textContent = `Bought for: ${(lead.timeline.purchase_dld.price_aed / 1000000).toFixed(2)}M AED`;
    document.getElementById("timeline-p-meta").textContent = `Size: ${lead.timeline.purchase_dld.bua_sqft} sqft BUA | Plot: ${lead.timeline.purchase_dld.plot_sqft} sqft`;

    // Permit Event
    document.getElementById("timeline-permit-date").textContent = lead.timeline.permit.date;
    document.getElementById("timeline-permit-type").textContent = lead.timeline.permit.type;
    document.getElementById("timeline-permit-meta").textContent = `Issuer: ${lead.timeline.permit.issuer} | Permit #${lead.timeline.permit.id}`;

    // GEE Change Detection
    document.getElementById("timeline-gee-date").textContent = lead.timeline.gee_change.date;
    document.getElementById("timeline-gee-desc").textContent = lead.timeline.gee_change.description;
    document.getElementById("timeline-gee-meta").textContent = `Sentinel-2 Satellite Scan | Alg Certainty: ${Math.round(lead.gee_confidence*100)}%`;

    // DED License (Optional)
    const dedStep = document.getElementById("step-ded");
    if (lead.timeline.ded_license) {
        document.getElementById("timeline-ded-date").textContent = lead.timeline.ded_license.date;
        document.getElementById("timeline-ded-desc").textContent = `${lead.timeline.ded_license.name} - ${lead.timeline.ded_license.activity}`;
        document.getElementById("timeline-ded-meta").textContent = `License No: ${lead.timeline.ded_license.license_no} | Scraped from Invest in Dubai`;
        dedStep.classList.remove("hidden");
    } else {
        dedStep.classList.add("hidden");
    }

    // Google Maps Pin (Optional)
    const gmapsStep = document.getElementById("step-gmaps");
    if (lead.timeline.google_maps_pin) {
        document.getElementById("timeline-gmaps-date").textContent = lead.timeline.google_maps_pin.date;
        document.getElementById("timeline-gmaps-desc").innerHTML = `<a href="${lead.timeline.google_maps_pin.url}" target="_blank" style="color:var(--color-primary);text-decoration:none;">${lead.timeline.google_maps_pin.name} <i class="fa-solid fa-arrow-up-right-from-square"></i></a>`;
        document.getElementById("timeline-gmaps-meta").textContent = `Rating: ${lead.timeline.google_maps_pin.rating} | Scraped via Places API`;
        gmapsStep.classList.remove("hidden");
    } else {
        gmapsStep.classList.add("hidden");
    }

    // Resale Event
    document.getElementById("timeline-s-date").textContent = lead.timeline.resale_dld.date;
    const priceText = `Sold for: ${(lead.timeline.resale_dld.price_aed / 1000000).toFixed(2)}M AED (Delta: +${( (lead.timeline.resale_dld.price_aed - lead.timeline.purchase_dld.price_aed) / 1000000).toFixed(2)}M AED)`;
    document.getElementById("timeline-s-price").textContent = priceText;
    
    const resale = lead.timeline.resale_dld;
    const netProf = resale.net_renovation_profit_aed;
    const roiBox = document.getElementById("timeline-s-roi");
    roiBox.innerHTML = `
        <strong>Renovation Net Profit: ${netProf > 0 ? '+' : ''}${(netProf / 1000).toFixed(0)}k AED</strong><br>
        Renovation ROI: ${resale.renovation_roi_pct}% (Outperformed neighborhood baseline growth by ${roundFloat(resale.actual_gain_pct - resale.market_gain_baseline_pct, 1)}%)
    `;

    // Show Timeline Card
    document.getElementById("timeline-card").classList.remove("hidden");
}

// 9. Generate Ads copywriting
function generateAdCopy(communityName, stats) {
    const metaBox = document.getElementById("ad-text-meta");
    const developer = currentCommunity ? currentCommunity.developer : "UAE Master Developers";
    
    const extensionsText = `🔥 ${communityName} Owners: Room Extensions ROI Report!

Data from recent Land Department transactions shows that adding an extra bedroom/study in ${communityName} returns massive ROI on average, adding up to 3.8M AED to resale values.

Are you an owner of a ${developer} property? Are you leaving money on the table? Get a custom design concept and extension quote from us. 

👉 Click here to check your plot's extension potential: [Link]`;

    const poolText = `🌴 ${communityName} Landscaping Report: Pool additions yield 86% ROI!

Thinking of upgrading your garden? Our analysis of ${communityName} villa sales proves that homes with private swimming pools sell for an average of 280,000 AED more than their unrenovated neighbors.

We specialize in high-ROI, premium villa pool designs for ${developer} communities. Don't settle for high costs and low value.

👉 View our ${communityName} portfolio and get a free estimate: [Link]`;

    if (communityName === "Palm Jumeirah") {
        metaBox.textContent = extensionsText;
    } else {
        metaBox.textContent = poolText;
    }

    // Bind copy button listener
    const copyBtns = document.querySelectorAll(".copy-btn");
    copyBtns.forEach(btn => {
        btn.onclick = () => {
            const targetId = btn.getAttribute("data-target");
            const textEl = document.getElementById(targetId);
            navigator.clipboard.writeText(textEl.textContent);
            btn.innerHTML = `<i class="fa-solid fa-check"></i> Copied!`;
            setTimeout(() => {
                btn.innerHTML = `<i class="fa-solid fa-copy"></i> Copy Ad Text`;
            }, 2000);
        };
    });
}

// 10. Map Tab Layer Switching
function setActiveLayer(layerType, tabButton) {
    if (!beforeTileLayer || !afterTileLayer || !changeTileLayer) return;

    // Remove active tab styling
    document.querySelectorAll(".layer-tab").forEach(t => t.classList.remove("active"));
    tabButton.classList.add("active");

    // Remove S2 RGB layers first
    map.removeLayer(beforeTileLayer);
    map.removeLayer(afterTileLayer);

    if (layerType === "before") {
        beforeTileLayer.addTo(map);
    } else if (layerType === "after") {
        afterTileLayer.addTo(map);
    } else if (layerType === "change") {
        afterTileLayer.addTo(map); // Keep after image as base
        // GEE Change mask handles overlay, always stays on top if checked
    }
}

function setActiveTabUI(layerType) {
    document.querySelectorAll(".layer-tab").forEach(t => t.classList.remove("active"));
    const tab = document.getElementById(`btn-layer-${layerType}`);
    if (tab) tab.classList.add("active");
}

// 11. Export CSV formatted for Meta/Google Ads location geofencing
function exportLeadsCSV() {
    if (allLeads.length === 0) {
        showToast("No leads available to export. Run analysis first.");
        return;
    }

    // CSV format: Latitude, Longitude, Radius (m), Name (Lead ID)
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Latitude,Longitude,Radius,Name,RenovationType,ROIPct\n";

    allLeads.forEach(lead => {
        // Drop pins with a 50-meter radius around the villa coordinate (perfect for geofencing neighbors)
        const row = `${lead.coordinates[0]},${lead.coordinates[1]},50,${lead.id},${lead.renovation_type},${lead.timeline.resale_dld.renovation_roi_pct}`;
        csvContent += row + "\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    
    const timestamp = new Date().toISOString().slice(0,10);
    link.setAttribute("download", `renoprospect_leads_${timestamp}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast("Leads CSV exported successfully.");
}

// 12. UI Notification Helper
function showToast(message) {
    // Create temporary toast banner
    const toast = document.createElement("div");
    toast.style.position = "fixed";
    toast.style.bottom = "2rem";
    toast.style.right = "2rem";
    toast.style.background = "rgba(15, 23, 42, 0.9)";
    toast.style.border = "1px solid var(--color-primary)";
    toast.style.boxShadow = "0 0 10px var(--color-primary-glow)";
    toast.style.color = "var(--text-primary)";
    toast.style.padding = "0.75rem 1.25rem";
    toast.style.borderRadius = "8px";
    toast.style.fontSize = "0.85rem";
    toast.style.zIndex = "9999";
    toast.style.fontFamily = "var(--font-body)";
    toast.style.pointerEvents = "none";
    toast.innerHTML = `<i class="fa-solid fa-satellite animate-pulse" style="color:var(--color-primary); margin-right:0.5rem;"></i> ${message}`;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.5s ease";
        setTimeout(() => document.body.removeChild(toast), 500);
    }, 3000);
}

function roundFloat(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}
