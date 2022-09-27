import fetch from 'node-fetch';
import fs from 'node:fs/promises';

import *  as svg from './svg/svg.js'

async function getSbcParliamentData() {
    const request_payload = {
        "query": [
          {
            "code": "Region",
            "selection": {
              "filter": "vs:RegionValkretsTot99",
              "values": ["VR00"]
            }
          },
          {
            "code": "Parti",
            "selection": {
              "filter": "item",
                "values": ["M", "C", "FP", "KD", "MP", "NYD", "S", "V", "SD"]
            }
          }
        ],
        "response": { "format": "json" }
      };
    
    
    const scb_response = await fetch(
        'https://api.scb.se/OV0104/v1/doris/sv/ssd/START/ME/ME0104/ME0104C/Riksdagsmandat',
        {method: 'POST', body: JSON.stringify(request_payload), headers: {'Content-Type': 'application/json'}}
    );
    const sbc_data = await scb_response.json();
    var parliament_by_year = {};
    sbc_data.data.forEach(row => {
        if (!parliament_by_year[row.key[2]]) parliament_by_year[row.key[2]] = {}
        parliament_by_year[row.key[2]][row.key[1]] = row.values[0]
    })
    
    return parliament_by_year;
}

async function cache(cacheKey, getSlowValue) {
    const cacheFileName = `${cacheKey}.json`
    let data = undefined
    try {
        data = JSON.parse(await fs.readFile(cacheFileName,'utf8'))
    } catch (e) {
        data = await getSlowValue()
        await fs.writeFile(cacheFileName, JSON.stringify(data), 'utf8')
    }
    return data
}

function rgb(r,g,b) {
    return `rgb(${r},${g},${b})`
}

let swedish_parties = [
    {code: 'V' , name: 'Vänsterpartiet', colour: rgb(145, 20, 20)},
    {code: 'S' , name: 'Socialdemokraterna', colour: rgb(224, 46, 61)},
    {code: 'MP' , name: 'Miljöpartiet', colour: rgb(130, 200, 130)},
    {code: 'C' , name: 'Centerpartiet', colour: rgb(49, 165, 50)},
    {code: 'FP' , name: 'Liberalerna', colour: rgb(30, 105, 170)},
    {code: 'NYD' , name: 'Ny demokrati', colour: rgb(100,80,0) },
    {code: 'KD' , name: 'Kristdemokraterna', colour: rgb(51, 29, 121) },
    {code: 'M' , name: 'Moderaterna', colour: rgb(125, 190, 225) },
    {code: 'SD' , name: 'Sverigedemokraterna', colour: rgb(255, 195, 70)},
]

let party_order = swedish_parties.map(p => p.code);

const parliaments = await cache('riksdagsmandat',getSbcParliamentData)

let structured_parliaments = Object.keys(parliaments).map(year => {
    let results = 
        Object.entries(parliaments[year])
            .map((v) => { return {code: v[0], mandates: Number.parseInt(v[1])}})
            .filter(v => !Number.isNaN(v.mandates) && v.mandates > 0)
    results.sort((a,b) => party_order.indexOf(a.code) - party_order.indexOf(b.code))
    return {year: year, results: results}
})


function rect(x,y,width, height) {
  let node = {
    node: "rect",
    props: [],
    children: []
  }
  props.push({x:`${x}px`})
  props.push({y:`${y}px`})
  props.push({width:`${width}px`})
  props.push({height:`${height}px`})

  return node;
}

function generateStripeForOneYear(year, x_y, size, party_mandates) {
  let svgElements = [];
  let totalMandates = party_mandates.results.map(r => r.mandates).reduce((p,c) => p+c, 0)
  
  let rollingMandates = 0;
  party_mandates.results.forEach(party => {
    let single_box_top = (rollingMandates / totalMandates) * size[1]
    rollingMandates += party.mandates;
    let single_box_bottom = (rollingMandates / totalMandates) * size[1]
    
    // let rectangle = rect(x, y, width, height, )
    let r = new svg.Rectangle(x_y[0], single_box_top+x_y[1], size[0], single_box_bottom-single_box_top)
    r.setAttribute('id', `bar${year}${party.code.toLowerCase()}`)
    r.addClass(`party${party.code.toLowerCase()}`)
    svgElements.push(r)

    console.log(`<rect id="bar${year}${party.code.toLowerCase()}" class="party${party.code.toLowerCase()}" \
      width="${size[0]}px" height="${(single_box_bottom-single_box_top)}px" x="${x_y[0]}px" y="${single_box_top+x_y[1]}px"/>`)
  })

  return svgElements
}

let allElements = []
const single_year_slice_size = [20,200]
let x_y = [20,20]
structured_parliaments.forEach(year => {
  let newElements = generateStripeForOneYear(year.year, x_y, single_year_slice_size, year)
  x_y[0] += single_year_slice_size[0]
  allElements.push(...newElements)
})

console.log(allElements)