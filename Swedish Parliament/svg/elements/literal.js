import { SvgElement } from "./svgElement.js";

class Literal extends SvgElement {
    constructor(content) {
        super()
        this.content = content
    }

    toString() {
        return content
    }
}

export { Literal }