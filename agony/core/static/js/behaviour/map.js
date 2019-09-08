class Map {
    constructor() {
        const mapPathLight = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
        const mapPathDark = "https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png";

        let streets = L.tileLayer(mapPathLight);
        let dark = L.tileLayer(mapPathDark);

        this.savesLayer = L.layerGroup();
        this.savedMarkers = [];

        this.searchLayer = L.layerGroup();
        this.searchedMarkers = [];

        this.searchCircleLayer = L.layerGroup();

        let baseLayers = {
            "Світла тема": streets,
            "Темна тема": dark,
        };

        let itemLayer = {
            "Збережені": this.savesLayer,
            "Пошук": this.searchLayer,
            "Круг пошуку": this.searchCircleLayer
        };

        this.myMap = L.map(
            'div_main_objects_search_map',
            {
                layers: [dark, this.searchLayer],
                zoomControl: false,
                attributionControl: false
            }
        ).setView([48.9773383, 32.4930533], 6);

        this.itemsLayers = L.control.layers(baseLayers, itemLayer).addTo(this.myMap);
        this.itemsLayers._layerControlInputs[0].onclick = () => Theme.SetMapTheme("light");
        this.itemsLayers._layerControlInputs[1].onclick = () => Theme.SetMapTheme("dark");

        this.searchCircle = L.circle([0, 0], {
            color: "var(--search_circle)",
            fillColor: "var(--search_circle)",
            fillOpacity: 0.5,
            radius: 0
        }).addTo(this.searchCircleLayer);
        this.myMap.on('click', (e) => {
            if (this.itemsLayers._layerControlInputs[4].checked) {
                if (e.originalEvent.ctrlKey) {
                    let x1 = e.latlng.lat;
                    let y1 = e.latlng.lng;
                    let x2 = this.searchCircle._latlng.lat;
                    let y2 = this.searchCircle._latlng.lng;
                    this.searchCircle
                        .setRadius(this.Distance(x1, y1, x2, y2, "K") * 1000);
                } else {
                    this.searchCircle
                        .setLatLng(e.latlng);
                }
            }
        });
    }

    UpdateTheme(themeName) {
        if (themeName === "dark") {
            this.itemsLayers._layerControlInputs[1].click();
        } else if (themeName === "light") {
            this.itemsLayers._layerControlInputs[0].click();
        }
    }

    Distance(lat1, lon1, lat2, lon2, unit) {
        if ((lat1 === lat2) && (lon1 === lon2)) {
            return 0;
        } else {
            let radLat1 = Math.PI * lat1 / 180;
            let radLat2 = Math.PI * lat2 / 180;
            let theta = lon1 - lon2;
            let radTheta = Math.PI * theta / 180;
            let dist = Math.sin(radLat1) * Math.sin(radLat2) + Math.cos(radLat1) * Math.cos(radLat2) * Math.cos(radTheta);
            if (dist > 1) {
                dist = 1;
            }
            dist = Math.acos(dist);
            dist = dist * 180 / Math.PI;
            dist = dist * 60 * 1.1515;
            if (unit === "K") {
                dist = dist * 1.609344
            }
            if (unit === "N") {
                dist = dist * 0.8684
            }
            return dist;
        }
    }

    AddMarkerToLayer(lat, lon, title, layer, iconURL) {
        let LeafIcon = L.Icon.extend({
            options: {
                iconSize: [50, 50],
                iconAnchor: [25, 50],
                popupAnchor: [0, -50]
            }
        });

        let pointer = new LeafIcon({iconUrl: iconURL});

        let marker = L.marker([lat, lon], {icon: pointer})
            .addTo(layer)
            .bindPopup(title);

        if (layer === this.savesLayer) {
            this.savedMarkers.push(marker);
        } else {
            this.searchedMarkers.push(marker);
        }

        return marker;
    }

    RemoveAllMarkersFromSearchLayer() {
        this.searchedMarkers.forEach(v => v.removeFrom(this.searchLayer));
        this.searchedMarkers = [];
    }

    RemoveMarkerFromSavesLayer(marker, layer) {
        marker.removeFrom(layer);
        for (let i = 0; i < layer.length; i++) {
            if (layer[i] === marker) {
                layer.splice(i, 1);
                return;
            }
        }
    }
}