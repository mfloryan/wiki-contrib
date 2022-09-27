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

    toString() {
        let result = `<${this.name} `
        
        let formattedAttributes = 
            Object.entries(this.attributes)
            .map(entry => `${entry[0]}="${entry[1].toString()}"`)
        result += formattedAttributes.join(" ")

        if (this.children) {
            result += `>`
            result += `</${this.name}>`
        } else {
            result += ` />`
        }
        return result
    }

}

export { SvgElement }
