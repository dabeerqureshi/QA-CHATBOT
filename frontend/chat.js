document.getElementById("send-btn").addEventListener("click", async () => {
  const inputField = document.getElementById("chat-input");
  const chatLog = document.getElementById("chat-log");
  const userInput = inputField.value.trim();

  if (!userInput) return;

  chatLog.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;
  inputField.value = "";

  try {
    const res = await fetch(`http://127.0.0.1:8000/chat?query=${encodeURIComponent(userInput)}`);
    const data = await res.json();
    chatLog.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
  } catch (err) {
    chatLog.innerHTML += `<div><strong>Error:</strong> Unable to reach server</div>`;
  }

  chatLog.scrollTop = chatLog.scrollHeight;
});
