import requests
import csv
from datetime import datetime

API_KEY = 'b97591668f40c5e0dd5bfd519f558171'
# Coordenadas de Quito
LAT = -3.9931
LON = -79.2036
# URL del API
URL = f'http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'

def format_row(timestamp, temperature, humidity, description):
    # Define el formato de la fila con separación por '|'
    return f"{timestamp:<24} | {temperature:<15} | {humidity:<11} | {description:<20}"

def save_to_csv(header, row, file_path):
    try:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            # Escribe la cabecera solo si el archivo está vacío
            if file.tell() == 0:
                writer.writerow(header)
            writer.writerow(row)
    except IOError as e:
        print(f"Error al guardar el archivo CSV: {e}")

try:
    # Realiza la solicitud al API
    response = requests.get(URL)
    response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK

    # Convierte la respuesta en formato JSON
    data = response.json()

    # Verifica si la respuesta contiene un código de error
    if data.get('cod') != 200:
        raise Exception(f"Error en la solicitud: {data.get('message')}")

    # Extrae la información que necesitas
    temperature = round(data['main']['temp'], 2)  # Redondea la temperatura a 2 decimales
    humidity = data['main']['humidity']
    description = data['weather'][0]['description'].capitalize()  # Capitaliza la descripción
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Formatea los datos
    formatted_temperature = f"{temperature:.2f} °C"
    formatted_humidity = f"{humidity} %"

    # Define el encabezado y la fila
    header = ['Timestamp', 'Temperature (°C)', 'Humidity (%)', 'Description']
    row = [timestamp, formatted_temperature, formatted_humidity, description]

    # Guarda los datos en el archivo CSV
    file_path = '/home/santiago/LojaWeather/clima-loja-hoy.csv'  # Cambia a una ruta donde tengas permisos
    save_to_csv(header, row, file_path)

    # Imprime el mensaje de éxito en la consola
    print("Solicitud al API completada exitosamente.")

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud al API: {e}")
except Exception as e:
    print(f"Error: {e}")
