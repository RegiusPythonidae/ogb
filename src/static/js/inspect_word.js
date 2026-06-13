const detailsBar = document.getElementsByClassName("word-details")[0]

const selectedWord = document.getElementById("selectedWord")
const lemmaInput = document.getElementById("lemma")
const grammarInput = document.getElementById("grammarTags")
const greekInput = document.getElementById("greekText")
const armenianInput = document.getElementById("armenianText")
const englishInput = document.getElementById("georgianText")


const words = document.getElementsByClassName("paragraph-word")
let currentlySelectedId = null;
for (let word of words) {
    word.addEventListener("click", () => {
        if (detailsBar.classList.contains("d-none")) detailsBar.classList.toggle("d-none")

        const existingSelection = document.getElementsByClassName("selected")[0]
        if (existingSelection) existingSelection.classList.toggle("selected");

        word.classList.toggle("selected")
        selectedWord.innerText = word.dataset.text;
        lemmaInput.value = word.dataset.lemma;
        grammarInput.value = word.dataset.grammar;
        greekInput.value = word.dataset.greek;
        armenianInput.value = word.dataset.armenian;
        englishInput.value = word.dataset.english;
        currentlySelectedId = word.dataset.id
    })
}

document.getElementById("closeDetailsBtn").addEventListener("click", () => {
    detailsBar.classList.add("d-none")
})