function showMoreLess(model, id) {
  var dots = document.getElementById(model + "-dots" + id);
  var moreText = document.getElementById(model + "-more" + id);
  var btnText = document.getElementById(model + "-myBtn" + id);

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "...";
    moreText.style.display = "none";
  } else {
     dots.style.display = "none";
     btnText.innerHTML = "...";
     moreText.style.display = "inline";
  }

}