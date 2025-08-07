import requests
import csv
from datetime import datetime

urls = [
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Google Chrome", "Google Chrome"),
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Windows_10","Windows 10"),
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Ubuntu","Ubuntu"),
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Apache", "Apache HTTP Server"),
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=MySQL", "MySQL"),
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Cisco_IOS", "Cisco IOS"),
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=FortiOS", "Fortinet FortiOS"),
    ("https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=ESXi", "VMware ESXi")
]

cve_filtrados = []

def obter_dados_da_api(url, aplicacao):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status() # verificar se a resposta foi sucedida ou seja =200

        if resposta.text.strip(): # valida se a página não é em branco
            dados = resposta.json()
            print(dados)

            if "vulnerabilities" in dados:
                for item in dados["vulnerabilities"]:
                    cve_info = item.get("cve", {})

                    cve_id = cve_info.get("id", "N/A")
                    data_publicacao = cve_info.get("published", "N/A")
                    descricao = cve_info.get("descriptions", [{}])[0].get("value", "sem descrição")

                    try:
                        data_publicacao_formatada = datetime.strptime(data_publicacao, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
                    except ValueError:
                        data_publicacao_formatada = data_publicacao

                    # Ajuste para capturar a severidade corretamente
                    severidade = "N/A"  # Caso não haja dados de severidade
                    if "metrics" in cve_info:
                        if "cvssMetricV31" in cve_info["metrics"]:
                            severidade = cve_info["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                        elif "cvssMetricV30" in cve_info["metrics"]:
                            severidade = cve_info["metrics"]["cvssMetricV30"][0]["cvssData"]["baseScore"]
                        elif "cvssMetricV2" in cve_info["metrics"]:
                            severidade = cve_info["metrics"]["cvssMetricV2"][0]["cvssData"]["baseScore"]

                    produtos_afetados = []
                    if "affects" in cve_info:
                        produtos_afetados = [product.get("product", "desconhecido") for product in cve_info["affects"]]

                    if "2025" in data_publicacao:
                        cve_filtrados.append({
                            "CVE ID": cve_id,
                            "Publicação": data_publicacao_formatada,
                            "Descrição": descricao,
                            "Severidade": severidade,
                            "Aplicações": aplicacao
                        })
        else:
            print(f"A resposta da API {url} estava vazia")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para {url}: {e}")
    except ValueError as e:
        print(f"Erro ao tentar decodificar o JSON da resposta de {url}: {e}")
            
for url, aplicacao in urls:
    obter_dados_da_api(url, aplicacao)

with open("C:/Users/Julio Barbosa/Desktop/updateseverity2.csv", mode='w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.DictWriter(arquivo_csv, fieldnames=["CVE ID", "Publicação", "Descrição", "Severidade", "Aplicações"])
    writer.writeheader()
    writer.writerows(cve_filtrados)
           
for cve in cve_filtrados:
    print(f"CVE: {cve['CVE ID']}")
    print(f"Publicado em: {cve['Publicação']}")
    print(f"Descrição: {cve['Descrição']}")
    print(f"Severidade: {cve['Severidade']}")
    print(f"Aplicações: {cve['Aplicações']}")

print("Arquivo CSV gerado")