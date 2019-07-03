window.onload = function () {
    Setup();
};
let canvas;
let renderer;
let camera;
window.onresize = function () {
    canvas = document.getElementById("canvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true
    });
    renderer.setClearColor(0x000000);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(innerWidth, innerHeight);

    camera = new THREE.PerspectiveCamera(55, canvas.width / canvas.height);
    camera.rotation.x = -Math.PI / 5;
    camera.position.set(0, -100, 0);
};

let setup = true;
let plane;
let light;
let buildings = [];

let buildingCount = 15;

let buildingSize = 100;

let buildingOff = 100;

let buildingsOffsetZ = -1000;

let buildingsScaleX;

let buildingColor = "black";
let fogColor = "white";

function Setup() {
    canvas = document.getElementById("canvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true
    });
    renderer.setClearColor(0x000000);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(innerWidth, innerHeight);

    scene = new THREE.Scene();
    fogColor = new THREE.Color(fogColor);
    scene.background = fogColor;
    scene.fog = new THREE.Fog(fogColor, 0.0040, 2000);

    camera = new THREE.PerspectiveCamera(55, canvas.width / canvas.height);
    camera.rotation.x = -Math.PI / 5;
    camera.position.set(0, -100, 0);

    plane = new Plane();
    plane.show();

    for (let x = 0; x < buildingCount; x++) {
        buildings[x] = [];
        for (let y = 0; y < buildingCount; y++) {
            buildings[x][y] = new Building();
            buildings[x][y].show(x, y);
        }
    }

    let update = function () {
        let scroll = window.pageYOffset || document.documentElement.scrollTop;
        camera.position.set(0, scroll / 5 - 100, camera.position.z);
        camera.rotation.y = scroll / 2000;

        buildingsScaleX += buildingsScaleX < 1 ? 0.005 : 0;

        for (let x = 0; x < buildingCount; x++) {
            for (let y = 0; y < buildingCount; y++) {
                if (!!buildings[x][y]) {
                    let b = buildings[x][y];
                    const bMesh = b.mesh.scale;
                    const bPosition = b.mesh.position;

                    bMesh.y = buildingsScaleX;

                    bPosition.z += 1;
                    if (bPosition.z > buildingCount * (buildingSize + buildingOff) / 2 + buildingsOffsetZ) {
                        bPosition.z = -buildingCount / 2 * (buildingSize + buildingOff) + buildingsOffsetZ;
                    }
                }
            }
        }

        renderer.render(scene, camera);
        requestAnimationFrame(update);
    };

    if (setup) {
        setup = false;
        update();
    }
}

buildingsScaleX = 0;

function Building() {
    this.geometry;
    this.mesh;
    this.material;
    this.height = Math.random() * 700 + 100;
    this.size = Math.random() * buildingSize + 50;

    this.show = (x, z) => {
        if (Math.random() > 0.6) {
            this.geometry = new THREE.BoxGeometry(this.size, this.height, this.size);

        } else {
            this.geometry = new THREE.CylinderGeometry(
                this.size / 2,
                this.size / 2,
                this.height,
                (Math.random() * 5 + 3) | 0
            );
        }
        this.material = new THREE.MeshBasicMaterial({
            color: buildingColor,
        });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.position.x = x * (buildingSize + buildingOff) - buildingCount / 2 * (buildingSize + buildingOff);
        this.mesh.position.y = -800;
        this.mesh.position.z = z * (buildingSize + buildingOff) - buildingCount / 2 *
            (buildingSize + buildingOff) + buildingsOffsetZ;
        this.mesh.scale.y = 0.0001;
        this.mesh.rotation.x = 50;
        scene.add(this.mesh);
    }
}

function Plane() {
    this.geometry;
    this.mesh;
    this.material;

    this.show = function () {
        this.geometry = new THREE.PlaneGeometry(10000, 10000, 2, 2);

        this.material = new THREE.MeshBasicMaterial({
            color: buildingColor,
        });

        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.rotation.x = -Math.PI / 2;
        this.mesh.position.y = -800;

        scene.add(this.mesh);
    }
}
