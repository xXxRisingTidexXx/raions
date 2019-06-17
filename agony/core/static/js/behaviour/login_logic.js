let passwordNode = document.getElementById("input_password");
let emailNode = document.getElementById("input_email");

const SERVER_URL = window.origin + "/";

document.getElementById("button_submit").onclick = function () {
    if (emailNode.value.length > 0 && passwordNode.value.length > 0) {
        let options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: emailNode.value,
                password: passwordNode.value
            })
        };

        fetch(`${SERVER_URL}auth/`, options)
            .then(res => {
                let contentType = res.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    return res.json();
                }
                throw new TypeError("No JSON");
            })
            .then(data => {
                if (!!data.token) {
                    sessionStorage.setItem("profile_token", data.token);
                    window.location = `${SERVER_URL}profile/`;
                } else {
                    document.getElementById("alertBox").style.top = "0px";
                }
            })
            .catch(err => {
                console.log(err);
                document.getElementById("alertBox").style.top = "0px";
            });
    }
};

document.getElementById("input_email").oninput = function () {
    document.getElementById("alertBox").style.top = "-120px";
};

document.getElementById("input_password").oninput = function () {
    document.getElementById("alertBox").style.top = "-120px";
};

document.getElementById("button_show_password").onclick = function () {
    passwordNode.type = passwordNode.type === "password" ?
        passwordNode.type = "text" :
        passwordNode.type = "password";
};