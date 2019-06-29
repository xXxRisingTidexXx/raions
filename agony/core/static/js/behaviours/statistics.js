class Statistics {
	constructor() {
		this.mapContainer = document.getElementById("map_container_districts_svg");
		this.fullStatistics = document.getElementById("div_full_statistics");
		this.lowestRate = document.getElementById("price_low");
		this.highrstRate = document.getElementById("price_high");
		this.minRate = null;
		this.maxRate = null;
	}

	InitializeStatistics(data) {
		this.minRate = this.GetMinRate(data.counties);
		this.maxRate = this.GetMaxRate(data.counties);
		this.lowestRate.innerText = `${Item.FormatPrice(this.minRate)} $`;
		this.highrstRate.innerText = `${Item.FormatPrice(this.maxRate)} $`;
		this.FillMap(data.counties);
	}

	GetMapHexColor(color) {
		return color.toString(16).length === 2 ? color.toString(16) : "0" + color.toString(16);
	}

	GetMapPieceColor(price, minRange, maxRange) {
		let a = minRange + (((maxRange - minRange) * (price - this.minRate)) / (this.maxRate - this.minRate));
		return a | 0;
	}

	GetMinRate(countiesData) {
		let minRate = null;
		for (let data of countiesData) {
			if (minRate === null) {
				minRate = data.average_rate;
			} else if (data.average_rate < minRate) {
				minRate = data.average_rate;
			}
		}
		return minRate;
	}

	GetMaxRate(countiesData) {
		let maxRate = null;
		for (let data of countiesData) {
			if (maxRate === null) {
				maxRate = data.average_rate;
			} else if (data.average_rate > maxRate) {
				maxRate = data.average_rate;
			}
		}
		return maxRate;
	}

	FillMap(data) {
		data.forEach((v) => this.AddMapPiece(v));
		data.forEach((v) => this.AddMapPieceText(v));
	}

	AddMapPiece(data) {
		let g = document.createElementNS("http://www.w3.org/2000/svg", "g");
		let path = document.createElementNS("http://www.w3.org/2000/svg", "path");

		let red = this.GetMapHexColor(this.GetMapPieceColor(data.average_rate, 237, 192));
		let green = this.GetMapHexColor(this.GetMapPieceColor(data.average_rate, 143, 36));
		let blue = this.GetMapHexColor(this.GetMapPieceColor(data.average_rate, 3, 37));

		g.setAttributeNS(null, "fill", `#${red}${green}${blue}`);
		path.setAttributeNS(null, "transform", "translate(0,1000) scale(0.1,-0.1)");
		path.setAttributeNS(null, "d", data.path);

		path.onclick = () => this.DisplayDistrictStatistics(data);
		// path.onmousemove = (e) => this.ShowInfoBox(e);
		// path.onmouseout = () => this.RemoveInfoBox();

		g.appendChild(path);

		this.mapContainer.appendChild(g);
	}

	AddMapPieceText(data) {
		let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
		let textPrice = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
		let textPercent = document.createElementNS("http://www.w3.org/2000/svg", "tspan");

		let px = data.left * 10 + 30;
		let py = data.top * 10 + 10;
		text.setAttributeNS(null, "x", px);
		text.setAttributeNS(null, "y", py + 10);

		textPrice.setAttributeNS(null, "x", px);
		textPrice.setAttributeNS(null, "y", py + 30);

		textPercent.setAttributeNS(null, "x", px);
		textPercent.setAttributeNS(null, "y", py + 50);

		text.innerHTML = data.name;
		textPrice.innerHTML = `${Item.FormatPrice(data.average_rate)} $`;
		textPercent.innerHTML = data.percent > 0 ? `+${data.percent} %` : `${data.percent} %`;
		textPercent.setAttribute("fill", data.percent > 0 ? "yellowGreen" : "red");

		text.appendChild(textPrice);
		text.appendChild(textPercent);

		this.mapContainer.appendChild(text);
	}

	DisplayDistrictStatistics(data) {
		this.RemoveDistrictStatistics(data);
		this.ShowDistrictStatistics(data);
	}

	ShowDistrictStatistics(data) {
		let container = document.createElement("div");
		let title = document.createElement("p");
		let detail1 = document.createElement("p");
		let detail2 = document.createElement("p");

		container.id = "county_statistics";
		title.className = "title";
		detail1.className = "detail";
		detail2.className = "detail";
		detail2.style.color = data.percent > 0 ? "yellowgreen" : "red";

		title.innerHTML = data.name;
		detail1.innerHTML = `<b>Average rate :</b> ${Item.FormatPrice(data.average_rate)} $`;
		detail2.innerHTML = `<b>Growth in percentage :</b> ${data.percent > 0 ? `+${data.percent}` : data.percent} %`;

		container.appendChild(title);
		container.appendChild(detail1);
		container.appendChild(detail2);
		this.fullStatistics.appendChild(container);
	}

	RemoveDistrictStatistics() {
		let node = document.getElementById("county_statistics");
		if (!!node) {
			node.parentNode.removeChild(node);
		}
	}

	ClearMap() {
		let len = this.mapContainer.children.length;
		for (let i = 0; i < len; i++) {
			this.mapContainer.removeChild(this.mapContainer.children[0]);
		}
	}

	ClearDescription() {
		let len = this.fullStatistics.children.length;
		for (let i = 0; i < len; i++) {
			this.fullStatistics.removeChild(this.fullStatistics.children[0]);
		}
	}

	ClearStatistics() {
		this.ClearMap();
		this.ClearDescription();
	}

	ShowInfoBox(e) {
		let box = document.getElementById("map_statistics_info_box");
		if (!box) {
			this.CreateInfoBox(e);
		} else {
			e = e || window.event;

			let pageX = e.pageX;
			let pageY = e.pageY;
			if (pageX === undefined) {
				pageX = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
				pageY = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
			}

			box.setAttributeNS(null, "x", `${pageX+3}px`);
			box.setAttributeNS(null, "y", `${pageY+3}px`);
		}
	}

	CreateInfoBox(e) {
		e = e || window.event;
		let box = document.createElementNS('http://www.w3.org/2000/svg', 'rect');

		let pageX = e.pageX;
		let pageY = e.pageY;
		if (pageX === undefined) {
			pageX = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
			pageY = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
		}

		box.id = "map_statistics_info_box";

		box.setAttributeNS(null, "x", `${pageX+3}px`);
		box.setAttributeNS(null, "y", `${pageY+3}px`);
		box.setAttributeNS(null, "rx", `20px`);
		box.setAttributeNS(null, "ry", `20px`);
		box.setAttribute("width", "200px");
		box.setAttribute("height", "50px");

		box.style.fill = "rgba(0,0,0,0.9)";
		box.style.stroke = "var(--second)";
		box.style.strokeWidth = "3px";

		this.mapContainer.appendChild(box);
	}

	RemoveInfoBox() {
		let box = document.getElementById("map_statistics_info_box");
		if (!!box) {
			this.mapContainer.removeChild(box);
		}
	}
}

