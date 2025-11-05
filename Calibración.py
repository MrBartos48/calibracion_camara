import numpy as np
import cv2 as cv
import glob

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points (10x7 = 70 puntos)
objp = np.zeros((10*7,3), np.float32)
objp[:,:2] = np.mgrid[0:10,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
img_size = (0, 0) # Variable para almacenar el tamaño de la imagen

cv.namedWindow('img', cv.WINDOW_NORMAL)
cv.resizeWindow('img', 1000, 700)

images = glob.glob('*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Capturar el tamaño de la imagen (W, H)
    h, w = img.shape[:2]
    img_size = (w, h) 

    # Find the chess board corners (10,7)
    ret, corners = cv.findChessboardCorners(gray, (10,7), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (10,7), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)

cv.destroyAllWindows()

# --- CALIBRACIÓN FINAL ---
# Usar img_size para el tamaño de la imagen
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img_size, None, None)

# Correción de distorsión (Usando la primera imagen de la lista como ejemplo)
if len(images) > 0:
    img_to_undistort = cv.imread(images[0])
    h_undistort, w_undistort = img_to_undistort.shape[:2]
    
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w_undistort, h_undistort), 1, (w_undistort, h_undistort))
    
    # Undistort
    dst = cv.undistort(img_to_undistort, mtx, dist, None, newcameramtx)
    
    # Crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite('calibresult.png', dst)

# Reproyección del error
mean_error = 0
for i in range(len(objpoints)):
    # Error de reproyección: Compara los puntos 2D originales con los reproyectados
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print(f"\n--- Resultados de la Calibración ---")
print(f"Matriz de la Cámara (mtx):\n{mtx}")
print(f"Coeficientes de Distorsión (dist):\n{dist}")
print(f"Error de Reproyección Total: {mean_error/len(objpoints):.4f}")
print("---")
print("Imagen corregida guardada como 'calibresult.png'")

# Guardar los parámetros en un archivo .npz
np.savez('calib_params.npz', mtx=mtx, dist=dist)
print("Parámetros de calibración guardados en 'calib_params.npz'")