class Filters {
    constructor() {
        this.detailsCount = 0;
        this.detailNodes = new Set();

        this.node = {
            filterObjects: document.getElementById("div_panel_filters_objects"),
            state: document.getElementById("filters_select_state"),
            locality: document.getElementById("filters_select_locality"),
            county: document.getElementById("filters_select_county"),
            numeric: {
                area: {
                    from: document.getElementById("filters_area_from"),
                    to: document.getElementById("filters_area_to")
                },
                kitchenArea: {
                    from: document.getElementById("filters_kitchen_area_from"),
                    to: document.getElementById("filters_kitchen_area_to"),
                },
                livingArea: {
                    from: document.getElementById("filters_living_area_from"),
                    to: document.getElementById("filters_living_area_to"),
                },
                rooms: {
                    from: document.getElementById("filters_rooms_from"),
                    to: document.getElementById("filters_rooms_to")
                },
                floor: {
                    from: document.getElementById("filters_floor_from"),
                    to: document.getElementById("filters_floor_to")
                },
                totalFloor: {
                    from: document.getElementById("filters_total_floor_from"),
                    to: document.getElementById("filters_total_floor_to")
                },
                ceilingHeight: {
                    from: document.getElementById("filter_celling_height_from"),
                    to: document.getElementById("filter_celling_height_to")
                }
            }
        };

        for (let k1 in this.node.numeric) {
            for (let k2 in this.node.numeric[k1]) {
                this.node.numeric[k1][k2].oninput = () => {
                    this.node.numeric[k1][k2].value = this.node.numeric[k1][k2].value.replace("-", "");
                    WINDOWS.AlertBoxHide();
                }
            }
        }
    }

    Verify() {
        for (let k1 in this.node.numeric) {
            if (this.node.numeric[k1].to.value !== "" && this.node.numeric[k1].from.value !== "") {
                if ((+this.node.numeric[k1].to.value) < (+this.node.numeric[k1].from.value)) {
                    WINDOWS.AlertBoxShow(450);
                    WINDOWS.AlertBoxSetMessage(`Some troubles in filter ${k1}`);
                    return false;
                }
            }
        }
        return true;
    }

    GetParameters() {
        let dict = {};

        if (this.node.state.value !== "") {
            dict["state"] = this.node.state.value;
        }
        if (this.node.locality.value !== "") {
            dict["locality"] = this.node.locality.value;
        }
        if (this.node.county.value !== "") {
            dict["county"] = this.node.county.value;
        }

        if (this.node.numeric.area.from.value !== "") {
            dict["area_from"] = +this.node.numeric.area.from.value;
        }
        if (this.node.numeric.area.to.value !== "") {
            dict["area_to"] = +this.node.numeric.area.to.value;
        }

        if (this.node.numeric.kitchenArea.from.value !== "") {
            dict["kitchen_area_from"] = +this.node.numeric.kitchenArea.from.value;
        }
        if (this.node.numeric.kitchenArea.to.value !== "") {
            dict["kitchen_area_to"] = +this.node.numeric.kitchenArea.to.value;
        }

        if (this.node.numeric.livingArea.from.value !== "") {
            dict["living_area_from"] = +this.node.numeric.livingArea.from.value;
        }
        if (this.node.numeric.livingArea.to.value !== "") {
            dict["living_area_to"] = +this.node.numeric.livingArea.to.value;
        }

        if (this.node.numeric.rooms.from.value !== "") {
            dict["rooms_from"] = +this.node.numeric.rooms.from.value;
        }
        if (this.node.numeric.rooms.to.value !== "") {
            dict["rooms_to"] = +this.node.numeric.rooms.to.value;
        }

        if (this.node.numeric.floor.from.value !== "") {
            dict["floor_from"] = +this.node.numeric.floor.from.value;
        }
        if (this.node.numeric.floor.to.value !== "") {
            dict["floor_to"] = +this.node.numeric.floor.to.value;
        }

        if (this.node.numeric.totalFloor.from.value !== "") {
            dict["total_floor_from"] = +this.node.numeric.totalFloor.from.value;
        }
        if (this.node.numeric.totalFloor.to.value !== "") {
            dict["total_floor_to"] = +this.node.numeric.totalFloor.to.value;
        }

        if (this.node.numeric.ceilingHeight.from.value !== "") {
            dict["ceiling_height_from"] = +this.node.numeric.ceilingHeight.from.value;
        }
        if (this.node.numeric.ceilingHeight.to.value !== "") {
            dict["ceiling_height_to"] = +this.node.numeric.ceilingHeight.to.value;
        }

        dict["details"] = [];
        this.detailNodes.forEach(v => {
            if (v.children[0].value !== "")
                dict["details"].push(v.children[0].value);
        });

        console.table(dict);
        return dict;
    }

    AutocompleteGeolocation(nodeToFill, unitName) {
        let params = {};
        if (this.node.state.value !== "") {
            params["state"] = this.node.state.value;
        }
        if (this.node.locality.value !== "") {
            params["locality"] = this.node.locality.value;
        }
        if (this.node.county.value !== "") {
            params["county"] = this.node.county.value;
        }
        AJAX.GetGeolocationAutocomplete(nodeToFill, unitName, params);
    }

    AddAutocompleteOption(node, option) {
        let optionNode = document.createElement("option");

        optionNode.value = option;
        optionNode.innerText = option;

        node.appendChild(optionNode);
    }

    RemoveAutocompleteOptions(node) {
        for (let i = node.children.length - 1; i >= 0; i--) {
            node.removeChild(node.children[0]);
        }
    }

    AddDetail() {
        this.node.filterObjects.removeChild(this.node.filterObjects.children[this.node.filterObjects.children.length - 1]);

        let hr = document.createElement("hr");
        let div = document.createElement("div");
        let input = document.createElement("input");
        let datalist = document.createElement("datalist");
        let button = document.createElement("button");

        div.setAttribute("class", "filters_detail");
        input.setAttribute("type", "text");
        input.setAttribute("list", `filter_detail_${this.detailsCount}_datalist`);

        input.id = `filter_detail_${this.detailsCount}`;
        datalist.id = `filter_detail_${this.detailsCount}_datalist`;

        button.innerHTML = "✖";

        div.appendChild(input);
        div.appendChild(datalist);
        div.appendChild(button);

        button.onclick = () => this.RemoveDetail(div);

        this.node.filterObjects.appendChild(div);
        this.node.filterObjects.appendChild(hr);

        this.detailNodes.add(div);
        this.detailsCount++;

        input.oninput = () => {
            let val = input.value;
            if (val.length % 2 === 0 && val.length !== 0) {
                FILTERS.RemoveAutocompleteOptions(datalist);
                AJAX.GetDetailsAutocomplete(datalist, val);
            }
        };
    }

    RemoveDetail(node) {
        this.detailNodes.delete(node);
        this.node.filterObjects.removeChild(node);
    }
}