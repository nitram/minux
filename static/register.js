function validCheck() {
    if (!isEmpty(1)) {
        document.querySelector('.valid-btn.next-btn').disabled = false;
    }
    else {
        document.querySelector('.valid-btn.next-btn').disabled = true;
    }

    if (!isEmpty(2)) {
        document.querySelector('.btn.valid-btn').disabled = false;
    }
    else {
        document.querySelector('.btn.valid-btn').disabled = true;
    }
}


function isEmpty(formGrp=1) {
    let inputs = document.querySelectorAll(`.form-group:nth-child(${formGrp}) input`);

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].value == null || inputs[i].value == '') {
            return true;
        }
    }
    return false;
}


function slideLeft() {
    let formGrps = document.querySelectorAll('.form-area .form-group');

    formGrps[0].style.transform = "translateX(-100%)";
    formGrps[1].style.transform = "translateX(0%)";
    document.querySelector('#firstname').tabIndex = -1;
    document.querySelector('#lastname').tabIndex = -1;
    document.querySelector('#email').tabIndex = 0;
    document.querySelector('#password').tabIndex = 0;
    document.querySelector('.valid-btn.next-btn').classList.add('d-none');
    document.querySelector('.btn.valid-btn').classList.remove('d-none');
    document.querySelector('.back-btn').classList.remove('hide');

    email = document.querySelector('#email')
    if (email.value == null || email.value == '') {
        setTimeout(() => {
            console.log("focused");
            email.focus();
        }, 440);
    }
}


function slideRight() {
    let formGrps = document.querySelectorAll('.form-area .form-group');

    formGrps[0].style.transform = "translateX(0%)";
    formGrps[1].style.transform = "translateX(100%)";
    document.querySelector('#firstname').tabIndex = 0;
    document.querySelector('#lastname').tabIndex = 0;
    document.querySelector('#email').tabIndex = -1;
    document.querySelector('#password').tabIndex = -1;
    document.querySelector('.valid-btn.next-btn').classList.remove('d-none');
    document.querySelector('.btn.valid-btn').classList.add('d-none');
    document.querySelector('.back-btn').classList.add('hide');
}


document.addEventListener('DOMContentLoaded', function() {
    let inputs = document.querySelectorAll('input');

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].onkeyup = validCheck;
    }

    let nextBtn = document.querySelector('.next-btn');
    nextBtn.onclick = slideLeft

    let backBtn = document.querySelector('.back-btn');
    backBtn.onclick = slideRight
});