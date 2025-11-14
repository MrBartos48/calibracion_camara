import os

def renombrar_fotos_por_bloque(directorio_trabajo='.'):
    """
    Renombra las fotos en el directorio de trabajo según la ley:
    nombre = f'{x}{y}', donde x es un número de 4 dígitos que incrementa
    cada 4 fotos, y y es una letra (a, b, c, d) que se reinicia cada 4 fotos.

    :param directorio_trabajo: La ruta de la carpeta a procesar. Por defecto es el directorio actual ('.').
    """
    # 1. Definir las letras (y) y extensiones de imagen
    letras = ['a', 'b', 'c', 'd']
    extensiones_imagen = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    print(f"Buscando archivos en: {os.path.abspath(directorio_trabajo)}")
    
    # 2. Obtener la lista de archivos, filtrando solo imágenes
    # Usamos sorted() para asegurar un orden consistente (alfabético por nombre original)
    try:
        archivos = sorted([
            f for f in os.listdir(directorio_trabajo)
            if f.lower().endswith(extensiones_imagen) and os.path.isfile(os.path.join(directorio_trabajo, f))
        ])
    except FileNotFoundError:
        print(f"Error: El directorio '{directorio_trabajo}' no fue encontrado.")
        return

    if not archivos:
        print("No se encontraron archivos de imagen en el directorio especificado.")
        return

    print(f"Se encontraron {len(archivos)} imágenes para renombrar.")
    
    # 3. Iterar sobre los archivos para renombrarlos
    for indice, nombre_antiguo in enumerate(archivos):
        # 4. Obtener la extensión original del archivo
        # Esto es crucial para que las imágenes sigan siendo válidas
        nombre_base, extension = os.path.splitext(nombre_antiguo)
        
        # 5. Calcular los componentes 'x' y 'y'
        
        # 'x' (Número de 4 dígitos): Se incrementa cada 4 fotos
        # Usamos división entera (//) y sumamos 1 porque el índice empieza en 0
        # Ejemplo: 
        # indice 0, 1, 2, 3 -> (0, 1, 2, 3) // 4 = 0 -> x_num = 0 + 1 = 1
        # indice 4, 5, 6, 7 -> (4, 5, 6, 7) // 4 = 1 -> x_num = 1 + 1 = 2
        x_num = (indice // 4) + 1
        
        # Formatear 'x' como un string de 4 dígitos con ceros a la izquierda
        x = f'{x_num:04d}'
        
        # 'y' (Letra): Se repite en el ciclo a, b, c, d
        # Usamos el operador módulo (%) para obtener el índice de la letra
        # Ejemplo:
        # indice 0, 4, 8, 12 -> 0 % 4 = 0 -> letra = letras[0] = 'a'
        # indice 1, 5, 9, 13 -> 1 % 4 = 1 -> letra = letras[1] = 'b'
        y = letras[indice % 4]
        
        # 6. Crear el nuevo nombre completo
        nombre_nuevo = f'{x}{y}{extension}'
        
        # 7. Renombrar el archivo
        ruta_antigua = os.path.join(directorio_trabajo, nombre_antiguo)
        ruta_nueva = os.path.join(directorio_trabajo, nombre_nuevo)
        
        try:
            os.rename(ruta_antigua, ruta_nueva)
            print(f"Renombrado: {nombre_antiguo} -> {nombre_nuevo}")
        except Exception as e:
            print(f"Error al renombrar {nombre_antiguo}: {e}")

# Ejecutar la función
# NOTA: Asegúrate de que este script esté en la misma carpeta que las fotos
# o especifica la ruta de la carpeta si es diferente.
if __name__ == '__main__':
    # Puedes cambiar '.' por la ruta de tu carpeta (ej: '/ruta/a/mis/fotos')
    renombrar_fotos_por_bloque('.')