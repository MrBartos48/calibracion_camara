import numpy as np
import cv2 as cv
import os

def corregir_distorsion(imagen_entrada, mtx, dist):
    """Aplica la corrección de distorsión a una imagen usando los parámetros de calibración."""
    h, w = imagen_entrada.shape[:2]
    
    # Se utiliza alpha=0 para que se recorten los píxeles inválidos (más zoom)
    # Si quieres mantener todos los píxeles (con bordes negros) usa alpha=1
    alpha = 0 
    
    # 1. Obtener la matriz óptima de la cámara
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), alpha, (w, h)) 
    
    # 2. Corregir la distorsión
    # El mapa de reproyección ('initUndistortRectifyMap' y 'remap') es más rápido 
    # en procesamiento masivo, pero 'undistort' es más simple y suficiente aquí.
    dst = cv.undistort(imagen_entrada, mtx, dist, None, newcameramtx)
    
    # 3. Recortar la imagen si se usó Alpha=0 (para eliminar bordes no válidos)
    if alpha == 0:
        x, y, w_crop, h_crop = roi
        # Solo aplica el recorte si el ROI es válido (es decir, no cubre toda la imagen)
        if w_crop > 0 and h_crop > 0:
            dst = dst[y:y+h_crop, x:x+w_crop]
    
    return dst

# --- Proceso de Carga y Aplicación Masiva ---

# 1. Cargar los parámetros guardados
try:
    calib_data = np.load('calib_params.npz')
    mtx_loaded = calib_data['mtx']
    dist_loaded = calib_data['dist']
    print("✅ Parámetros de calibración cargados con éxito de 'calib_params.npz'.")
    
except FileNotFoundError:
    print("❌ Error: El archivo 'calib_params.npz' no fue encontrado. Asegúrate de que esté en la misma carpeta.")
    exit()

# 2. Definir las extensiones de imagen a procesar y el directorio
extensiones_imagen = ('.jpg', '.jpeg', '.png', '.tiff', '.webp')
directorio_trabajo = '.' # Directorio actual

# 3. Obtener y ordenar la lista de archivos de imagen
try:
    archivos_imagen = sorted([
        f for f in os.listdir(directorio_trabajo)
        if f.lower().endswith(extensiones_imagen) and os.path.isfile(os.path.join(directorio_trabajo, f))
    ])
except Exception as e:
    print(f"❌ Error al listar archivos: {e}")
    exit()

if not archivos_imagen:
    print("⚠️ No se encontraron archivos de imagen para corregir en el directorio.")
else:
    print(f"Comenzando la corrección de distorsión para {len(archivos_imagen)} imágenes...")
    
    # 4. Procesar cada imagen
    for nombre_archivo in archivos_imagen:
        ruta_completa = os.path.join(directorio_trabajo, nombre_archivo)
        
        # Cargar la imagen
        imagen_original = cv.imread(ruta_completa)
        
        if imagen_original is None:
            print(f"   ❌ No se pudo cargar la imagen: {nombre_archivo}. Saltando.")
            continue
            
        print(f"   ⚙️ Procesando: {nombre_archivo}")
        
        # Aplicar la corrección
        imagen_corregida = corregir_distorsion(imagen_original, mtx_loaded, dist_loaded)
        
        # 5. Sobreescribir el archivo original
        # NOTA: cv.imwrite determinará el formato de guardado basándose en la extensión
        # de 'nombre_archivo', lo cual es crucial para mantener la consistencia.
        if cv.imwrite(ruta_completa, imagen_corregida):
            print(f"   ✅ Sobreescrito con éxito: {nombre_archivo}")
        else:
            print(f"   ❌ Error al guardar/sobreescribir: {nombre_archivo}")

print("\nProceso de corrección de distorsión masiva finalizado.")