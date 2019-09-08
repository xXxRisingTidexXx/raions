class Language {
    constructor() {
        this.item = {
            type: "Тип",
            url: "URL Адресса",
            published: "Опубліковано",
            address: "Адресса",
            price: "Ціна",
            rate: "Ціна за кв. метр",
            area: "Загальна площа",
            livingArea: "Житлова площа",
            kitchenArea: "Площа кухні",
            rooms: "Кількість кімнат",
            floor: "Поверх",
            totalFloor: "Поверховість",
            ceilingHeight: "Висота стелі",
            constructionYear: "Рік побудови",
            planing: "Планування",
            wallType: "Тип стін",
            doorType: "Тип дверей",
            windowType: "Тип вікон",
            bathrooms: "Санвузли",
            bedrooms: "Спальні",
            elevators: "Ліфти",
            buildingType: "Тип будівлі",
            heating: "Опалення",
            warming: "Утеплення",
            gas: "Газ",
            furniture: "Меблі",
            state: "Стан будинку",
            housing: "Тип житла"
        };

        this.alternativeName = {
            "housing": this.item.housing,
            "construction_years": this.item.constructionYear,
            "planning": this.item.planing,
            "state": this.item.state,
            "wall_type": this.item.wallType,
            "door_type": this.item.doorType,
            "window_type": this.item.windowType,
            "bathrooms": this.item.bathrooms,
            "bedrooms": this.item.bedrooms,
            "passenger_elevators": this.item.elevators,
            "building_type": this.item.buildingType,
            "heating": this.item.heating,
            "warming": this.item.warming,
            "gas": this.item.gas,
            "furniture": this.item.furniture,
        };

        this.itemsMessage = {
            noSaves: "[ Немає збережених квартир ]",
            noFound: "[ Нічого не знайдено ]",
        }
    }
}