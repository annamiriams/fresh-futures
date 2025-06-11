/**
 * Fresh Futures Map Components
 * Core mapping functionality using Leaflet + Mapbox
 */

//  * NOTE FOR DEVELOPERS: 
//  * This file uses JSDoc documentation comments (the /** */ blocks above functions).
//  * These provide:
//  * - Parameter types and descriptions for better IDE support
//  * - Auto-completion hints when you use these methods
//  * - Automatic documentation generation
//  * 
//  * Example: When you type addMarker(, your IDE will show:
//  * addMarker(lat: number, lng: number, options?: object)
//  * 
//  * Attribution: https://jsdoc.app/
//  */

class FreshFuturesMap {
    constructor(containerId, options = {}) {
        // Default options for the map
        this.options = {
            center: [39.8283, -98.5795], // Geographic center of US (default)
            zoom: 4,
            maxZoom: 18,
            minZoom: 3,
            ...options // Spread operator merges user options with defaults
        };
        
        // Store the container ID and initialize the map
        this.containerId = containerId;
        this.map = null;
        this.currentMarker = null; // Track the current location marker
        this.mapboxToken = null; // Will be set from Django template
        
        // Initialize the map when class is created
        this.initializeMap();
    }
    
    /**
     * Initialize the Leaflet map with Mapbox tiles
     */
    initializeMap() {
        // Create the Leaflet map instance
        this.map = L.map(this.containerId).setView(this.options.center, this.options.zoom);
        
        // Add Mapbox tile layer
        // Note: mapboxToken will be passed from Django template
        const mapboxUrl = `https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=${window.MAPBOX_TOKEN}`;
        
        L.tileLayer(mapboxUrl, {
            attribution: '© <a href="https://www.mapbox.com/">Mapbox</a> © <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
            tileSize: 512,
            zoomOffset: -1,
            maxZoom: this.options.maxZoom,
            minZoom: this.options.minZoom
        }).addTo(this.map);
        
        console.log('Fresh Futures Map initialized successfully!');
    }
    
    /**
     * Add a marker to the map (JSDoc style)
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude  
     * @param {object} options - Marker options (popup text, draggable, etc.)
     */
    addMarker(lat, lng, options = {}) {
        // Remove existing marker if it exists (for single marker scenarios)
        if (this.currentMarker && options.replaceCurrent !== false) {
            this.map.removeLayer(this.currentMarker);
        }
        
        // Create new marker
        const marker = L.marker([lat, lng], {
            draggable: options.draggable || false
        }).addTo(this.map);
        
        // Add popup if provided
        if (options.popupText) {
            marker.bindPopup(options.popupText);
        }
        
        // Store as current marker
        this.currentMarker = marker;
        
        // Set up drag event if marker is draggable
        if (options.draggable && options.onDrag) {
            marker.on('dragend', (e) => {
                const position = e.target.getLatLng();
                options.onDrag(position.lat, position.lng);
            });
        }
        
        return marker;
    }
    
    /**
     * Handle map click events (JSDoc style)
     * @param {function} callback - Function to call when map is clicked
     */
    onMapClick(callback) {
        this.map.on('click', (e) => {
            const { lat, lng } = e.latlng;
            callback(lat, lng, e);
        });
    }
    
    /**
     * Center the map on specific coordinates (JSDoc style)
     * This is useful for focusing on a specific garden or location
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     * @param {number} zoom - Optional zoom level
     */
    centerOn(lat, lng, zoom = null) {
        if (zoom) {
            this.map.setView([lat, lng], zoom);
        } else {
            this.map.setView([lat, lng]);
        }
    }
    
    /**
     * Geocode an address to coordinates using Mapbox Geocoding API (JSDoc style)
     * @param {string} address - Address to geocode
     * @param {function} callback - Function to call with results
     */
    async geocodeAddress(address, callback) {
        try {
            const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(address)}.json?access_token=${window.MAPBOX_TOKEN}&limit=5`;
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.features && data.features.length > 0) {
                // Mapbox returns coordinates as [lng, lat], so we need to flip them
                const results = data.features.map(feature => ({
                    address: feature.place_name,
                    lat: feature.center[1], // Note: flipped from Mapbox format
                    lng: feature.center[0], // Note: flipped from Mapbox format
                    bbox: feature.bbox // Bounding box for zooming
                }));
                
                callback(null, results);
            } else {
                callback('No results found', null);
            }
        } catch (error) {
            console.error('Geocoding error:', error);
            callback('Geocoding service error', null);
        }
    }
    
    /**
     * Reverse geocode coordinates to an address (JSDoc style)
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude  
     * @param {function} callback - Function to call with address
     */
    async reverseGeocode(lat, lng, callback) {
        try {
            const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${window.MAPBOX_TOKEN}`;
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.features && data.features.length > 0) {
                // Get the most relevant address (usually the first result)
                const address = data.features[0].place_name;
                callback(null, address);
            } else {
                callback('Address not found', null);
            }
        } catch (error) {
            console.error('Reverse geocoding error:', error);
            callback('Reverse geocoding service error', null);
        }
    }
    
    /**
     * Fit the map to show all markers
     * Useful when displaying multiple gardens
     */
    fitToMarkers(markers) {
        if (markers.length === 0) return;
        
        // Create a group of all markers
        const group = new L.featureGroup(markers);
        
        // Fit the map to show all markers
        this.map.fitBounds(group.getBounds().pad(0.1)); // 10% padding
    }
    
    /**
     * Get the current map bounds
     * Useful for finding gardens in the current view
     */
    getCurrentBounds() {
        const bounds = this.map.getBounds();
        return {
            north: bounds.getNorth(),
            south: bounds.getSouth(), 
            east: bounds.getEast(),
            west: bounds.getWest()
        };
    }
    
    /**
     * Clean up the map instance
     * Call this when removing the map from the DOM
     */
    destroy() {
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
    }
}

/**
 * Function-based geocoder to avoid CSP class definition issues
 * * This prevents "unsafe-eval" CSP violations in strict security environments
 */
function FreshFuturesGeocoder() {
    this.mapboxToken = window.MAPBOX_TOKEN;
}

/**
 * Geocode an address to coordinates using Mapbox Geocoding API
 */
FreshFuturesGeocoder.prototype.geocodeAddress = async function(address, callback) {
    try {
        // encodeURIComponent handles special characters in addresses
        const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(address)}.json?access_token=${this.mapboxToken}&limit=5`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.features && data.features.length > 0) {
            const results = data.features.map(feature => ({
                address: feature.place_name,
                lat: feature.center[1], // Note: flipped from Mapbox format
                lng: feature.center[0], // Note: flipped from Mapbox format
                bbox: feature.bbox
            }));
            
            callback(null, results);
        } else {
            callback('No results found', null);
        }
    } catch (error) {
        console.error('Geocoding error:', error);
        callback('Geocoding service error', null);
    }
};

/**
 * Reverse geocode coordinates to an address
 */
FreshFuturesGeocoder.prototype.reverseGeocode = async function(lat, lng, callback) {
    try {
        const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${this.mapboxToken}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.features && data.features.length > 0) {
            const address = data.features[0].place_name;
            callback(null, address);
        } else {
            callback('Address not found', null);
        }
    } catch (error) {
        console.error('Reverse geocoding error:', error);
        callback('Reverse geocoding service error', null);
    }
};


// Export the classes to the global window object for use in other files
window.FreshFuturesMap = FreshFuturesMap;
window.FreshFuturesGeocoder = FreshFuturesGeocoder;

