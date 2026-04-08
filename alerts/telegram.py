import requests
from torch.testing._internal.common_subclass import DiagTensorBelow

class TelegramAlert:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token.strip()
        self.chat_id = str(chat_id).strip()

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": text
        }

        response = requests.post(url, data=payload)
        print("📩 Message:", response.text)

    def send_image(self, image_path):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

        with open(image_path, "rb") as img:
            files = {"photo": img}
            data = {"chat_id": self.chat_id}

            response = requests.post(url, files=files, data=data)
            print("📸 Image:", response.text)


# ===========================================================
#                     SAME ALTERNATE CODE BELOW
# ============================================================


# import requests

# class TelegramAlert:
#     def __init__(self, bot_token, chat_id):
#         """
#         self.bot_token =8677721345:AAF3Rdx8ticqtkSG-BoyaZ7hXAXkYE1Ld3Q
#         chat_id   ="8277408775" 
#         """

#         self.bot_token = bot_token
#         self.chat_id = chat_id
        
        

#     def send_message(self, text):
#         """
#         Send a text message to Telegram
#         """
#         url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

#         payload = {
#             "chat_id": self.chat_id,
#             "text": text
#         }

#         try:
#             response = requests.post(url, data=payload, timeout=5)
#             print("📩 Message response:", response.text)
#         except Exception as e:
#             print("❌ Message failed:", e)

#     def send_image(self, image_path):
#         """
#         Send an image to Telegram
#         """

#         url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

#         try:
#             with open(image_path, "rb") as img:
#                 files = {"photo": img}
#                 data = {"chat_id": self.chat_id}

#                 response = requests.post(url, files=files, data=data, timeout=10)
#                 print("📸 Image response:", response.text)

#         except Exception as e:
#             print("❌ Image failed:", e)