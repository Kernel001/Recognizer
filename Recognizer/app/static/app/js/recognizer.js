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

function addTargetClick(){
  console.log(`add target clicked`)
  if (liveSocket == undefined) {
    console.error("No connection to server!")
    return
  }

  picFile = document.getElementById('photo').file
  var reader = new FileReader()

  reader.onload = function(evt) {
    liveSocket.send(JSON.stringify({
      "oper":"target.add",
      "data":
          {
            "target_name": document.getElementById('targetName').value,
            "target_photo": base64ArrayBuffer(evt.target.result)
          }
    }))
  }
  reader.readAsArrayBuffer(picFile)

  clearChilds('targetsTable')

  var url = `http://${window.location.host}/app/targets/`
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function(){
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      console.log(xmlHttp.responseText);
      document.getElementById('targetsTable').innerHTML = xmlHttp.responseText
  }
  xmlHttp.open("GET", url, true);
  xmlHttp.send(null)
}

function clearChilds(parentElementId){
  rows = document.getElementById(parentElementId)
  while(rows.firstChild){
    rows.removeChild(rows.lastChild)
  }
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

  clearChilds('sourceTable')

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

function base64ArrayBuffer(arrayBuffer) {
  var base64    = ''
  var encodings = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

  var bytes         = new Uint8Array(arrayBuffer)
  var byteLength    = bytes.byteLength
  var byteRemainder = byteLength % 3
  var mainLength    = byteLength - byteRemainder

  var a, b, c, d
  var chunk

  // Main loop deals with bytes in chunks of 3
  for (var i = 0; i < mainLength; i = i + 3) {
    // Combine the three bytes into a single integer
    chunk = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2]

    // Use bitmasks to extract 6-bit segments from the triplet
    a = (chunk & 16515072) >> 18 // 16515072 = (2^6 - 1) << 18
    b = (chunk & 258048)   >> 12 // 258048   = (2^6 - 1) << 12
    c = (chunk & 4032)     >>  6 // 4032     = (2^6 - 1) << 6
    d = chunk & 63               // 63       = 2^6 - 1

    // Convert the raw binary segments to the appropriate ASCII encoding
    base64 += encodings[a] + encodings[b] + encodings[c] + encodings[d]
  }

  // Deal with the remaining bytes and padding
  if (byteRemainder == 1) {
    chunk = bytes[mainLength]

    a = (chunk & 252) >> 2 // 252 = (2^6 - 1) << 2

    // Set the 4 least significant bits to zero
    b = (chunk & 3)   << 4 // 3   = 2^2 - 1

    base64 += encodings[a] + encodings[b] + '=='
  } else if (byteRemainder == 2) {
    chunk = (bytes[mainLength] << 8) | bytes[mainLength + 1]

    a = (chunk & 64512) >> 10 // 64512 = (2^6 - 1) << 10
    b = (chunk & 1008)  >>  4 // 1008  = (2^6 - 1) << 4

    // Set the 2 least significant bits to zero
    c = (chunk & 15)    <<  2 // 15    = 2^4 - 1

    base64 += encodings[a] + encodings[b] + encodings[c] + '='
  }

  return base64
}
