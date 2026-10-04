import os
from pathlib import Path


# Projet créé dans le dossier courant
base = Path(".")


# 1) Dossiers principaux visibles à la racine du dépôt source
folders = [
    ".github",
    ".github/ISSUE_TEMPLATE",

    "01_Day_Introduction",
    "02_Day_Variables_builtin_functions",
    "03_Day_Operators",
    "04_Day_Strings",
    "05_Day_Lists",
    "06_Day_Tuples",
    "07_Day_Sets",
    "08_Day_Dictionaries",
    "09_Day_Conditionals",
    "10_Day_Loops",
    "11_Day_Functions",
    "12_Day_Modules",
    "13_Day_List_comprehension",
    "14_Day_Higher_order_functions",
    "15_Day_Python_type_errors",
    "16_Day_Python_date_time",
    "17_Day_Exception_handling",
    "18_Day_Regular_expressions",
    "19_Day_File_handling",
    "20_Day_Python_package_manager",
    "21_Day_Classes_and_objects",
    "22_Day_Web_scraping",
    "23_Day_Virtual_environment",
    "24_Day_Statistics",
    "25_Day_Pandas",
    "26_Day_Python_web",
    "27_Day_Python_with_mongodb",
    "28_Day_API",
    "29_Day_Building_API",
    "30_Day_Conclusions",

    "Chinese",
    "French",
    "German",
    "Greek",
    "Korean",
    "Persain",
    "Portuguese",
    "Spanish",
    "Ukrainian",
    "Uzbek",
    "korean",

    "data",
    "files",
    "images",
    "mypackage",
    "numpy_files",
    "old_files",
    "python_for_web",
    "test_files",
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
    "README.md",
    "mymodule.py",
    "numpy.md",

    ".github/FUNDING.yml",

    "mypackage/__init__.py",

    "data/.gitkeep",
    "files/.gitkeep",
    "images/.gitkeep",
    "numpy_files/.gitkeep",
    "old_files/.gitkeep",
    "python_for_web/.gitkeep",
    "test_files/.gitkeep",

    "French/README.md",
    "Chinese/README.md",
    "German/README.md",
    "Greek/README.md",
    "Korean/README.md",
    "Persain/README.md",
    "Portuguese/README.md",
    "Spanish/README.md",
    "Ukrainian/README.md",
    "Uzbek/README.md",
    "korean/README.md",
]


# Ajout des fichiers principaux pour chaque jour
for day in range(1, 31):
    day_folders = [
        "01_Day_Introduction",
        "02_Day_Variables_builtin_functions",
        "03_Day_Operators",
        "04_Day_Strings",
        "05_Day_Lists",
        "06_Day_Tuples",
        "07_Day_Sets",
        "08_Day_Dictionaries",
        "09_Day_Conditionals",
        "10_Day_Loops",
        "11_Day_Functions",
        "12_Day_Modules",
        "13_Day_List_comprehension",
        "14_Day_Higher_order_functions",
        "15_Day_Python_type_errors",
        "16_Day_Python_date_time",
        "17_Day_Exception_handling",
        "18_Day_Regular_expressions",
        "19_Day_File_handling",
        "20_Day_Python_package_manager",
        "21_Day_Classes_and_objects",
        "22_Day_Web_scraping",
        "23_Day_Virtual_environment",
        "24_Day_Statistics",
        "25_Day_Pandas",
        "26_Day_Python_web",
        "27_Day_Python_with_mongodb",
        "28_Day_API",
        "29_Day_Building_API",
        "30_Day_Conclusions",
    ]

    folder_name = day_folders[day - 1]

    files.append(f"{folder_name}/README.md")
    files.append(f"{folder_name}/main.py")
    files.append(f"{folder_name}/exercises.py")


# 3) Création des fichiers
for fi in files:
    file = base / fi

    if file.exists():
        print(f"⏭️  Fichier déjà existant : {file}")

    elif fi == ".gitignore":
        file.write_text(
            """# Virtual environments
venv/
.venv/
env/

# Python cache
__pycache__/
*.py[cod]
*$py.class

# Jupyter
.ipynb_checkpoints/

# Environment variables
.env

# IDE
.vscode/
.idea/

# Operating system files
.DS_Store
Thumbs.db

# Python build files
build/
dist/
*.egg-info/

# Test files
.pytest_cache/
.coverage
htmlcov/
""",
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi == "README.md":
        file.write_text(
            """# 30 Days of Python

This repository contains my personal learning notes, exercises and Python
practice based on the **30 Days of Python** challenge.

## Objective

The challenge is a progressive path to learn Python through practical
examples and exercises.

It is structured in 30 days, but I will follow it at my own pace.

## Source

Original repository:

https://github.com/Asabeneh/30-Days-Of-Python

## Main structure

```text
01_Day_Introduction/
02_Day_Variables_builtin_functions/
03_Day_Operators/
...
30_Day_Conclusions/
```

## Author

Abdeldjalil Benaïfa
""",
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi == "mymodule.py":
        file.write_text(
            '''# -*- coding: utf-8 -*-
"""
Personal Python module for the 30 Days of Python challenge.
"""


def generate_full_name(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}"


def sum_two_numbers(number_one: float, number_two: float) -> float:
    return number_one + number_two
''',
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi == "numpy.md":
        file.write_text(
            """# NumPy Notes

Personal notes and exercises about NumPy.

## Installation

```powershell
python -m pip install numpy
```

## Import

```python
import numpy as np
```
""",
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi == ".github/FUNDING.yml":
        file.write_text(
            """# GitHub Sponsors configuration
# github: []
# patreon: []
# ko_fi: []
""",
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi.endswith("/README.md") and any(
        language in fi
        for language in [
            "French/",
            "Chinese/",
            "German/",
            "Greek/",
            "Korean/",
            "Persain/",
            "Portuguese/",
            "Spanish/",
            "Ukrainian/",
            "Uzbek/",
            "korean/",
        ]
    ):
        language = fi.split("/")[0]

        file.write_text(
            f"""# 30 Days of Python — {language}

This folder is reserved for notes, translations or exercises in {language}.
""",
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi.endswith("/README.md"):
        folder_name = file.parent.name
        day_number = folder_name[:2]
        topic = folder_name[7:].replace("_", " ")

        file.write_text(
            f"""# Day {day_number} — {topic}

## Objectives

- Understand the concepts of this lesson
- Reproduce the examples
- Complete the exercises
- Write personal notes and corrections

## Files

- `main.py`: examples and personal practice
- `exercises.py`: exercise solutions
- `README.md`: lesson notes and objectives

## Checklist

- [ ] Read the lesson
- [ ] Run the examples
- [ ] Complete exercises
- [ ] Commit progress to Git
""",
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi.endswith("/main.py"):
        folder_name = file.parent.name
        day_number = folder_name[:2]
        topic = folder_name[7:].replace("_", " ")

        file.write_text(
            f'''# -*- coding: utf-8 -*-
"""
Day {day_number} — {topic}
30 Days of Python challenge
"""


print("Day {day_number} — {topic}")
''',
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    elif fi.endswith("/exercises.py"):
        folder_name = file.parent.name
        day_number = folder_name[:2]

        file.write_text(
            f'''# -*- coding: utf-8 -*-
"""
Exercises — Day {day_number}
"""


# Write your exercise solutions below.
''',
            encoding="utf-8",
        )

        print(f"✅ Fichier créé : {file.resolve()}")

    else:
        file.write_text("", encoding="utf-8")
        print(f"✅ Fichier créé : {file.resolve()}")


print("\n🎉 Structure principale créée avec succès.")
print(f"📂 Chemin du projet : {base.resolve()}")