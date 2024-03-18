import requests

def obtener_coordenadas(lugar):
    # Reemplaza "lugar" con tu dirección de interés
    url = f"https://nominatim.openstreetmap.org/search?q={lugar}&format=json"
    
    # Realiza la solicitud
    response = requests.get(url)
    
    # Verifica que la respuesta sea exitosa
    if response.status_code == 200:
        data = response.json()
        if data:
            # Retorna las primeras coordenadas encontradas
            return (float(data[0]['lat']), float(data[0]['lon']))
        else:
            print("No se encontraron resultados.")
    else:
        print("Error en la solicitud.")

# Ejemplo de uso
lugar = "San Miguel, La Paz, Bolivia"
coordenadas = obtener_coordenadas(lugar)
print("Coordenadas de San Miguel:", coordenadas)

lugar = "Obrajes, La Paz, Bolivia"
coordenadas = obtener_coordenadas(lugar)
print("Coordenadas de Obrajes:", coordenadas)
