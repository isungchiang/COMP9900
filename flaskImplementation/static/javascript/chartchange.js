var btnList = document.getElementsByTagName("button");
console.log(btnList);
var daily = document.getElementById("daily");
var weekly = document.getElementById("weekly");
var monthly = document.getElementById("monthly");

btnList[2].onclick = function () {
  btnList[2].style.color = "#fff";
  btnList[2].style.backgroundColor = "#5b7da2";
  btnList[3].style.color = "";
  btnList[3].style.backgroundColor = "";
  btnList[4].style.color = "";
  btnList[4].style.backgroundColor = "";
  daily.style.display = "block";
  weekly.style.display = "none";
  monthly.style.display = "none";
}

btnList[3].onclick=function () {
  btnList[2].style.color = "";
  btnList[2].style.backgroundColor = "";
  btnList[3].style.color = "#fff";
  btnList[3].style.backgroundColor = "#5b7da2";
  btnList[4].style.color = "";
  btnList[4].style.backgroundColor = "";
  daily.style.display = "none";
  weekly.style.display = "block";
  monthly.style.display = "none";
}

btnList[4].onclick = function () {
  btnList[2].style.color = "";
  btnList[2].style.backgroundColor = "";
  btnList[3].style.color = "";
  btnList[3].style.backgroundColor = "";
  btnList[4].style.color = "#fff";
  btnList[4].style.backgroundColor = "#5b7da2";
  daily.style.display = "none";
  weekly.style.display = "none";
  monthly.style.display = "block";
}

