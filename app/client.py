import requests

url = "http://localhost:8080/"
response = requests.get(url)

print("Ответ от сервера:", response.text)
