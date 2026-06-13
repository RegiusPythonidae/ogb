document.getElementById("autoFill").addEventListener("click", () => {
    fetch(`/word/${currentlySelectedId}`)
        .then(response => response.json())
        .then(result => {
            lemmaInput.value = result.lemma;
            grammarInput.value = result.grammar;
            greekInput.value = result.greek;
            armenianInput.value = result.armenian;
            englishInput.value = result.english;
        })
})

const toastLiveExample = document.getElementById('successToast')
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
document.getElementById("save").addEventListener("click", async () => {
    const selectedWord = document.getElementsByClassName("selected")[0]
    selectedWord.dataset.lemma = lemmaInput.value;
    selectedWord.dataset.grammar = grammarInput.value;
    selectedWord.dataset.greek = greekInput.value;
    selectedWord.dataset.armenian = armenianInput.value;
    selectedWord.dataset.english = englishInput.value;
    selectedWord.dataset.id = currentlySelectedId;

    const response = await fetch(`/word/${currentlySelectedId}`, {
        method: "POST",
        headers: {"Content-Type": "application/json",},
        body: JSON.stringify({
            "lemma": lemmaInput.value,
            "grammar": grammarInput.value,
            "greek": greekInput.value,
            "armenian": armenianInput.value,
            "english": englishInput.value
        }),
    })

    if (response.status === 200) {
        selectedWord.classList.remove("is-untagged")
        selectedWord.classList.add("tag-fixed")
        toastBootstrap.show()
    }
})