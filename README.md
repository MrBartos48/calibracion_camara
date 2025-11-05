# calibracion_camara
Códigos usados para la calibración de cualquier cámara usando opencv. Permite obtener la Matriz de la Cámara y los Coeficientes de Distorsión para corregir futuras imágenes. Colocar ambos códigos dentro de una misma área de trabajo.

1. Calibración.py
   **Objetivo:**
   - Calcular los parámetros fijos (intrínsecos) de tu cámara.
   **Requisitos:**
   - Las 10 o más imágenes de muestra del tablero de ajedrez deben estar en la carpeta de trabajo.
   **Resultado:**
   - El script calcula la Matriz de la Cámara (mtx) y los Coeficientes de Distorsión (dist). Guarda estos dos parámetros en el archivo "calib_params.npz". Genera una imagen de ejemplo corregida (calibresult.png) y muestra el Error de Reproyección (que debe ser bajo, cercano a 0).
   Una vez que este paso se ejecuta con éxito, nunca más se necesita repetir, a menos que se cambie la cámara, la lente o se modifique significativamente la configuración de enfoque.

2. Corrección.py
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
