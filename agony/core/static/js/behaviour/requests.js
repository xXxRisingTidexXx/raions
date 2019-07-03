class Requests {
    static page = 0;
    static serverURL = window.origin + "/";
    static token = sessionStorage.getItem("profile_token");
    static savedFilters = {};
    static fetchParams = {
        getSaved: {
            method: "GET",
            headers: {
                "Authorization": `JWT ${Requests.token}`
            },
        },
        getPage: {
            method: "POST",
            headers: {
                "Authorization": `JWT ${Requests.token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(Requests.savedFilters)
        },
    };

    static GetSaves() {
        fetch(`${Requests.serverURL}saved/`, Requests.fetchParams.getSaved)
            .then(res => {
                let contentType = res.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    return res.json();
                }

                throw new TypeError("No JSON");
            })
            .then(data => {
                SAVES_HOLDER.RemoveAlerts();
                if (data["saved_flats"].length > 0) {
                    data["saved_flats"].forEach(v => {
                        SAVES_HOLDER.AddUniqueItem(v.id);
                        SAVES_HOLDER.AddItem(new Item(v, "save"));
                    });
                } else {
                    SAVES_HOLDER.AddAlert(LANGUAGE.itemsMessage.noSaves);
                }
            })
            .catch(err => {
                SAVES_HOLDER.AddAlert(LANGUAGE.itemsMessage.noSaves);
                console.log(err);
            });
    }

    static GetFiltersPage({
                              addPage = 1,
                              filters = Requests.savedFilters
                          } = {}) {
        Requests.savedFilters = filters;
        Requests.fetchParams.getPage.body = JSON.stringify(Requests.savedFilters);
        Requests.savedFilters["number"] = Requests.page;
        Requests.page += addPage;

        if (Requests.page === 0) {
            SEARCH_HOLDER.Clear();
            SEARCH_HOLDER.ClearUniqueItems();
            SEARCH_HOLDER.paginationButton = null;
        }

        fetch(`${Requests.serverURL}lookup/flats/`, Requests.fetchParams.getPage)
            .then(res => {
                let contentType = res.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    return res.json();
                }

                throw new TypeError("No JSON");
            })
            .then(data => {
                SEARCH_HOLDER.RemoveAlerts();
                if (data.length > 0) {
                    data.forEach(v => {
                        if (!SEARCH_HOLDER.HasUniqueItem(v.id)) {
                            SEARCH_HOLDER.AddUniqueItem(v.id);
                            SEARCH_HOLDER.AddItem(new Item(v, "search"));
                        }
                    });
                    if (data.length === 20) {
                        SEARCH_HOLDER.AddPaginationButton(Requests.GetFiltersPage);
                    }
                } else if (Requests.page === 0) {
                    SEARCH_HOLDER.AddAlert(LANGUAGE.itemsMessage.noFound);
                    SEARCH_HOLDER.RemovePaginationButton();
                } else {
                    SEARCH_HOLDER.RemovePaginationButton();
                }
            })
            .catch(err => {
                SEARCH_HOLDER.AddAlert(LANGUAGE.itemsMessage.noFound);
                console.log(err);
            });
    }

    SaveItem(json) {
        if (!SAVES_HOLDER.HasUniqueItem(json.id)) {
            SAVES_HOLDER.AddUniqueItem(json.id);

            $.ajax({
                url: `${Requests.serverURL}saved/flats/${json.id}/`,
                type: "PATCH",
                async: true,
                headers: {
                    "Authorization": `JWT ${Requests.token}`
                },
                success: () => {
                    WINDOWS.AlertBoxSetMessage("Saved!");
                    if (WINDOWS.filtersPanel.style.right === "0px" ||
                        WINDOWS.filtersPanel.style.right === ""
                    ) {
                        WINDOWS.AlertBoxShow(450);
                    } else {
                        WINDOWS.AlertBoxShow(50);
                    }
                    setTimeout(() => WINDOWS.AlertBoxHide(), 2000);
                }
            });

            SAVES_HOLDER.RemoveAlerts();
            SAVES_HOLDER.AddItem(new Item(json, "save"));
        } else {
            WINDOWS.AlertBoxSetMessage("This item has already saved!");
            if (WINDOWS.filtersPanel.style.right === "0px" ||
                WINDOWS.filtersPanel.style.right === ""
            ) {
                WINDOWS.AlertBoxShow(450);
            } else {
                WINDOWS.AlertBoxShow(50);
            }
            setTimeout(() => WINDOWS.AlertBoxHide(), 2000);
        }
    }

    RemoveItem(json, node) {
        SAVES_HOLDER.DeleteUniqueItem(json.id);

        $.ajax({
            url: `${Requests.serverURL}saved/flats/${json.id}/`,
            type: "DELETE",
            async: true,
            headers: {
                "Authorization": `JWT ${Requests.token}`
            },
        });

        SAVES_HOLDER.RemoveItem(node);
        if (SAVES_HOLDER.holderNode.children.length === 0) {
            SAVES_HOLDER.AddAlert(LANGUAGE.itemsMessage.noSaves);
        }
    }

    GetGeolocationAutocomplete(nodeToFill, unitName, params) {
        $.ajax({
            url: `${Requests.serverURL}geolocation-autocomplete/`,
            type: "GET",
            async: true,
            data: params,
            headers: {
                "Authorization": `JWT ${Requests.token}`
            },

            success: function (result) {
                let valuesToAdd = new Set();
                result.forEach(v => {
                    if (!valuesToAdd.has(v[unitName])) {
                        valuesToAdd.add(v[unitName]);
                    }
                });
                valuesToAdd.forEach(v => FILTERS.AddAutocompleteOption(nodeToFill, v));
            }
        });
    }

    GetDetailsAutocomplete(nodeToFill, value) {
        $.ajax({
            url: `${Requests.serverURL}detail-autocomplete/`,
            type: "GET",
            async: true,
            data: {
                "value": value
            },
            headers: {
                "Authorization": `JWT ${Requests.token}`
            },

            success: (result) => result.forEach(v => FILTERS.AddAutocompleteOption(nodeToFill, v)),
        });
    }
}