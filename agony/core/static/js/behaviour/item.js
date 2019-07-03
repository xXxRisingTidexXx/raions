class Item {
    constructor(json, action) {
        this.json = json;
        this.action = action;
        this.node = this.BuildItemExample();

        let markerTitle =
            `${LANGUAGE.item.price} : ${Item.FormatPrice(json.price)} $<br>
            ${LANGUAGE.item.rate} : ${Item.FormatPrice(json.rate)} $<br>
            ${LANGUAGE.item.rooms} : ${json.rooms}`;

        if (action === "save") {
            this.marker = MAP.AddMarkerToLayer(
                json.geolocation.geometry["coordinates"][1],
                json.geolocation.geometry["coordinates"][0],
                markerTitle,
                MAP.savesLayer,
                "https://image.flaticon.com/icons/svg/138/138945.svg"
            );
            this.marker.on('dblclick', (e) => {
                if (!e.originalEvent.ctrlKey) {
                    WINDOWS.Toggle("saves");
                    this.node.scrollIntoView({
                        inline: "center", behavior: "smooth"
                    });
                    if (this.node.style.borderTopWidth !== "10px") {
                        this.node.click();
                    }
                }else{
                    this.ShowFull();
                }
            });
        } else {
            this.marker = MAP.AddMarkerToLayer(
                json.geolocation.geometry["coordinates"][1],
                json.geolocation.geometry["coordinates"][0],
                markerTitle,
                MAP.searchLayer,
                "https://image.flaticon.com/icons/svg/684/684908.svg"
            );
            this.marker.on('dblclick', (e) => {
                if (!e.originalEvent.ctrlKey) {
                    WINDOWS.TargetSearchTypeWindow("items");
                    this.node.scrollIntoView({
                        inline: "center", behavior: "smooth"
                    });
                    if (this.node.style.borderTopWidth !== "10px") {
                        this.node.click();
                    }
                }else{
                    this.ShowFull();
                }
            });
        }

        return this.node;
    }

    BuildItemExample() {
        let buildNode = document.createElement("div");
        buildNode.setAttribute("class", "obj_example");

        buildNode.onclick = () => {
            if (buildNode.style.borderTopWidth === "10px") {
                buildNode.style.borderTopWidth = "0px";
                buildNode.style.borderBottomWidth = "0px";
            } else {
                buildNode.style.borderTopWidth = "10px";
                buildNode.style.borderBottomWidth = "10px";
            }
        };

        let geo = [];
        if (this.json.geolocation.properties.state) {
            geo.push(this.json.geolocation.properties.state);
        }
        if (this.json.geolocation.properties.locality) {
            geo.push(this.json.geolocation.properties.locality);
        }
        if (this.json.geolocation.properties.county) {
            geo.push(this.json.geolocation.properties.county);
        }

        buildNode.appendChild(this.NewItemExampleParagraph(
            geo.join(", "),
            "address",
            buildNode.onclick
        ));
        buildNode.appendChild(this.NewItemExampleParagraph(
            `<b>${LANGUAGE.item.price}</b><br>${Item.FormatPrice(this.json.price)} $`,
            "price",
            buildNode.onclick
        ));
        buildNode.appendChild(this.NewItemExampleParagraph(
            `<b>${LANGUAGE.item.area}</b><br>${this.json.area} m<sup>2</sup>`,
            "area",
            buildNode.onclick
        ));
        buildNode.appendChild(this.NewItemExampleParagraph(
            `<b>${LANGUAGE.item.rooms}</b><br>${this.json.rooms}`,
            "rooms",
            buildNode.onclick
        ));

        buildNode.appendChild(this.NewItemExampleImage());

        buildNode.appendChild(this.NewItemExampleButtonAction(buildNode.onclick));

        buildNode.appendChild(this.NewItemExampleButtonSource(buildNode.onclick));

        buildNode.appendChild(this.NewItemExampleButtonMap(buildNode.onclick));

        buildNode.appendChild(this.NewItemExampleButtonFullItem(buildNode.onclick));

        return buildNode;
    }

    NewItemExampleParagraph(text, attr, event) {
        let par = document.createElement("P");
        par.setAttribute("class", attr);
        par.innerHTML = text;

        let onClick = () => {
            if (par.style.borderTopWidth === "3px") {
                par.style.borderTopWidth = "0px";
                par.style.borderBottomWidth = "0px";
            } else {
                par.style.borderTopWidth = "3px";
                par.style.borderBottomWidth = "3px";
            }
        };

        par.onclick = () => {
            onClick();
            event();
        };

        return par
    }

    NewItemExampleImage() {
        let image = document.createElement("img");
        image.setAttribute("class", "image");
        if (!!this.json["avatar"]) {
            image.src = this.json["avatar"];
        } else {
            image.src = "../static/images/home.png";
            image.style.width = "200px";
            image.style.margin = "auto";
        }
        return image;
    }

    NewItemExampleButtonAction(event) {
        let button = document.createElement("div");
        button.setAttribute("class", "buttonSave");

        let image = document.createElement("IMG");

        if (this.action === "save") {
            image.src = "../static/images/delete.png";
            button.onclick = () => {
                this.Remove();
                event();
            }
        } else {
            image.src = "../static/images/bookmark.png";
            button.onclick = () => {
                this.Save();
                event();
            }
        }

        button.appendChild(image);

        return button;
    }

    NewItemExampleButtonSource(event) {
        let button = document.createElement("div");
        button.setAttribute("class", "buttonShowWeb");

        let image = document.createElement("IMG");
        image.src = "../static/images/global.png";
        button.appendChild(image);

        button.onclick = () => {
            let win = window.open(this.json.url, '_blank');
            win.focus();
            event();
        };

        return button;
    }

    NewItemExampleButtonMap(event) {
        let button = document.createElement("div");
        button.setAttribute("class", "buttonShowMap");

        let image = document.createElement("IMG");
        image.src = "../static/images/mapPointer.png";
        button.appendChild(image);

        button.onclick = (e) => {
            if (e.ctrlKey) {
                let url = `http://www.google.com/maps/place/${this.json.geolocation.geometry["coordinates"][1]},${this.json.geolocation.geometry["coordinates"][0]}`;
                window.open(url, '_blank');
                window.focus();
            } else {
                if (WINDOWS.openedWindow !== "search") {
                    WINDOWS.Toggle("search");
                }
                WINDOWS.TargetSearchTypeWindow("map");
                MAP.myMap.setView(this.marker.getLatLng(), 20);
                if (this.action === "save") {
                    if (!MAP.itemsLayers._layerControlInputs[2].checked) {
                        MAP.itemsLayers._layerControlInputs[2].click();
                    }
                    if (MAP.itemsLayers._layerControlInputs[3].checked) {
                        MAP.itemsLayers._layerControlInputs[3].click();
                    }
                } else {
                    if (MAP.itemsLayers._layerControlInputs[2].checked) {
                        MAP.itemsLayers._layerControlInputs[2].click();
                    }
                    if (!MAP.itemsLayers._layerControlInputs[3].checked) {
                        MAP.itemsLayers._layerControlInputs[3].click();
                    }
                }
            }
            event();
        };

        return button;
    }

    NewItemExampleButtonFullItem(event) {
        let button = document.createElement("div");
        button.setAttribute("class", "buttonShowFull");

        let image = document.createElement("img");
        image.src = "../static/images/home.png";
        button.appendChild(image);

        button.onclick = () => {
            this.ShowFull();
            event();
        };

        return button;
    }

    Save() {
        AJAX.SaveItem(this.json);
    }

    Remove() {
        AJAX.RemoveItem(this.json, this.node);
        MAP.RemoveMarkerFromSavesLayer(this.marker, MAP.savesLayer);
    }

    ShowFull() {
        Item.FullClear();
        this.FullAddAvatar();

        let buttonsParams = {
            source: {
                url: this.json.url,
            },
            map: {
                url: `http://www.google.com/maps/place/${this.json.geolocation.geometry["coordinates"][1]},${this.json.geolocation.geometry["coordinates"][0]}`,
            }
        };
        this.FullSetButtonsAction(buttonsParams);

        let geo = [];
        let geoAdd = (p) => {if (!!p) geo.push(p)};

        geoAdd(this.json.geolocation.properties["state"]);
        geoAdd(this.json.geolocation.properties["locality"]);
        geoAdd(this.json.geolocation.properties["county"]);
        geoAdd(this.json.geolocation.properties["neighbourhood"]);
        geoAdd(this.json.geolocation.properties["road"]);
        geoAdd(this.json.geolocation.properties["house_number"]);

        let mainParams = [["geolocation", "", geo.join(", ")]];

        if (!!this.json.price) {
            mainParams.push(["price", LANGUAGE.item.price + " : ", Item.FormatPrice(this.json.price) + " $"]);
        }
        if (!!this.json.rate) {
            mainParams.push(["rate", LANGUAGE.item.rate + " : ", Item.FormatPrice(this.json.rate) + " $"]);
        }
        Item.FullAddMainParameters(mainParams);

        let params = [];

        if (!!this.json["area"]) {
            params.push([
                "../static/images/area-measure.png",
                LANGUAGE.item.area + " : ",
                this.json["area"] + " m<sup>2</sup>"
            ]);
        }

        if (!!this.json["living_area"]) {
            params.push([
                "../static/images/armchair.png",
                LANGUAGE.item.livingArea + " : ",
                this.json["living_area"] + " m<sup>2</sup>"
            ]);
        }

        if (!!this.json["kitchen_area"]) {
            params.push([
                "../static/images/cooking_pot.png",
                LANGUAGE.item.kitchenArea + " : ",
                this.json["kitchen_area"] + " m<sup>2</sup>"
            ]);
        }

        if (!!this.json["rooms"]) {
            params.push([
                "../static/images/cube.png",
                LANGUAGE.item.rooms + " : ",
                this.json["rooms"]
            ]);
        }

        if (!!this.json["floor"]) {
            params.push([
                "../static/images/balcony.png",
                LANGUAGE.item.floor + " : ",
                this.json["floor"]
            ]);
        }

        if (!!this.json["total_floor"]) {
            params.push([
                "../static/images/roof.png",
                LANGUAGE.item.totalFloor + " : ",
                this.json["total_floor"]
            ]);
        }

        if (!!this.json["ceiling_height"]) {
            params.push([
                "../static/images/ceiling-height.png ",
                LANGUAGE.item.ceilingHeight + " : ",
                this.json["ceiling_height"]
            ]);
        }

        Item.FullAddParameters(params);

        let details = [];
        for (let i = 0; i < this.json["details"].length; i++) {
            let param = [];
            param.push(LANGUAGE.alternativeName[this.json.details[i]["feature"]] + " : ");
            param.push(this.json["details"][i]["value"]);

            details.push(param);
        }
        Item.FullAddDetails(details);

        WINDOWS.FullItemToggle(true);
    }

    static FullClear() {
        let objectImage = document.getElementById("flat_image");
        while (objectImage.children.length !== 0) {
            objectImage.removeChild(objectImage.children[0]);
        }

        let objectMainParams = document.getElementById("flat_main_params");
        while (objectMainParams.children.length !== 0) {
            objectMainParams.removeChild(objectMainParams.children[0]);
        }

        let objectParams = document.getElementById("flat_params_optional");
        while (objectParams.children.length !== 0) {
            objectParams.removeChild(objectParams.children[0]);
        }

        let objectDetails = document.getElementById("flat_params_details");
        while (objectDetails.children.length !== 0) {
            objectDetails.removeChild(objectDetails.children[0]);
        }
    }

    FullAddAvatar() {
        let container = document.getElementById("flat_image");

        let image = document.createElement("img");
        if (!!this.json["avatar"]) {
            image.src = this.json["avatar"];
        } else {
            image.src = "../static/images/home.png";
        }

        container.appendChild(image);
    }

    static FullAddMainParameters(params) {
        let objectMainParamsContainer = document.getElementById("flat_main_params");
        for (let i = 0; i < params.length; i++) {
            let paramNode = document.createElement("P");

            paramNode.innerHTML = params[i][1] + params[i][2];
            paramNode.setAttribute("class", params[i][0]);

            objectMainParamsContainer.appendChild(paramNode);
        }
    }

    static FullAddParameters(params) {
        let objectParamsContainer = document.getElementById("flat_params_optional");
        for (let i = 0; i < params.length; i++) {
            let container = document.createElement("div");
            let imageContainer = document.createElement("div");
            let image = document.createElement("IMG");
            let pName = document.createElement("P");
            let pDescription = document.createElement("P");

            image.src = params[i][0];
            pName.innerHTML = "<b>" + params[i][1] + "</b >";
            pDescription.innerHTML = params[i][2];

            imageContainer.appendChild(image);
            container.appendChild(imageContainer);
            container.appendChild(pName);
            container.appendChild(pDescription);
            objectParamsContainer.appendChild(container);
        }
    }

    static FullAddDetails(details) {
        let objectDetailsContainer = document.getElementById("flat_params_details");
        for (let i = 0; i < details.length; i++) {
            let container = document.createElement("div");
            let pName = document.createElement("P");
            let pDescription = document.createElement("P");

            pName.innerHTML = "<b>" + details[i][0] + "</b>";
            pDescription.innerHTML = details[i][1];

            container.appendChild(pName);
            container.appendChild(pDescription);
            objectDetailsContainer.appendChild(container);
        }
    }

    FullSetButtonsAction(buttonsParams) {
        document.getElementById("btn_full_object_open_map").onclick = function () {
            let win = window.open(buttonsParams.map.url, '_blank');
            win.focus();
        };

        document.getElementById("btn_full_object_open_source").onclick = function () {
            let win = window.open(buttonsParams.source.url, '_blank');
            win.focus();
        }
    }

    static FormatPrice(price) {
        let decim = !!price.toString().split(".")[1] ? "." + price.toString().split(".")[1] : "";
        let cPrice = price.toString().split(".")[0].split("").reverse().join("");
        let newPrice = "";
        for (let i = 0; i < cPrice.length; i++) {
            if (i % 3 === 0 && i !== 0) {
                newPrice += "`";
            }
            newPrice += cPrice[i];
        }

        return newPrice.split("").reverse().join("") + (+decim === 0 ? "" : decim);
    }
}