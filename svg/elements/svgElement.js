class SvgElement {
    constructor(name) {
        this.name = name
        this.children = []
        this.attributes = {}
    }

    setAttribute(key, value) {
        this.attributes[key] = value
    }

    addClass(value) {
        this.attributes['class'] = value;
    }

}

export { SvgElement }
