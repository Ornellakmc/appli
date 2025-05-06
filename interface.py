import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from filtres import *
import os

# Variables globales
photo_originale = None
photo_affichee = None
image_label = None
historique = []
indice_historique = -1

def ouvrir_image():
    global photo_originale, photo_affichee, historique, indice_historique
    print("Ouverture d'image...")
    chemin = filedialog.askopenfilename(title="Choisir une image", filetypes=[("Images", "*.jpg *.png *.jpeg")])
    if chemin:
        # Ouvrir l'image en mode RGB pour éviter les problèmes de couleurs
        photo_originale = Image.open(chemin).convert("RGB")
        photo_affichee = photo_originale.copy()
        historique = [photo_affichee.copy()]
        indice_historique = 0
        afficher_image()

def afficher_image():
    global image_label, photo_affichee
    print("Affichage de l'image...")
    # Convertir l'image PIL en format compatible avec Tkinter
    tk_image = ImageTk.PhotoImage(photo_affichee)
    image_label.configure(image=tk_image)
    image_label.image = tk_image  # Sauvegarde l'image dans l'attribut de l'objet Label
    image_label.update_idletasks()  # Force la mise à jour de l'image

def appliquer_filtre(filtre):
    global photo_affichee, historique, indice_historique
    print("Application du filtre...")
    if photo_affichee:
        historique = historique[:indice_historique + 1]  # Limiter l'historique à l'indice actuel
        photo_affichee = filtre(historique[indice_historique].copy())  # Appliquer le filtre
        historique.append(photo_affichee.copy())  # Ajouter l'image filtrée à l'historique
        indice_historique += 1
        afficher_image()  # Afficher l'image après le filtre

def annuler():
    global indice_historique, photo_affichee
    print("Annulation...")
    if indice_historique > 0:
        indice_historique -= 1
        photo_affichee = historique[indice_historique].copy()
        afficher_image()

def retablir():
    global indice_historique, photo_affichee
    print("Rétablissement...")
    if indice_historique < len(historique) - 1:
        indice_historique += 1
        photo_affichee = historique[indice_historique].copy()
        afficher_image()

def sauvegarder_image():
    print("Sauvegarde de l'image...")
    if photo_affichee:
        chemin = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if chemin:
            photo_affichee.save(chemin)

def lancer_interface():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from PIL import Image, ImageTk
    from filtres import filtre_flou_uniforme

    # Variables internes
    photo_originale = None
    photo_affichee = None
    historique = []
    indice_historique = -1

    def ouvrir_image():
        nonlocal photo_originale, photo_affichee, historique, indice_historique
        chemin = filedialog.askopenfilename(title="Choisir une image", filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if chemin:
            photo_originale = Image.open(chemin).convert("RGB")
            photo_affichee = photo_originale.copy()
            historique = [photo_affichee.copy()]
            indice_historique = 0
            afficher_image()

    def afficher_image():
        nonlocal image_label, photo_affichee
        if photo_affichee:
            tk_image = ImageTk.PhotoImage(photo_affichee)
            image_label.configure(image=tk_image)
            image_label.image = tk_image

    def appliquer_filtre(filtre):
        nonlocal photo_affichee, historique, indice_historique
        if photo_affichee:
            historique[:] = historique[:indice_historique + 1]
            photo_affichee = filtre(historique[indice_historique].copy())
            historique.append(photo_affichee.copy())
            indice_historique += 1
            afficher_image()

    def annuler():
        nonlocal indice_historique, photo_affichee
        if indice_historique > 0:
            indice_historique -= 1
            photo_affichee = historique[indice_historique].copy()
            afficher_image()

    def retablir():
        nonlocal indice_historique, photo_affichee
        if indice_historique < len(historique) - 1:
            indice_historique += 1
            photo_affichee = historique[indice_historique].copy()
            afficher_image()

    def sauvegarder_image():
        if photo_affichee:
            chemin = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if chemin:
                photo_affichee.save(chemin)

    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("UVSQolor")
    fenetre.lift()
    fenetre.attributes('-topmost', True)
    fenetre.after(100, lambda: fenetre.attributes('-topmost', False))

    # Menu principal
    menu = tk.Menu(fenetre)
    fenetre.config(menu=menu)

    # Menu Fichier
    fichier_menu = tk.Menu(menu, tearoff=0)
    fichier_menu.add_command(label="Ouvrir", command=ouvrir_image)
    fichier_menu.add_command(label="Sauvegarder", command=sauvegarder_image)
    fichier_menu.add_separator()
    fichier_menu.add_command(label="Quitter", command=fenetre.quit)
    menu.add_cascade(label="Fichier", menu=fichier_menu)

    # Menu Édition
    edition_menu = tk.Menu(menu, tearoff=0)
    edition_menu.add_command(label="Annuler", command=annuler)
    edition_menu.add_command(label="Rétablir", command=retablir)
    menu.add_cascade(label="Édition", menu=edition_menu)

    # Menu Filtres
    filtre_menu = tk.Menu(menu, tearoff=0)
    filtre_menu.add_command(label="Flou uniforme", command=lambda: appliquer_filtre(filtre_flou_uniforme))
    menu.add_cascade(label="Filtres", menu=filtre_menu)

    # Zone d'affichage de l'image
    image_label = tk.Label(fenetre)
    image_label.pack()

    print("Interface prête...")
    fenetre.mainloop()