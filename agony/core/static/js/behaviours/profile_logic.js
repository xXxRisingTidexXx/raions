const AJAX = new Requests();
const WINDOWS = new Windows();
const FILTERS = new Filters();
const LANGUAGE = new Language();
const STATISTICS = new Statistics();
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

document
    .getElementById("btn_view_statistics")
    .onclick = () => WINDOWS.Toggle("statistics");

document
    .getElementById("btn_window_full_statistics_close")
    .onclick = () => {
    STATISTICS.ClearStatistics();
    WINDOWS.StatisticsToggle(false)
};

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
    .getElementById("btn_sort_price")
    .onclick = () => SEARCH_HOLDER.SortBy("price");

document
    .getElementById("btn_sort_area")
    .onclick = () => SEARCH_HOLDER.SortBy("area");

document
    .getElementById("btn_sort_rooms")
    .onclick = () => SEARCH_HOLDER.SortBy("rooms");

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
        if (WINDOWS.isToggledFullItem){
            WINDOWS.FullItemToggle(false);
            console.log("a");
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
WINDOWS.StatisticsToggle(false);
WINDOWS.FullItemToggle(false);
WINDOWS.AlertBoxHide();
WINDOWS.TargetSearchTypeWindow("items");
MAP.UpdateTheme(Theme.GetMapTheme());