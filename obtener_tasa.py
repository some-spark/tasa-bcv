import requests
import warnings
from bs4 import BeautifulSoup
from decimal import Decimal, ROUND_HALF_UP
import json 
from datetime import datetime, timezone

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.bcv.org.ve/"

def main():


    headers = {"User-Agent": "Mozilla/5.0 (compatible; mi-scraper/1.0)"}
    
    try:
        resp = requests.get(URL, headers=headers, timeout=10, verify=False)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error de red: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    # Buscar tasa USD
    tasa_elem = soup.select_one('#dolar .strong-tb')
    if tasa_elem is None:
        print("No encontré elemento de tasa (¿cambió el HTML?)")
        return
    
    tasa_texto = tasa_elem.text.strip()
    tasa_limpia = tasa_texto.replace(',', '.')
    tasa = Decimal(tasa_limpia).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Buscar fecha valor
    fecha_span = soup.find('span', property='dc:date')
    if fecha_span is None:
        print("No encontré fecha valor")
        return
    
    fecha_valor = fecha_span.get('content')
    fecha_corta = fecha_valor.split('T')[0]

    data = {
    "tasa": float(tasa),
    "fecha_valor": fecha_corta,
    "actualizado": datetime.now(timezone.utc).isoformat(timespec='seconds').replace(' -00:00', 'z')
    }

    print(f"tasa.json guardado: {data}")

    with open('tasa.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Tasa $: {tasa} | Fecha valor: {fecha_corta}")

if __name__ == "__main__":
    main()