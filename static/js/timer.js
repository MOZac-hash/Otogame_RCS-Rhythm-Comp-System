const EndTime = "May 1, 2023 12:00:00" //比赛（直播）时间
let days = document.querySelector('.days .number'),
    hours = document.querySelector('.hours .number'),
    minutes = document.querySelector('.minutes .number'),
    seconds = document.querySelector('.seconds .number'),
    DDL = document.querySelector('.content .endTime'),
    jumpBt = document.querySelector('.content .button'),
    countDownDate = new Date(EndTime).getTime();

let counter = setInterval(()=>{
    let dateNow = new Date().getTime();
    let dataDiff = countDownDate - dateNow;

    let day = Math.floor(dataDiff/(1000*60*60*24));
    let hour = Math.floor((dataDiff%(1000*60*60*24))/(1000*60*60));
    let minute = Math.floor((dataDiff % (1000 * 60 * 60)) / (1000 * 60));
    let second = Math.floor((dataDiff % (1000 * 60)) / (1000));

    days.innerHTML = day < 10 ? `0${day}` :day;
    hours.innerHTML = hour < 10 ? `0${hour}` :hour;
    minutes.innerHTML = minute < 10 ? `0${minute}` :minute;
    seconds.innerHTML = second < 10 ? `0${second}` :second;
    DDL.innerHTML = EndTime;

    if(dataDiff == 0){
        clearInterval(counter)
    }
},1000)

document.getElementById("buttonPC").style.visibility="hidden";
//获取浏览器navigator对象的userAgent属性（浏览器用于HTTP请求的用户代理头的值）
var info = navigator.userAgent;
//通过正则表达式的test方法判断是否包含“Mobile”字符串
var isPhone = /mobile/i.test(info);
//如果包含“Mobile”（是手机设备）则返回true
 if(isPhone){//如果是手机,跳转到
    document.getElementById("buttonPC").style.visibility="hidden";
    document.getElementById("buttonPC").style.display="none";
    document.getElementById("buttonMobile").style.visibility="visible";
    document.getElementById("buttonMobile").style.display="inline";
}else {  //如果是电脑跳转到
     document.getElementById("buttonPC").style.display="inline";
     document.getElementById("buttonPC").style.visibility="visible";
     document.getElementById("buttonMobile").style.display="none";
     document.getElementById("buttonMobile").style.visibility="hidden";
 }