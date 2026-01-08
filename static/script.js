const chatBox = document.getElementById("chat-box");
const inputField = document.getElementById("user-input");

// Allow sending with Enter key
inputField.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const question = inputField.value.trim();
    if (question === "") return;

    // 1. Add User Message
    addMessage(question, "user-message");
    inputField.value = "";

    // 2. Add "Typing..." placeholder
    const loadingId = "loading-" + Date.now();
    addMessage("Analyzing streams...", "bot-message", loadingId);

    // 3. Send to Backend
    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        const loadingMsg = document.getElementById(loadingId);
        if (loadingMsg) loadingMsg.remove();

        // 4. Show Bot Response
        let finalHtml = data.answer;

        // Append sources if available
        if (data.sources && data.sources.length > 0) {
            finalHtml += `<div class="sources-container"><strong>Sources:</strong><br>`;
            data.sources.forEach(source => {
                // Truncate long sources for cleaner look
                const shortSource = source.length > 100 ? source.substring(0, 100) + "..." : source;
                finalHtml += `• ${shortSource}<br>`;
            });
            finalHtml += `</div>`;
        }

        addMessage(finalHtml, "bot-message", null, true);
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById(loadingId).innerText = "Error: Could not connect to intelligence server.";
    });
}

function addMessage(text, className, id = null, isHtml = false) {
    const div = document.createElement("div");
    div.className = `message ${className}`;
    if (id) div.id = id;

    if (isHtml) {
        div.innerHTML = text; // Allow HTML for sources
    } else {
        div.innerText = text; // Safer for user input
    }

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
}