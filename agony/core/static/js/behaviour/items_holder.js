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

        this.paginationButton = document.createElement("button");
        this.paginationButton.setAttribute("class", "paginationButton");

        this.paginationButton.onclick = () => action();
        this.holderNode.appendChild(this.paginationButton);
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
}