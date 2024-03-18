# Algoritmos de Camino Corto en la ciudad de La Paz
Este repositorio contiene el código utilizado en el video de YouTube titulado __"Comparando Algoritmos: A* vs Dijkstra, en el mapa de la ciudad"__. El video proporciona una comparación visual entre los algoritmos A* y Dijkstra en el contexto de encontrar caminos en un mapa de la ciudad representado como un grafo.

[**¡Míralo aquí!**](https://youtu.be/oMgfGkFSgI0) (está en español).

![paragit](https://github.com/santifiorino/maps_pathfinding/assets/94584235/6741cab4-477d-4241-9d0f-8c8b9465b5b6)

## Introducción
Los experimentos realizados en el video se pueden reproducir fácilmente agregando alguna lógica de guardado de imágenes a este cuaderno, asegurando que guarde cada fotograma intermedio en lugar de solo el final. Opté por no incorporar un mecanismo de impresión completo en el cuaderno para evitar complejidad innecesaria y mantener la claridad. Sin embargo, si se desea, implementar esta característica es sencillo. Los experimentos realizados en el video son los siguientes:

### Experimento 1: Eficiencia de Búsqueda de Caminos
El primer experimento se centra en comparar la eficiencia de los algoritmos A* y Dijkstra. Medimos el número de iteraciones que cada algoritmo toma para encontrar un camino, y luego analizamos la distancia, velocidad y tiempo del camino reconstruido. La visualización en el video ilustra la expansión de los algoritmos desde el origen hasta el destino, destacando las carreteras consideradas durante el proceso.

La conclusión de este experimento es que, aunque Dijkstra puede tomar más iteraciones y producir un camino ligeramente más largo, encuentra el camino más rápido absoluto. Por otro lado, A* es más rápido de ejecutar pero puede no siempre producir el camino óptimo.

### Experimento 2: Análisis del Uso de Carreteras
En el segundo experimento, realizamos un análisis más profundo del uso de carreteras ejecutando un algoritmo varias veces desde puntos de partida aleatorios. Cada vez que se ejecuta el algoritmo, incrementamos un contador para cada carretera del camino encontrado. Luego, podemos trazar un mapa de calor para ver qué carreteras fueron las más utilizadas por cada algoritmo.

El análisis del mapa de calor revela observaciones interesantes. El algoritmo de Dijkstra exhibe una tendencia a priorizar autopistas y carreteras principales debido a su potencial para rutas más rápidas hacia el destino. Por el contrario, el algoritmo A* podría elegir caminos no convencionales, priorizando la eficiencia en alcanzar el destino durante su ejecución. Como resultado, puede ignorar desviaciones hacia autopistas o carreteras principales, a pesar de su potencial para un viaje más rápido, ya que podrían alargar el camino.

## Cómo usar
Este código depende de la biblioteca osmnx. Por favor, consulta [la documentación de osmnx](https://osmnx.readthedocs.io/en/stable/) para obtener instrucciones de instalación y pautas de uso detalladas. Una vez instalado, puedes utilizar todas las funcionalidades proporcionadas en el cuaderno para reproducir los experimentos realizados en el video y explorar análisis adicionales.

## Configuración del entorno virtual y dependencias

Para ejecutar este código, es recomendable usar un entorno virtual de Python. Esto ayuda a gestionar las dependencias de manera aislada y evita conflictos con otras librerías. Sigue estos pasos para configurar tu entorno:

1. Crea un entorno virtual de Python, navega al directorio del proyecto.:
    ```
    python -m venv venv
    ```
3. Activa el entorno virtual:
- En Windows:
  ```
  .\venv\Scripts\activate
  ```
- En Linux o macOS:
  ```
  source venv/bin/activate
  ```
4. Una vez activado el entorno virtual, instala las dependencias necesarias ejecutando:
    ```
    pip install -r requirements.txt
    ```