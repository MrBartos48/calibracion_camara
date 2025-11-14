import numpy as np
import cv2 as cv

def corregir_distorsion(imagen_entrada, mtx, dist):
    """Aplica la corrección de distorsión a una imagen usando los parámetros de calibración."""
    h, w = imagen_entrada.shape[:2]
    
    # 1. Obtener la matriz óptima de la cámara
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h)) 
    
    # 2. Corregir la distorsión
    dst = cv.undistort(imagen_entrada, mtx, dist, None, newcameramtx)
    
    # 3. Recortar la imagen (para eliminar bordes no válidos si se usó Alpha=0)
    x, y, w_crop, h_crop = roi
    dst = dst[y:y+h_crop, x:x+w_crop]
    
    return dst

# --- Proceso de Carga y Uso ---

# 1. Cargar los parámetros guardados
try:
    calib_data = np.load('calib_params.npz')
    mtx_loaded = calib_data['mtx']
    dist_loaded = calib_data['dist']
    print("Parámetros de calibración cargados con éxito.")
    
except FileNotFoundError:
    print("Error: El archivo 'calib_params.npz' no fue encontrado.")
    exit()

# 2. Cargar una nueva imagen para corregir
img_nombre = "20251105_010154"
nueva_imagen = cv.imread(f'{img_nombre}.jpg')

if nueva_imagen is not None:
    # 3. Aplicar la corrección
    imagen_corregida = corregir_distorsion(nueva_imagen, mtx_loaded, dist_loaded)
    
    # 4. Guardar y mostrar
    cv.imwrite('nueva_foto_corregida.jpg', imagen_corregida)
    
    # --- CORRECCIÓN DE VISUALIZACIÓN APLICADA AQUÍ ---
    # 4.1 Inicializar y redimensionar la ventana "Original"
    cv.namedWindow('Original', cv.WINDOW_NORMAL)
    cv.resizeWindow('Original', 800, 600) # Tamaño de ejemplo (ajústalo si es necesario)
    
    # 4.2 Inicializar y redimensionar la ventana "Corregida"
    cv.namedWindow('Corregida', cv.WINDOW_NORMAL)
    cv.resizeWindow('Corregida', 800, 600)
    
    # 4.3 Mostrar las imágenes
    cv.imshow('Original', nueva_imagen)
    cv.imshow('Corregida', imagen_corregida)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("Error: No se pudo cargar la imagen de entrada.")
