function showMoreLess(model, id, more='...', less='...') {
  var dots = document.getElementById(model + "-dots" + id);
  var moreText = document.getElementById(model + "-more" + id);
  var btnText = document.getElementById(model + "-myBtn" + id);

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = more
    moreText.style.display = "none";
  } else {
     dots.style.display = "none";
     btnText.innerHTML = less;
     moreText.style.display = "inline";
  }
}


// reply for comment
function addComment(commentNumber, id) {
    document.getElementById("parent").value = id;
	document.getElementById("commentText").innerText = `#${commentNumber}. `;
};
// end reply for comment


// forms validation
const commentText = document.getElementById("commentText");
const reviewTitle = document.getElementById("reviewTitle");
const reviewText = document.getElementById("reviewText");

commentText.addEventListener("invalid", function (event) {
	if (commentText.validity.valueMissing) {
        commentText.setCustomValidity("Обязательное поле");
    } else if (commentText.validity.tooShort) {
        commentText.setCustomValidity("Минимальная длинна сообщения 10 символов");
    } else {
    	commentText.setCustomValidity("");
    }
});

reviewTitle.addEventListener("invalid", function (event) {
	if (reviewTitle.validity.valueMissing) {
        reviewTitle.setCustomValidity("Обязательное поле");
    } else if (reviewTitle.validity.tooShort) {
        reviewTitle.setCustomValidity("Минимальная длинна заголовка 10 символов");
    } else if (reviewTitle.validity.tooLong) {
        reviewTitle.setCustomValidity("Максимальная длинна заголовка 100 символов");
    } else {
    	reviewTitle.setCustomValidity("");
    }
});

reviewText.addEventListener("invalid", function (event) {
	if (reviewText.validity.valueMissing) {
        reviewText.setCustomValidity("Обязательное поле");
    } else if (reviewText.validity.tooShort) {
        reviewText.setCustomValidity("Минимальная длинна рецензии 700 символов");
    } else {
    	reviewText.setCustomValidity("");
    }
});
// end forms validation


// show replies
function toggle_visibility(id)
    {
        var e = document.getElementById(id);
        if ( e.style.display == 'block' )
            e.style.display = 'none';
        else
            e.style.display = 'block';
    }
// end show replies
