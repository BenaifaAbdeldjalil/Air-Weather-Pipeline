import os
from pathlib import Path


# Projet créé dans le dossier courant
base = Path(".")


# 1) Dossiers principaux visibles à la racine du dépôt source
folders = [
    ".github",
    ".github/ISSUE_TEMPLATE",
    "data",
    "data/raw",
    "data/external",
    "data/processed",
    "logs",
    "sql",
    "sql/ddl",
    "sql/queries",
    "dbt_project",
    "tests",
    "src",
    "src/extract",
    "src/transform",
    "src/load",
    "src/quality",
    "src/utils"
]


# Création du dossier principal
if not base.exists():
    base.mkdir(parents=True, exist_ok=True)
    print(f"✅ Projet créé : {base.resolve()}")
else:
    print(f"⏭️  Projet déjà existant : {base.resolve()}")


# Création des dossiers
for folder in folders:
    path = base / folder

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Dossier créé : {path}")
    else:
        print(f"⏭️  Dossier déjà existant : {path}")


print("\n📁 Contenu actuel de la racine du projet :")
print(os.listdir(base))


# 2) Fichiers principaux du dépôt
files = [
    ".gitignore",
    ".env.example",
    "requirements-dev.txt",
    "pyproject.toml",
    "src/config.py",
    "src/main.py",
    "data/.gitkeep"
]

print("\n🎉 Structure principale créée avec succès.")
print(f"📂 Chemin du projet : {base.resolve()}")