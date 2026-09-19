const detailsBar = document.getElementsByClassName("word-details")[0]

const selectedWord = document.getElementById("selectedWord")
const lemmaInput = document.getElementById("lemma")
const grammarInput = document.getElementById("grammarTags")
const greekInput = document.getElementById("greekText")
const armenianInput = document.getElementById("armenianText")
const englishInput = document.getElementById("georgianText")


const words = document.getElementsByClassName("paragraph-word")

let currentlySelectedId = null;
let activeTooltip = null;
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

    word.addEventListener("mouseenter", () => {
        if (activeTooltip) {
            activeTooltip.remove();
        }

        const tooltip = document.createElement("div");
        tooltip.className = "word-tooltip";

        const content = [];
        if (word.dataset.lemma) content.push(`<strong>ლემა:</strong> ${word.dataset.lemma}`);
        if (word.dataset.grammar) content.push(`<strong>თეგები:</strong> ${word.dataset.grammar}`);
        if (word.dataset.greek) content.push(`<strong>ბერძნული:</strong> ${word.dataset.greek}`);
        if (word.dataset.english) content.push(`<strong>ინგლისური:</strong> ${word.dataset.english}`);
        if (word.dataset.armenian) content.push(`<strong>სომხური:</strong> ${word.dataset.armenian}`);

        tooltip.innerHTML = content.join("<br>");
        document.body.appendChild(tooltip);

        const rect = word.getBoundingClientRect();
        tooltip.style.position = "fixed";
        tooltip.style.left = (rect.left + rect.width / 2) + "px";
        tooltip.style.top = (rect.top - 10) + "px";
        tooltip.style.transform = "translateX(-50%) translateY(-100%)";

        activeTooltip = tooltip;
    })

    word.addEventListener("mouseleave", () => {
        if (activeTooltip) {
            activeTooltip.remove();
            activeTooltip = null;
        }
    });
}

document.getElementById("closeDetailsBtn").addEventListener("click", () => {
    detailsBar.classList.add("d-none")
})