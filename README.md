![image](https://github.com/AxelK1999/algBusquedaHeuristica/assets/69541858/271d5160-5758-4797-a70f-d19acf0f17e0)


**Instalaciones requeridas**
- Instalar python :  `https://www.python.org/ `
- Una vez posicionado en la carpeta raiz del proyecto, en la terminal:  `pip install -r requirements.txt`
  
**USO**
  - Para ejecutar aplicacion, ejecutar en la terminal estando posicionado en el proyecto:  `python app.py `

**Descripción del Problema:**

Los problemas de búsqueda en grandes espacios de estados presentan desafíos significativos debido a la necesidad de analizar múltiples caminos, muchos de los cuales pueden no ser útiles. Para abordar este problema, se emplean técnicas heurísticas que guían la búsqueda descartando caminos no prometedores.

En este contexto, este trabajo se centra en la implementación y comparación de dos algoritmos de búsqueda heurística: Escalada Simple y Máxima Pendiente. Ambos algoritmos utilizan funciones heurísticas ( distancia en línea recta y distancia Manhattan) para estimar la distancia restante hacia el objetivo, optimizando el proceso de búsqueda.

**Ejemplo de Uso:**

 - Paso 1: Ingresar la cantidad de estados que tendra el grafo y presionar `crear estados`
 - Paso 2: Ingresar el nombre(una letra) de cada estado vacio creado, su posicion y conexiones manualmente o presionar `cargar datos de estados automatico`.
 - Paso 3: Presionar `cargar grafo` 
 - Paso 4: Seleccionar el estado inicial y final por medio de los desplegables una vez cargado el grafo
 - Paso 5: Selecciona la heurística a utilizar (Distancia en Línea Recta o Distancia Manhattan) y el algoritmo a implementar por medio de sus desplegables correspondientes.
 - Paso 6: Ejecuta los algoritmos y observa el proceso paso a paso en la interfaz de visualización `Paso siguiente`, `Paso antrior`,`Grafo completo`.
 - Paso 7: Revisa la comparación de resultados, analizando la cantidad de pasos y la capacidad de los algoritmos para superar obstáculos, presionando `ver estadisticas`.
 - Paso 8: Para ver el grafo resultante del algoritmo no seleccionado, para realizar la comparacion visual, presionar `ver grafo alg. no seleccionado`
