class Element {

    /**
     * 
     * @param {HTMLElement} htmlElement 
     */
    constructor(htmlElement) {
        this.element = htmlElement;
    }

    createChildElement() {
        const child = document.createElement('div');
        this.element.appendChild(child);
        return new Element(child)
    }

    removeChildElements() {
        for (let i = 0; i < this.element.children.length; i++) {
            this.element.removeChild(children[i]);
        }
    }

    /**
     * 
     * @param {string} className 
     * @returns 
     */
    addClass(className) {
        if (!this.element.classList.contains(className)) {
            this.element.classList.add(className);
        }
        return this;
    }

    /**
     * 
     * @param {string} className 
     * @returns 
     */
    removeClass(className) {
        if (this.element.classList.contains(className)) {
            this.element.classList.remove(className);
        }
        return this;
    }
}