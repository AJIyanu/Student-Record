const stateSelect = document.getElementById('states');
const lgaSelect = document.getElementById('lgas');

fetch('/states')
.then(response => response.json())
.then(options => {
  options.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.textContent = option;
    optionElement.value = option;
    stateSelect.appendChild(optionElement)
  });
});

stateSelect.addEventListener('change', (event) => {
  const seloption = event.target.value;
  // console.log('change detected');

  // console.log(seloption)

  fetch('/lga/' + seloption)
  .then(response => response.json())
  .then(options => {
    // console.log(options);
    while(lgaSelect.firstChild) {
      lgaSelect.removeChild(lgaSelect.firstChild);
    }
  options.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.textContent = option;
    lgaSelect.appendChild(optionElement)
  });
});
});
