import { SvgElement } from "./svgElement.js"
import { Literal } from './literal.js'

class Text extends SvgElement {
    constructor(x, y, text) {
        super("text")
        this.attributes['x'] = new Value(x)
        this.attributes['y'] = new Value(y)
        this.children = [ new Literal(text) ]
    }
}