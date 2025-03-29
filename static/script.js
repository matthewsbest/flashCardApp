let words = [];
let currentIndex = 0;
let levelTotal = 0;
let totalCounter = 0;
let grandTotal = 0;

async function startGame() {
    const level = document.getElementById("levelSelect").value;

    // Fetch words for the selected level
    const response = await fetch("/get_words", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ level })
    });

    const data = await response.json();
    words = data.words;
    levelTotal = words.length;
    grandTotal = data.total_words;

    currentIndex = 0;
    totalCounter = 0;

    // Initialize counters and card
    document.getElementById("flashcard").textContent = "Click to Start";
    document.getElementById("levelCounter").textContent = 0;
    document.getElementById("levelTotal").textContent = levelTotal;
    document.getElementById("totalCounter").textContent = totalCounter;
    document.getElementById("grandTotal").textContent = grandTotal;
}

function nextWord() {
    // Show the next word or finish the level
    if (currentIndex < words.length) {
        document.getElementById("flashcard").textContent = words[currentIndex];
        currentIndex++;
        document.getElementById("levelCounter").textContent = currentIndex;
        document.getElementById("totalCounter").textContent = totalCounter + currentIndex;
    } else {
        document.getElementById("flashcard").textContent = "✅ Completed! Select a new level.";
    }
}
