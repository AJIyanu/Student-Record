let userData = document.getElementById('all-data').getAttribute('data-user');
const allInput = document.querySelectorAll('input');
const allSelect = document.querySelectorAll('select');
const textAreaAll = document.querySelectorAll('textarea');


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
