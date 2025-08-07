import requests
import webbrowser

url = "https://api.thecatapi.com/v1/images/search"
response = requests.get(url)

if response.status_code ==200:
        dados = response.json()
        imagem_url = dados [0]["url"]
        webbrowser.open(imagem_url)
else:
        print (f"Erro na requisição: {response.status_code}")