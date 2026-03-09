/* ================= MAP ================= */

var map = L.map('map').setView([22.9734,78.6569],5)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
maxZoom:19
}).addTo(map)

let markers=[]
let routeLine=null


/* ================= INPUTS ================= */

const fromInput=document.getElementById("fromInput")
const toInput=document.getElementById("toInput")
const daysInput=document.getElementById("daysInput")
const budgetInput=document.getElementById("budgetInput")

const button=document.querySelector(".plan-btn")

button.addEventListener("click",generatePlan)



/* ================= AUTOCOMPLETE ================= */

async function loadPlaces(){

try{

let res=await fetch("data/india_places.json")
let data=await res.json()

let list=document.getElementById("places")

for(let state in data){

let option=document.createElement("option")
option.value=state
list.appendChild(option)

for(let district in data[state]){

let op=document.createElement("option")
op.value=district
list.appendChild(op)

data[state][district].forEach(place=>{

let p=document.createElement("option")
p.value=place
list.appendChild(p)

})

}

}

}catch(err){

console.log("Autocomplete load error",err)

}

}

loadPlaces()



/* ================= IMAGE ================= */

function getPlaceImage(place){

return `https://source.unsplash.com/800x500/?${place},tourism`

}



/* ================= GENERATE PLAN ================= */

async function generatePlan(){

let from=fromInput.value.trim()
let to=toInput.value.trim()
let days=parseInt(daysInput.value)
let budget=budgetInput.value

if(!from || !to || !days){

alert("Please fill all fields")
return

}

try{

let response=await fetch("http://127.0.0.1:8000/generate-trip",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
destination:to,
days:days
})

})

let data=await response.json()

let plan=data.plan

let itinerary=``

plan.forEach(item => {

itinerary += `

<div class="dayCard">

<img src="${getPlaceImage(item.place)}"
style="
width:100%;
height:200px;
object-fit:cover;
border-radius:10px;
margin-bottom:10px;
">

<h3>Day ${item.day}</h3>

<p>📍 Visit: <b>${item.place}</b></p>

<p>🏨 Hotel: <b>${item.hotel}</b></p>

<p>🍽 Food: <b>${item.food}</b></p>

<p>📸 Nearby: <b>${item.nearby}</b></p>

<p>📝 ${item.description}</p>

</div>

`

})


let container=document.getElementById("travelResult")

container.innerHTML=`

<h2>🌍 AI Trip Plan</h2>

<p><b>From:</b> ${from}</p>
<p><b>Destination:</b> ${to}</p>
<p><b>Days:</b> ${days}</p>
<p><b>Budget:</b> ₹${budget}</p>

<hr>

<h2>📅 Day-by-Day Plan</h2>

${itinerary}

<div id="distanceBox"></div>

`


/* ================= CLEAR OLD MARKERS ================= */

markers.forEach(m => map.removeLayer(m))
markers=[]

if(routeLine){
map.removeLayer(routeLine)
}


/* ================= MAP ROUTE ================= */

let fromData=await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${from}`)
let fromJson=await fromData.json()

let toData=await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${to}`)
let toJson=await toData.json()

if(fromJson.length==0 || toJson.length==0){

console.log("Location not found")
return

}

let fromLat=parseFloat(fromJson[0].lat)
let fromLon=parseFloat(fromJson[0].lon)

let toLat=parseFloat(toJson[0].lat)
let toLon=parseFloat(toJson[0].lon)


let startMarker=L.marker([fromLat,fromLon]).addTo(map).bindPopup("Start: "+from)
let endMarker=L.marker([toLat,toLon]).addTo(map).bindPopup("Destination: "+to)

markers.push(startMarker)
markers.push(endMarker)


routeLine=L.polyline([
[fromLat,fromLon],
[toLat,toLon]
],{
color:'yellow',
weight:5
}).addTo(map)

map.fitBounds(routeLine.getBounds())


/* ================= DISTANCE ================= */

let distance=map.distance(
[fromLat,fromLon],
[toLat,toLon]
)/1000

let hours=(distance/60).toFixed(1)

document.getElementById("distanceBox").innerHTML=`

<p>📏 Distance: <b>${distance.toFixed(0)} km</b></p>

<p>⏱ Travel Time: <b>${hours} hours</b></p>

`

}

catch(err){

console.log(err)
alert("Backend connection error")

}

}