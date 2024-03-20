from PIL import Image

# Carga las imágenes
imagen_fondo = Image.open("frames/reconstruct-a-star/frame_00062.png")
imagen_superior = Image.open("frames/reconstruct-dijkstra/frame_00050.png")  # Asegúrate de que esta imagen tenga canal alfa

# Ajustar la transparencia de la imagen superior
# Si la imagen superior no tiene un canal alfa, descomenta la siguiente línea para agregar uno
# imagen_superior = imagen_superior.convert("RGBA")

# Crear una nueva imagen con canal alfa para controlar la transparencia
imagen_transparente = Image.new("RGBA", imagen_superior.size)
for x in range(imagen_superior.width):
    for y in range(imagen_superior.height):
        r, g, b, a = imagen_superior.getpixel((x, y))
        imagen_transparente.putpixel((x, y), (r, g, b, int(a * 0.5)))  # Ajusta el 0.5 según la transparencia deseada

# Superponer la imagen transparente sobre el fondo
imagen_final = Image.alpha_composite(imagen_fondo.convert("RGBA"), imagen_transparente)

# Guardar la imagen resultante
imagen_final.save("frames/final.png")
