import requests

token = "8677721345:AAF3Rdx8ticqtkSG-BoyaZ7hXAXkYE1Ld3Q"

url = f"https://api.telegram.org/bot{token}/getMe"

response = requests.get(url)

print(response.text)