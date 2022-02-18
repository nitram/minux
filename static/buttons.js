function validCheck() {
    console.log("validCheck run")
    let inputs = document.querySelectorAll('input');

    if (!isEmpty(inputs)) {
        document.querySelector('.valid-btn').disabled = false;
    }
    else {
        document.querySelector('.valid-btn').disabled = true;
    }
}

function isEmpty(inputs) {
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].value == null || inputs[i].value == '') {
            return true;
        }
    }
    return false;
}

document.addEventListener('DOMContentLoaded', function() {
    let inputs = document.querySelectorAll('input');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].onkeyup = validCheck
    }
});