/**
 * Fresh Futures Garden Map Components
 * Specialized mapping functionality for garden discovery and profiles
 */

class GardenMap extends FreshFuturesMap {
    // Constructor: special method that runs when creating a new GardenMap instance
    // Usage: const map = new GardenMap('map-container', {zoom: 12});
    constructor(containerId, options = {}) {
        // options: object with optional settings (zoom, center, etc.)
        // Default to a reasonable zoom level for garden viewing
        const defaultOptions = {
            center: [39.8283, -98.5795], // Center of US
            zoom: 10,
            ...options // Merge in any custom options passed by user
        };

        // super(): calls the parent class (FreshFuturesMap) constructor
        // This sets up the basic map functionality before we add garden-specific features
        super(containerId, defaultOptions);

        // Store garden-specific data
        this.gardens = [];
        this.userLocation = null;
        this.gardenMarkers = [];
    }

    /**
     * Initialize map for garden discovery page
     * Shows multiple gardens with clustering and search
     */
    initDiscoverMode(gardens, userLocation = null) {
        this.gardens = gardens;
        this.userLocation = userLocation;

        // If user has location, center map there
        if (userLocation) {
            this.centerOn(userLocation.lat, userLocation.lng, 12);
            this.addUserLocationMarker(userLocation.lat, userLocation.lng);
        }

        // Add all garden markers
        this.displayGardens(gardens);

        // Set up search functionality
        this.setupGardenSearch();

        console.log('Garden discovery mode initialized with', gardens.length, 'gardens');
    }

    /**
     * Initialize map for gardener profile page
     * Shows single garden location
     */
    initProfileMode(garden) {
        if (!garden.latitude || !garden.longitude) {
            console.log('Garden has no location data');
            return;
        }

        // Center on the garden location
        this.centerOn(garden.latitude, garden.longitude, 15);

        // Add garden marker
        this.addGardenMarker(garden, {
            showPopup: true,
            popupContent: this.createGardenPopup(garden)
        });

        console.log('Garden profile mode initialized for:', garden.name);
    }

    /**
     * Add user's location marker (different style from gardens)
     */
    // L is Leaflet's main namespace that contains all its methods
    addUserLocationMarker(lat, lng) {
        const userIcon = L.divIcon({
            // creates a custom "You" marker for the user's location that we can style with CSS
            className: 'user-location-marker',
            html: '<div class="user-marker-inner">You</div>',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });

        // Use the icon on a marker
        const marker = L.marker([lat, lng], { icon: userIcon }).addTo(this.map);
        marker.bindPopup('Your Location');

        return marker;
    }

    /**
     * Add a garden marker to the map
     */
    addGardenMarker(garden, options = {}) {
        if (!garden.latitude || !garden.longitude) {
            console.warn('Garden has no coordinates:', garden.name);
            return null;
        }

        // Create custom garden icon
        const gardenIcon = L.divIcon({
            className: 'garden-marker',
            html: '<div class="garden-marker-inner">🌱</div>',
            iconSize: [25, 25],
            iconAnchor: [12, 12]
        });

        const marker = L.marker([garden.latitude, garden.longitude], {
            icon: gardenIcon
        }).addTo(this.map);

        // Add popup with garden info
        const popupContent = options.popupContent || this.createGardenPopup(garden);
        marker.bindPopup(popupContent);

        // Show popup immediately if requested
        if (options.showPopup) {
            marker.openPopup();
        }

        // Store reference to garden data on marker
        marker.gardenData = garden;

        // Keep track of garden markers
        this.gardenMarkers.push(marker);

        return marker;
    }

    /**
     * Display multiple gardens on the map
     */
    displayGardens(gardens) {
        // Clear existing garden markers
        this.clearGardenMarkers();

        // Add marker for each garden
        gardens.forEach(garden => {
            this.addGardenMarker(garden);
        });

        // Fit map to show all gardens if we have any
        if (this.gardenMarkers.length > 0) {
            this.fitToMarkers(this.gardenMarkers);
        }

        console.log('Displayed', this.gardenMarkers.length, 'garden markers');
    }

    /**
     * Clear all garden markers from the map
     */
    clearGardenMarkers() {
        this.gardenMarkers.forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.gardenMarkers = [];
    }

    /**
     * Create HTML content for garden popup
     */
    createGardenPopup(garden) {
        return `
            <div class="garden-popup">
                <h3 class="garden-popup-title">${garden.name}</h3>
                <p class="garden-popup-description">${garden.description || 'No description available'}</p>
                <div class="garden-popup-details">
                    <p><strong>Address:</strong> ${garden.address || 'Address not provided'}</p>
                    <p><strong>Created by:</strong> ${garden.created_by_name || 'Unknown'}</p>
                    ${garden.timeline ? `<p><strong>Timeline:</strong> ${garden.timeline}</p>` : ''}
                </div>
                <div class="garden-popup-actions">
                    <a href="/gardens/${garden.id}/" class="garden-popup-link">View Details</a>
                </div>
            </div>
        `;
    }

