from pathlib import Path

# 1. On récupère le chemin absolu du fichier config.py
# 2. On remonte l'arborescence pour trouver la racine du projet
# src/clinical_tool/config.py -> parent -> src -> parent -> racine
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Définition des chemins clés
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

# Optionnel : Création automatique des dossiers s'ils n'existent pas
# Comme ça, tu n'as pas d'erreur "Directory not found"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
