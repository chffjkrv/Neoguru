import os
import requests
from bs4 import BeautifulSoup
import logging

# Configuración del registro
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Nombre del archivo que contiene las URLs
archivo_urls = 'URLs.txt'

# Directorio donde se guardarán los resultados
directorio_resultados = 'Results'

# Crear el directorio si no existe
if not os.path.exists(directorio_resultados):
    os.makedirs(directorio_resultados)
    logging.info(f'Directorio {directorio_resultados} creado.')
else:
    logging.info(f'Directorio {directorio_resultados} ya existe.')

# Leer las URLs desde el archivo
try:
    with open(archivo_urls, 'r') as file:
        urls = [linea.strip() for linea in file if linea.strip()]
    logging.info(f'Se han leído {len(urls)} URLs desde {archivo_urls}.')
except FileNotFoundError:
    logging.error(f'Error: El archivo {archivo_urls} no se encontró.')
    exit(1)

# Función para generar un nombre de archivo válido a partir de la URL
def generar_nombre_archivo(url):
    nombre_archivo = url.replace('https://', '').replace('http://', '').replace('/', '_')
    return os.path.join(directorio_resultados, f'{nombre_archivo}.txt')

# Función para realizar scraping de una URL y guardar el contenido en un archivo
def scrape_y_guardar(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        logging.info(f'Iniciando solicitud GET para {url}.')
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        logging.info(f'Solicitud GET exitosa para {url}.')
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extraer el contenido deseado; aquí se extrae todo el texto de la página
        contenido = soup.get_text()
        # Generar un nombre de archivo basado en la URL
        nombre_archivo = generar_nombre_archivo(url)
        # Guardar el contenido en un archivo de texto
        with open(nombre_archivo, 'w', encoding='utf-8') as file:
            file.write(contenido)
        logging.info(f'Contenido de {url} guardado en {nombre_archivo}.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error al acceder a {url}: {e}')

# Iterar sobre las URLs y realizar scraping
for i, url in enumerate(urls, start=1):
    logging.info(f'Procesando URL {i} de {len(urls)}: {url}')
    scrape_y_guardar(url)
    logging.info(f'Finalizado procesamiento de URL {i} de {len(urls)}: {url}')

logging.info('Proceso de scraping completado.')
