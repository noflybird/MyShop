"__author=ethan"
//数据上报
function analytis(){
  var info;
  info = getInfo();
  batchSends(info);
}

function send(uploadData) {
  var _data = Base64.encode(uploadData);
  var url = "http://192.168.199.148:80/upload.gif?" + _data;
  fetch(
    url,
    {method:"head", mode:"no-cors"}
  )
}

function batchSends(infoData){
  var num = 2;
  var u_key = "u_data";
  var obj;
  var key = localStorage.getItem(u_key);
  if(key==null){
    obj = []
  }else{
    obj = JSON.parse(key)

  }

  if(obj.length >= num){
    send(JSON.stringify((obj)))
    localStorage.removeItem((u_key));
  }else{
    obj.push(infoData);
    localStorage.setItem(u_key,JSON.stringify(obj));
  }
}

function basicInfo(){
  var baseData = {};
  var uuid = null;
  var agent = null;

  uuid = getUUID();
  agent = getAgent();

  baseData['name'] = uuid;
  baseData['agent'] = agent;
  baseData['time'] = Date.now()

  return baseData;
}

function getUUID(){
  var uid = null;
  var c_key = 'name';
  var start = document.cookie.indexOf(c_key+"=");

  if(start!==-1){
    start = start + c_key.length + 1;
    var end = document.cookie.length;
    uid = unescape(document.cookie.substring(start, end));
  }
  return uid

}

function getAgent(){
  var agent = null;
  var userAgent = navigator.userAgent;
  var agents = ["windows", "Mac OS", "Android", "IPhone", "IPad"];
  var flag = true;
  for(var i=0;i<agents.length;i++){
    if(userAgent.indexOf(agents[i])>0){
      agent = agents[i];
      flag = true;
      break;
    }
  }
  if(flag){
    agent = "windows";
  }

  return agent
}

function getInfo(extendData=null){
  var data;
  data = basicInfo();
  data['event'] = extendData;
  return data;
}

export {getInfo, batchSends, analytis}
