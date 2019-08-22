class Windows {
    constructor() {
        this.saves = document.getElementById("window_home");
        this.search = document.getElementById("window_search");
        this.settings = document.getElementById("window_settings");
        this.statistics = document.getElementById("window_statistics");
        this.fullItem = document.getElementById("window_full_object");
        this.fullStatistics = document.getElementById("window_full_statistics");
        this.filtersButton = document.getElementById("panel_filters_toggle_button");
        this.filtersPanel = document.getElementById("panel_filters");
        this.alertBox = document.getElementById("alert_box");
        this.searchObjectsItem = document.getElementById("div_main_objects_search");
        this.searchObjectsMap = document.getElementById("div_main_objects_search_map");
        this.gradientOverlayLeft = document.getElementById("gradient_overlay_left");
        this.gradientOverlayRight = document.getElementById("gradient_overlay_right");

        this.openedWindow = "saves";
        this.isToggledFullItem = false;

        this.filtersButton.onclick = () => {
            this.AlertBoxHide();
            if (this.filtersPanel.style.right === "-540px" || this.filtersPanel.style.right === "") {
                this.filtersPanel.style.right = "0";
                this.filtersButton.style.right = "515px";
            } else {
                this.filtersPanel.style.right = "-540px";
                this.filtersButton.style.right = "-20px";
            }
        }
    }

    TargetSearchTypeWindow(windowName) {
        switch (windowName) {
            case "items":
                this.searchObjectsMap.style.visibility = "hidden";
                this.searchObjectsItem.style.visibility = null;
                this.gradientOverlayLeft.style.visibility = null;
                this.gradientOverlayRight.style.visibility = null;
                break;

            case "map":
                this.searchObjectsMap.style.visibility = null;
                this.searchObjectsItem.style.visibility = "hidden";
                this.gradientOverlayLeft.style.visibility = "hidden";
                this.gradientOverlayRight.style.visibility = "hidden";
                break;
        }
    }

    // StatisticsToggle(state) {
    // 	if (state) {
    // 		this.fullStatistics.style.visibility = null;
    // 	} else {
    // 		this.fullStatistics.style.visibility = "hidden";
    // 	}
    // }

    FullItemToggle(state) {
        if (state) {
            this.isToggledFullItem = true;
            this.fullItem.style.visibility = null;
        } else {
            this.isToggledFullItem = false;
            this.fullItem.style.visibility = "hidden";
        }
    }

    AlertBoxShow(position) {
        this.alertBox.style.right = `${position}px`;
    }

    AlertBoxHide() {
        this.alertBox.style.right = "-450px";
    }

    AlertBoxSetMessage(message) {
        this.alertBox.children[0].innerHTML = message;
    }

    Toggle(window_name) {
        this.openedWindow = window_name;

        if (window_name === "saves") {
            this.saves.style.display = null;
        } else {
            this.saves.style.display = 'none';
        }

        if (window_name === "search") {
            this.search.style.display = null;
            this.filtersPanel.style.display = null;
            this.filtersButton.style.display = null;
            this.alertBox.style.display = null;
        } else {
            this.search.style.display = "none";
            this.filtersPanel.style.display = "none";
            this.filtersButton.style.display = "none";
            this.alertBox.style.display = "none";
        }

        if (window_name === "settings") {
            this.settings.style.display = null;
        } else {
            this.settings.style.display = "none";
        }

        // if (window_name === "statistics") {
        // 	this.statistics.style.display = null;
        // } else {
        // 	this.statistics.style.display = "none";
        // }
    }
}