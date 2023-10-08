let userData = document.getElementById('all-data').getAttribute('data-user');
const allInput = document.querySelectorAll('input');
const allSelect = document.querySelectorAll('select');
const textAreaAll = document.querySelectorAll('textarea');

// FILL IN ALREADY FILLED DETAILS TO THE FORM
userData = JSON.parse(userData);

console.log(userData);
// console.log(allInput);
for (const name of allInput) {
    if (name.id == "pp-image") {
    } else if (userData[name.name] === undefined) {
    } else if (name.name === "dob") {
        name.value = userData[name.name].split('T')[0];
    } else {
        name.value = userData[name.name];
    }
}

for (const name of textAreaAll) {
    if (userData[name.name] === undefined) {
    } else {
        name.value = userData[name.name];
    }
}

for (const name of allSelect) {
    if (name.name == "state") {
    } else if (name.name == "lga") {
    } else if (name.name == "country-code") {
    } else if (userData[name.name] === undefined) {
    } else {
    name.value = userData[name.name];
    }
}


// GET CRSF TOKEN FOR FORM SUBMIT

const getCookies = function () {
    const pairs = document.cookie.split(";");
    let cookies = {};
    for (let i = 0; i < pairs.length; i++) {
      const pair = pairs[i].split("=");
      cookies[(pair[0] + "").trim()] = unescape(pair.slice(1).join("="));
    }
    return cookies;
  };

const getCookieValue = function (cookieName) {
const cookies = getCookies();
return cookies[cookieName];
};

const csrf = getCookieValue('csrf_access_token');

// SUBMIT FORM FUNCTION

function submitForm(form) {
    var url = form.action;
    var formData = new FormData();
    $('.form').find("input[name]").each(function(index, node) {
      formData.append(node.name, node.value);
    });

    $('.form').find('select[name]').each(function (index, node) {
        formData.append(node.name, node.value);
    });

    $('.form').find('textarea[name]').each(function (index, node) {
        formData.append(node.name, node.value);
    })



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
        console.log(response);
      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });
  }
