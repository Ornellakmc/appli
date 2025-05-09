import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from filtres import filtre_flou_uniforme, filtre_rehaussement
import os

photo_originale = None
photo_affichee = None
historique = []
indice_historique = -1
image_label = None

def afficher_image():
    global image_label, photo_affichee
    if photo_affichee:
        tk_image = ImageTk.PhotoImage(photo_affichee)
        image_label.configure(image=tk_image)
        image_label.image = tk_image

def appliquer_filtre_popup(filtre_func, nom_filtre):
    def appliquer_et_afficher(intensite):
        global photo_affichee, historique, indice_historique
        if photo_affichee:
            intensite_val = float(intensite)
            historique = historique[:indice_historique + 1]
            nouvelle = filtre_func(historique[indice_historique].copy(), intensite=intensite_val)
            photo_affichee = nouvelle
            historique.append(photo_affichee.copy())
            indice_historique += 1
            afficher_image()

    popup = tk.Toplevel()
    popup.title(f"{nom_filtre} - Intensité")
    tk.Label(popup, text="Intensité :").pack()
    slider = tk.Scale(popup, from_=1, to=10, orient="horizontal", resolution=1, command=appliquer_et_afficher)
    slider.set(1)
    slider.pack()

def annuler():
    global indice_historique, photo_affichee
    if indice_historique > 0:
        indice_historique -= 1
        photo_affichee = historique[indice_historique].copy()
        afficher_image()

def retablir():
    global indice_historique, photo_affichee
    if indice_historique < len(historique) - 1:
        indice_historique += 1
        photo_affichee = historique[indice_historique].copy()
        afficher_image()

def sauvegarder_image():
    global photo_affichee
    if photo_affichee:
        chemin = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if chemin:
            photo_affichee.save(chemin)

def ouvrir_image():
    global photo_originale, photo_affichee, historique, indice_historique
    chemin = filedialog.askopenfilename(title="Choisir une image", filetypes=[("Images", "*.jpg *.png *.jpeg")])
    if chemin:
        photo_originale = Image.open(chemin).convert("RGB")
        photo_affichee = photo_originale.copy()
        historique.clear()
        historique.append(photo_affichee.copy())
        indice_historique = 0
        afficher_image()

def lancer_interface():
    global image_label
    fenetre = tk.Tk()
    fenetre.title("UVSQolor")

    menu = tk.Menu(fenetre)
    fenetre.config(menu=menu)

    fichier_menu = tk.Menu(menu, tearoff=0)
    fichier_menu.add_command(label="Ouvrir", command=ouvrir_image)
    fichier_menu.add_command(label="Sauvegarder", command=sauvegarder_image)
    fichier_menu.add_command(label="Quitter", command=fenetre.quit)
    menu.add_cascade(label="Fichier", menu=fichier_menu)

    edition_menu = tk.Menu(menu, tearoff=0)
    edition_menu.add_command(label="Annuler", command=annuler)
    edition_menu.add_command(label="Rétablir", command=retablir)
    menu.add_cascade(label="Édition", menu=edition_menu)

    filtre_menu = tk.Menu(menu, tearoff=0)
    filtre_menu.add_command(label="Flou uniforme", command=lambda: appliquer_filtre_popup(filtre_flou_uniforme, "Flou"))
    filtre_menu.add_command(label="Rehaussement", command=lambda: appliquer_filtre_popup(filtre_rehaussement, "Rehaussement"))
    menu.add_cascade(label="Filtres", menu=filtre_menu)

    image_label = tk.Label(fenetre)
    image_label.pack()

    fenetre.mainloop()
