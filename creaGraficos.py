import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Directorios
data_dir = 'datos'
output_dir = 'graficos'
os.makedirs(output_dir, exist_ok=True)

date = datetime.now()
current_month = int(date.strftime('%m')) -1

# Iterar sobre cada archivo JSON en la carpeta 'datos' y generar un gráfico
for json_file in os.listdir(data_dir):
    if json_file.endswith('.json'):
        file_path = os.path.join(data_dir, json_file)

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        years = []
        max_temps = []
        min_temps = []

        for entry in data:
            year = entry["ano"]
            max_temp = entry["valores"].get("maxAbs")
            min_temp = entry["valores"].get("minAbs")

            # Verificar que los valores de temperatura no sean None
            if max_temp is not None and min_temp is not None:
                years.append(year)
                max_temps.append(max_temp)
                min_temps.append(min_temp)

        # Verificar si hay datos suficientes para generar el gráfico
        if years:
            # Crear el gráfico
            plt.figure(figsize=(10, 6))
            plt.bar(years, max_temps, color='red', alpha=0.6, label='Temp. Máxima')
            plt.bar(years, min_temps, color='blue', alpha=0.6, label='Temp. Mínima')

            # Configurar título y etiquetas
            plt.title(f'Promedio Temperatura Mensual ({current_month}) Hostotica Máxima y Mínima - Estación {json_file[:-5]}')
            plt.xlabel('Años')
            plt.ylabel('Temperatura (°C)')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.5)

            # Guardar el gráfico en la carpeta 'graficos'
            output_path = os.path.join(output_dir, f'{json_file[:-5]}.png')
            plt.savefig(output_path)
            plt.close()

            print(f'Gráfico guardado en: {output_path}')
        else:
            # No hay datos válidos para generar el gráfico
            print(f"No se encontraron datos válidos para {json_file[:-5]}")