import tkinter as tk

def lancer_interface():
    print("Lancement de l'interface...")
    fenetre = tk.Tk()
    fenetre.title("Test Interface")
    label = tk.Label(fenetre, text="Interface fonctionnelle !")
    label.pack(padx=20, pady=20)
    fenetre.mainloop()
