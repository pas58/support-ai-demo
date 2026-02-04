from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>AI Support Demo</title>
        </head>
        <body style="font-family: Arial; max-width: 700px; margin: 40px auto;">
            <h2>AI Support Demo (E-commerce)</h2>

            <div style="margin: 14px 0; color: #666;">
                Examples:
                <ul>
                  <li>How long is shipping?</li>
                  <li>What is your return policy?</li>
                  <li>Where is my order?</li>
                </ul>
            </div>

            <input id="msg" style="width: 78%; padding: 10px;" placeholder="Type your message..." />
            <button onclick="sendMsg()" style="padding: 10px 14px;">Send</button>

            <div id="chat" style="margin-top: 20px; padding: 12px; border: 1px solid #ddd; border-radius: 10px; min-height: 180px;"></div>

            <script>
              async function sendMsg() {
                const inp = document.getElementById('msg');
                const text = inp.value.trim();
                if (!text) return;

                const chat = document.getElementById('chat');
                chat.innerHTML += `<p><b>You:</b> ${text}</p>`;
                inp.value = '';

                const res = await fetch('/api/chat', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<p><b>Assistant:</b> ${data.reply}</p>`;
              }
            </script>
        </body>
    </html>
    """

@app.post("/api/chat")
def chat(msg: ChatMessage):
    text = (msg.message or "").lower()

# Delivery / Shipping
if any(k in text for k in ["delivery", "deliver", "shipping", "ship", "достав", "курьер", "срок"]):
    reply = "Доставка обычно занимает 3–5 рабочих дней. Если скажешь город или страну — уточню точнее."

# Returns / Refunds
elif any(k in text for k in ["return", "refund", "exchange", "возврат", "вернуть", "обмен", "возмещ"]):
    reply = "Возврат возможен в течение 30 дней после получения. Это будет возврат денег или обмен?"

# Order status / Tracking
elif any(k in text for k in ["order", "tracking", "track", "status", "where is", "заказ", "где", "мой заказ", "трек", "номер"]):
    reply = "Пожалуйста, напиши номер заказа или трек-номер — я проверю статус."

# Default
else:
    reply = "Уточни, пожалуйста: это про доставку, возврат или статус заказа?"

    return {"reply": reply}
