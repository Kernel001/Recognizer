let url = `ws://${window.location.host}/ws/socket-server/`
const liveSocket = new WebSocket(url)

liveSocket.onmessage = function(e){
  console.log("Message recieved!")
  console.log(e.data)
}

function openNewPhoto(){
    pic = document.getElementById('photo')
    imgPath = document.getElementById('formFile').files[0]
    pic.classList.add("obj")
    pic.file=imgPath

    var reader = new FileReader()
    reader.onload = (function(aImg) {return function(e) {aImg.src = e.target.result}})(pic)
    reader.readAsDataURL(imgPath)
}

function startSourceClick(sourceID){
    console.log(`Starting source: ${sourceID}`)
}

function addSourceClick() {
  console.log("new source clicked!")
  if (liveSocket == undefined) {
    console.error("No connection to server!")
    return
  }

  liveSocket.send(JSON.stringify({
    "oper":"source.add",
    "data":
        {
          "ipAdress": document.getElementById('ipAdress').value,
          "descr": document.getElementById('descr').value,
          "feedName": document.getElementById('feedName').value
        }
  }))

  rows = document.getElementById('sourceTable')
  while(rows.firstChild){
    rows.removeChild(rows.lastChild)
  }

  var url = `http://${window.location.host}/app/sources/`
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function(){
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      console.log(xmlHttp.responseText);
      rows.innerHTML = xmlHttp.responseText
  }
  xmlHttp.open("GET", url, true);
  xmlHttp.send(null)
}
