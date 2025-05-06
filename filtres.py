import numpy as np
from PIL import Image
from scipy.signal import convolve2d

def filtre_flou_uniforme(image):
    matrice = np.array(image).astype(np.float32)  # Convertir l'image en tableau numpy
    noyau = np.ones((5, 5)) / 25  # Noyau de flou uniforme
    resultats = []

    for canal in range(3):  # R, G, B
        canal_filtré = convolve2d(matrice[:, :, canal], noyau, mode='same', boundary='symm')
        canal_filtré = np.clip(canal_filtré, 0, 255)  # S'assurer que les valeurs sont entre 0 et 255
        resultats.append(canal_filtré)

    image_filtrée = np.stack(resultats, axis=2).astype(np.uint8)
    return Image.fromarray(image_filtrée)  # Convertir le résultat en image PIL
