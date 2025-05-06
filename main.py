import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from scipy.signal import convolve2d

# ------------------ FONCTIONS DE FLOU ------------------

def creer_noyau_flou(taille):
    """
    Crée un noyau de flou uniforme carré de taille impaire.
    """
    assert taille % 2 == 1, "Le noyau doit avoir une taille impaire"
    return np.ones((taille, taille)) / (taille * taille)

def appliquer_flou(image_array, taille_noyau):
    """
    Applique un flou uniforme à une image NumPy avec un noyau de taille donnée.
    """
    noyau = creer_noyau_flou(taille_noyau)
    image_floutee = np.zeros_like(image_array)
    
    for i in range(3):  # Boucle sur R, G, B
        image_floutee[:, :, i] = convolve2d(
            image_array[:, :, i],
            noyau,
            mode="same",
            boundary="symm"
        )
    return np.clip(image_floutee, 0, 255).astype(np.uint8)

# ------------------ INTERFACE UTILISATEUR ------------------

def charger_image():
    global image_originale, photo_originale
    chemin = filedialog.askopenfilename()
    if chemin:
        img = Image.open(chemin).convert("RGB")
        img = img.resize((400, 400))
        image_originale = img
        photo_originale = np.array(img)
        afficher_image(photo_originale)

def afficher_image(img_array):
    global photo, image_label
    img_pil = Image.fromarray(img_array)
    photo = ImageTk.PhotoImage(img_pil)
    image_label.config(image=photo)
    image_label.image = photo

def maj_flou(valeur):
    if image_originale is None:
        return
    taille = int(valeur)
    if taille % 2 == 0:
        taille += 1
    image_floutee = appliquer_flou(photo_originale, taille)
    afficher_image(image_floutee)

# ------------------ INITIALISATION ------------------

image_originale = None
photo_originale = None
photo = None

racine = tk.Tk()
racine.title("Filtre de flou uniforme - UVSQolor")

bouton_charger = tk.Button(racine, text="Charger une image", command=charger_image)
bouton_charger.pack(pady=10)

curseur_flou = tk.Scale(
    racine,
    from_=1,
    to=21,
    resolution=2,
    orient=tk.HORIZONTAL,
    label="Intensité du flou (taille du noyau)",
    command=maj_flou
)
curseur_flou.set(1)
curseur_flou.pack(pady=10)

image_label = tk.Label(racine)
image_label.pack()

racine.mainloop()
