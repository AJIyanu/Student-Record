const showForm = document.querySelector(".show-form");
const signIn = document.querySelector(".sign-in");
const getStarted = document.querySelectorAll("#get-started-btn");
const getStartedBox = document.querySelectorAll('.box')
const getStartedForm = document.querySelector('.get-started');
const aboutUs = document.querySelector('.about-us');
const labelIcon = document.querySelector('.show-form .bi');
const level = document.querySelector('#level');
let msg = document.getElementById('all-data').getAttribute('data-msg');

// console.log(msg);
try {
  if (msg !== "") {
    let notis = new AWN({
        position: "top-right",
        durations: {info: 8000,},
        labels: {info: "Not Successful!"},
    });
    notis.info(`${msg}! Please select get started button to register`);
    console.log(msg)
  }
} catch (error) {
  console.error(error);
}

// console.log(showForm);
// console.log(getStartedForm);
// getStarted.forEach(item => console.log(item));
// console.log(signIn);
// console.log(level);

showForm.addEventListener("click", () => {
    if (signIn.style.display === 'none') {
        signIn.style.display = 'block';
    } else {
        signIn.style.display = 'none';
    }
    if (getStartedForm.style.display === 'block') {
        signIn.style.display = 'none';
        getStartedForm.style.display = 'none';
        aboutUs.style.paddingTop = '180pt';
        getStartedBox.forEach((hideme) => hideme.style.display = 'block');
        labelIcon.classList.add('bi-door-open-fill');
        labelIcon.classList.remove('bi-person-vcard');
    }
})

getStarted.forEach((button, index) => {
    button.addEventListener('click', () => {
        getStartedBox.forEach((hideme) => hideme.style.display = 'none');
        aboutUs.style.paddingTop = '18pt';
        signIn.style.display = 'none';
        getStartedForm.style.display = 'block';
        labelIcon.classList.remove('bi-door-open-fill');
        labelIcon.classList.add('bi-person-vcard');
        if (index === 0) {
            level.querySelector('option[value="Certificate"]').selected = true;
        } else if (index == 1) {
            level.querySelector("option[value='Diploma']").selected = true;
        } else {
            level.querySelector("option[value='Advanced']").selected = true;
        }
        labelIcon.scrollIntoView({behavior: "smooth"});
    })
})

const confirm_pwd = document.getElementById("confirm-password");
const pwd = document.getElementById("password2");
const submit = document.getElementById("submit-btn2");


confirm_pwd.addEventListener("input", (event) => {
    if (confirm_pwd.value !== pwd.value) {
        confirm_pwd.style.backgroundColor = "rgba(255, 0, 0, 0.252)";
    } else {
        confirm_pwd.style.backgroundColor = "rgba(30, 255, 0, 0.363)";
    }
})


submit.addEventListener("click", (e) => {
    if (confirm_pwd.value !== pwd.value) {
        e.preventDefault()
    }
})

// NOT A COMPLETE THOUGHT YET IMOPRTING SWAL AND AJAX REQUEST
