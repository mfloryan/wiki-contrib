import { Value } from '../infrastructure/value.js'
import { SvgElement } from './svgElement.js'

class Rectangle extends SvgElement {
    constructor(x, y, width, height) {
        super('rect')
        this.attributes['x'] = new Value(x)
        this.attributes['y'] = new Value(y)
        this.attributes['width'] = new Value(width)
        this.attributes['height'] = new Value(height)
        this.children = undefined
    }
}

export { Rectangle }
