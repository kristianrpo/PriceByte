var ProductImg = document.getElementById("ProductImg");
var SmallImg = document.getElementsByClassName("small-img");
for (let i = 0;i<SmallImg.length;i++){
  SmallImg[i].onclick = function() {
    ProductImg.src = SmallImg[i].src;
  }
}