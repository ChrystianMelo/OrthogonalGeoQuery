import os
import urllib.request
import filtrar_csv

def baixar_arquivo_se_necessario(url, nome_arquivo):
    if os.path.exists(nome_arquivo):
        print(f"[✓] O arquivo '{nome_arquivo}' já existe. Nenhum download necessário.")
        return

    print(f"[↓] Baixando '{nome_arquivo}'...")

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            with open(nome_arquivo, 'wb') as f:
                f.write(response.read())
        print(f"[✔] Download concluído e salvo como '{nome_arquivo}'")
    except Exception as e:
        print(f"[✗] Erro ao baixar: {e}")

if __name__ == '__main__':
    url = "https://ckan.pbh.gov.br/dataset/ec3efaac-0ca6-4846-9e32-0ffff2d76dbb/resource/a35a0ed3-c933-4919-b23f-b925c37b64b8/download/20241001_atividade_economica.csv"
    nome_arquivo = "20241001_atividade_economica.csv"
    
    baixar_arquivo_se_necessario(url, nome_arquivo)

    filtrar_csv.main()