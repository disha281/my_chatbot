async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");
  const message = input.value.trim();
  if (!message) return;

  // User message bubble
  chatBox.innerHTML += `
    <div class="flex justify-end">
      <div class="bg-pink-500 text-white px-4 py-2 rounded-xl max-w-xs">
        ${message}
      </div>
    </div>
  `;

  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  // Send to backend
  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();

  // Bot reply bubble
  chatBox.innerHTML += `
    <div class="flex justify-start">
      <div class="bg-white border px-4 py-2 rounded-xl max-w-xs">
        ${data.reply || "⚠️ Error"}
      </div>
    </div>
  `;

  chatBox.scrollTop = chatBox.scrollHeight;
}
