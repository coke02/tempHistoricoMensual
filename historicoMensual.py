import requests
import json
import os
from datetime import datetime

# Configuración inicial
date = datetime.now()
current_year = int(date.strftime('%Y'))
current_month = int(date.strftime('%m'))
previous_month = current_month - 1 if current_month > 1 else 12
previous_month_name = datetime(1900, previous_month, 1).strftime('%B')
previous_year = current_year if previous_month != 12 else current_year - 1

my_User = '' #Tu usuario de MeteoChile registrate eb la pagina de MeteoChile para obtener un usuario y token
my_Key = '' #https://climatologia.meteochile.gob.cl/application/usuario/loginUsuario

# Directorio donde se guardarán los archivos JSON
output_dir = 'datos'
os.makedirs(output_dir, exist_ok=True)

# Cargar listado de estaciones
with open('listado_estaciones_automaticas.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

diccionario_estacionesAutomaticas = data['diccionario_estacionesAutomaticas']

# Iterar sobre cada estación
for estacion, cod_Estaciones in diccionario_estacionesAutomaticas.items():
    print(f"Obteniendo datos para la estación {cod_Estaciones}...")

    try:
        url = f'https://climatologia.meteochile.gob.cl/application/servicios/getTemperaturaHistorica/{cod_Estaciones}?usuario={my_User}&token={my_Key}'
        response = requests.get(url)
        data = response.json()

        # Filtrar datos del mes anterior para todos los años disponibles en la estación
        datos_filtrados = []
        if "datosHistoricos" in data and "mensuales" in data["datosHistoricos"]:
            for registro in data["datosHistoricos"]["mensuales"]:
                if registro["mes"] == previous_month:
                    datos_filtrados.append(registro)

        # Guardar resultados en un archivo JSON si se encontraron datos
        if datos_filtrados:
            output_file = os.path.join(output_dir, f"{cod_Estaciones}.json")
            with open(output_file, 'w', encoding='utf-8') as json_file:
                json.dump(datos_filtrados, json_file, ensure_ascii=False, indent=4)
            print(f"Datos guardados en {output_file}")
        else:
            print(f"No se encontraron datos para el mes de {previous_month_name} en la estación {cod_Estaciones}")

    except Exception as e:
        print(f'Error al obtener datos de la estación {cod_Estaciones}: {e}')
        continue