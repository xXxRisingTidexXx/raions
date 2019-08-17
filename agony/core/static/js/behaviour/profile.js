const AJAX = new Requests();
const WINDOWS = new Windows();
const FILTERS = new Filters();
const LANGUAGE = new Language();
// const STATISTICS = new Statistics();
const MAP = new Map();

const SAVES_HOLDER = new ItemsHolder(
    document.getElementById("div_main_objects_saved")
);
const SEARCH_HOLDER = new ItemsHolder(
    document.getElementById("div_main_objects_search")
);

document
    .getElementById("btn_view_saves")
    .onclick = () => WINDOWS.Toggle("saves");

document
    .getElementById("btn_view_search")
    .onclick = () => WINDOWS.Toggle("search");

document
    .getElementById("btn_view_settings")
    .onclick = () => WINDOWS.Toggle("settings");

// document
//     .getElementById("btn_view_statistics")
//     .onclick = () => WINDOWS.Toggle("statistics");
//
// document
//     .getElementById("btn_window_full_statistics_close")
//     .onclick = () => {
//     STATISTICS.ClearStatistics();
//     WINDOWS.StatisticsToggle(false)
// };

document
    .getElementById("btn_full_object_exit")
    .onclick = () => WINDOWS.FullItemToggle(false);

// document
// 	.getElementById("btn_get_statistics")
// 	.onclick = () => WINDOWS.StatisticsToggle(true);

document
    .getElementById("alert_box")
    .onclick = () => WINDOWS.AlertBoxHide();

document
    .getElementById("btn_search")
    .onclick = () => {
    if (FILTERS.Verify()) {
        Requests.GetFiltersPage({addPage: -Requests.page, filters: FILTERS.GetParameters()});
        MAP.RemoveAllMarkersFromSearchLayer(MAP.searchLayer);
    }
};

document
    .getElementById("filters_select_state")
    .oninput = () => {
    let val = document.getElementById("filters_select_state").value;
    if (val.length % 2 === 0 && val.length !== 0) {
        FILTERS.RemoveAutocompleteOptions(document.getElementById("filters_select_state_details"));
        FILTERS.AutocompleteGeolocation(
            document.getElementById("filters_select_state_details"),
            "state"
        )
    }
};

document
    .getElementById("filters_select_locality")
    .oninput = () => {
    let val = document.getElementById("filters_select_locality").value;
    if (val.length % 2 === 0 && val.length !== 0) {
        FILTERS.RemoveAutocompleteOptions(document.getElementById("filters_select_locality_details"));
        FILTERS.AutocompleteGeolocation(
            document.getElementById("filters_select_locality_details"),
            "locality"
        )
    }
};

document
    .getElementById("filters_select_county")
    .oninput = () => {
    let val = document.getElementById("filters_select_county").value;
    if (val.length % 2 === 0 && val.length !== 0) {
        FILTERS.RemoveAutocompleteOptions(document.getElementById("filters_select_county_details"));
        FILTERS.AutocompleteGeolocation(
            document.getElementById("filters_select_county_details"),
            "county"
        )
    }
};

document
    .getElementById("btn_add_detail")
    .onclick = () => FILTERS.AddDetail();

document
    .getElementById("btn_show_items")
    .onclick = () => WINDOWS.TargetSearchTypeWindow("items");

document
    .getElementById("btn_show_map")
    .onclick = () => WINDOWS.TargetSearchTypeWindow("map");

let appActions = (key, altKey) => {
    if (altKey) {
        if (WINDOWS.isToggledFullItem) {
            WINDOWS.FullItemToggle(false);
        }
    } else if (key === "z" || key === "Z" ||
        key === "я" || key === "Я") {
        if (WINDOWS.openedWindow !== "saves") {
            WINDOWS.Toggle("saves");
        }
    } else if (key === "x" || key === "X" ||
        key === "ч" || key === "Ч") {
        if (WINDOWS.openedWindow !== "search")
            WINDOWS.Toggle("search");
        else {
            WINDOWS.filtersButton.onclick();
        }
    }
};

document.addEventListener('keyup', e => {
    if (e.ctrlKey) {
        appActions(e.key, e.altKey);
    }
});

Requests.GetSaves();
WINDOWS.Toggle("saves");
// WINDOWS.StatisticsToggle(false);
WINDOWS.FullItemToggle(false);
WINDOWS.AlertBoxHide();
WINDOWS.TargetSearchTypeWindow("items");
MAP.UpdateTheme(Theme.GetMapTheme());

