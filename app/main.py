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
    <title>Демонстрация поддержки ИИ</title>
</head>
<body style="font-family: Arial; max-width: 700px; margin: 40px auto;">

    <h2>Демонстрация поддержки ИИ (электронная коммерция)</h2>

    <div style="margin: 14px 0; color: #555;">
        <strong>Примеры вопросов клиентов:</strong>
        <ul>
            <li>Сколько времени занимает доставка?</li>
            <li>Как оформить возврат товара?</li>
            <li>Где мой заказ?</li>
        </ul>
    </div>

    <input
        id="msg"
        style="width: 78%; padding: 10px;"
        placeholder="Введите вопрос клиента..."
    />
    <button onclick="sendMsg()" style="padding: 10px 14px;">
        Отправить
    </button>

    <div
        id="chat"
        style="margin-top: 20px; padding: 12px; border: 1px solid #ddd; border-radius: 10px; min-height: 180px;"
    ></div>

    <script>
        async function sendMsg() {
            const input = document.getElementById("msg");
            const chat = document.getElementById("chat");
            const text = input.value.trim();
            if (!text) return;

            chat.innerHTML += "<p><strong>Вы:</strong> " + text + "</p>";
            input.value = "";

            const res = await fetch("/api/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ message: text })
            });

            const data = await res.json();
            chat.innerHTML += "<p><strong>Ассистент:</strong> " + data.reply + "</p>";
        }
    </script>

</body>
</html>
    """

@app.post("/api/chat")
def chat(msg: ChatMessage):
    text = (msg.message or "").lower()


# Delivery / Shipping
if any(k in text for k in ["достав", "shipping", "delivery"]):
    reply = "Стандартная доставка занимает 3–5 рабочих дней."

# Returns / Refunds
elif any(k in text for k in ["возврат", "вернут", "обмен", "refund", "return"]):
    reply = "Возврат возможен в течение 30 дней после получения. Это будет возврат денег или обмен?"

# Order status / Tracking
elif any(k in text for k in ["заказ", "где", "мой заказ", "трек", "отслеж", "tracking", "track"]):
    reply = "Пожалуйста, напишите номер заказа или трек-номер — я проверю статус."

# Default
else:
    reply = "Уточни, пожалуйста: это про доставку, возврат или статус заказа?"
    return {"reply": reply}
