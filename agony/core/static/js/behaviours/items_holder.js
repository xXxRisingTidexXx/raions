class ItemsHolder {
    constructor(node) {
        this.holderNode = node;
        this.paginationButton = null;
        this.uniqueItems = new Set();
    }

    HasUniqueItem(id) {
        return this.uniqueItems.has(id);
    }

    AddUniqueItem(id) {
        this.uniqueItems.add(id);
    }

    DeleteUniqueItem(id) {
        this.uniqueItems.delete(id);
    }

    ClearUniqueItems() {
        this.uniqueItems = new Set();
    }

    AddItem(node) {
        this.holderNode.appendChild(node);
    }

    RemoveItem(node) {
        this.holderNode.removeChild(node);
    }

    AddAlert(message) {
        let alert = document.createElement("p");

        alert.setAttribute("class", "message");
        alert.innerText = message;

        this.AddItem(alert);
    }

    RemoveAlerts() {
        let messages = this.holderNode.getElementsByClassName("message");
        for (let i = messages.length - 1; i >= 0; i--) {
            this.RemoveItem(messages[0]);
        }
    }

    AddPaginationButton(action) {
        this.RemovePaginationButton();

        let pagButton = document.createElement("button");
        pagButton.setAttribute("class", "paginationButton");
        pagButton.innerHTML = "►";

        pagButton.onclick = () => action();

        this.paginationButton = pagButton;
        this.holderNode.appendChild(pagButton);
    }

    RemovePaginationButton() {
        if (!!this.paginationButton) {
            this.holderNode.removeChild(this.paginationButton);
        }
    }

    Clear() {
        let length = this.holderNode.children.length;
        for (let i = 0; i < length; i++) {
            this.holderNode.removeChild(this.holderNode.children[0]);
        }
    }

    SortBy(sortName) {
        let elements = this.holderNode.getElementsByClassName(sortName);
        let paginationButton = this.holderNode.getElementsByClassName("paginationButton")[0];
        let elementsPrice = [];

        for (let i = 0; i < elements.length; i++) {
            elementsPrice[i] = {};

            let number = elements[i].innerHTML.split(".")[0].match(/\d/g).join("");

            elementsPrice[i].price = +number;
            elementsPrice[i].parrentNode = elements[i].parentElement;
        }

        this.Clear();

        elementsPrice.sort((a, b) => b.price - a.price);

        elementsPrice.forEach(v => this.holderNode.appendChild(v.parrentNode));

        if (!!paginationButton)
            this.AddItem(paginationButton);
    }
}