let flats = [
    {
        "id": 4726,
        "url": "https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-cherkassyi-tsentr-pionerskaya-ulitsa-14958937.html",
        "avatar": "https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja-kvartira-cherkassyi-tsentr-pionerskaya-ulitsa__93298565fl.jpg",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.0682702,
                    49.4364832
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u041f\u0440\u0438\u0434\u043d\u0456\u043f\u0440\u043e\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u041c\u0438\u0442\u043d\u0438\u0446\u044c\u043a\u0430 \u0432\u0443\u043b\u0438\u0446\u044f",
                "house_number": null
            }
        },
        "price": "45000.00",
        "rate": "662.00",
        "area": 68.0,
        "living_area": 45.0,
        "kitchen_area": 15.0,
        "rooms": 3,
        "floor": 1,
        "total_floor": 9,
        "ceiling_height": 2.5,
        "details": [
            {
                "feature": "planning",
                "value": "separate planning",
                "group": "interior"
            },
            {
                "feature": "bathrooms",
                "value": "adjacent bathrooms",
                "group": "supplies"
            },
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "wall_type",
                "value": "brick",
                "group": "building"
            },
            {
                "feature": "passenger_elevators",
                "value": "1 passenger elevator",
                "group": "building"
            },
            {
                "feature": "gas",
                "value": "gas is present",
                "group": "supplies"
            },
            {
                "feature": "state",
                "value": "authorial project",
                "group": "interior"
            },
            {
                "feature": "housing",
                "value": "secondary housing",
                "group": "building"
            },
            {
                "feature": "warming",
                "value": "internal insulation",
                "group": "supplies"
            },
            {
                "feature": "window_type",
                "value": "metal-plastic windows",
                "group": "interior"
            }
        ]
    },
    {
        "id": 4269,
        "url": "https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-cherkassyi-kazbet-shevchenko-bulvar-15665250.html",
        "avatar": "https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja-kvartira-cherkassyi-kazbet-shevchenko-bulvar__98395630fl.jpg",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.0433872792018,
                    49.4547177
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u0421\u043e\u0441\u043d\u0456\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u0428\u0435\u0432\u0447\u0435\u043d\u043a\u0430 \u0431\u0443\u043b\u044c\u0432\u0430\u0440",
                "house_number": "69"
            }
        },
        "price": "21500.00",
        "rate": "371.00",
        "area": 58.0,
        "living_area": 43.0,
        "kitchen_area": 6.0,
        "rooms": 3,
        "floor": 1,
        "total_floor": 5,
        "ceiling_height": 3.0,
        "details": [
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "bathrooms",
                "value": "separate bathrooms",
                "group": "supplies"
            },
            {
                "feature": "wall_type",
                "value": "brick",
                "group": "building"
            },
            {
                "feature": "gas",
                "value": "gas is present",
                "group": "supplies"
            },
            {
                "feature": "housing",
                "value": "secondary housing",
                "group": "building"
            },
            {
                "feature": "bedrooms",
                "value": "2 bedrooms",
                "group": "interior"
            },
            {
                "feature": "window_type",
                "value": "metal-plastic windows",
                "group": "interior"
            },
            {
                "feature": "planning",
                "value": "adjacent-separate planning",
                "group": "interior"
            }
        ]
    },
    {
        "id": 5218,
        "url": "https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-cherkassyi-tsentr-shevchenko-bulvar-14948738.html",
        "avatar": "https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja-kvartira-cherkassyi-tsentr-shevchenko-bulvar__98477063fl.jpg",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.0628279,
                    49.4418561
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u041f\u0440\u0438\u0434\u043d\u0456\u043f\u0440\u043e\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u0428\u0435\u0432\u0447\u0435\u043d\u043a\u0430 \u0431\u0443\u043b\u044c\u0432\u0430\u0440",
                "house_number": null
            }
        },
        "price": "46800.00",
        "rate": "557.00",
        "area": 84.0,
        "living_area": 60.0,
        "kitchen_area": 9.0,
        "rooms": 3,
        "floor": 3,
        "total_floor": 4,
        "ceiling_height": 3.0,
        "details": [
            {
                "feature": "bathrooms",
                "value": "adjacent bathrooms",
                "group": "supplies"
            },
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "wall_type",
                "value": "brick",
                "group": "building"
            },
            {
                "feature": "gas",
                "value": "gas is present",
                "group": "supplies"
            },
            {
                "feature": "state",
                "value": "good state",
                "group": "interior"
            },
            {
                "feature": "housing",
                "value": "secondary housing",
                "group": "building"
            },
            {
                "feature": "window_type",
                "value": "metal-plastic windows",
                "group": "interior"
            },
            {
                "feature": "door_type",
                "value": "metal door",
                "group": "interior"
            }
        ]
    },
    {
        "id": 7673,
        "url": "https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-cherkassyi-himposelok-himikov-prospekt-15321653.html",
        "avatar": "https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja-kvartira-cherkassyi-himposelok-himikov-prospekt__96594431fl.jpg",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.049347614596,
                    49.40498335
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u041f\u0440\u0438\u0434\u043d\u0456\u043f\u0440\u043e\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u0425\u0456\u043c\u0456\u043a\u0456\u0432 \u043f\u0440\u043e\u0441\u043f\u0435\u043a\u0442",
                "house_number": "54"
            }
        },
        "price": "24900.00",
        "rate": "362.00",
        "area": 68.8,
        "living_area": 39.0,
        "kitchen_area": 7.5,
        "rooms": 3,
        "floor": 11,
        "total_floor": 14,
        "ceiling_height": 2.5,
        "details": [
            {
                "feature": "planning",
                "value": "separate planning",
                "group": "interior"
            },
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "bathrooms",
                "value": "separate bathrooms",
                "group": "supplies"
            },
            {
                "feature": "wall_type",
                "value": "brick",
                "group": "building"
            },
            {
                "feature": "passenger_elevators",
                "value": "1 passenger elevator",
                "group": "building"
            },
            {
                "feature": "bedrooms",
                "value": "3 bedrooms",
                "group": "interior"
            },
            {
                "feature": "window_type",
                "value": "wooden and metal-plastic windows",
                "group": "interior"
            },
            {
                "feature": "state",
                "value": "good state",
                "group": "interior"
            },
            {
                "feature": "door_type",
                "value": "wooden and metal door",
                "group": "interior"
            },
            {
                "feature": "housing",
                "value": "secondary housing",
                "group": "building"
            },
            {
                "feature": "gas",
                "value": "gas is absent",
                "group": "supplies"
            }
        ]
    },
    {
        "id": 6308,
        "url": "https://www.olx.ua/obyavlenie/chastichka-italii-v-cherkassah-IDEhLv1.html",
        "avatar": "https://apollo-ireland.akamaized.net:443/v1/files/in8d0y812k1r2-UA/image;s=644x461",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.06334538315,
                    49.44523945
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u0421\u043e\u0441\u043d\u0456\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u041e\u0441\u0442\u0430\u0444\u0456\u044f \u0414\u0430\u0448\u043a\u043e\u0432\u0438\u0447\u0430 \u0432\u0443\u043b\u0438\u0446\u044f",
                "house_number": "20"
            }
        },
        "price": "470000.00",
        "rate": "2848.49",
        "area": 165.0,
        "living_area": null,
        "kitchen_area": 30.0,
        "rooms": 3,
        "floor": 6,
        "total_floor": 10,
        "ceiling_height": null,
        "details": [
            {
                "feature": "planning",
                "value": "separate planning",
                "group": "interior"
            },
            {
                "feature": "building_type",
                "value": "the housing stock since 2011",
                "group": "building"
            },
            {
                "feature": "furniture",
                "value": "furniture is present",
                "group": "interior"
            },
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "wall_type",
                "value": "monolith",
                "group": "building"
            },
            {
                "feature": "state",
                "value": "authorial project",
                "group": "interior"
            }
        ]
    },
    {
        "id": 7111,
        "url": "https://www.olx.ua/obyavlenie/prodazh-3-k-kvartiru-v-samomu-tsentr-msta-z-yaksnim-remontom-IDEchCf.html",
        "avatar": "https://apollo-ireland.akamaized.net:443/v1/files/l3uei7lmp0ql1-UA/image;s=644x461",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.0606637774718,
                    49.4145166
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u0421\u043e\u0441\u043d\u0456\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u042f\u0446\u0438\u043a\u0430 \u0432\u0443\u043b\u0438\u0446\u044f",
                "house_number": "8/1"
            }
        },
        "price": "39999.00",
        "rate": "727.26",
        "area": 55.0,
        "living_area": null,
        "kitchen_area": 38.0,
        "rooms": 3,
        "floor": 3,
        "total_floor": 5,
        "ceiling_height": null,
        "details": [
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "planning",
                "value": "adjacent through planning",
                "group": "interior"
            },
            {
                "feature": "state",
                "value": "authorial project",
                "group": "interior"
            }
        ]
    },
    {
        "id": 6922,
        "url": "https://www.olx.ua/obyavlenie/3k-kvartira-zhk-pushkina-po-ul-pushkina-33-r-n-kazbet-IDDbse7.html",
        "avatar": "https://apollo-ireland.akamaized.net:443/v1/files/wy82kx4ghy4s2-UA/image;s=644x461",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.0606637774718,
                    49.4145166
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u0421\u043e\u0441\u043d\u0456\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u042f\u0446\u0438\u043a\u0430 \u0432\u0443\u043b\u0438\u0446\u044f",
                "house_number": "8/1"
            }
        },
        "price": "47025.00",
        "rate": "475.00",
        "area": 99.0,
        "living_area": null,
        "kitchen_area": 13.0,
        "rooms": 3,
        "floor": 5,
        "total_floor": 16,
        "ceiling_height": null,
        "details": [
            {
                "feature": "planning",
                "value": "separate planning",
                "group": "interior"
            },
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "state",
                "value": "after construction",
                "group": "interior"
            },
            {
                "feature": "building_type",
                "value": "under construction",
                "group": "building"
            },
            {
                "feature": "wall_type",
                "value": "monolith",
                "group": "building"
            },
            {
                "feature": "bathrooms",
                "value": "2 and more bathrooms",
                "group": "supplies"
            }
        ]
    },
    {
        "id": 6358,
        "url": "https://www.olx.ua/obyavlenie/3k-kvartira-v-tsentre-IDC1Yyh.html",
        "avatar": "https://apollo-ireland.akamaized.net:443/v1/files/dejrcw4ypvrp3-UA/image;s=644x461",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.0606637774718,
                    49.4145166
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u0421\u043e\u0441\u043d\u0456\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u042f\u0446\u0438\u043a\u0430 \u0432\u0443\u043b\u0438\u0446\u044f",
                "house_number": "8/1"
            }
        },
        "price": "46800.00",
        "rate": "557.14",
        "area": 84.0,
        "living_area": null,
        "kitchen_area": 9.0,
        "rooms": 3,
        "floor": 3,
        "total_floor": 4,
        "ceiling_height": null,
        "details": [
            {
                "feature": "bathrooms",
                "value": "adjacent bathrooms",
                "group": "supplies"
            },
            {
                "feature": "wall_type",
                "value": "brick",
                "group": "building"
            },
            {
                "feature": "planning",
                "value": "studio",
                "group": "interior"
            },
            {
                "feature": "state",
                "value": "residential state",
                "group": "interior"
            }
        ]
    },
    {
        "id": 6888,
        "url": "https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-cherkassyi-tsentr-baydyivishnevetskogo-ulitsa-14037780.html",
        "avatar": "https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja-kvartira-cherkassyi-tsentr-baydyivishnevetskogo-ulitsa__96357644fl.jpg",
        "geolocation": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    32.0610878,
                    49.446379
                ]
            },
            "properties": {
                "state": "\u0427\u0435\u0440\u043a\u0430\u0441\u044c\u043a\u0430 \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                "locality": "\u0427\u0435\u0440\u043a\u0430\u0441\u0438",
                "county": "\u0421\u043e\u0441\u043d\u0456\u0432\u0441\u044c\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                "neighbourhood": null,
                "road": "\u0411\u0430\u0439\u0434\u0438 \u0412\u0438\u0448\u043d\u0435\u0432\u0435\u0446\u044c\u043a\u043e\u0433\u043e \u0432\u0443\u043b\u0438\u0446\u044f",
                "house_number": null
            }
        },
        "price": "51000.00",
        "rate": "487.00",
        "area": 104.7,
        "living_area": 46.0,
        "kitchen_area": 11.0,
        "rooms": 3,
        "floor": 1,
        "total_floor": 4,
        "ceiling_height": null,
        "details": [
            {
                "feature": "planning",
                "value": "separate planning",
                "group": "interior"
            },
            {
                "feature": "heating",
                "value": "centralized heating",
                "group": "supplies"
            },
            {
                "feature": "bathrooms",
                "value": "separate bathrooms",
                "group": "supplies"
            },
            {
                "feature": "wall_type",
                "value": "brick",
                "group": "building"
            },
            {
                "feature": "gas",
                "value": "gas is present",
                "group": "supplies"
            },
            {
                "feature": "state",
                "value": "good state",
                "group": "interior"
            },
            {
                "feature": "housing",
                "value": "secondary housing",
                "group": "building"
            },
            {
                "feature": "bedrooms",
                "value": "2 bedrooms",
                "group": "interior"
            },
            {
                "feature": "window_type",
                "value": "metal-plastic windows",
                "group": "interior"
            },
            {
                "feature": "passenger_elevators",
                "value": "without passenger elevators",
                "group": "building"
            },
            {
                "feature": "door_type",
                "value": "metal door",
                "group": "interior"
            }
        ]
    }
];

flats.forEach(f => SAVES_HOLDER.AddItem(new Item(f, "delete")));
flats.forEach(f => SEARCH_HOLDER.AddItem(new Item(f, "save")));
SEARCH_HOLDER.AddPaginationButton();