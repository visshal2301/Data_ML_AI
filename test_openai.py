import socket

try:
    print("Google DNS:", socket.gethostbyname("google.com"))
except Exception as e:
    print("Google Error:", e)

try:
    print("OpenAI DNS:", socket.gethostbyname("api.openai.com"))
except Exception as e:
    print("OpenAI Error:", e)
