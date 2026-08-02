const $ = (id) => document.getElementById(id);
const micButton = $("micButton"), commandText = $("command"), responseText = $("response"), statusText = $("status"), orb = $("orb");
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

function setListening(active) { micButton.disabled = active; micButton.innerHTML = active ? "🎙 Listening…" : "🎙 Start listening"; statusText.textContent = active ? "Listening carefully…" : "Ready to listen"; orb.classList.toggle("active", active); }
function speak(text) { if (!window.speechSynthesis) return; window.speechSynthesis.cancel(); const utterance = new SpeechSynthesisUtterance(text); utterance.lang = "en-IN"; utterance.rate = .95; window.speechSynthesis.speak(utterance); }
async function sendCommand(query) {
  if (!query.trim()) return;
  commandText.textContent = query; responseText.textContent = "Thinking…"; statusText.textContent = "Processing command";
  try {
    const res = await fetch("/process-command", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query})});
    const data = await res.json(); responseText.textContent = data.response; statusText.textContent = "Ready to listen"; speak(data.response);
    if (data.action === "open_url") window.open(data.data, "_blank", "noopener");
    if (data.action === "reminder") setTimeout(() => { const note = `Reminder: ${data.data}`; responseText.textContent = note; speak(note); }, 60000);
    if (data.action === "show_history") loadHistory();
  } catch { responseText.textContent = "I could not connect to the Python server. Please try again."; statusText.textContent = "Connection issue"; }
}
if (SpeechRecognition) {
  const recognition = new SpeechRecognition(); recognition.lang = "en-IN"; recognition.interimResults = false; recognition.maxAlternatives = 1;
  micButton.addEventListener("click", () => { setListening(true); recognition.start(); });
  recognition.onresult = (event) => sendCommand(event.results[0][0].transcript);
  recognition.onerror = () => { responseText.textContent = "I could not understand that. You can type your command instead."; setListening(false); };
  recognition.onend = () => setListening(false);
} else { micButton.disabled = true; statusText.textContent = "Voice input is not supported by this browser. Use the text box below."; }
$("commandForm").addEventListener("submit", (event) => { event.preventDefault(); const input=$("commandInput"); sendCommand(input.value); input.value=""; });
document.querySelectorAll("[data-command]").forEach(button => button.addEventListener("click", () => sendCommand(button.dataset.command)));
async function loadHistory() { const data = await (await fetch("/history")).json(); $("historyList").innerHTML = data.length ? data.map(item => `<li><strong>${escapeHtml(item.command)}</strong><br><small>${item.time}</small></li>`).join("") : "<li>No commands yet.</li>"; $("historyPanel").classList.remove("hidden"); }
function escapeHtml(value) { const el=document.createElement("div"); el.textContent=value; return el.innerHTML; }
$("clearHistory").addEventListener("click", async () => { await fetch("/history", {method:"DELETE"}); loadHistory(); });
