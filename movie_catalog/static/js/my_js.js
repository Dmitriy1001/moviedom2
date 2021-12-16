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
function addReply(commentNumber, id) {
    document.getElementById("com_parent").value = id;
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
function editObject(model, id) {
    var objSection = document.getElementById(model + 'Section' + '-' + id);
    var objText = document.getElementById(model + 'Text' + '-' + id);
    var objEdit = document.getElementById(model + 'Edit' + '-' + id);
    var objDelete = document.getElementById(model + 'Del' + '-' + id);
    var objActions = document.getElementById(model + 'Actions' + '-' + id);

    var buttonCancel = document.getElementById(model + 'BtnCnl' + '-' + id);
    var buttonSave = document.getElementById(model + 'BtnSave' + '-' + id);
    var buttonDelete = document.getElementById(model + 'BtnDel' + '-' + id);

    if (objText.style.display == 'block') {
        objText.style.display = 'none';
        objEdit.style.display = 'block';
        buttonCancel.innerHTML = 'Отменить';
        buttonSave.style.display = 'block';
        buttonDelete.style.display = 'none';
    }
    else {
        objText.style.display = 'block';
        objEdit.style.display = 'none';
        buttonCancel.innerHTML = 'Изменить';
        buttonSave.style.display = 'none';
        buttonDelete.style.display = 'block';
    }

}
// end edit comment & replies


// delete comment & replies
function deleteObject(model, id) {
    var objSection = document.getElementById(model + 'Section' + '-' + id);
    var objDelete = document.getElementById(model + 'Del' + '-' + id);
    var objActions = document.getElementById(model + 'Actions' + '-' + id);

    if (objSection.style.display == 'block') {
        objSection.style.display = 'none';
        objActions.style.display = 'none';
        objDelete.style.display = 'block';
    }

    else {
        objDelete.style.display = 'none';
        objSection.style.display = 'block';
        objActions.style.display = '';
    }

}
// end delete comment & replies