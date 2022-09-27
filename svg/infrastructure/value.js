import { Units } from "./unit.js"

class Value {
    constructor(value, unit = Units.px) {
        this.value = value
        this.unit = unit
    }

    toString() {
        return `${this.value}${this.unit}`
    }
}

export { Value }