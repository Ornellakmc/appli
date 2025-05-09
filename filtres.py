import numpy as np
from PIL import Image
from scipy.signal import convolve2d

def applique_noyau(image, noyau):
    matrice = np.array(image).astype(np.float32)
    resultats = []
    for canal in range(3):  # R, G, B
        canal_filtré = convolve2d(matrice[:, :, canal], noyau, mode='same', boundary='symm')
        canal_filtré = np.clip(canal_filtré, 0, 255)
        resultats.append(canal_filtré)
    image_filtrée = np.stack(resultats, axis=2).astype(np.uint8)
    return Image.fromarray(image_filtrée)

def filtre_flou_uniforme(image, intensite=1):
    taille = 3 + 2 * int(intensite)  # taille 3, 5, 7, etc.
    noyau = np.ones((taille, taille)) / (taille * taille)
    return applique_noyau(image, noyau)

def filtre_rehaussement(image, intensite=1):
    facteur = float(intensite)
    noyau = np.array([[0, -1, 0],
                      [-1, 4 + facteur, -1],
                      [0, -1, 0]])
    return applique_noyau(image, noyau)
