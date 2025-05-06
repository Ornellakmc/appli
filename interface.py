def lancer_interface():
    print("Lancement de l'interface...")  # Pour vérifier si la fonction est bien appelée
    global image_label
    fenetre = tk.Tk()
    fenetre.title("UVSQolor")

    # Mise à jour de l'écran avant de démarrer la boucle Tkinter
    fenetre.update()

    menu = tk.Menu(fenetre)
    fenetre.config(menu=menu)

    fichier_menu = tk.Menu(menu, tearoff=0)
    fichier_menu.add_command(label="Ouvrir", command=ouvrir_image)
    fichier_menu.add_command(label="Sauvegarder", command=sauvegarder_image)
    fichier_menu.add_separator()
    fichier_menu.add_command(label="Quitter", command=fenetre.quit)
    menu.add_cascade(label="Fichier", menu=fichier_menu)

    edition_menu = tk.Menu(menu, tearoff=0)
    edition_menu.add_command(label="Annuler", command=annuler)
    edition_menu.add_command(label="Rétablir", command=retablir)
    menu.add_cascade(label="Édition", menu=edition_menu)

    filtre_menu = tk.Menu(menu, tearoff=0)
    filtre_menu.add_command(label="Flou uniforme", command=lambda: appliquer_filtre(filtre_flou_uniforme))
    menu.add_cascade(label="Filtres", menu=filtre_menu)

    image_label = tk.Label(fenetre)
    image_label.pack()

    fenetre.mainloop()
