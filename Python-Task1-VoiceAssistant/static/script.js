document.addEventListener("DOMContentLoaded", () => {
    const micButton = document.getElementById("micButton");
    const commandInput = document.getElementById("commandInput");
    const commandForm = document.getElementById("commandForm");
    const commandDisplay = document.getElementById("command");
    const responseDisplay = document.getElementById("response");
    const historyPanel = document.getElementById("historyPanel");
    const historyList = document.getElementById("historyList");
    const clearHistoryBtn = document.getElementById("clearHistory");

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            document.getElementById("status").textContent = "Listening...";
            micButton.classList.add("listening");
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            commandDisplay.textContent = transcript;
            sendToServer(transcript);
        };

        recognition.onerror = (event) => {
            document.getElementById("status").textContent = "Ready to listen";
            micButton.classList.remove("listening");
        };

        recognition.onend = () => {
            document.getElementById("status").textContent = "Ready to listen";
            micButton.classList.remove("listening");
        };
    }

    if (micButton) {
        micButton.addEventListener("click", () => {
            if (recognition) {
                try {
                    recognition.start();
                } catch (e) {
                    recognition.stop();
                }
            } else {
                alert("Speech recognition is not supported in your browser.");
            }
        });
    }

    if (commandForm) {
        commandForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const text = commandInput.value.trim();
            if (text) {
                commandDisplay.textContent = text;
                sendToServer(text);
                commandInput.value = "";
            }
        });
    }

    // Quick Buttons Handler
    document.querySelectorAll('.quick button').forEach(button => {
        button.addEventListener('click', () => {
            const cmd = button.getAttribute('data-command');
            commandDisplay.textContent = cmd;
            sendToServer(cmd);
        });
    });

    // Send Command to Flask Backend
    function sendToServer(cmd) {
        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command: cmd })
        })
        .then(response => response.json())
        .then(data => {
            const resText = data.response;
            responseDisplay.textContent = resText;

            // Handle browser actions (YouTube, Google, Search)
            if (resText.includes("Opening YouTube")) {
                window.open("https://www.youtube.com", "_blank");
            } else if (resText.includes("Opening Google")) {
                window.open("https://www.google.com", "_blank");
            } else if (resText.includes("Searching") && resText.includes("on Google")) {
                let searchQuery = resText.replace("Searching ", "").replace(" on Google.", "").trim();
                window.open(`https://www.google.com/search?q=${searchQuery}`, "_blank");
            }

            // Show History if requested
            if (cmd.toLowerCase().includes("show history")) {
                loadHistory();
            }
        })
        .catch(err => {
            console.error("Error:", err);
            responseDisplay.textContent = "Sorry, something went wrong.";
        });
    }

    function loadHistory() {
        fetch('/history')
        .then(res => res.json())
        .then(data => {
            historyList.innerHTML = "";
            if (data.history && data.history.length > 0) {
                historyPanel.classList.remove("hidden");
                data.history.forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = `You: ${item.command} | Jarvis: ${item.response}`;
                    historyList.appendChild(li);
                });
            } else {
                historyList.innerHTML = "<li>No history found.</li>";
                historyPanel.classList.remove("hidden");
            }
        });
    }

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener("click", () => {
            fetch('/clear_history', { method: 'POST' })
            .then(() => {
                historyList.innerHTML = "";
                historyPanel.classList.add("hidden");
            });
        });
    }
});