async function sendMessage() {
  const query = document.getElementById("chat-input").value;
  const res = await fetch(`https://your-api.onrender.com/chat?query=${encodeURIComponent(query)}`);
  const data = await res.json();
  document.getElementById("chat-response").innerText = data.response;
}
