import os
import urllib.request
import filtrar_csv

def downloadFile(url, filename):
    """
    Baixa um arquivo da URL fornecida, caso ele ainda não exista localmente.

    Parâmetros:
        url (str): URL do arquivo a ser baixado.
        filename (str): Nome do arquivo local onde o conteúdo será salvo.
    """
    if os.path.exists(filename):
        print(f"[✓] O arquivo '{filename}' já existe. Nenhum download necessário.")
        return

    print(f"[↓] Baixando '{filename}'...")

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        print(f"[✔] Download concluído e salvo como '{filename}'")
    except Exception as e:
        print(f"[✗] Erro ao baixar: {e}")

if __name__ == '__main__':
    url = "https://ckan.pbh.gov.br/dataset/ec3efaac-0ca6-4846-9e32-0ffff2d76dbb/resource/a35a0ed3-c933-4919-b23f-b925c37b64b8/download/20241001_atividade_economica.csv"
    filename = "20241001_atividade_economica.csv"
    
    downloadFile(url, filename)

    filtrar_csv.main()