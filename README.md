# calibracion_camara
Códigos usados para la calibración de cualquier cámara usando opencv. Permite obtener la Matriz de la Cámara y los Coeficientes de Distorsión para corregir futuras imágenes. Colocar ambos códigos dentro de una misma área de trabajo.

**1. Calibración.py**

   **Objetivo:**
   - Calcular los parámetros fijos (intrínsecos) de tu cámara.
   
   **Requisitos:**
   - Las 10 o más imágenes de muestra del tablero de ajedrez deben estar en la carpeta de trabajo.
   
   **Resultado:**
   - El script calcula la Matriz de la Cámara (mtx) y los Coeficientes de Distorsión (dist). Guarda estos dos parámetros en el archivo "calib_params.npz". Genera una imagen de ejemplo corregida (calibresult.png) y muestra el Error de Reproyección (que debe ser bajo, cercano a 0).
   Una vez que este paso se ejecuta con éxito, nunca más se necesita repetir, a menos que se cambie la cámara, la lente o se modifique significativamente la configuración de enfoque.

**2. Corrección_inicial.py**

   **Objetivo:**
   - Eliminar la distorsión de cualquier nueva foto.

   **Requisitos:**
   - La foto nueva que se desea operar.
   - El archivo de parámetros "calib_params.npz".
   
   **Proceso:**
   - El script carga "mtx" y "dist" desde "calib_params.npz".
   - Modificar en la línea 34: img_nombre = "20251105_010154" y colocar el nombre de la nueva foto.
   - El script aplica la función "corregir_distorsion" a la nueva foto.
   
   **Resultado:**
   - Muestra la imagen original y la corregida.
   - Guarda la imagen corregida como "nueva_foto_corregida.jpg".

**3. Rotulador.py**

   **Objetivo:**
   - Dar el formato a las imágenes según lo indicado (ej: 0001a, 0001b, etc.).

   **Requisitos:**
   - Estar dentro de la misma carpeta que el conjunto de fotos a renombrar (ordenados alfabéticamente).
   
   **Proceso:**
   - El script recorre cada imagen de la carpeta de trabajo y la renombra siguiendo la ley: nombre = f'{x}{y}'.
   - x: Número entero de 4 dígitos (relleno de 0 a la izquierda) que aumenta una unidad cada 4 fotos.
   - y: Letras (a, b, c, d) cuyo índice aumenta en una unidad para cada foto y cuyo índice se reinicia cada 4 fotos.
   
   **Resultado:**
   - Sobreescribe cada imagen con su correspondiente nombre.

**4. Corrección_total.py**

   **Objetivo:**
   - Eliminar la distorsión de todo el conjunto de fotos.

   **Requisitos:**
   - Estar dentro de la misma carpeta que el conjunto de fotos a corregir.
   - El archivo de parámetros "calib_params.npz" obtenido en Calibración.py.
   
   **Proceso:**
   - El script carga "mtx" y "dist" desde "calib_params.npz".
   - Recorre todas las imágenes dentro de la carpeta de trabajo.
   - El script aplica la función "corregir_distorsion" a cada foto y las sobreescribe con el mismo nombre.
   
   **Resultado:**
   - Guarda las imágenes corregidas con el mismo nombre.
