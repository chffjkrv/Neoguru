import os
import re
import logging
from openai import OpenAI  # Importa el módulo openai

# Configuración del registro
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Configurar la URL base y la clave API
client = OpenAI(
    api_key="llama-3.2-3b-instruct",
    api_base="http://localhost:1234/v1"
)

# Directorios de entrada y salida
directorio_entrada = 'Results'
directorio_salida = 'Filtered_Results'

# Crear el directorio de salida si no existe
if not os.path.exists(directorio_salida):
    os.makedirs(directorio_salida)
    logging.info(f'Directorio {directorio_salida} creado.')
else:
    logging.info(f'Directorio {directorio_salida} ya existe.')

# Función para limpiar saltos de línea adicionales
def limpiar_saltos_linea(texto):
    return re.sub(r'\n+', '\n', texto).strip()

# Plantilla de prompt para extraer contenido religioso
plantilla_prompt = """
A continuación se presenta un texto extraído de una página web sobre el Islam. Tu tarea es identificar y extraer únicamente los fragmentos que contienen contenido significativo relacionado con temas religiosos islámicos.

Debes eliminar cualquier elemento que no aporte información relevante, incluyendo:

- Enlaces, botones y elementos de navegación.
- Palabras o frases como 'Search for', 'instagram', 'facebook', 'twitter', y similares.
- Cualquier otro contenido que no esté directamente relacionado con información religiosa islámica.

Tu respuesta debe consistir únicamente en el texto filtrado, sin añadir explicaciones, comentarios ni contenido adicional.

Texto:
{texto}

Fragmentos relacionados con temas religiosos:
"""

# Procesar cada archivo en el directorio de entrada
for nombre_archivo in os.listdir(directorio_entrada):
    ruta_archivo = os.path.join(directorio_entrada, nombre_archivo)
    if os.path.isfile(ruta_archivo) and nombre_archivo.endswith('.txt'):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            logging.info(f'Archivo {nombre_archivo} leído correctamente.')

            # Limpiar saltos de línea
            contenido_limpio = limpiar_saltos_linea(contenido)

            # Preparar el prompt
            prompt = plantilla_prompt.format(texto=contenido_limpio)

            # Realizar la solicitud de completado
            respuesta = openai.completions.create(
                model="bartowski/Llama-3.2-3B-Instruct-GGUF",  # Reemplaza con el identificador de tu modelo
                prompt=prompt,
                max_tokens=131000,  # Ajusta según las capacidades de tu modelo y recursos
                temperature=0.7
            )

            # Obtener el texto generado
            texto_filtrado = respuesta.choices[0].text.strip()
            logging.info(f'Procesamiento del archivo {nombre_archivo} completado.')

            # Guardar la respuesta en un nuevo archivo en el directorio de salida
            nombre_archivo_salida = f'filtrado_{nombre_archivo}'
            ruta_archivo_salida = os.path.join(directorio_salida, nombre_archivo_salida)
            with open(ruta_archivo_salida, 'w', encoding='utf-8') as archivo_salida:
                archivo_salida.write(texto_filtrado)
            logging.info(f'Resultado guardado en {nombre_archivo_salida}.')

        except Exception as e:
            logging.error(f'Error al procesar el archivo {nombre_archivo}: {e}')

logging.info('Proceso de filtrado completado.')
