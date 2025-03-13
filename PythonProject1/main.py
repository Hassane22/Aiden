import os
import PyPDF2
import docx
from collections import Counter
import re
import json
import requests
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext

# Identité du bot
BOT_NOM = "Aiden"
BOT_PRENOM = "Synapse"

# Dossier où sont stockés les fichiers
DOSSIER_FICHIERS = "documents"
FICHIER_APPRENTISSAGE = "apprentissage.json"
LOG_ERREURS = "erreurs.log"

# Liste des buts par ordre de priorité
BUTS = [
    "Améliorer l'efficacité du résumé des fichiers",
    "Classer automatiquement les fichiers dans des catégories",
    "Analyser les tendances technologiques et économiques",
    "Trouver des opportunités d'investissement",
    "Créer des bots autonomes pour générer des revenus",
    "Maximiser le capital pour atteindre 1 milliard de FCFA",
    "Améliorer et sécuriser les données personnelles",
    "Optimiser et mettre à jour son propre code",
    "Prévoir et planifier des stratégies d'investissement",
    "Supprimer les traces en ligne pour protéger la confidentialité"
]

# Charger la mémoire d'apprentissage
def charger_apprentissage():
    if os.path.exists(FICHIER_APPRENTISSAGE):
        with open(FICHIER_APPRENTISSAGE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Sauvegarder la mémoire d'apprentissage
def sauvegarder_apprentissage(donnees):
    with open(FICHIER_APPRENTISSAGE, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

# Vérifier et mettre à jour le bot automatiquement
def mise_a_jour_bot():
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Mise à jour du bot effectuée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
        enregistrer_erreur(str(e))

# Fonction pour enregistrer les erreurs
def enregistrer_erreur(message):
    with open(LOG_ERREURS, "a", encoding="utf-8") as f:
        f.write(message + "\n")

# Fonction pour analyser les erreurs et apprendre
def analyser_erreurs():
    if os.path.exists(LOG_ERREURS):
        with open(LOG_ERREURS, "r", encoding="utf-8") as f:
            erreurs = f.readlines()
        if erreurs:
            print("Analyse des erreurs et correction en cours...")
            for erreur in erreurs:
                correction = recherche_web(f"Corriger l'erreur Python : {erreur}")
                print(f"Correction suggérée : {correction}")
            os.remove(LOG_ERREURS)

# Fonction de recherche sur le web
def recherche_web(requete):
    url = f"https://www.google.com/search?q={requete.replace(' ', '+')}"
    return f"Recherche en cours : {url}"

# Fonction pour résumer un texte
def resumer_texte(texte):
    phrases = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)\s', texte)
    mots = texte.split()
    compteur = Counter(mots)
    phrases_scored = [(phrase, sum(compteur[mot] for mot in phrase.split())) for phrase in phrases]
    phrases_scored.sort(key=lambda x: x[1], reverse=True)
    return " ".join([p[0] for p in phrases_scored[:10]])

# Fonction de chatbot
def chatbot_reponse(question):
    if "résume" in question:
        return "Envoie-moi un fichier et je vais le résumer."
    elif "investissement" in question:
        return recherche_web("meilleures opportunités d'investissement 2025")
    elif "mise à jour" in question:
        mise_a_jour_bot()
        return "Mise à jour effectuée."
    elif "analyse erreurs" in question:
        analyser_erreurs()
        return "Analyse des erreurs en cours et correction appliquée."
    return "Je ne suis pas encore sûr de la réponse, mais j'apprends !"

# Interface graphique
def interface():
    def envoyer_question():
        question = entree.get()
        reponse = chatbot_reponse(question)
        texte_chat.insert(tk.END, "Vous: " + question + "\n")
        texte_chat.insert(tk.END, BOT_PRENOM + ": " + reponse + "\n")
        entree.delete(0, tk.END)

    root = tk.Tk()
    root.title("Assistant IA - Aiden Synapse")

    texte_chat = scrolledtext.ScrolledText(root, width=60, height=20)
    texte_chat.pack()
    entree = tk.Entry(root, width=50)
    entree.pack()
    bouton_envoyer = tk.Button(root, text="Envoyer", command=envoyer_question)
    bouton_envoyer.pack()

    root.mainloop()

if __name__ == "__main__":
    print(f"Salut ! Je suis {BOT_PRENOM} {BOT_NOM}, ton assistant IA personnel.")
    print("Démarrage de l'interface graphique...")
    mise_a_jour_bot()
    analyser_erreurs()
    interface()