    /**
     * Set up search functionality for garden discovery
     */
    setupGardenSearch() {
        // Find the search input field in the HTML
        const searchInput = document.getElementById('garden-search-input');
        if (!searchInput) return;

        let searchTimeout; // Will store timer ID for debouncing

        // Listen for every keystroke in the search box
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout); // Cancel previous timer if user is still typing
            const query = e.target.value.toLowerCase().trim();

            // Debounce search to avoid searching on every keystroke
            // Sets a new timer to run filterGardens() after 300ms
            searchTimeout = setTimeout(() => {
                this.filterGardens(query);
            }, 300);
        });
    }

    /**
     * Filter gardens based on search query
     */
    filterGardens(query) {
        if (!query) {
            // Show all gardens if no search query
            this.displayGardens(this.gardens);
            return;
        }

        // Filter gardens by name, description, or address
        // Converts everything to lowercase for case-insensitive searching
        const filteredGardens = this.gardens.filter(garden => {
            return garden.name.toLowerCase().includes(query) ||
                (garden.description && garden.description.toLowerCase().includes(query)) ||
                (garden.address && garden.address.toLowerCase().includes(query)) ||
                (garden.created_by_name && garden.created_by_name.toLowerCase().includes(query));
        });

        this.displayGardens(filteredGardens);

        console.log('Filtered to', filteredGardens.length, 'gardens for query:', query);
    }

    /**
     * Find gardens near a specific location
     */
    findNearbyGardens(lat, lng, radiusMiles = 10) {
        if (!this.gardens.length) return [];

        // Simple distance calculation (not perfect for long distances, but fine for local gardens)
        const nearbyGardens = this.gardens.filter(garden => {
            if (!garden.latitude || !garden.longitude) return false;

            const distance = this.calculateDistance(lat, lng, garden.latitude, garden.longitude);
            return distance <= radiusMiles;
        });

        // Sort by distance
        nearbyGardens.sort((a, b) => {
            const distA = this.calculateDistance(lat, lng, a.latitude, a.longitude);
            const distB = this.calculateDistance(lat, lng, b.latitude, b.longitude);
            return distA - distB;
        });

        return nearbyGardens;
    }

    /**
     * Calculate distance between two points in miles
     * Uses Haversine formula for accuracy
     */
    calculateDistance(lat1, lng1, lat2, lng2) {
        const R = 3959; // Earth's radius in miles
        // Convert latitude and longitude differences to radians
        // (Math functions work with radians, not degrees)
        const dLat = this.toRadians(lat2 - lat1);
        const dLng = this.toRadians(lng2 - lng1);

        // Haversine formula: calculates shortest distance between two points on a sphere
        // 'a' represents the square of half the chord length between the points
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) *
            Math.sin(dLng / 2) * Math.sin(dLng / 2);

        // 'c' is the angular distance in radians
        // atan2 is more accurate than atan for this calculation
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        // Multiply by Earth's radius to get distance in miles
        return R * c; // Distance in miles
    }

    /**
     * Convert degrees to radians
     */
    toRadians(degrees) {
        return degrees * (Math.PI / 180);
    }

    /**
     * Get user's current location using browser's geolocation API and center map there
     * Asks user for permission, then returns their coordinates
     */
    getUserLocation(callback) {
        // Check if browser supports geolocation (most modern browsers do)
        if (!navigator.geolocation) {
            console.error('Geolocation is not supported by this browser');
            callback('Geolocation not supported', null);
            return;
        }

        // navigator.geolocation.getCurrentPosition() triggers browser permission popup
        // "Allow Fresh Futures to access your location?"
        navigator.geolocation.getCurrentPosition(
            // Success callback: user allowed location access
            (position) => {
                const location = {
                    lat: position.coords.latitude,    // GPS coordinates
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy // Accuracy in meters
                };

                console.log('User location obtained:', location);
                callback(null, location); // Standard callback pattern: (error, result)
            },
            // Error callback: user denied permission or location failed
            (error) => {
                console.error('Error getting user location:', error);
                callback(error.message, null);
            },
            // Options for location accuracy and timing
            {
                enableHighAccuracy: true, // Use GPS if available (more accurate but slower)
                timeout: 10000,          // Give up after 10 seconds
                maximumAge: 300000       // Use cached location if less than 5 minutes old
            }
        );
    }
}

// Make available globally
window.GardenMap = GardenMap;