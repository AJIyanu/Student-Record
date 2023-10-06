const showForm = document.querySelector(".show-form");
const signIn = document.querySelector(".sign-in");
const getStarted = document.querySelectorAll("#get-started-btn");
const getStartedBox = document.querySelectorAll('.box')
const getStartedForm = document.querySelector('.get-started');
const aboutUs = document.querySelector('.about-us');
const labelIcon = document.querySelector('.show-form .bi');
const level = document.querySelector('#level');
let userData = document.getElementById('all-data').getAttribute('data-user')

userData = JSON.parse(userData);

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

$.ajax({
    url: url,
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    headers: {
      "X-CSRF-Token": csrf
    },
    success: function(response) {
      if (response.hasOwnProperty("success")) {
          Swal.fire({
              text: response.success,
              icon: 'success',
              allowOutsideClick: false,
              showCancelButton: true,
              confirmButtonText: 'Home',
              cancelButtonText: 'New'
            }).then((result) => {
              if (result.isConfirmed) {
                window.location.href = "/dashboard/nurses";
              } else if (result.dismiss === Swal.DismissReason.cancel) {
                window.location.href = "/vitalsign";
              }
            });
      } else if (response.hasOwnProperty("error")) {
          Swal.fire({
              text: "There has been an error! Either you are not authorized or an internal error. If error persist, contact administrator",
              icon: 'error',
              allowOutsideClick: false,
              showCancelButton: true,
              confirmButtonText: 'Sign in as a Nurse',
              cancelButtonText: 'Try Again'
            }).then((result) => {
              if (result.isConfirmed) {
                window.location.href = "/dashboard/nurses";
              } else if (result.dismiss === Swal.DismissReason.cancel) {
                window.location.href = "/vitalsign";
              }
            });
      }
    },
    error: function(xhr, status, error) {
      console.error(error);
    }
  });
