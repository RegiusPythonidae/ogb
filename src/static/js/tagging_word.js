const LOCAL = 'http://localhost:5000';
const GLOBAL = 'http://ogb.iliauni.edu.ge';
const URL = GLOBAL;

const words = document.getElementsByClassName('tooltip-info');
const inputField = {
  content: document.getElementById('word-input'),
  gram: document.getElementById('gram-input'),
  lemma: document.getElementById('lemma-input'),
  grc: document.getElementById('grc-input'),
  arm: document.getElementById('arm-input'),
  eng: document.getElementById('eng-input'),
  returnJson() {
    return {
      content: this.content.value,
      gram: this.gram.value,
      lemma: this.lemma.value,
      grc: this.grc.value,
      arm: this.arm.value,
      eng: this.eng.value,
    };
  },

};

let currentWordId = 0;

function parseWordID(word) {
  return word.slice(5);
}

function stripWord(word) {
  return word.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '').replace(/\s{2,}/g, ' ');
}

function updateWord() {
  const myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/json');

  const raw = JSON.stringify(inputField.returnJson());
  console.log(raw);
  const requestOptions = {
    method: 'PUT',
    headers: myHeaders,
    body: raw,
    redirect: 'follow',
  };

  fetch(`${URL}/api/word_tags/${currentWordId}`, requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.log('error', error));
}

async function getWordData(wordId) {
  const requestOptions = {
    method: 'GET',
    redirect: 'follow',
  };
  const response = await fetch(`${URL}/api/word_tags/${wordId}`, requestOptions)
    .catch((error) => console.log('error', error));

  console.log(response.status); // 200
  console.log(response.statusText); // OK

  if (response.status === 200) {
    const data = await response.json();

    // eslint-disable-next-line no-multi-assign
    inputField.content.value = data.content;
    inputField.content.placeholder = stripWord(data.content);
    // eslint-disable-next-line prefer-const,no-restricted-syntax
    for (let [key, value] of Object.entries(data)) {
      if (key in inputField) {
        if (value == null) {
          inputField[key].value = '';
        } else {
          inputField[key].value = value;
        }
      }
    }
  }
}

async function getSuggestion() {
  const requestOptions = {
    method: 'GET',
    redirect: 'follow',
  };
  const response = await fetch(`${URL}/api/word_tags/similar/${inputField.content.value}`, requestOptions)
    .catch((error) => console.log('error', error));

  console.log(response.status); // 200
  console.log(response.statusText); // OK

  if (response.status === 200) {
    const data = await response.json();

    // eslint-disable-next-line prefer-const,no-restricted-syntax
    for (let [key, value] of Object.entries(data)) {
      if (key in inputField) {
        if (value == null) {
          inputField[key].value = '';
        } else {
          inputField[key].value = value;
        }
      }
    }
  }
}

function loadWordInFields() {
  const _id = parseWordID(this.id);
  currentWordId = _id;
  getWordData(_id);
}

function clearFields() {
  inputField.gram.value = '';
  inputField.lemma.value = '';
  inputField.grc.value = '';
  inputField.arm.value = '';
  inputField.eng.value = '';
}

for (let i = 0; i < words.length; i += 1) {
  // eslint-disable-next-line no-loop-func
  words[i].addEventListener('click', loadWordInFields);
}

const submitButton = document.getElementById('submitFields');
const clearButton = document.getElementById('clearFields');
const autofillButton = document.getElementById('autofillFields');

submitButton.addEventListener('click', updateWord);
clearButton.addEventListener('click', clearFields);
autofillButton.addEventListener('click', getSuggestion);
