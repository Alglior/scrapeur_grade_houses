import os
import subprocess
import sys

SCRIPTS_DIR = "src"

def verifier_creer_dossier():
    """Vérifie si le dossier src existe, le crée si nécessaire."""
    if not os.path.exists(SCRIPTS_DIR):
        print(f"\nCréation du dossier {SCRIPTS_DIR}...")
        os.makedirs(SCRIPTS_DIR)
        print(f"Dossier {SCRIPTS_DIR} créé avec succès.")

def lister_scripts():
    """Liste tous les fichiers .py dans le dossier src."""
    verifier_creer_dossier()
    scripts = []
    for fichier in os.listdir(SCRIPTS_DIR):
        if fichier.endswith('.py'):
            scripts.append(fichier)
    return scripts

def executer_script(script_path):
    """Execute un script Python depuis le dossier src."""
    chemin_complet = os.path.join(SCRIPTS_DIR, script_path)
    
    if not os.path.isfile(chemin_complet):
        print(f"\nErreur : Le fichier {SCRIPTS_DIR}/{script_path} n'existe pas.")
        return
        
    try:
        print(f"\nExécution de {SCRIPTS_DIR}/{script_path}...")
        # Utilisation de sys.executable pour obtenir le bon interpréteur Python
        subprocess.run([sys.executable, chemin_complet], check=True)
        print(f"\nExécution de {script_path} terminée.")
    except subprocess.CalledProcessError as e:
        print(f"\nErreur lors de l'exécution de {script_path}")
        print(f"Code d'erreur : {e.returncode}")

def afficher_menu(scripts):
    """Affiche le menu avec la liste des scripts disponibles."""
    print(f"\n=== Menu Principal ({SCRIPTS_DIR}/) ===")
    print("Scripts disponibles :")
    
    for i, script in enumerate(scripts, 1):
        print(f"{i}. {script}")
    
    print(f"{len(scripts) + 1}. Actualiser la liste des scripts")
    print(f"{len(scripts) + 2}. Quitter")

def main():
    while True:
        scripts = lister_scripts()
        
        if not scripts:
            print(f"\nAucun script .py trouvé dans le dossier {SCRIPTS_DIR}/")
            choix = input("\n1. Actualiser la liste\n2. Quitter\nVotre choix : ")
            if choix == "1":
                continue
            else:
                break
        
        afficher_menu(scripts)
        
        try:
            choix = int(input("\nChoisissez un script à exécuter : "))
            
            if choix == len(scripts) + 1:  # Option Actualiser
                print("\nActualisation de la liste des scripts...")
                continue
            elif choix == len(scripts) + 2:  # Option Quitter
                print("\nAu revoir !")
                break
            elif 1 <= choix <= len(scripts):
                script_choisi = scripts[choix - 1]
                executer_script(script_choisi)
            else:
                print("\nChoix invalide.")
        except ValueError:
            print("\nVeuillez entrer un nombre valide.")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()