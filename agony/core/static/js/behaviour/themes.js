class Theme {
    static SetOptionalColor() {
        this.colorBackground = document.getElementById("color_background");
        this.colorBackground.value = this.GetRootColor("--background");
        this.colorBackground.oninput = function () {
            Theme.SetRootColor("--background", document.getElementById("color_background").value);
        };

        this.colorObjectPBackground = document.getElementById("color_object_p_background");
        this.colorObjectPBackground.value = this.GetRootColor("--object_p_background");
        this.colorObjectPBackground.oninput = function () {
            Theme.SetRootColor("--object_p_background", document.getElementById("color_object_p_background").value);
        };

        this.colorObjectPColor = document.getElementById("color_object_p_color");
        this.colorObjectPColor.value = this.GetRootColor("--object_p_color");
        this.colorObjectPColor.oninput = function () {
            Theme.SetRootColor("--object_p_color", document.getElementById("color_object_p_color").value);
        };

        this.colorFirst = document.getElementById("color_first");
        this.colorFirst.value = this.GetRootColor("--first");
        this.colorFirst.oninput = function () {
            Theme.SetRootColor("--first", document.getElementById("color_first").value);
        };

        this.colorSecond = document.getElementById("color_second");
        this.colorSecond.value = this.GetRootColor("--second");
        this.colorSecond.oninput = function () {
            Theme.SetRootColor("--second", document.getElementById("color_second").value);
        };

        this.colorPanels = document.getElementById("color_panels");
        this.colorPanels.value = this.GetRootColor("--panels");
        this.colorPanels.oninput = function () {
            Theme.SetRootColor("--panels", document.getElementById("color_panels").value);
        };

        this.colorObjectFullBackground = document.getElementById("color_object_full_background");
        this.colorObjectFullBackground.value = this.GetRootColor("--object_full_background");
        this.colorObjectFullBackground.oninput = function () {
            Theme.SetRootColor("--object_full_background", document.getElementById("color_object_full_background").value);
        };

        this.colorOptions = document.getElementById("color_options");
        this.colorOptions.value = this.GetRootColor("--options");
        this.colorOptions.oninput = function () {
            Theme.SetRootColor("--options", document.getElementById("color_options").value);
        };

        this.colorStatisticsHover = document.getElementById("color_statistics_hover");
        this.colorStatisticsHover.value = this.GetRootColor("--statistics_path_hover");
        this.colorStatisticsHover.oninput = function () {
            Theme.SetRootColor("--statistics_path_hover", document.getElementById("color_statistics_hover").value);
        };

        let colorSearchCircle = document.getElementById("color_search_circle");
        colorSearchCircle.value = this.GetRootColor("--search_circle");
        colorSearchCircle.oninput = () => {
            Theme.SetRootColor("--search_circle", colorSearchCircle.value);
        };
    }

    static GetRootColor(path) {
        return getComputedStyle(document.documentElement).getPropertyValue(path).replace(" ", "");
    }

    static SetRootColor(path, value) {
        document.documentElement.style.setProperty(path, value);
        localStorage.setItem(path, value);
    }

    static SetDarkTheme() {
        Theme.SetRootColor("--background", "#000000");
        Theme.SetRootColor("--object_p_background", "#000000");
        Theme.SetRootColor("--object_p_color", "#ffffff");
        Theme.SetRootColor("--first", "#ffa500");
        Theme.SetRootColor("--second", "#9acd32");
        Theme.SetRootColor("--panels", "#000000");
        Theme.SetRootColor("--object_full_background", "#000000");
        Theme.SetRootColor("--options", "#000000");
        Theme.SetRootColor("--statistics_path_hover", "#ffffff");
        Theme.SetRootColor("--search_circle", "#ffa500");

        Theme.SetRootColor("--object", "rgba(255,255,255,0.1)");

        MAP.UpdateTheme("dark");
        Theme.SetMapTheme("dark");
    }

    static SetNeonTheme() {
        Theme.SetRootColor("--background", "#343434"); //52 52 52
        Theme.SetRootColor("--object_p_background", "#dddddd"); // 221 221 221
        Theme.SetRootColor("--object_p_color", "#dfffff"); // 223 255 255
        Theme.SetRootColor("--first", "#ff88f9"); // 255 136 249
        Theme.SetRootColor("--second", "#3ccbdb"); // 60 203 219
        Theme.SetRootColor("--panels", "#292423"); // 41 36 35
        Theme.SetRootColor("--object_full_background", "#121212"); // 116 116 116
        Theme.SetRootColor("--options", "#292929"); // 41 41 41
        Theme.SetRootColor("--statistics_path_hover", "#ffffff"); // 255 255 255
        Theme.SetRootColor("--search_circle", "#ff88f9");

        Theme.SetRootColor("--object", "rgba(255,255,255,0.1)");

        MAP.UpdateTheme("dark");
        Theme.SetMapTheme("dark");
    }

    static SetWhiteThemeDomria() {
        Theme.SetRootColor("--background", "#ffffff");
        Theme.SetRootColor("--object_p_background", "#dddddd");
        Theme.SetRootColor("--object_p_color", "#000000");
        Theme.SetRootColor("--first", "#3c9806");
        Theme.SetRootColor("--second", "#256799");
        Theme.SetRootColor("--panels", "#ffffff");
        Theme.SetRootColor("--object_full_background", "#eeeeee");
        Theme.SetRootColor("--options", "#ffffff");
        Theme.SetRootColor("--statistics_path_hover", "#000000");
        Theme.SetRootColor("--search_circle", "#3c9806");

        Theme.SetRootColor("--object", "rgba(0,0,0,0.05)");

        MAP.UpdateTheme("light");
        Theme.SetMapTheme("light");
    }

    static LoadColors() {
        if (!localStorage.getItem("--search_circle"))
            Theme.SetRootColor("--search_circle", localStorage.getItem("--search_circle"));

        if (!localStorage.getItem("--background"))
            Theme.SetRootColor("--background", localStorage.getItem("--background"));

        if (!localStorage.getItem("--object_p_background"))
            Theme.SetRootColor("--object_p_background", localStorage.getItem("--object_p_background"));

        if (!localStorage.getItem("--object_p_color"))
            Theme.SetRootColor("--object_p_color", localStorage.getItem("--object_p_color"));

        if (!localStorage.getItem("--first"))
            Theme.SetRootColor("--first", localStorage.getItem("--first"));

        if (!localStorage.getItem("--second"))
            Theme.SetRootColor("--second", localStorage.getItem("--second"));

        if (!localStorage.getItem("--panels"))
            Theme.SetRootColor("--panels", localStorage.getItem("--panels"));

        if (!localStorage.getItem("--object_full_background"))
            Theme.SetRootColor("--object_full_background", localStorage.getItem("--object_full_background"));

        if (!localStorage.getItem("--options"))
            Theme.SetRootColor("--options", localStorage.getItem("--options"));

        if (!localStorage.getItem("--statistics_path_hover"))
            Theme.SetRootColor("--statistics_path_hover", localStorage.getItem("--statistics_path_hover"));

        if (!localStorage.getItem("--object"))
            Theme.SetRootColor("--object", localStorage.getItem("--object"));
    }

    static SetMapTheme(value) {
        localStorage.setItem("mapTheme", value);
    }

    static GetMapTheme() {
        return localStorage.getItem("mapTheme");
    }
}

document.getElementById("btn_theme_dark").onclick = () => {
    Theme.SetDarkTheme();
    Theme.SetOptionalColor();
};

document.getElementById("btn_theme_white_domria").onclick = () => {
    Theme.SetWhiteThemeDomria();
    Theme.SetOptionalColor();
};

document.getElementById("btn_theme_neon").onclick = () => {
    Theme.SetNeonTheme();
    Theme.SetOptionalColor();
};

Theme.LoadColors();
Theme.SetOptionalColor();
