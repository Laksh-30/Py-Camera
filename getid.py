import requests

TOKEN = "8677721345:AAF3Rdx8ticqtkSG-BoyaZ7hXAXkYE1Ld3Q"

CHAT_ID = "8277408775"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "🔥 DIRECT TEST"
}

print(requests.post(url, data=payload).text)
