window.onload = function toast() {
    const info = JSON.parse(document.getElementById("info").textContent);
    alert(info);
    let chips = document.createElement('div');
    chips.classList.add('chips');
    chips.innerText = info;
    document.body.appendChild(chips);

    if (document.querySelector('.chips-field')) {
        document.querySelector('.chips-field').appendChild(chips);
    }
    else {
        let chipsField = document.createElement('div');
        chipsFields.classList.add('chips');
        document.body.appendChild(ChipsField);
    }

};
