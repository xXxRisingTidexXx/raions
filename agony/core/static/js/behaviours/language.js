class Language {
	constructor() {
		this.item = {
			type: "Type",
			url: "URL",
			published: "Published",
			address: "Address",
			price: "Price",
			rate: "Rate",
			area: "Area",
			livingArea: "Living area",
			kitchenArea: "Kitchen area",
			rooms: "Rooms",
			floor: "Floor",
			totalFloor: "Total floor",
			ceilingHeight: "Ceiling height",
			constructionYear: "Construction year",
			planing: "Planing",
			wallType: "Wall type",
			doorType: "Door type",
			windowType: "Window type",
			bathrooms: "Bathrooms",
			bedrooms: "Bedrooms",
			elevators: "Elevators",
			buildingType: "Building type",
			heating: "Heating",
			warming: "Warming",
			gas: "Gas",
			furniture: "Furniture",
			state: "State",
			housing: "Housing"
		};

		this.alternativeName = {
			"housing" : this.item.housing,
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
			noSaves: "[ You have no saves ]",
			noFound: "[ No objects found ]",
		}
	}
}