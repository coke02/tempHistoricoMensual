import requests
import json
from datetime import datetime

date = datetime.now()
past_year = int(date.strftime('%Y')) - 1

my_User = '' #Tu usuario de MeteoChile registrate eb la pagina de MeteoChile para obtener un usuario y token
my_Key = '' #https://climatologia.meteochile.gob.cl/application/usuario/loginUsuario

with open('listado_estaciones_automaticas.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

diccionario_estacionesAutomaticas = data['diccionario_estacionesAutomaticas']

# Crear un diccionario para almacenar los datos de temperatura histórica
resultados = {}

for estacion in diccionario_estacionesAutomaticas:
    cod_Estaciones = diccionario_estacionesAutomaticas[estacion]
    print(f"Obteniendo datos para la estación {cod_Estaciones}...")

    try:
        url = f'https://climatologia.meteochile.gob.cl/application/servicios/getTemperaturaHistorica/{cod_Estaciones}?usuario={my_User}&token={my_Key}'
        response = requests.get(url)
        data = response.json()

    except Exception as e:
        print(f'Error al obtener datos de la estación {cod_Estaciones}: {e}')
        continue

    datosEstacion = data.get('datosHistoricos', {}).get('anuales')

    # Verificar que datosEstacion no sea None y que sea una lista
    if datosEstacion and isinstance(datosEstacion, list):
        # Buscar el año específico en los datos anuales
        for registro in datosEstacion:
            if registro.get('ano') == int(past_year):
                temperatura_historica = registro.get('valores', {})
                resultados[cod_Estaciones] = {
                    'nombreEstacion': data['datosEstacion']['nombreEstacion'],
                    'mediaCli': temperatura_historica.get('mediaCli'),
                    'mediaAri': temperatura_historica.get('mediaAri'),
                    'feMaxAbs': temperatura_historica.get('feMaxAbs'),
                    'maxAbs': temperatura_historica.get('maxAbs'),
                    'minAbs': temperatura_historica.get('minAbs'),
                    'feMinAbs': temperatura_historica.get('feMinAbs')
                }
                print(f"Estación {cod_Estaciones} - Temperatura Media del Año {past_year}: {temperatura_historica.get('mediaCli')}")
                break
        else:
            print(f'No hay datos para el año {past_year} en la estación {cod_Estaciones}.')
    else:
        print(f'La estructura de datos es incorrecta o no hay datos anuales para la estación {cod_Estaciones}.')

# Guardar los resultados en un archivo JSON
with open(f'temperatura_historica_{past_year}(3).json', 'w', encoding='utf-8') as outfile:
    json.dump(resultados, outfile, ensure_ascii=False, indent=4)

print("Datos guardados en 'temperatura_historica_2023.json'")