let KievStatMap = {
	counties: [
		{
			path: `M7558 6392 c-36 -13 -92 -60 -260 -219 -117 -111 -234 -219 -260
			-240 -38 -30 -191 -96 -765 -330 -395 -161 -738 -300 -763 -309 -25 -10 -46
			-18 -48 -19 -2 -2 18 -41 43 -87 44 -81 50 -86 107 -112 33 -16 62 -36 65 -45
			2 -9 18 -22 34 -28 27 -10 29 -14 19 -32 -6 -12 -22 -28 -36 -37 -23 -16 -26
			-15 -64 12 -92 67 -126 73 -118 23 2 -19 21 -33 86 -65 99 -49 125 -70 102
			-84 -28 -18 -61 -10 -107 25 -26 20 -51 34 -57 32 -25 -8 -117 -337 -136 -490
			-11 -79 -10 -96 10 -180 53 -221 64 -247 140 -330 44 -49 56 -56 93 -59 37 -3
			45 -8 72 -48 17 -25 43 -83 59 -130 16 -47 30 -87 32 -89 1 -1 13 4 25 13 26
			18 47 10 97 -37 42 -40 53 -29 62 60 4 37 13 89 20 114 16 57 10 76 -32 94
			-18 7 -44 25 -57 39 -24 25 -24 27 -12 93 7 38 14 86 15 108 1 39 2 40 33 37
			27 -2 34 2 39 22 5 20 13 24 66 30 119 12 114 15 128 -59 14 -77 6 -74 175
			-47 100 16 113 16 149 2 l38 -15 -5 -111 -4 -111 44 5 c38 4 49 1 85 -28 l41
			-33 19 22 c10 13 18 33 18 45 0 39 15 49 61 43 39 -5 62 -21 72 -51 2 -6 35 4
			83 26 l79 36 3 46 c3 41 6 46 28 46 13 0 24 2 24 5 0 20 -53 118 -79 144 -43
			44 -49 76 -20 107 12 13 40 30 62 36 32 10 37 15 32 32 -19 69 -25 126 -15
			174 24 130 73 132 187 8 57 -62 65 -67 164 -102 57 -20 112 -40 121 -45 13 -7
			35 -1 80 22 l62 31 105 -17 c59 -9 114 -19 124 -22 17 -5 18 -3 3 26 -25 47
			-21 80 11 92 34 13 22 24 -51 46 -32 10 -58 23 -58 28 0 9 94 54 144 69 15 4
			13 12 -17 62 -40 66 -52 116 -37 149 9 19 34 31 123 60 62 19 118 35 125 35 7
			0 30 -21 52 -46 l39 -45 99 -10 c54 -5 110 -11 123 -12 22 -2 28 7 61 93 20
			52 45 109 56 127 18 30 18 32 1 51 -18 19 -94 45 -173 57 -58 9 -139 59 -175
			108 -56 77 -56 77 -5 156 62 97 61 119 -9 193 -48 51 -57 57 -78 49 -21 -8
			-39 0 -122 56 l-98 65 7 52 6 53 -98 44 c-88 40 -109 55 -229 168 -73 68 -133
			127 -133 131 0 4 34 20 75 35 49 17 73 31 68 39 -3 6 -14 22 -24 36 -12 19
			-15 30 -8 43 6 10 8 26 4 36 -3 11 -1 22 5 26 12 7 14 25 3 24 -5 0 -29 -8
			-55 -17z`,
			name: "Darnytsia",
			top: 48,
			left: 60,
			average_rate: 24000,
			percent: 0.22
		},
		{
			path: `M7180 8972 c0 -43 -9 -67 -51 -144 -57 -102 -57 -104 -40 -257 15
			-136 14 -233 -1 -254 -8 -9 -48 -23 -100 -34 -79 -16 -89 -16 -103 -2 -14 14
			-14 20 0 58 8 24 15 47 15 52 0 42 -232 -53 -407 -167 -68 -44 -83 -58 -83
			-79 0 -36 -21 -83 -92 -208 l-62 -108 -55 6 c-31 3 -202 15 -381 26 -179 11
			-424 26 -544 34 -121 8 -241 15 -268 15 -44 0 -48 -2 -48 -24 0 -21 8 -26 68
			-41 37 -9 75 -24 85 -32 44 -41 45 -162 2 -206 -22 -21 -23 -28 -15 -58 6 -19
			10 -44 10 -57 0 -35 -49 -78 -98 -87 -56 -9 -88 12 -115 75 -16 39 -26 49 -50
			54 -37 8 -95 7 -124 0 -24 -7 -55 -73 -73 -159 -14 -63 -14 -222 0 -295 12
			-65 48 -178 59 -184 4 -3 35 8 68 23 71 34 90 36 518 56 l310 15 27 -30 c39
			-42 41 -62 25 -196 l-15 -119 46 -82 c25 -45 52 -85 60 -88 8 -3 46 -26 84
			-51 l68 -45 30 -97 c16 -53 37 -128 46 -165 21 -85 42 -100 110 -75 41 15 44
			14 49 -3 5 -14 16 -19 39 -19 28 0 36 -5 47 -32 7 -18 14 -35 15 -37 2 -2 24
			10 49 25 l46 29 -7 55 c-4 32 -17 70 -30 90 -25 36 -31 108 -18 191 l6 37 317
			153 c334 161 697 330 794 369 46 18 57 26 50 39 -10 22 -7 90 5 122 9 22 24
			31 82 48 l71 22 -3 51 c-3 49 -1 53 30 74 19 13 53 26 78 30 24 3 44 8 44 10
			0 2 -18 31 -39 64 -44 67 -59 116 -42 133 15 15 68 -11 119 -58 22 -19 43 -35
			47 -35 4 0 5 26 3 57 l-3 56 60 24 c366 147 644 267 693 299 l23 15 -21 26
			c-35 45 -52 120 -57 269 l-6 140 -28 16 c-35 21 -46 60 -30 112 7 23 15 55 18
			71 5 30 4 31 -70 52 -118 35 -219 124 -276 243 -14 30 -26 56 -27 58 -1 2 -16
			-4 -33 -13 -21 -11 -31 -23 -31 -39 0 -32 -16 -43 -80 -51 -30 -3 -63 -9 -72
			-11 -12 -4 -27 15 -60 75 -48 90 -43 88 -153 67 l-69 -14 -206 80 c-113 44
			-211 82 -217 85 -10 4 -13 -9 -13 -45z`,
			name: "Desna",
			top: 26,
			left: 57,
			average_rate: 24900,
			percent: 0.13
		},
		{
			path: `M4965 6930 c-55 -4 -112 -10 -125 -14 -46 -13 -100 -39 -100 -48 0
			-5 16 -32 36 -60 43 -63 43 -61 -36 -229 -85 -180 -110 -251 -110 -313 0 -71
			17 -90 110 -124 42 -16 105 -50 140 -76 36 -26 101 -71 144 -99 75 -49 80 -55
			96 -107 9 -30 26 -74 38 -96 37 -73 138 -198 193 -239 55 -42 104 -108 114
			-156 4 -16 12 -29 18 -29 7 0 344 129 751 287 l739 287 308 300 309 299 -26
			34 -25 34 17 52 c23 70 22 69 52 53 24 -12 31 -12 64 5 21 11 38 25 38 31 0 6
			-11 31 -25 55 l-26 43 -40 -21 c-23 -11 -43 -18 -46 -16 -2 3 -7 27 -11 54 -4
			26 -12 48 -18 48 -6 0 -287 -119 -623 -265 l-613 -265 7 -80 c4 -52 11 -84 21
			-91 12 -9 14 -34 12 -120 l-3 -109 -65 -23 -65 -23 -25 30 c-28 33 -80 48
			-120 33 -20 -7 -34 -3 -73 22 -48 31 -48 31 -44 76 4 37 -3 66 -46 171 l-52
			127 -82 43 -82 44 -41 101 c-44 113 -48 139 -23 166 20 23 21 93 2 167 l-13
			51 -275 -1 c-152 -1 -321 -5 -376 -9z`,
			name: "Dnipro",
			top: 36,
			left: 48,
			average_rate: 18600,
			percent: -0.04
		},
		{
			path: `M4134 5754 c-21 -15 -41 -28 -43 -30 -2 -2 20 -27 49 -56 77 -78 133
			-155 133 -183 0 -32 -26 -61 -75 -86 -43 -22 -65 -51 -74 -97 -12 -58 1 -79
			66 -108 72 -32 81 -57 17 -48 -98 14 -156 -26 -202 -140 -43 -105 -109 -150
			-187 -127 -44 14 -43 14 -52 -15 -4 -14 0 -27 14 -39 20 -18 26 -58 14 -89 -4
			-12 -20 -16 -54 -16 -71 0 -109 -10 -115 -31 -4 -12 -18 -19 -43 -21 -34 -3
			-37 -6 -52 -55 -15 -51 -15 -52 -40 -38 -14 8 -30 14 -37 15 -6 0 -62 -64
			-123 -142 l-113 -141 29 -21 c76 -55 75 -53 62 -138 l-11 -77 36 -45 c38 -46
			113 -90 144 -84 12 2 19 14 21 33 8 92 39 115 155 115 l77 0 0 -39 c0 -27 8
			-49 25 -69 22 -26 23 -32 13 -60 -11 -27 -10 -34 9 -54 15 -17 23 -43 27 -93
			12 -120 16 -136 42 -145 31 -12 31 -42 -1 -97 l-26 -43 55 0 c47 0 57 3 67 23
			6 12 13 23 14 25 2 2 47 -17 100 -42 l97 -46 -56 -47 c-31 -26 -56 -52 -56
			-58 0 -5 18 -30 40 -55 l39 -45 38 23 c21 12 57 32 81 44 l42 22 16 -23 c35
			-50 193 -129 321 -161 49 -13 51 -14 47 -44 -9 -71 -24 -239 -24 -269 0 -27 6
			-36 34 -51 l34 -18 -59 -98 c-32 -54 -59 -99 -59 -101 0 -2 39 -3 86 -1 111 4
			140 -7 155 -61 15 -58 3 -132 -35 -210 l-33 -68 74 -50 73 -50 0 -117 0 -118
			144 0 145 1 31 -30 c68 -65 132 -246 164 -467 9 -57 21 -191 27 -298 6 -107
			13 -196 14 -197 2 -4 665 255 673 262 2 2 -19 32 -48 66 -85 103 -86 124 -4
			147 41 12 94 46 94 62 0 4 -14 13 -30 20 -45 19 -130 102 -130 128 0 41 -41
			130 -81 176 l-40 45 10 73 c13 94 0 122 -108 241 -120 130 -136 172 -78 208
			29 18 43 20 137 15 58 -3 136 -8 173 -12 85 -8 107 7 107 72 0 78 -36 150
			-107 218 -66 62 -113 129 -113 160 0 9 10 46 22 81 l23 64 -21 27 c-11 15 -61
			50 -111 78 -51 28 -103 62 -117 75 -23 22 -25 29 -19 81 l5 56 -55 48 c-69 59
			-80 87 -71 193 l7 82 -41 11 c-30 8 -52 23 -79 57 -73 90 -138 155 -180 180
			-83 48 -123 116 -123 209 0 51 -25 79 -83 94 -70 18 -92 29 -140 73 l-47 42 8
			83 c5 52 13 86 21 92 17 10 50 0 123 -36 59 -29 83 -27 55 3 -8 10 -39 66 -67
			124 -50 103 -74 189 -53 189 16 0 27 -19 58 -100 62 -164 120 -260 159 -260
			32 0 47 38 56 150 5 52 14 109 20 127 6 17 10 48 8 69 -3 36 -6 39 -42 46 -22
			5 -45 13 -53 19 -39 33 13 83 62 61 14 -7 28 -12 31 -12 3 0 4 35 2 78 -3 74
			-4 77 -28 80 -41 6 -53 22 -34 43 9 10 25 21 35 24 17 6 19 17 19 92 0 77 -2
			84 -17 78 -10 -4 -33 -13 -52 -20 -27 -10 -39 -24 -61 -71 -15 -33 -44 -74
			-64 -93 -31 -30 -44 -35 -93 -38 -35 -3 -80 2 -113 12 -30 9 -100 22 -155 30
			-55 7 -113 17 -130 21 -80 19 -117 59 -92 98 14 20 9 37 -63 228 l-79 206 6
			94 6 95 -60 16 c-79 23 -93 22 -139 -9z`,
			name: "Holosiiv",
			top: 60,
			left: 40,
			average_rate: 28100,
			percent: 0.11
		},
		{
			path: `M3315 7605 c-27 -8 -53 -14 -57 -15 -4 0 -30 -20 -57 -44 -57 -51
			-94 -61 -256 -71 -235 -15 -549 -58 -617 -84 -33 -12 -33 -11 -13 -186 11 -96
			19 -133 31 -140 9 -5 157 -110 329 -232 l314 -223 88 0 88 0 1 33 c0 37 61
			138 96 161 13 8 42 17 65 21 34 5 44 4 49 -9 5 -13 22 -16 78 -16 l72 0 21
			-44 22 -44 61 5 c51 5 63 3 74 -12 13 -18 15 -18 51 3 27 17 46 21 70 16 32
			-6 33 -8 28 -40 -5 -29 -3 -34 14 -34 24 0 100 -63 108 -91 5 -16 14 -20 39
			-18 21 2 42 -4 59 -18 24 -19 26 -25 20 -72 l-6 -51 31 3 c18 2 41 12 52 22
			19 17 21 17 52 -8 18 -13 51 -40 72 -59 l40 -35 -22 -37 c-21 -35 -21 -38 -6
			-76 9 -22 19 -40 23 -40 3 0 19 16 35 36 l28 36 25 -24 c24 -23 25 -23 40 -3
			11 15 13 36 8 90 l-6 70 -72 67 -72 67 -55 -5 c-43 -4 -63 -1 -90 15 -19 11
			-54 29 -76 40 -47 22 -169 133 -205 186 -17 24 -32 35 -49 35 -14 0 -45 12
			-69 25 -33 19 -47 23 -57 14 -20 -17 -42 -4 -57 33 -8 18 -47 64 -88 102 -113
			105 -115 108 -123 266 -11 218 -17 270 -32 270 -19 0 -18 10 6 72 11 29 20 54
			20 56 0 7 -82 -1 -125 -13z`,
			name: "Podil",
			top: 26.5,
			left: 24,
			average_rate: 21000,
			percent: 0.08
		},
		{
			path: `M3249 6718 c-12 -23 -31 -55 -42 -69 -19 -27 -19 -29 -2 -102 10 -45
			15 -87 11 -104 -5 -17 -44 -63 -102 -119 -52 -50 -94 -95 -94 -101 0 -6 6 -15
			13 -21 6 -6 199 -61 427 -122 l415 -112 88 -94 c51 -54 97 -94 108 -94 10 0
			39 10 64 22 l45 22 83 -27 c103 -33 117 -34 148 -1 19 20 25 40 30 100 5 64
			10 80 38 114 29 36 32 46 29 98 l-3 57 -53 0 c-50 -1 -56 -4 -87 -40 l-34 -40
			-25 58 c-24 54 -28 57 -61 57 -19 0 -35 3 -35 8 0 4 11 25 25 47 32 53 31 77
			-5 103 -38 28 -43 28 -85 -9 -32 -28 -38 -30 -63 -20 -16 7 -36 25 -45 41 -17
			27 -17 32 -2 60 23 44 17 75 -15 74 -14 -1 -33 -4 -42 -9 -14 -5 -18 -2 -18
			14 0 11 -11 28 -25 37 -14 9 -25 24 -25 33 0 25 -20 41 -54 41 -19 0 -40 10
			-59 27 l-28 28 -42 -23 -41 -23 -17 22 c-14 19 -22 21 -61 15 -41 -6 -47 -4
			-62 19 -15 23 -22 25 -87 25 -64 0 -73 3 -91 25 -15 19 -29 25 -59 25 -35 0
			-40 -3 -60 -42z`,
			name: "Shevchenko",
			top: 35,
			left: 31,
			average_rate: 45300,
			percent: -0.19
		},
		{
			path: `M3022 6122 c-10 -31 -31 -56 -99 -113 -119 -102 -120 -103 -133 -146
			-9 -28 -9 -49 -1 -78 18 -68 216 -415 254 -446 19 -16 45 -50 57 -76 12 -26
			35 -63 51 -81 16 -18 38 -50 49 -72 23 -46 26 -37 -53 -169 -32 -53 -46 -86
			-39 -89 7 -2 12 -20 12 -41 0 -50 15 -64 48 -43 24 16 25 15 81 -48 31 -36 70
			-80 88 -100 l32 -35 16 23 c10 13 27 35 40 50 21 24 26 25 44 14 18 -11 21
			-10 21 7 0 40 10 50 46 44 33 -5 34 -4 34 26 l0 31 84 -6 c80 -7 84 -6 91 15
			4 13 5 24 3 25 -1 1 -16 10 -32 20 -26 16 -28 21 -22 59 4 23 10 45 15 50 4 4
			29 -2 55 -13 53 -24 112 -28 145 -11 27 15 61 68 61 96 0 26 44 120 61 131 7
			4 38 13 68 20 l56 11 -31 12 c-29 11 -32 17 -38 65 -7 51 -5 57 36 124 41 67
			45 71 83 74 35 3 40 6 43 30 3 23 -26 57 -187 230 l-190 203 -408 119 c-224
			65 -413 120 -419 123 -6 2 -16 -14 -22 -35z`,
			name: "Solomyansk",
			top: 43,
			left: 29,
			average_rate: 19900,
			percent: -0.03
		},
		{
			path: `M1465 8039 c-4 -6 -12 -63 -18 -127 l-12 -117 -65 -10 -65 -10 -9
			-57 c-8 -54 -11 -59 -57 -88 -26 -18 -51 -40 -54 -51 -9 -27 -53 -47 -117 -55
			-71 -8 -137 -55 -178 -126 -29 -52 -39 -101 -21 -113 5 -3 12 -18 16 -34 6
			-29 44 -70 82 -90 16 -8 22 -22 25 -62 3 -48 0 -55 -34 -94 -31 -35 -38 -51
			-38 -85 0 -75 -47 -123 -136 -137 -20 -3 -38 -11 -40 -17 -2 -6 -13 -63 -23
			-126 -21 -123 -19 -133 27 -145 40 -10 72 -44 72 -77 0 -21 -19 -49 -81 -116
			-96 -103 -136 -158 -161 -224 -24 -64 -23 -74 9 -90 24 -12 28 -19 25 -52 -2
			-27 2 -45 16 -60 48 -52 52 -84 17 -117 -13 -13 -25 -33 -25 -44 0 -11 -14
			-38 -30 -59 -39 -51 -39 -93 0 -173 25 -53 33 -63 55 -63 38 0 94 26 101 47
			14 46 61 123 74 123 21 0 95 -51 120 -83 27 -34 42 -34 87 0 32 24 34 30 30
			67 -2 28 5 69 24 126 15 47 34 117 42 155 13 64 16 70 38 69 13 0 130 -26 260
			-57 202 -49 240 -56 265 -46 16 6 46 11 67 10 21 0 48 5 60 11 12 7 69 28 127
			48 76 26 106 40 108 53 2 11 -3 20 -15 23 -10 3 -35 32 -57 64 -32 50 -54 70
			-137 122 -54 35 -99 68 -99 74 0 5 6 19 14 29 14 19 15 19 35 1 16 -14 31 -18
			66 -14 l45 6 0 -33 c0 -48 52 -115 90 -115 23 0 35 -8 55 -37 14 -21 25 -48
			25 -60 0 -14 10 -27 27 -35 18 -9 30 -23 33 -43 4 -24 12 -31 42 -38 l36 -9 7
			-76 c10 -113 34 -221 60 -274 34 -68 169 -242 255 -329 42 -42 113 -104 159
			-138 87 -64 283 -167 338 -177 29 -6 33 -3 54 37 12 24 35 63 50 86 42 60 39
			96 -12 147 -23 22 -48 59 -56 81 -7 22 -31 60 -53 86 -56 67 -195 281 -238
			367 -27 55 -36 87 -36 125 -1 76 18 111 88 161 76 55 141 122 155 159 6 16 11
			48 11 72 0 39 5 48 43 82 122 109 160 167 155 236 l-3 42 -105 5 -105 5 -58
			48 c-64 52 -202 146 -452 307 -88 57 -163 108 -167 113 -7 12 -23 118 -39 262
			-6 55 -16 106 -22 113 -6 8 -32 24 -57 37 -26 13 -187 150 -363 309 -175 157
			-324 286 -332 286 -8 0 -17 -5 -20 -11z`,
			name: "Svyatoshyn",
			top: 31,
			left: 12,
			average_rate: 15200,
			percent: 0.09
		},
		{
			path: `M4535 6074 c-8 -20 -15 -39 -15 -42 0 -3 -11 -20 -25 -38 -21 -28
			-25 -43 -25 -104 0 -69 -1 -72 -41 -115 -45 -49 -58 -89 -59 -186 0 -48 8 -74
			58 -180 105 -224 109 -236 87 -306 -11 -36 41 -56 167 -63 89 -5 112 -9 137
			-28 25 -18 43 -22 104 -22 74 0 75 0 110 39 53 58 62 97 61 246 -2 218 -43
			384 -127 512 -46 71 -152 174 -232 225 -65 42 -168 98 -180 98 -2 0 -12 -16
			-20 -36z`,
			name: "Pechersk",
			top: 43,
			left: 40.5,
			average_rate: 19400,
			percent: 0.13
		},
		{
			path: `M2430 8795 l0 -132 -37 -7 c-21 -3 -141 -6 -266 -6 -177 0 -259 -5
			-365 -20 -182 -27 -182 -27 -182 -49 0 -16 18 -25 93 -48 88 -27 92 -30 95
			-59 5 -50 54 -87 150 -114 l82 -23 -6 -36 c-4 -20 -7 -37 -8 -38 -2 -2 -33 1
			-70 5 -61 8 -69 7 -81 -11 -12 -17 -11 -23 7 -47 17 -23 18 -30 7 -48 -7 -12
			-25 -22 -39 -24 -21 -3 -25 -9 -28 -40 -2 -21 -6 -38 -8 -38 -3 0 -57 45 -120
			100 l-115 100 -48 -24 c-44 -23 -49 -24 -64 -9 -14 14 -20 15 -44 4 l-28 -13
			70 -66 c449 -420 804 -722 849 -722 7 0 41 12 77 26 59 25 80 27 269 35 113 4
			273 8 356 8 l152 1 26 34 c39 52 139 97 226 104 82 6 87 0 71 -80 -8 -42 -6
			-98 12 -266 l22 -212 103 -109 c96 -103 107 -111 180 -139 42 -17 95 -33 118
			-36 37 -7 43 -13 78 -73 50 -87 79 -113 125 -113 54 0 64 11 56 58 -6 40 -6
			41 30 51 23 6 77 6 153 1 227 -18 342 -9 342 26 0 7 -12 16 -27 20 -88 19 -99
			28 -78 60 14 21 13 27 -4 66 -11 24 -22 55 -25 69 -9 43 -75 134 -106 146 -46
			17 -84 85 -88 157 -4 55 -1 65 22 93 14 17 38 36 53 42 l28 11 -3 118 c-3 92
			-7 124 -22 149 l-19 32 61 31 c108 54 124 41 120 -101 -3 -104 8 -130 28 -61
			19 65 23 156 10 196 -26 80 -102 139 -225 175 -111 32 -212 108 -287 215 -65
			94 -90 175 -90 294 l1 92 -42 1 c-67 2 -92 12 -90 37 4 32 -36 44 -121 37 -39
			-3 -81 -8 -93 -11 -19 -3 -24 2 -32 33 -5 21 -13 84 -17 141 l-7 102 -47 0
			c-53 0 -51 3 -93 -130 l-14 -45 -19 93 c-10 51 -21 97 -24 101 -3 5 -227 11
			-497 13 l-493 5 0 -132z`,
			name: "Obolon",
			top: 17,
			left: 25,
			average_rate: 16700,
			percent: 0.15
		},
	]
}