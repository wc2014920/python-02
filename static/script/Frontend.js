var val;
var value2 = [];
var len = [];
var jsonobj = null;
var isDone = false;
var tmp = [];

function getLocation() {
var send = document.getElementById('send');
var x = document.getElementById('title');
var latitude = document.getElementById('inputGrouphidden01');
var longitude = document.getElementById('inputGrouphidden02');
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
    function(position) {
            console.log(position);
            latitude.value = position.coords.latitude;
            longitude.value = position.coords.longitude
    },
    function(error) {
    switch(error.code)
    {
    case error.PERMISSION_DENIED:
      x.innerHTML="你已拒絕地理資訊存取服務<br>若要啟用<br>請重新載入並允許該服務<br>謝謝"
      send.style.display="none"
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML="Location information is unavailable."
      send.style.display="none"
      break;
    case error.TIMEOUT:
      x.innerHTML="The request to get user location timed out."
      send.style.display="none"
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML="An unknown error occurred."
      send.style.display="none"
      break;
    default :
    send.style.display=""
    }
    });
    console.info("地理資訊服務可取得");
  } else {
    console.info("地理資訊服務不支援");
  }
}
function yourfunction(){
    var val = document.getElementById('inputGroupSelect01').value;
    console.info(val);
    $.getJSON("/HOME/" + val, {}, function (r) {
        jsonobj = r;        //將資料庫回傳值放到jsonobj
        console.info(jsonobj);
        len.push(jsonobj["length"][0]);
        isDone = deleteOption(inputGroupSelect02);
        while(isDone!=true){}
        isDone = false;
        for (var num = 0; num < len[0]; num++) {   //將回傳值塞入參數
            value2.push(jsonobj["data"][num]);
            isDone = addOption(inputGroupSelect02,jsonobj["data"][num],jsonobj["data"][num]);
            while(isDone!=true){}
            isDone=false;
        }
        inputGroupSelect02.selectedIndex=0;
    });
}
function deleteOption(list){
    var x = document.getElementById("inputGroupSelect02");
    $("#inputGroupSelect02").children('option:not(:first)').remove();
    return true;
}
function addOption(list, text, value){
    var index=list.options.length;
    list.options[index]=new Option(text, value);
    return true;
}