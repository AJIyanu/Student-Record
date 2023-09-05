const showForm = document.querySelector(".show-form");
const signIn = document.querySelector(".sign-in");
const getStarted = document.querySelectorAll("#get-started-btn");
const getStartedBox = document.querySelectorAll('.box')
const getStartedForm = document.querySelector('.get-started');
const aboutUs = document.querySelector('.about-us');
const labelIcon = document.querySelector('.show-form .bi');
const level = document.querySelector('#level');

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
            level.querySelector('option[value="certificate"]').selected = true;
        } else if (index == 1) {
            level.querySelector("option[value='diploma']").selected = true;
        } else {
            level.querySelector("option[value='advanced']").selected = true;
        }
        labelIcon.scrollIntoView({behavior: "smooth"});
    })
})
