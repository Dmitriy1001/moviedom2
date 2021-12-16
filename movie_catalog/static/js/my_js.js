$(document).ready(function () {
    var location = JSON.parse(document.getElementById("location").textContent);
    var edited_comment = JSON.parse(document.getElementById("edited_comment").textContent);
    if(location) {
        window.location.href = location;
    };

    if(edited_comment) {
        window.location.hash = 'com' + edited_comment;
    };

});


function showMoreLess(model, id, more='...', less='...') {
  var dots = document.getElementById(model + "-dots" + id);
  var moreText = document.getElementById(model + "-more" + id);
  var btnText = document.getElementById(model + "-myBtn" + id);

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = more;
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


// edit comment & replies
function editPost(model, id) {
    // Get the modal
    var modal = document.getElementById('editWindow' + '-' + model + id);
    // Get the button that opens the modal
    var btn = document.getElementById('editBtn' + '-' + model + id);
    // Get the <span> element that closes the modal
    var close = document.getElementById('editClose' + '-' + model + id);

    if (modal.style.display == 'block')
          modal.style.display = 'none';
    else
          modal.style.display = 'block';

    // When the user clicks on <span> (x), close the modal
    close.onclick = function() {
      modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
}
// end edit comment & replies


function editComment(model, id) {
    var objText = document.getElementById(model + 'Text' + '-' + id);
    var objEdit = document.getElementById(model + 'Edit' + '-' + id);
    var buttonCancel = document.getElementById(model + 'BtnCnl' + '-' + id);
    var buttonSave = document.getElementById(model + 'BtnSave' + '-' + id);

    if (objText.style.display == 'block') {
        objText.style.display = 'none';
        objEdit.style.display = 'block';
        buttonCancel.innerHTML = 'Отменить';
        buttonSave.style.display = 'block';
    }
    else {
        objText.style.display = 'block';
        objEdit.style.display = 'none';
        buttonCancel.innerHTML = 'Изменить';
        buttonSave.style.display = 'none';
    }
}
