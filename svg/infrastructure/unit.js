class Unit {
    constructor(unit) { 
        this.unit = unit
    }

    toString() {
        return `${this.unit}`
    }

}

const Units = {
    px: new Unit('px')
}

export { Unit, Units }
