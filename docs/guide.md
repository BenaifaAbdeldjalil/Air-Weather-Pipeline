\# Plan complet du projet : de la Phase 0 à la Phase 10



Le plan est adapté à votre sujet (météo et qualité de l'air, 8 villes, 12 mois, grain horaire). Il ne contient aucun code : il fixe le chemin, et chaque phase sera détaillée au format TP complet (indices 1/2/3, critères, diagnostic) quand nous y arriverons.



\## Vue d'ensemble



| Phase | Thème | Durée estimée | Livrable principal |

|---|---|---|---|

| 0 | Cadrage et conception | 3 à 4 h | 3 fichiers `docs/` |

| 1 | Poste, dépôt, GitHub | 2 h | Premier push propre |

| 2 | PostgreSQL et modélisation | 3 à 4 h | DDL dans `sql/ddl/` |

| 3 | Extraction API | 4 à 5 h | Module d'extraction + test mock |

| 4 | Ingestion CSV / Excel | 3 à 4 h | Lecteurs + rapport qualité |

| 5 | Transformation Pandas | 5 à 6 h | Transformations + tests unitaires |

| 6 | Chargement PostgreSQL | 4 à 5 h | Tables `raw` et `staging` + log d'exécution |

| 7 | Orchestration Python | 2 à 3 h | `main.py` en une commande |

| 8 | dbt | 6 à 8 h | Modèles, tests, docs dbt |

| 9 | Documentation et qualité | 3 h | README complet |

| 10 | Démo et roadmap | 2 h | Démo de 5 à 10 min |



Total : environ 37 à 50 h, soit 6 à 8 semaines à raison de quelques soirées par semaine.



\## Cible finale du projet



\*\*Schémas PostgreSQL\*\*

\- `raw` : `weather\_hourly\_raw`, `air\_quality\_hourly\_raw`, `communes\_ref\_raw`, `population\_ref\_raw`

\- `staging` : `city`, `weather\_observation`, `air\_quality\_observation`, `rejected\_rows`

\- `ops` : `pipeline\_run\_log`

\- `analytics` (via dbt) : `mart\_daily\_city\_environment`, `mart\_monthly\_air\_quality\_kpi`, éventuellement `mart\_pollution\_episodes`



Ces noms sont indicatifs. Vous les confirmerez en Phase 0 et 2.



\## Phase 0 : Cadrage et conception



\- \*\*Objectifs\*\* : besoin métier, sources testées, entités et clés, règles de qualité, indicateurs, décisions.

\- \*\*Notions\*\* : grain, clé métier vs technique, fait vs dimension, dimensions de la qualité de données.

\- \*\*Fichiers\*\* : `docs/architecture.md`, `docs/data\_dictionary.md`, `docs/decisions.md`.

\- \*\*Validation\*\* : chaque entité a un grain et une clé, au moins 8 règles `DQ-xx` mesurables, au moins 4 indicateurs.

\- \*\*Erreur fréquente\*\* : grain flou, fuseau horaire ignoré.

\- \*\*Commit\*\* : `docs: add project scoping, data dictionary and quality rules`



\## Phase 1 : Poste et dépôt



\- \*\*Objectifs\*\* : projet local reproductible, Git et GitHub propres, aucun secret versionné.

\- \*\*Notions\*\* : `venv`, `pip freeze` vs `requirements.txt`, séparation prod/dev, `.gitignore`, `.env` vs `.env.example`, Conventional Commits.

\- \*\*Fichiers\*\* : `.gitignore`, `.env.example`, `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, `README.md` (v0), arborescence `src/` et `tests/` avec des `\_\_init\_\_.py` vides.

\- \*\*Commandes\*\* : `python -m venv .venv`, activation, `pip install`, `git init`, `git remote add`, `git push`.

\- \*\*Exercices\*\* : décider quoi ignorer (`.env`, `.venv/`, `data/raw/`, `logs/`, `target/` de dbt) et justifier chaque ligne.

\- \*\*Validation\*\* : `git status` ne montre aucun secret, le dépôt se clone et s'installe sur un autre dossier.

\- \*\*Erreur fréquente\*\* : commiter `.env` puis le supprimer (il reste dans l'historique).

\- \*\*Commits\*\* : `chore: initialize repository structure`, `docs: add initial README`



\## Phase 2 : PostgreSQL et modélisation



\- \*\*Objectifs\*\* : base, schémas, tables, contraintes, journalisation.

\- \*\*Notions\*\* : `CREATE SCHEMA`, types (`timestamptz` vs `timestamp`, `numeric`, `text`), clés primaires composites, `CHECK`, `NOT NULL`, index, rôles et droits, DDL idempotent (`IF NOT EXISTS`).

\- \*\*Fichiers\*\* : `sql/ddl/001\_create\_schemas.sql`, `002\_create\_raw\_tables.sql`, `003\_create\_staging\_tables.sql`, `004\_create\_ops\_tables.sql`, `src/config.py` (v0), `src/utils/db.py`.

\- \*\*Exercices\*\* : concevoir les tables à partir de votre dictionnaire, créer `pipeline\_run\_log`, ouvrir une connexion avec SQLAlchemy et exécuter `SELECT 1`.

\- \*\*Validation\*\* : les scripts DDL se rejouent sans erreur, la connexion Python fonctionne via variables d'environnement.

\- \*\*Erreur fréquente\*\* : mot de passe en dur, mauvais choix entre `timestamp` et `timestamptz`.

\- \*\*Commit\*\* : `feat(db): add schemas and DDL scripts`



\## Phase 3 : Extraction API



\- \*\*Objectifs\*\* : appeler Open-Meteo (météo et air) de façon robuste.

\- \*\*Notions\*\* : HTTP (méthodes, statuts, paramètres), JSON, `requests`, `timeout`, `raise\_for\_status`, `try/except` ciblés, retry avec backoff simple, `logging`, `pathlib`, type hints, mock avec `pytest` (`unittest.mock` ou `monkeypatch`).

\- \*\*Fichiers\*\* : `src/extract/api\_client.py`, `src/utils/logging\_config.py`, `tests/test\_extract/test\_api\_client.py`.

\- \*\*Exercices\*\* : une fonction par API, gestion de timeout, d'erreur HTTP, de JSON invalide et de réponse vide, retry, sauvegarde d'un échantillon brut dans `data/raw/`, un test avec requête HTTP simulée.

\- \*\*Validation\*\* : le module fonctionne pour 8 villes, un échec simulé produit un log clair et non un crash obscur, le test passe sans accès réseau.

\- \*\*Erreur fréquente\*\* : oublier le `timeout` (le programme peut bloquer indéfiniment), capturer `Exception` partout.

\- \*\*Commit\*\* : `feat(extract): add weather and air quality API client`



\## Phase 4 : Ingestion CSV et Excel



\- \*\*Objectifs\*\* : lire le référentiel des communes (CSV) et les populations (Excel), diagnostiquer leur qualité.

\- \*\*Notions\*\* : `pd.read\_csv` (séparateur, encodage, `dtype`), `pd.read\_excel` (feuille, lignes d'en-tête à sauter, `openpyxl`), codes INSEE à lire en texte (zéros initiaux, Corse 2A/2B), `df.info()`, `isna()`, `duplicated()`, normalisation des noms de colonnes.

\- \*\*Fichiers\*\* : `src/extract/file\_readers.py`, `src/quality/profiling.py`, `tests/test\_extract/test\_file\_readers.py`.

\- \*\*Exercices\*\* : une fonction de lecture par type de fichier, un rapport de qualité (lignes, nulls par colonne, doublons) par source.

\- \*\*Validation\*\* : les codes INSEE conservent leurs zéros, les noms de colonnes sont standardisés en `snake\_case`.

\- \*\*Erreur fréquente\*\* : lecture automatique du code INSEE en entier (`01001` devient `1001`).

\- \*\*Commit\*\* : `feat(extract): add csv and excel readers with profiling`



\## Phase 5 : Transformation avec Pandas



\- \*\*Objectifs\*\* : passer du brut à des données propres, jointes et validées.

\- \*\*Notions\*\* : JSON en listes parallèles vers DataFrame, `pd.DataFrame` à partir de dictionnaires, `to\_datetime` et fuseaux, `str.strip/lower`, `merge` (types de jointure, `validate=`), `drop\_duplicates`, masques booléens, séparation valides/rejets, fonctions pures testables.

\- \*\*Fichiers\*\* : `src/transform/weather.py`, `air\_quality.py`, `cities.py`, `src/quality/rules.py`, `tests/test\_transform/`.

\- \*\*Exercices\*\* : transformer chaque réponse API en table longue, appliquer vos règles `DQ-xx`, produire deux DataFrames (valides, rejetés avec motif), jointure avec le référentiel, au moins 3 tests unitaires de règles.

\- \*\*Validation\*\* : valides + rejetés = lignes d'entrée, aucune ligne perdue silencieusement, les tests passent.

\- \*\*Erreur fréquente\*\* : jointure qui multiplie les lignes (clé non unique), `SettingWithCopyWarning` ignoré.

\- \*\*Commit\*\* : `feat(transform): add cleaning, validation and rejection logic`



\## Phase 6 : Chargement PostgreSQL



\- \*\*Objectifs\*\* : alimenter `raw` et `staging` de façon rejouable, tracer chaque exécution.

\- \*\*Notions\*\* : SQLAlchemy `engine` et `Connection`, transactions (`begin`, commit, rollback), context managers, `DataFrame.to\_sql` et ses limites, `TRUNCATE` puis rechargement, puis `INSERT ... ON CONFLICT DO UPDATE` (upsert), requêtes de vérification.

\- \*\*Fichiers\*\* : `src/load/postgres\_loader.py`, `src/load/run\_log.py`, `tests/test\_load/`, `sql/queries/checks.sql`.

\- \*\*Exercices\*\* : charger `raw` tel quel, charger `staging` après validation, écrire une ligne dans `pipeline\_run\_log` (début, source, extraites, valides, rejets, statut, erreur), rejouer deux fois et prouver l'idempotence, provoquer une erreur et vérifier le rollback.

\- \*\*Validation\*\* : deux exécutions successives donnent le même nombre de lignes, les comptages SQL concordent avec les logs.

\- \*\*Erreur fréquente\*\* : `to\_sql(if\_exists="append")` qui duplique à chaque exécution.

\- \*\*Commit\*\* : `feat(load): add idempotent postgres loading and run logging`



\## Phase 7 : Orchestration Python



\- \*\*Objectifs\*\* : tout lancer avec une seule commande.

\- \*\*Notions\*\* : point d'entrée `if \_\_name\_\_ == "\_\_main\_\_"`, `argparse` (optionnel), codes de sortie (`sys.exit`), exceptions personnalisées, configuration centralisée (dataclass), logs vers fichier avec rotation simple.

\- \*\*Fichiers\*\* : `src/main.py`, `src/config.py` (v1).

\- \*\*Exercices\*\* : enchaîner extraction, transformation, contrôles, chargement ; capturer les erreurs globales ; retourner 0 en succès et non-zéro en échec.

\- \*\*Validation\*\* : `python -m src.main` fonctionne de bout en bout depuis un dépôt fraîchement cloné, un échec renvoie un code non nul et une ligne `FAILED` dans le log d'exécution.

\- \*\*Erreur fréquente\*\* : `except Exception: pass` qui masque les erreurs, imports relatifs cassés.

\- \*\*Commit\*\* : `feat: add pipeline entrypoint with error handling and logging`



\## Phase 8 : dbt



\- \*\*Objectifs\*\* : refaire la transformation en SQL ELT et comparer à Pandas.

\- \*\*Notions\*\* : Python ETL vs SQL ELT, `source()` vs `ref()`, materializations (view, table), couches staging / intermediate / marts, `profiles.yml` et variables d'environnement (`env\_var`), tests génériques, documentation et lineage.

\- \*\*Fichiers\*\* : `dbt\_project/dbt\_project.yml`, `models/staging/\_sources.yml`, `stg\_\*.sql`, `models/intermediate/int\_hourly\_city\_environment.sql`, `models/marts/mart\_\*.sql`, `\_models.yml` (tests et descriptions). `profiles.yml` reste \*\*hors dépôt\*\*.

\- \*\*Commandes\*\* : `dbt debug`, `dbt run`, `dbt test`, `dbt docs generate`, `dbt docs serve`. Chacune sera expliquée en détail (ce qu'elle vérifie, ce qu'elle crée, comment lire le résultat).

\- \*\*Exercices\*\* : déclarer les sources, 3 à 4 modèles staging, 1 modèle intermediate, 2 marts minimum, tests `not\_null`, `unique`, `relationships`, `accepted\_values`, un test volontairement cassé pour observer l'échec.

\- \*\*Validation\*\* : `dbt run` et `dbt test` passent, le lineage est lisible dans les docs, les marts correspondent à vos indicateurs de la Phase 0.

\- \*\*Erreur fréquente\*\* : `profiles.yml` commité avec le mot de passe, confusion entre schéma source et schéma cible.

\- \*\*Commit\*\* : `feat(dbt): add staging, intermediate and mart models with tests`



\## Phase 9 : Documentation et qualité



\- \*\*Objectifs\*\* : rendre le projet compréhensible et reproductible par un tiers.

\- \*\*Contenu\*\* : README (contexte, architecture, installation, exécution, dépannage, qualité de données, décisions et compromis, hypothèses et limites), `data\_dictionary.md` mis à jour, passage final de `pytest` et `dbt test`.

\- \*\*Validation\*\* : une personne extérieure peut installer et exécuter à partir du README seul.

\- \*\*Commit\*\* : `docs: complete README, architecture and troubleshooting guide`



\## Phase 10 : Démo et améliorations



\- \*\*Objectifs\*\* : présenter le projet, définir la suite.

\- \*\*Contenu\*\* : scénario de démonstration de 5 à 10 min (extraction, rejets, chargement, dbt, mart, requête d'analyse), 5 à 8 requêtes SQL d'analyse, roadmap priorisée (CI GitHub Actions, tests de données avancés, ingestion incrémentale, Docker, Prefect ou Airflow, Parquet, cloud, Metabase ou Power BI).

\- \*\*Commit\*\* : `docs: add demo script and improvement roadmap`



\## Règles de travail pour toute la suite



\- Chaque phase suit le format en 11 points, avec indices 1/2/3.

\- Vous m'envoyez votre code, vos erreurs ou vos résultats, et je corrige localement sans réécrire l'ensemble.

\- Aucun script final complet avant que vous ayez essayé.

\- Un commit Conventional Commit par étape significative.



\## Prochaine étape



Nous sommes toujours en \*\*Phase 0\*\*. Ce plan est la feuille de route, pas le cadrage lui-même : les exercices 1 à 8 de ma réponse précédente restent à produire par vous, car c'est ce qui vous fait réfléchir à votre propre conception.



Pour avancer, envoyez-moi votre premier jet, même incomplet, de l'exercice 1 (besoin métier et questions analytiques) et de l'exercice 2 (tableau des sources). Si vous préférez commencer plus petit, répondez d'abord à la question de contrôle : \*\*quelle est la clé d'unicité d'une ligne de `weather\_observation`, et pourquoi `city\_id` seul ne suffit-il pas ?\*\*



\# Phase 1 : Initialisation du poste et du dépôt



Avant d'avancer, un point sur la Phase 0. Je ne peux pas la valider sans votre travail, et la Phase 2 (création des tables) en dépend directement : dictionnaire de données, clés, règles de qualité. Je vous propose donc de \*\*mener la Phase 1 maintenant\*\* (elle est indépendante) et de \*\*compléter les docs de la Phase 0 en parallèle\*\*, puis de me les envoyer avant d'attaquer la Phase 2.



\## 1. Phase et objectif



\*\*Phase 1 sur 10.\*\* À la fin, vous aurez :



\- un projet local avec environnement virtuel ;

\- une arborescence propre ;

\- un dépôt Git relié à GitHub ;

\- aucun secret versionné ;

\- un premier push avec des commits explicites.



\## 2. Contexte



Un pipeline qui ne s'installe que sur votre machine n'est pas un projet professionnel. Cette phase pose trois garanties :



\- \*\*Reproductibilité\*\* : un tiers clone le dépôt, installe les dépendances et obtient le même environnement.

\- \*\*Sécurité\*\* : un mot de passe poussé sur GitHub doit être considéré comme compromis, même si vous le supprimez ensuite (il reste dans l'historique).

\- \*\*Traçabilité\*\* : un historique de commits lisible permet de comprendre l'évolution du projet.



\## 3. Notions à comprendre



\- \*\*Environnement virtuel (`venv`)\*\* : un dossier qui isole les paquets Python du projet de ceux du système. Sans lui, deux projets aux versions de `pandas` différentes se cassent mutuellement.

\- \*\*`requirements.txt` vs `requirements-dev.txt`\*\* : le premier liste ce qui est nécessaire pour exécuter le pipeline, le second ce qui sert au développement (tests, linter). Le second peut inclure le premier avec `-r requirements.txt`.

\- \*\*Épingler les versions\*\* : `pandas==2.2.3` (reproductible) contre `pandas` (imprévisible). Un compromis courant est `pandas>=2.2,<3`.

\- \*\*`.gitignore`\*\* : liste de motifs que Git ne suivra jamais. Il n'agit \*\*pas\*\* sur ce qui est déjà suivi.

\- \*\*`.env` vs `.env.example`\*\* : `.env` contient les vrais secrets (ignoré). `.env.example` contient les mêmes clés avec des valeurs factices (versionné), pour documenter la configuration attendue.

\- \*\*Zones de Git\*\* : répertoire de travail → index (`git add`) → historique (`git commit`) → dépôt distant (`git push`).

\- \*\*Conventional Commits\*\* : format `type(scope): description`, avec les types `feat`, `fix`, `docs`, `chore`, `test`, `refactor`.

\- \*\*`\_\_init\_\_.py`\*\* : marque un dossier comme package Python importable.



\## 4. Travail à réaliser par vous



\*\*Exercice 1 : Dossier et environnement virtuel.\*\* Dans `air-weather-pipeline/` (créé en Phase 0), créez l'environnement virtuel `.venv` et activez-le. Vérifiez avec `which python` (Linux/macOS) ou `where python` (Windows) que l'interpréteur pointe bien dans `.venv`.



\*\*Exercice 2 : Arborescence.\*\* Créez les dossiers et fichiers de l'architecture cible, \*\*sans dbt pour l'instant\*\* :



```

data/{raw,external,processed}  logs/  sql/{ddl,queries}

src/{extract,transform,load,quality,utils}  tests/{test\_extract,test\_transform,test\_load}

```



Ajoutez un `\_\_init\_\_.py` vide dans `src/` et chacun de ses sous-dossiers, ainsi que dans `tests/` et ses sous-dossiers. Git ne suit pas les dossiers vides : ajoutez un fichier `.gitkeep` dans `data/raw/`, `data/external/`, `data/processed/` et `logs/`.



\*\*Exercice 3 : Dépendances.\*\* Rédigez :



\- `requirements.txt` avec : `requests`, `pandas`, `openpyxl`, `SQLAlchemy`, `psycopg` (avec l'extra `binary`), `python-dotenv`.

\- `requirements-dev.txt` avec : `-r requirements.txt` et `pytest`.

\- \*\*Ne mettez pas `dbt-postgres` maintenant.\*\* Il impose ses propres versions de dépendances et peut entrer en conflit. Nous l'ajouterons en Phase 8, dans de bonnes conditions.



Installez, puis exécutez `pip list` et comparez avec votre fichier.



\*\*Exercice 4 : `.gitignore`.\*\* Écrivez-le vous-même. Pour chaque ligne, rédigez en commentaire \*\*pourquoi\*\* elle est là. Catégories à couvrir :



\- environnement virtuel ;

\- fichiers de secrets ;

\- caches Python et pytest ;

\- données brutes volumineuses ou potentiellement sous licence (mais \*\*pas\*\* les `.gitkeep`) ;

\- logs ;

\- artefacts dbt (futur) ;

\- fichiers d'éditeur ou d'OS.



\*\*Exercice 5 : `.env.example`.\*\* Listez les variables dont vous aurez besoin pour PostgreSQL (hôte, port, nom de base, utilisateur, mot de passe) avec des \*\*valeurs factices\*\*. Format attendu :



```

CLE=valeur\_factice

```



Créez ensuite votre vrai `.env` en le copiant, et vérifiez qu'il est bien ignoré.



\*\*Exercice 6 : `pyproject.toml` minimal.\*\* Il décrit le projet (nom, version, version de Python requise). Squelette :



```toml

\[project]

name = "air-weather-pipeline"

version = "0.1.0"

requires-python = ">=3.10"   # TODO: adapter à votre version de Python



\[tool.pytest.ini\_options]

\# TODO: indiquer à pytest où se trouvent les tests (clé "testpaths")

\# TODO: indiquer le dossier à ajouter au chemin d'import (clé "pythonpath")

```



\*\*Exercice 7 : README v0.\*\* Titre, description en 3 lignes, stack technique, et une section « Installation » à compléter plus tard. Pas plus : le vrai README arrive en Phase 9.



\*\*Exercice 8 : Git et GitHub.\*\*



1\. Initialisez le dépôt local.

2\. Créez le dépôt sur GitHub (vide : sans README ni `.gitignore` générés, pour éviter un conflit d'historiques).

3\. Reliez-le, puis poussez.

4\. Faites \*\*deux commits distincts\*\* (voir section 10).



\## 5. Fichiers concernés



`.gitignore`, `.env.example`, `.env` (local, jamais versionné), `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, `README.md`, les `\_\_init\_\_.py` et les `.gitkeep`. Vos trois fichiers `docs/` de la Phase 0 restent dans le dépôt.



\## 6. Commandes à exécuter



```bash

\# Environnement virtuel (crée le dossier .venv)

python3 -m venv .venv



\# Activation : Linux / macOS

source .venv/bin/activate

\# Activation : Windows PowerShell

\# .venv\\Scripts\\Activate.ps1



python --version

pip install --upgrade pip

pip install -r requirements-dev.txt

pip list



\# Arborescence : l'option -p crée les dossiers parents, les accolades génèrent plusieurs dossiers (bash)

mkdir -p data/{raw,external,processed} logs sql/{ddl,queries}

mkdir -p src/{extract,transform,load,quality,utils} tests/{test\_extract,test\_transform,test\_load}

touch src/\_\_init\_\_.py tests/\_\_init\_\_.py   # TODO: répéter pour chaque sous-dossier

touch data/raw/.gitkeep                   # TODO: répéter pour les autres



\# Git

git init

git branch -M main

git status

git add <fichiers>          # TODO: ajouter explicitement, éviter "git add ." tant que .gitignore n'est pas validé

git commit -m "<message>"

git remote add origin <URL\_DE\_VOTRE\_DEPOT>

git push -u origin main

git log --oneline

```



Notes de syntaxe :



\- `git add .` ajoute \*\*tout\*\* : c'est précisément ce qui fait fuiter un `.env` quand `.gitignore` est incomplet.

\- `git push -u origin main` pousse la branche `main` vers le dépôt distant nommé `origin` et mémorise le lien (`-u`), si bien que `git push` seul suffira ensuite.

\- `git status --ignored` affiche ce que Git ignore, très utile pour vérifier votre `.gitignore`.



\## 7. Indices progressifs



\*\*`.gitignore`\*\*



\- \*Indice 1\* : un motif `dossier/` ignore un dossier entier, `\*.ext` ignore une extension.

\- \*Indice 2\* : pour garder un `.gitkeep` dans un dossier dont le contenu est ignoré, il existe une règle de négation : une ligne qui commence par `!`. Attention à l'ordre : ignorer le contenu d'abord (`dossier/\*`), puis exclure l'exception.

\- \*Indice 3\* : testez avec `git status --ignored` et `git check-ignore -v <fichier>`. La seconde commande vous dit quelle règle ignore un fichier donné.



\*\*`pyproject.toml` (pytest)\*\*



\- \*Indice 1\* : les deux clés attendues acceptent une liste de chaînes.

\- \*Indice 2\* : si vos tests importent `src.extract...`, le dossier racine du projet doit être dans le chemin d'import. Quelle valeur représente « le dossier courant » ?



\*\*Reliaison au dépôt distant\*\*



\- \*Indice 1\* : `git remote -v` affiche les remotes configurés.

\- \*Indice 2\* : si GitHub vous demande un mot de passe, il attend en réalité un \*personal access token\* (ou une clé SSH). Les mots de passe de compte ne fonctionnent plus pour Git en HTTPS.



\*\*Dépendances\*\*



\- \*Indice 1\* : l'extra de `psycopg` s'écrit avec des crochets : `paquet\[extra]`.



\## 8. Critères de validation



\- `python -c "import pandas, requests, sqlalchemy, dotenv, openpyxl"` s'exécute sans erreur dans le venv activé.

\- `pytest` s'exécute et indique `no tests ran` (c'est normal et attendu : pas encore de tests).

\- `git status` est propre à la fin.

\- `git ls-files` ne liste \*\*ni\*\* `.env`, \*\*ni\*\* `.venv/`.

\- `git ls-files` liste bien `.env.example`.

\- Le dépôt GitHub affiche vos fichiers et au moins deux commits.

\- \*\*Test du clone\*\* : dans un autre dossier, `git clone`, création d'un nouveau venv, `pip install -r requirements-dev.txt` : tout fonctionne sans votre `.env`.



\## 9. Erreurs fréquentes et diagnostic



\- \*\*`.env` commité puis supprimé\*\* : il reste dans l'historique. Symptôme : `git log --all -- .env` affiche des commits. Si cela arrive, changez immédiatement le secret concerné. Retirer le fichier de l'historique est possible mais délicat ; nous le verrons si besoin.

\- \*\*`(.venv)` absent de l'invite\*\* : le venv n'est pas activé, et `pip install` installe dans le système. Symptôme : `ModuleNotFoundError` plus tard.

\- \*\*`.gitignore` sans effet sur un fichier déjà suivi\*\* : il faut d'abord le retirer de l'index avec `git rm --cached <fichier>`.

\- \*\*Dossiers vides absents du dépôt\*\* : normal, d'où les `.gitkeep`.

\- \*\*`git push` rejeté (`non-fast-forward`)\*\* : le dépôt GitHub contient déjà un commit (README généré). Évitez-le en créant un dépôt vide.

\- \*\*`pip freeze > requirements.txt`\*\* : fige aussi les dépendances transitives (des dizaines de lignes). Pour ce projet, un fichier écrit à la main avec les dépendances directes est plus lisible.

\- \*\*Mélange de commits\*\* : un seul commit « initial commit » contenant tout est une mauvaise pratique. Séparez structure et documentation.



\## 10. Livrable et commits Git attendus



Deux commits, dans cet ordre :



```

chore: initialize repository structure and dependencies

docs: add initial README and project scoping documents

```



Le premier contient `.gitignore`, `.env.example`, `requirements\*.txt`, `pyproject.toml`, l'arborescence. Le second contient `README.md` et `docs/`. Les deux sont poussés sur `origin/main`.



\## 11. Question de contrôle et ce que vous devez me transmettre



Envoyez-moi (copier-coller) :



1\. Votre \*\*`.gitignore`\*\* avec vos commentaires.

2\. La sortie de `git ls-files` et celle de `git log --oneline`.

3\. Votre \*\*`requirements.txt`\*\* et \*\*`requirements-dev.txt`\*\*.

4\. Le résultat de votre test du clone (réussi, ou le message d'erreur exact).



\*\*Question de contrôle\*\* : vous avez par erreur poussé un `.env` contenant un mot de passe PostgreSQL. Vous le supprimez dans un nouveau commit et poussez. Pourquoi le mot de passe est-il toujours exposé, et quelle est la toute première action à faire ?



Une fois vos retours reçus et vos fichiers `docs/` de la Phase 0 complétés, nous passerons à la \*\*Phase 2 (PostgreSQL et modélisation)\*\*. Je ne détaille pas les phases suivantes en TP complet à l'avance : chacune dépend de ce que vous aurez produit.





\# Phase 2 : PostgreSQL et modélisation



Cette phase dépend de vos livrables précédents.



\- \*\*Phase 1\*\* : les exercices de connexion et de dépôt en ont besoin (venv, `.env` ignoré, `requirements.txt`).

\- \*\*Phase 0\*\* : la conception des tables (exercice 4) s'appuie sur votre dictionnaire de données et vos règles de qualité. Si vous ne les avez pas terminés, partez de la structure réelle des réponses JSON d'Open-Meteo, que vous inspecterez vous-même. Je relirai votre modélisation et vous signalerai les trous.



\## 1. Phase et objectif



\*\*Phase 2 sur 10.\*\* À la fin, vous aurez :



\- une base PostgreSQL locale ;

\- quatre schémas (`raw`, `staging`, `analytics`, `ops`) ;

\- les tables de destination avec types, clés et contraintes ;

\- une table de journalisation des exécutions ;

\- des scripts DDL rejouables dans `sql/ddl/` ;

\- une connexion Python fonctionnelle, sans mot de passe en dur.



\## 2. Contexte



Dans un pipeline réel, la base est le contrat entre toutes les étapes :



\- Si le schéma est laxiste, les erreurs de qualité passent silencieusement jusqu'aux analyses.

\- Si le schéma est trop strict dès la couche brute, la moindre anomalie de la source fait échouer tout le chargement.



D'où la séparation en couches :



\- \*\*`raw`\*\* : tolérante. Elle conserve ce que la source a envoyé, avec peu de contraintes.

\- \*\*`staging`\*\* : stricte. Les données y sont typées, dédupliquées et contrôlées.

\- \*\*`analytics`\*\* : alimentée plus tard par dbt.

\- \*\*`ops`\*\* : contient les métadonnées du pipeline lui-même (journal d'exécution).



\## 3. Notions à comprendre



\- \*\*Base, schéma, table\*\* : une base contient des schémas (espaces de noms), qui contiennent des tables. On référence `schema.table`.

\- \*\*`timestamp` vs `timestamptz`\*\* : `timestamptz` stocke un instant absolu (converti en UTC en interne). `timestamp` stocke une date-heure sans fuseau, donc ambiguë. Pour des mesures horaires, la question est « quel instant exactement ? », ce qui pèse dans votre choix.

\- \*\*`numeric(p,s)` vs `double precision`\*\* : `numeric` est exact, `double precision` est flottant et plus rapide. Pour des mesures physiques, réfléchissez à la précision réellement nécessaire.

\- \*\*`text` vs `varchar(n)`\*\* : en PostgreSQL, il n'y a pas de gain de performance à limiter la longueur. Une contrainte `CHECK` exprime mieux une règle métier.

\- \*\*Clé primaire (simple, composite)\*\* : unicité et `NOT NULL` garantis. Une clé composite crée automatiquement un index sur les colonnes \*\*dans l'ordre déclaré\*\*.

\- \*\*Clé technique (`GENERATED ... AS IDENTITY`) vs clé métier\*\* : discutez le choix pour `city` en vous appuyant sur la Phase 0.

\- \*\*`CHECK`\*\* : contrainte sur les valeurs. \*\*Piège : un `CHECK` laisse passer `NULL`\*\* (le résultat est « inconnu », pas « faux »). Pour interdire les nuls, il faut `NOT NULL` en plus.

\- \*\*`FOREIGN KEY`\*\* : garantit l'existence de la ligne référencée. Elle a un coût au chargement.

\- \*\*Index\*\* : accélère les lectures, ralentit les écritures. La clé primaire en crée déjà un.

\- \*\*DDL idempotent\*\* : `CREATE SCHEMA IF NOT EXISTS`, `CREATE TABLE IF NOT EXISTS`. Le script se rejoue sans erreur.

\- \*\*Rôles et droits\*\* : un utilisateur dédié au pipeline (`LOGIN`, propriétaire de la base) évite de travailler en superutilisateur.

\- \*\*Colonnes de métadonnées d'ingestion\*\* : par exemple `ingested\_at` et `run\_id`. Elles permettent de savoir quand et par quelle exécution une ligne est arrivée.



Syntaxe illustrée sur une \*\*table fictive\*\* (sans rapport avec votre projet) :



```sql

CREATE SCHEMA IF NOT EXISTS demo;



CREATE TABLE IF NOT EXISTS demo.product (

&#x20;   product\_id   integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

&#x20;   sku          text NOT NULL UNIQUE,

&#x20;   price        numeric(10,2) CHECK (price >= 0),

&#x20;   created\_at   timestamptz NOT NULL DEFAULT now()

);



CREATE INDEX IF NOT EXISTS idx\_product\_created\_at ON demo.product (created\_at);

```



\- `GENERATED ALWAYS AS IDENTITY` : entier auto-incrémenté géré par PostgreSQL.

\- `UNIQUE` : unicité sans en faire la clé primaire.

\- `DEFAULT now()` : valeur par défaut calculée à l'insertion.

\- `numeric(10,2)` : jusqu'à 10 chiffres au total, dont 2 après la virgule.



\## 4. Travail à réaliser par vous



\*\*Exercice 1 : Installer et se connecter.\*\* Installez PostgreSQL 15 ou plus récent (paquet système, installateur officiel, ou gestionnaire de paquets de votre OS). Vérifiez que le serveur écoute (port 5432 par défaut) et ouvrez `psql`.



\*\*Exercice 2 : Base et rôle dédié.\*\* En superutilisateur, créez :



\- un rôle `pipeline\_user` avec mot de passe et droit de connexion ;

\- une base `air\_weather` dont il est propriétaire.



Mettez à jour votre `.env` local, et vérifiez que `.env.example` reste factice.



\*\*Exercice 3 : Schémas.\*\* Écrivez `sql/ddl/001\_create\_schemas.sql` créant `raw`, `staging`, `analytics`, `ops`. Rejouez-le deux fois pour vérifier qu'il ne produit aucune erreur.



\*\*Exercice 4 : Conception sur papier (avant d'écrire du SQL).\*\* Pour chacune des tables ci-dessous, produisez un tableau avec colonne, type, nullable, contrainte et justification du type :



| Schéma | Table | Rôle |

|---|---|---|

| `raw` | `weather\_hourly\_raw` | météo horaire telle que reçue |

| `raw` | `air\_quality\_hourly\_raw` | qualité de l'air horaire telle que reçue |

| `raw` | `communes\_ref\_raw` | référentiel communes (CSV) |

| `raw` | `population\_ref\_raw` | populations (Excel) |

| `staging` | `city` | dimension ville |

| `staging` | `weather\_observation` | météo nettoyée |

| `staging` | `air\_quality\_observation` | qualité de l'air nettoyée |

| `staging` | `rejected\_rows` | lignes rejetées avec motif |

| `ops` | `pipeline\_run\_log` | journal des exécutions |



Questions à trancher et à justifier par écrit :



\- Quel est le choix de typage dans `raw` (strict ou tolérant) et pourquoi ?

\- Quelle clé primaire pour chaque table `staging` (composite pour les observations) ?

\- Quelles contraintes `CHECK` traduisent vos règles `DQ-xx` de la Phase 0 ?

\- `staging.city` : clé technique ou clé métier (code INSEE) ?

\- Quelles colonnes de métadonnées d'ingestion ajoutez-vous dans `raw` ?

\- `rejected\_rows` : comment stocker des lignes de structures différentes (une colonne de type `jsonb` pour la ligne d'origine ?) et le motif de rejet ?



\*\*Exercice 5 : Scripts DDL.\*\* Écrivez, à partir de votre conception :



\- `002\_create\_raw\_tables.sql`

\- `003\_create\_staging\_tables.sql`

\- `004\_create\_ops\_tables.sql`



Squelette de départ pour `004` (la liste des colonnes est volontairement à votre charge) :



```sql

CREATE TABLE IF NOT EXISTS ops.pipeline\_run\_log (

&#x20;   -- TODO: technical primary key

&#x20;   -- TODO: run identifier shared by all sources of the same execution

&#x20;   -- TODO: source name

&#x20;   -- TODO: start and end timestamps (with time zone)

&#x20;   -- TODO: rows extracted / valid rows / rejected rows

&#x20;   -- TODO: status, constrained to a small set of allowed values

&#x20;   -- TODO: error message (nullable)

);

```



Pour `staging`, ajoutez au moins un index utile en lecture (justifiez-le) et précisez si une clé étrangère vers `staging.city` est pertinente.



\*\*Exercice 6 : Test de rejouabilité.\*\* Exécutez les quatre scripts dans l'ordre, deux fois de suite, puis inspectez le résultat avec les méta-commandes `psql`. Ensuite, supprimez la base et recréez tout depuis zéro à partir des scripts seuls : c'est la preuve que le DDL est complet.



\*\*Exercice 7 : Connexion Python.\*\* Créez `src/config.py` (v0) et `src/utils/db.py` pour ouvrir une connexion SQLAlchemy et exécuter `SELECT 1`. Squelettes :



```python

\# src/config.py

import os

from dotenv import load\_dotenv



load\_dotenv()  # reads the .env file and injects its variables into the process environment



\# TODO: read DB\_HOST, DB\_PORT, DB\_NAME, DB\_USER, DB\_PASSWORD with os.getenv

\# TODO: fail early with a clear message if a mandatory variable is missing

```



```python

\# src/utils/db.py

from sqlalchemy import create\_engine, text

from sqlalchemy.engine import Engine, URL



def get\_engine() -> Engine:

&#x20;   # TODO: build a URL object with URL.create(...) using values from config

&#x20;   # TODO: return create\_engine(url)

&#x20;   ...



def check\_connection(engine: Engine) -> bool:

&#x20;   # TODO: open a connection with a context manager ("with engine.connect() as conn")

&#x20;   # TODO: execute text("SELECT 1") and return True if it works

&#x20;   ...

```



Syntaxe nouvelle :



\- `load\_dotenv()` lit le fichier `.env` et place ses variables dans `os.environ`.

\- `URL.create(...)` construit l'URL de connexion en échappant correctement les caractères spéciaux du mot de passe. Le nom du pilote est `postgresql+psycopg` pour psycopg 3.

\- `with engine.connect() as conn:` est un \*context manager\* : la connexion est fermée automatiquement à la sortie du bloc, même en cas d'erreur.

\- `text("...")` marque une chaîne comme requête SQL brute pour SQLAlchemy.

\- `-> Engine` est un \*type hint\* : indication de type pour la lisibilité, non contraignante à l'exécution.



Ajoutez ensuite un petit script ou une exécution `python -m src.utils.db` qui affiche le résultat de `check\_connection`.



\*\*Exercice 8 (bonus facultatif).\*\* Créez une table `ops.demo\_check` fictive pour tester le comportement d'un `CHECK` avec une valeur `NULL`, puis supprimez-la. Notez ce que vous observez.



\## 5. Fichiers concernés



\- `sql/ddl/001\_create\_schemas.sql`

\- `sql/ddl/002\_create\_raw\_tables.sql`

\- `sql/ddl/003\_create\_staging\_tables.sql`

\- `sql/ddl/004\_create\_ops\_tables.sql`

\- `src/config.py`

\- `src/utils/db.py`

\- `.env` (local, ignoré) et `.env.example` (versionné, factice)

\- `docs/data\_dictionary.md` (à mettre à jour avec les types finaux)

\- `docs/decisions.md` (ajoutez vos décisions de modélisation)



\## 6. Commandes à exécuter



```bash

\# Ouvrir psql en superutilisateur (adapter selon votre OS / installation)

psql -U postgres -h localhost



\# Dans psql : création du rôle et de la base (à compléter par vous)

\#   CREATE ROLE pipeline\_user WITH LOGIN PASSWORD '<mot\_de\_passe\_local>';

\#   CREATE DATABASE air\_weather OWNER pipeline\_user;

\#   \\q



\# Se connecter avec le rôle du projet

psql -U pipeline\_user -h localhost -d air\_weather



\# Exécuter un script SQL depuis le shell

psql -U pipeline\_user -h localhost -d air\_weather -f sql/ddl/001\_create\_schemas.sql



\# Méta-commandes psql utiles

\#   \\dn              liste les schémas

\#   \\dt raw.\*        liste les tables du schéma raw

\#   \\d staging.city  décrit une table (colonnes, types, contraintes, index)

\#   \\du              liste les rôles

\#   \\conninfo        affiche la connexion courante



\# Vérification Python

python -m src.utils.db

```



Notes :



\- Le mot de passe saisi dans `psql` n'est \*\*pas\*\* versionné, mais ne l'écrivez jamais dans un fichier du dépôt. Il vit uniquement dans votre `.env`.

\- `-h localhost` force une connexion réseau (TCP). Sans lui, PostgreSQL peut utiliser une socket locale, avec un mode d'authentification différent (`peer`).

\- `-f` exécute le contenu d'un fichier et affiche le résultat de chaque instruction.



\## 7. Indices progressifs



\*\*Exercice 4 (conception)\*\*



\- \*Indice 1\* : pour `raw`, posez-vous la question « que se passe-t-il si l'API renvoie une valeur inattendue (`null`, texte vide) ? ». Une colonne trop stricte ferait échouer tout le chargement brut.

\- \*Indice 2\* : la clé primaire d'une observation staging reprend le grain défini en Phase 0 : identifiant de ville plus champ temporel. Tapez-la à voix haute : « une ville, une heure ».

\- \*Indice 3\* : pour `rejected\_rows`, vous avez besoin d'au moins : la table source, un motif de rejet (idéalement le code `DQ-xx`), la ligne d'origine sous une forme flexible, la date de rejet et l'identifiant d'exécution.



\*\*Exercice 5 (DDL)\*\*



\- \*Indice 1\* : pour une clé composite, la contrainte s'écrit après les colonnes : `PRIMARY KEY (col\_a, col\_b)`.

\- \*Indice 2\* : pour limiter un statut à quelques valeurs, utilisez un `CHECK (status IN (...))`. Quelles valeurs minimales pour un journal ? (au moins : en cours, réussi, échoué)

\- \*Indice 3\* : pour ajouter une clé étrangère : `FOREIGN KEY (col) REFERENCES schema.table (col)`. Réfléchissez à l'ordre de création des tables, car la table référencée doit exister avant.



\*\*Exercice 7 (Python)\*\*



\- \*Indice 1\* : `os.getenv("NOM")` renvoie `None` si la variable n'existe pas. Que se passe-t-il si vous concaténez `None` dans une URL ?

\- \*Indice 2\* : pour valider les variables obligatoires, une boucle sur une liste de noms avec `raise` d'une exception explicite suffit. Pas besoin de bibliothèque.

\- \*Indice 3\* : si l'import `from src.utils.db import ...` échoue, c'est probablement un `\_\_init\_\_.py` manquant ou une exécution depuis le mauvais dossier. Lancez toujours les commandes depuis la racine du projet.



\## 8. Critères de validation



\- `\\dn` affiche `raw`, `staging`, `analytics`, `ops`.

\- `\\dt raw.\*`, `\\dt staging.\*` et `\\dt ops.\*` affichent vos tables.

\- Les quatre scripts se rejouent deux fois de suite sans erreur.

\- La base peut être supprimée et recréée uniquement à partir des scripts.

\- `\\d staging.weather\_observation` montre la clé primaire composite et vos contraintes `CHECK`.

\- `python -m src.utils.db` affiche une connexion réussie.

\- `git grep -i password` ne montre aucun mot de passe réel dans les fichiers versionnés.

\- Chaque choix de type est justifié par écrit dans `docs/decisions.md` ou `docs/data\_dictionary.md`.



\## 9. Erreurs fréquentes et diagnostic



\- \*\*`FATAL: password authentication failed`\*\* : mot de passe erroné dans `.env`, ou rôle créé sans `LOGIN`. Vérifiez avec `\\du`.

\- \*\*`FATAL: Peer authentication failed`\*\* : vous vous connectez par socket locale. Ajoutez `-h localhost` ou configurez `pg\_hba.conf`.

\- \*\*`could not connect to server`\*\* : le service PostgreSQL n'est pas démarré, ou le port n'est pas 5432. Testez `\\conninfo` et le statut du service.

\- \*\*`ModuleNotFoundError: No module named 'psycopg'`\*\* : venv non activé, ou installation sans l'extra `binary`.

\- \*\*`NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgresql.psycopg2`\*\* : l'URL utilise `postgresql://` alors que seul psycopg 3 est installé. Précisez le pilote (`postgresql+psycopg`).

\- \*\*`.env` non chargé\*\* : `load\_dotenv()` cherche le fichier à partir du dossier courant. Lancez depuis la racine, ou passez un chemin explicite avec `pathlib`.

\- \*\*Mot de passe contenant `@` ou `/`\*\* : une URL construite par concaténation casse. D'où `URL.create`.

\- \*\*`timestamp` sans fuseau\*\* pour des mesures horaires : les décalages d'heure d'été apparaîtront plus tard comme des doublons ou des trous. Raisonnez sur l'instant absolu.

\- \*\*`CHECK (valeur >= 0)` sans `NOT NULL`\*\* : les `NULL` passent. Décidez explicitement quelles colonnes acceptent le nul.

\- \*\*`DROP` accidentel sur la mauvaise base\*\* : vérifiez avec `\\conninfo` avant toute commande destructive.

\- \*\*Tout en superutilisateur\*\* : les scripts fonctionnent, puis cassent en environnement réel. Travaillez dès maintenant avec `pipeline\_user`.



\## 10. Livrable et commits Git attendus



Deux commits :



```

feat(db): add schemas and DDL scripts

feat(db): add database configuration and connection helper

```



\- Le premier contient `sql/ddl/\*.sql` et les mises à jour de `docs/`.

\- Le second contient `src/config.py`, `src/utils/db.py` et `.env.example` mis à jour.

\- Vérifiez avant chaque commit : `git status` et `git diff --staged`.

\- Poussez sur `origin/main`.



\## 11. Question de contrôle et ce que vous devez me transmettre



Envoyez-moi (copier-coller) :



1\. Votre \*\*tableau de conception\*\* (exercice 4) avec vos justifications de types.

2\. Vos \*\*quatre fichiers DDL\*\*.

3\. La sortie de `\\dn` et de `\\d staging.weather\_observation`.

4\. Votre `src/config.py` et `src/utils/db.py`, ainsi que le résultat de `python -m src.utils.db` (ou l'erreur exacte).

5\. Si ce n'est pas déjà fait : vos documents de Phase 0 et le résultat de la Phase 1 (`git ls-files`, `.gitignore`).



\*\*Questions de contrôle :\*\*



1\. Un `CHECK (pm2\_5 >= 0)` est défini sur une colonne nullable. Une ligne avec `pm2\_5 = NULL` est-elle acceptée ? Pourquoi, et comment l'interdire si votre règle de qualité l'exige ?

2\. Pourquoi est-il généralement déconseillé de mettre des clés étrangères et des `CHECK` stricts sur les tables de la couche `raw` ?



Après relecture de votre modélisation et de votre code, nous passerons à la \*\*Phase 3 (Extraction API)\*\*.



# Phases 3 à 10 : TP détaillés

Vous avez demandé toutes les phases d'un coup. Les voici, chacune au format en 11 points. Le TP reste progressif et vous codez vous-même : je ne donne que des squelettes, des indices et des critères de validation.

Trois règles pour la suite :

- **Points de contrôle** : à la fin de chaque phase, envoyez-moi votre code et vos résultats. Je corrige localement, sans réécrire votre travail.
- **Ordre** : les phases 3 et 4 sont indépendantes de la base, vous pouvez les mener avant ou après la 2. Les phases 5 à 7 supposent que 2, 3 et 4 sont faites.
- **Détails des API** : je n'ai pas pu tester les endpoints Open-Meteo ici. Les noms de paramètres ci-dessous sont à confirmer dans la documentation, comme en Phase 0. Pour la même raison, je ne cite aucune limite d'appels ni profondeur d'historique : vérifiez-les vous-même (« Terms » et pages de documentation).

---

# Phase 3 : Extraction depuis l'API

## 1. Phase et objectif

Un module `src/extract/api_client.py` qui récupère, pour une ville et une période, la météo horaire et la qualité de l'air horaire. Il est robuste (timeout, erreurs HTTP, JSON invalide, réponse vide, retry), journalisé et testé sans réseau.

## 2. Contexte

Une API est un système extérieur que vous ne contrôlez pas : elle ralentit, tombe, change de format. Un extracteur de production ne suppose jamais que « ça marchera ». Il distingue les erreurs réessayables (réseau, 5xx) des erreurs définitives (400 : requête invalide).

## 3. Notions à comprendre

- **HTTP** : méthode `GET`, URL, paramètres de requête, en-têtes, code de statut (2xx ok, 4xx erreur client, 5xx erreur serveur).
- **Timeout** : sans lui, `requests` peut attendre indéfiniment.
- **`raise_for_status()`** : transforme un statut 4xx/5xx en exception `HTTPError`.
- **Exceptions ciblées** : `requests.Timeout`, `requests.ConnectionError`, `requests.HTTPError`, `ValueError` (JSON invalide). Capturer `Exception` partout masque les bugs.
- **Exception personnalisée** : une classe `ApiError(Exception)` unifie les échecs côté appelant.
- **Retry avec backoff** : réessayer N fois en attendant de plus en plus longtemps (1 s, 2 s, 4 s).
- **`logging`** : niveaux `DEBUG/INFO/WARNING/ERROR`, un logger par module via `logging.getLogger(__name__)`. Jamais de `print` dans un pipeline.
- **`pathlib.Path`** : manipulation de chemins portable.
- **Mock** : remplacer l'appel réseau par un faux dans les tests (`monkeypatch` de pytest ou `unittest.mock`).
- **Structure du JSON** : listes parallèles dans `hourly` (un tableau `time` et un tableau par variable). Vous le transformerez en Phase 5.

## 4. Travail à réaliser par vous

**Exercice 1 : Explorer l'API à la main.** Avec `curl` ou le navigateur, appelez l'API d'archive météo et l'API qualité de l'air pour une ville, 7 jours, avec les variables horaires de votre dictionnaire. Notez : l'URL de base, les paramètres, la structure JSON (clés de premier niveau, `hourly_units`), la longueur des tableaux, et le format de l'erreur pour une requête volontairement invalide.

**Exercice 2 : Configuration des villes.** Créez un fichier de configuration listant vos 8 villes (nom, code INSEE, latitude, longitude). Choisissez entre un dictionnaire Python dans `config.py` et un petit CSV dans `data/external/` (justifiez dans `decisions.md`).

**Exercice 3 : Logging.** Écrivez `src/utils/logging_config.py` avec une fonction `setup_logging()` : format lisible (date, niveau, module, message), sortie console et fichier dans `logs/`.

**Exercice 4 : Client API.** Écrivez l'extracteur selon ce squelette :

```python
# src/extract/api_client.py
import logging
import time
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

class ApiError(Exception):
    """Raised when an API call fails after all retries."""

def _get_json(url: str, params: dict, timeout: float = 30, max_retries: int = 3) -> dict:
    # TODO: loop over attempts
    # TODO: call requests.get with params and timeout
    # TODO: raise_for_status, then parse JSON
    # TODO: retry on Timeout / ConnectionError / 5xx, wait with exponential backoff
    # TODO: do NOT retry on 4xx, raise ApiError immediately
    # TODO: log each attempt and each failure
    ...

def fetch_weather(latitude: float, longitude: float, start_date: str, end_date: str) -> dict:
    # TODO: build params, call _get_json, check that the payload contains "hourly"
    ...

def fetch_air_quality(latitude: float, longitude: float, start_date: str, end_date: str) -> dict:
    # TODO: same pattern
    ...

def save_raw_sample(payload: dict, path: Path) -> None:
    # TODO: write JSON to disk (create parent folder if needed)
    ...
```

Syntaxe nouvelle :

- `params=` : `requests` encode lui-même le dictionnaire en `?cle=valeur&...`. Ne concaténez pas l'URL à la main.
- `def f(x: float = 30)` : valeur par défaut d'un argument.
- `raise ApiError("...") from exc` : chaîne l'exception d'origine pour garder la trace.
- `time.sleep(n)` : pause de `n` secondes.
- `for attempt in range(1, max_retries + 1)` : boucle de 1 à `max_retries`.

**Exercice 5 : Cas d'échec.** Provoquez volontairement : un timeout (valeur très petite), une variable inexistante (erreur 4xx), une URL inexistante, une réponse sans clé `hourly`. Vérifiez que chaque cas produit un log clair et une `ApiError`, pas une trace Python obscure.

**Exercice 6 : Test pytest sans réseau.** Écrivez au moins deux tests dans `tests/test_extract/test_api_client.py` : un succès (réponse simulée), un échec avec retry (le faux échoue deux fois puis réussit). Le but : zéro appel réseau pendant `pytest`.

**Exercice 7 : Boucle sur les 8 villes.** Extrayez les deux sources pour chaque ville, avec une pause courte entre appels pour rester poli avec le service. Sauvegardez un échantillon brut dans `data/raw/` (ignoré par Git).

**Bonus** : `requests.Session` pour réutiliser la connexion ; ajout d'un en-tête `User-Agent` explicite.

## 5. Fichiers concernés

`src/extract/api_client.py`, `src/utils/logging_config.py`, `src/config.py` (villes), `tests/test_extract/test_api_client.py`, `docs/decisions.md`.

## 6. Commandes à exécuter

```bash
curl -s "<URL_ARCHIVE>?latitude=...&longitude=...&start_date=...&end_date=...&hourly=...&timezone=UTC" | python -m json.tool | head -50
python -m src.extract.api_client      # si vous ajoutez un bloc __main__ de test manuel
pytest tests/test_extract -v
```

- `-s` de `curl` : mode silencieux.
- `python -m json.tool` : formate un JSON lisiblement.
- `pytest -v` : affiche chaque test.

## 7. Indices progressifs

**Retry**
- *Indice 1* : la boucle `for` s'arrête par un `return` en cas de succès. Que se passe-t-il à la sortie de la boucle sans succès ?
- *Indice 2* : le délai d'attente à la tentative `n` s'écrit avec une puissance de 2.
- *Indice 3* : l'objet `HTTPError` porte la réponse : `exc.response.status_code`. Comparez-le à 500 pour distinguer 4xx et 5xx.

**Test mock**
- *Indice 1* : le fixture `monkeypatch.setattr(objet, "nom", faux)` remplace un attribut le temps du test. Que remplacez-vous : `requests.get` tel que vu depuis **votre** module ?
- *Indice 2* : votre faux doit renvoyer un objet qui possède `.raise_for_status()` et `.json()`. Une petite classe locale suffit.
- *Indice 3* : pour ne pas attendre pendant les tests de retry, remplacez aussi `time.sleep`.

**Fuseau horaire**
- *Indice* : demandez `timezone=UTC` à l'API pour le brut. Les heures locales se répètent ou sautent lors du changement d'heure, ce qui crée des ambiguïtés. Vous convertirez en heure locale plus tard, côté analyse.

## 8. Critères de validation

- Les 8 villes sont extraites pour les deux sources.
- Les 4 cas d'échec donnent un log lisible et une `ApiError`.
- `pytest` passe hors connexion (coupez le Wi-Fi pour vérifier).
- Aucun `print`, aucun `except Exception` nu, aucun `timeout` oublié.
- Le dossier `data/raw/` n'apparaît pas dans `git status`.

## 9. Erreurs fréquentes et diagnostic

- **Pas de `timeout`** : le script « gèle ». Symptôme : aucune sortie pendant des minutes.
- **Retry sur toutes les erreurs** : une erreur 400 réessayée 3 fois est une perte de temps.
- **`response.json()` sur une page HTML d'erreur** : `JSONDecodeError`, qui hérite de `ValueError`. Capturez-le.
- **Test qui appelle vraiment le réseau** : le patch vise le mauvais chemin (`requests.get` au lieu de `api_client.requests.get`).
- **Plage de dates trop longue** : l'API peut refuser ou limiter. Si c'est le cas, découpez en tranches (mensuelles) : à décider selon votre exploration.
- **Valeurs `null`** dans les tableaux : normales, ne les traitez pas ici.

## 10. Livrable et commit

```
feat(extract): add weather and air quality API client
test(extract): add mocked tests for retry and error handling
```

## 11. Question de contrôle / à me transmettre

Envoyez : `api_client.py`, vos tests, la sortie de `pytest -v`, et un exemple de log d'échec. **Question** : pourquoi ne faut-il pas réessayer une erreur 400, mais bien une erreur 503 ?

---

# Phase 4 : Ingestion CSV et Excel

## 1. Phase et objectif

Lire le référentiel des communes (CSV) et les populations légales (Excel) avec Pandas, diagnostiquer leur qualité, standardiser les colonnes, et produire un rapport de qualité par source.

## 2. Contexte

Les fichiers « open data » sont rarement propres : encodages variés, séparateurs `;`, lignes de titre avant l'en-tête, feuilles multiples, codes INSEE devenus des entiers. Cette phase vous apprend à lire **sans corrompre**.

## 3. Notions à comprendre

- **`pd.read_csv`** : `sep`, `encoding`, `dtype`, `usecols`, `nrows`.
- **`pd.read_excel`** : `sheet_name`, `skiprows`, `header`, `dtype`. Nécessite `openpyxl` pour `.xlsx`.
- **Codes INSEE en texte** : `01001` doit rester `"01001"`, et la Corse a `2A`/`2B`. Lisez ces colonnes avec `dtype=str`.
- **Profilage** : `df.shape`, `df.dtypes`, `df.info()`, `df.isna().sum()`, `df.duplicated().sum()`, `df.describe()`.
- **Standardisation des noms de colonnes** : minuscules, espaces et accents remplacés, `snake_case`.
- **Fonction réutilisable** : une fonction par type de fichier, paramétrée, plutôt que du code copié.

Syntaxe isolée (exemple fictif) :

```python
df = pd.read_csv("file.csv", sep=";", encoding="utf-8", dtype={"code": str})
df.columns = df.columns.str.strip().str.lower()   # .str applies string methods to each column name
```

## 4. Travail à réaliser par vous

**Exercice 1 : Récupérer les fichiers.** Placez le CSV des communes et l'Excel des populations dans `data/external/` (ignoré par Git : documentez l'URL de téléchargement et la date dans le README, pas le fichier).

**Exercice 2 : Explorer avant de coder.** Ouvrez-les (éditeur de texte pour le CSV, tableur pour l'Excel). Notez : séparateur, encodage probable, nombre de feuilles, ligne où commence l'en-tête, colonnes utiles.

**Exercice 3 : Lecteurs.** Squelette :

```python
# src/extract/file_readers.py
from pathlib import Path
import pandas as pd

def read_communes_csv(path: Path) -> pd.DataFrame:
    # TODO: read with the right separator, encoding, and dtype=str for code columns
    # TODO: raise FileNotFoundError with a clear message if the file is missing
    ...

def read_population_excel(path: Path, sheet_name: str) -> pd.DataFrame:
    # TODO: skip the title rows, read the right sheet, keep INSEE code as string
    ...

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: lowercase, strip, replace spaces/accents/special chars by underscores
    ...
```

**Exercice 4 : Rapport de qualité.** Dans `src/quality/profiling.py`, écrivez une fonction qui reçoit un DataFrame et un nom de source, et retourne un dictionnaire : nombre de lignes, de colonnes, nulls par colonne, doublons, et nombre de valeurs distinctes de la clé. Journalisez-le.

**Exercice 5 : Filtrer sur vos 8 villes.** Isolez dans les deux sources les lignes de vos villes (par code INSEE). Vérifiez que chaque ville est trouvée **exactement une fois** dans chaque source.

**Exercice 6 : Tests.** Au moins un test par lecteur sur de petits fichiers temporaires (fixture `tmp_path` de pytest) : codes INSEE conservant leurs zéros, colonnes standardisées.

**Bonus** : détectez automatiquement l'encodage ou le séparateur ; comparez les noms de communes entre sources (accents, tirets, majuscules).

## 5. Fichiers concernés

`src/extract/file_readers.py`, `src/quality/profiling.py`, `tests/test_extract/test_file_readers.py`, `data/external/` (non versionné), `docs/data_dictionary.md`.

## 6. Commandes à exécuter

```bash
file -i data/external/communes.csv     # encodage devine (Linux/macOS)
head -5 data/external/communes.csv     # apercu des premieres lignes
pytest tests/test_extract -v
```

## 7. Indices progressifs

**Excel avec en-têtes décalés**
- *Indice 1* : `header=` et `skiprows=` n'ont pas le même effet. Lisez la doc de `read_excel`.
- *Indice 2* : lisez d'abord avec `header=None` pour voir les premières lignes brutes, puis ajustez.

**Noms de colonnes**
- *Indice 1* : chaîne `.str.strip().str.lower()`.
- *Indice 2* : les accents se traitent avec la bibliothèque standard `unicodedata`, ou en acceptant de renommer manuellement quelques colonnes.
- *Indice 3* : `.str.replace(r"[^a-z0-9]+", "_", regex=True)` remplace tout caractère non alphanumérique par un tiret bas.

**Codes INSEE**
- *Indice* : après lecture, `df["col"].str.len().value_counts()` révèle les longueurs inattendues. Un code à 4 caractères trahit un zéro perdu.

## 8. Critères de validation

- Les codes INSEE conservent leurs zéros initiaux.
- Les colonnes sont en `snake_case`.
- Chaque ville est trouvée une fois dans chaque source.
- Le rapport de qualité est produit et journalisé pour les deux sources.
- Les tests passent.

## 9. Erreurs fréquentes et diagnostic

- **Mauvais séparateur** : le DataFrame a une seule colonne. Essayez `sep=";"`.
- **`UnicodeDecodeError`** : encodage différent, souvent `latin-1`/`cp1252` pour les fichiers français anciens.
- **`01001` devient `1001`** : `dtype=str` oublié.
- **Colonnes `Unnamed: 0`** : les lignes de titre n'ont pas été sautées.
- **`ImportError: openpyxl`** : non installé dans le venv.
- **Doublons dus aux arrondissements** : Paris, Lyon et Marseille ont des codes spécifiques par arrondissement dans certains fichiers. Vérifiez ce que contient votre référentiel pour ces villes.

## 10. Livrable et commit

```
feat(extract): add csv and excel readers with profiling
test(extract): add tests for file readers
```

## 11. Question de contrôle / à me transmettre

Envoyez : `file_readers.py`, `profiling.py`, le rapport de qualité imprimé pour chaque source. **Question** : pourquoi lire un code INSEE comme un entier est-il un bug de conception, et pas seulement un détail de format ?

---

# Phase 5 : Transformation avec Pandas

## 1. Phase et objectif

Convertir les JSON de l'API en tables longues, nettoyer, valider selon vos règles `DQ-xx`, joindre avec le référentiel, et séparer **lignes valides** et **lignes rejetées** (avec motif).

## 2. Contexte

C'est le cœur du pipeline. Une règle de qualité n'a de valeur que si elle est appliquée **et** mesurée : une ligne rejetée sans trace est une donnée perdue silencieusement.

## 3. Notions à comprendre

- **Listes parallèles vers table longue** : `pd.DataFrame(payload["hourly"])` produit une ligne par heure.
- **Dates** : `pd.to_datetime(..., utc=True, errors="coerce")` (`coerce` transforme l'invalide en `NaT` plutôt que de planter).
- **Nettoyage de texte** : `.str.strip()`, `.str.upper()`, `.str.normalize`.
- **`merge`** : `how="left"/"inner"`, `on=`, et surtout `validate="m:1"` qui lève une erreur si la clé de droite n'est pas unique.
- **Masques booléens** : `mask = df["col"] < 0` ; `df[mask]` et `df[~mask]`.
- **`drop_duplicates(subset=[...])`** et `df.duplicated(subset=[...], keep=False)`.
- **Fonctions pures** : entrée DataFrame, sortie DataFrame, sans effet de bord : faciles à tester.
- **Bilan de lignes** : `valides + rejetées = entrée`. Si ce n'est pas vrai, vous perdez des données.
- **`SettingWithCopyWarning`** : modification d'une vue de DataFrame. Utilisez `.copy()` et `.loc`.

## 4. Travail à réaliser par vous

**Exercice 1 : JSON → DataFrame.** Pour chaque source API, une fonction qui prend le payload et renvoie un DataFrame long avec une colonne par variable, plus `latitude`, `longitude` et une colonne ville. Squelette :

```python
# src/transform/weather.py
import pandas as pd

def weather_payload_to_frame(payload: dict, city_code: str) -> pd.DataFrame:
    # TODO: build a DataFrame from payload["hourly"]
    # TODO: add the city identifier column
    # TODO: rename columns to match the staging schema
    ...
```

**Exercice 2 : Typage et nettoyage.** Convertir les timestamps en UTC, les mesures en numérique, uniformiser les identifiants de ville.

**Exercice 3 : Règles de qualité.** Dans `src/quality/rules.py`, une fonction par règle `DQ-xx` retournant un masque booléen des lignes **invalides**. Puis une fonction d'orchestration :

```python
# src/quality/rules.py
import pandas as pd

def check_pm25_non_negative(df: pd.DataFrame) -> pd.Series:
    # TODO: return a boolean Series: True where the row violates the rule
    ...

def split_valid_rejected(df: pd.DataFrame, rules: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    # TODO: apply each rule, collect the rule id for each rejected row
    # TODO: build the rejected DataFrame with a "rejection_reason" column
    # TODO: return (valid, rejected)
    ...
```

Syntaxe : `tuple[pd.DataFrame, pd.DataFrame]` indique que la fonction renvoie deux éléments ; `dict[str, Callable]` (de `typing`) est un dictionnaire nom-de-règle → fonction.

**Exercice 4 : Jointure avec le référentiel.** Joignez les observations avec la dimension `city` (communes + populations) avec `validate=`. Comptez les observations sans ville correspondante : ce sont des rejets (règle de cohérence).

**Exercice 5 : Bilan.** Affichez et journalisez : lignes en entrée, valides, rejetées par règle.

**Exercice 6 : Tests unitaires.** Au moins 3 tests, sur 3 règles différentes, avec de petits DataFrames construits à la main contenant un cas valide et un cas invalide.

**Bonus** : colonne `reject_reason` avec plusieurs motifs concaténés ; test de volumétrie (`24 × jours` par ville).

## 5. Fichiers concernés

`src/transform/weather.py`, `air_quality.py`, `cities.py`, `src/quality/rules.py`, `tests/test_transform/`.

## 6. Commandes à exécuter

```bash
python -c "import pandas as pd; print(pd.__version__)"
pytest tests/test_transform -v
```

## 7. Indices progressifs

**Jointure qui multiplie les lignes**
- *Indice 1* : comparez `len(avant)` et `len(après)`.
- *Indice 2* : `validate="m:1"` fait échouer la jointure si le côté droit a des doublons.
- *Indice 3* : dédoublonnez la dimension **avant** de joindre, en décidant explicitement quelle ligne garder.

**Rejets sans perte**
- *Indice* : construisez le masque de rejet global avec des `|` (OU logique) entre masques, puis `valid = df[~mask]`, `rejected = df[mask]`.

**Tests**
- *Indice* : `pd.testing.assert_series_equal` ou `assert result.tolist() == [...]`.

## 8. Critères de validation

- `len(valid) + len(rejected) == len(input)` dans tous les cas.
- Aucune ville multipliée par la jointure.
- Les dates sont toutes en UTC, sans `NaT` silencieux.
- 3 tests de règles passent.
- Chaque rejet porte son motif (`DQ-xx`).

## 9. Erreurs fréquentes et diagnostic

- **`NaN` ignoré par la règle** : `df["x"] < 0` renvoie `False` pour un `NaN`. Si le nul est invalide, testez `isna()` explicitement.
- **Jointure sur types différents** : `object` contre `int`. Les clés doivent avoir le même type.
- **Modification d'un slice** : `SettingWithCopyWarning`. Ajoutez `.copy()`.
- **Fuseau horaire perdu** : un `to_datetime` sans `utc=True` produit des datetimes naïfs.
- **Rejeter trop** : une règle trop stricte vide le jeu de données. Surveillez le taux de rejet.

## 10. Livrable et commit

```
feat(transform): add JSON-to-frame conversion and cleaning
feat(quality): add data quality rules with rejection logic
test(transform): add unit tests for quality rules
```

## 11. Question de contrôle / à me transmettre

Envoyez : vos fonctions de transformation et de règles, vos tests, et le bilan de lignes pour une ville. **Question** : pourquoi `validate="m:1"` protège-t-il contre un bug silencieux ?

---

# Phase 6 : Chargement PostgreSQL

## 1. Phase et objectif

Charger `raw` (tel quel) et `staging` (après validation), enregistrer chaque exécution dans `ops.pipeline_run_log`, et prouver que deux exécutions successives donnent le même résultat (idempotence).

## 2. Contexte

Un chargement non idempotent duplique les données à chaque relance. Un chargement sans transaction peut laisser la base à moitié mise à jour. Un chargement sans journal ne permet pas de savoir ce qui s'est passé.

## 3. Notions à comprendre

- **Transaction** : un bloc tout-ou-rien. `with engine.begin() as conn:` valide (`commit`) à la sortie normale et annule (`rollback`) sur exception.
- **`to_sql`** : `if_exists="append"` ajoute (duplique à chaque relance), `"replace"` détruit la table et ses contraintes. Les deux sont rarement adaptés tels quels.
- **`TRUNCATE`** puis rechargement : idempotence simple.
- **Upsert** : `INSERT ... ON CONFLICT (cles) DO UPDATE SET ...`. Nécessite une clé primaire ou unique.
- **Requêtes paramétrées** : `text("... :param")` avec un dictionnaire de valeurs. **Ne formatez jamais du SQL avec des f-strings** (injection SQL).
- **Chargement par lots** : `method="multi"` et `chunksize` pour les volumes.
- **Journalisation en cas d'échec** : l'écriture du journal doit se faire dans une transaction **séparée**, sinon le rollback efface aussi la trace de l'échec.

Syntaxe isolée (fictive) :

```python
with engine.begin() as conn:                      # commit on success, rollback on exception
    conn.execute(text("TRUNCATE demo.t"))
    df.to_sql("t", conn, schema="demo", if_exists="append", index=False)
```

## 4. Travail à réaliser par vous

**Exercice 1 : Chargement `raw`.** Squelette :

```python
# src/load/postgres_loader.py
import logging
import pandas as pd
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

def load_dataframe(engine: Engine, df: pd.DataFrame, schema: str, table: str, truncate: bool = True) -> int:
    # TODO: open a transaction
    # TODO: truncate the table if requested
    # TODO: insert the dataframe (no index, chunked)
    # TODO: log and return the number of inserted rows
    ...
```

**Exercice 2 : Chargement `staging`.** Même fonction pour les lignes valides, et `staging.rejected_rows` pour les rejets (ligne d'origine en `jsonb`).

**Exercice 3 : Journal d'exécution.** Dans `src/load/run_log.py`, deux fonctions : démarrer une exécution (insère une ligne `RUNNING`, renvoie son identifiant) et la terminer (met à jour statut, compteurs, message d'erreur, date de fin). Utilisez des requêtes paramétrées.

**Exercice 4 : Idempotence.** Exécutez le chargement deux fois et comparez `SELECT count(*)` et un contrôle de doublons sur la clé.

**Exercice 5 : Rollback.** Provoquez une erreur au milieu du chargement (par exemple, une ligne violant une contrainte) et prouvez que la table est inchangée.

**Exercice 6 : Requêtes de vérification.** Dans `sql/queries/checks.sql` : comptages par table, ville et période, doublons de clé, plage de dates, nulls par colonne.

**Exercice 7 (amélioration)** : remplacez `TRUNCATE + reload` de `staging` par un upsert avec `ON CONFLICT`. Comparez avantages et inconvénients dans `decisions.md`.

## 5. Fichiers concernés

`src/load/postgres_loader.py`, `src/load/run_log.py`, `tests/test_load/`, `sql/queries/checks.sql`.

## 6. Commandes à exécuter

```bash
psql -U pipeline_user -h localhost -d air_weather -f sql/queries/checks.sql
pytest tests/test_load -v
```

## 7. Indices progressifs

**Journal en cas d'échec**
- *Indice 1* : si l'insertion échoue, la transaction principale est annulée. Où écrivez-vous alors `FAILED` ?
- *Indice 2* : ouvrez une seconde connexion/transaction dans le bloc `except`.

**Upsert**
- *Indice 1* : la clause `ON CONFLICT (col_a, col_b)` doit correspondre exactement à la clé primaire.
- *Indice 2* : dans `DO UPDATE SET col = EXCLUDED.col`, `EXCLUDED` désigne la ligne qu'on tentait d'insérer.

**Types**
- *Indice* : `to_sql` crée la table si elle n'existe pas, mais vos DDL l'ont déjà créée : utilisez `append` pour conserver vos contraintes.

## 8. Critères de validation

- Deux exécutions : mêmes comptages, aucun doublon.
- Une erreur provoquée laisse la base inchangée.
- Chaque exécution a une ligne dans `ops.pipeline_run_log` avec statut et compteurs corrects.
- Les comptages SQL concordent avec les logs Python.
- Aucun SQL construit par f-string avec des valeurs.

## 9. Erreurs fréquentes et diagnostic

- **`if_exists="replace"`** : détruit vos clés et contraintes.
- **Doublons à chaque relance** : `append` sans `TRUNCATE`.
- **`StringDataRightTruncation` / violation de type** : types DataFrame incompatibles avec les colonnes. Vérifiez `df.dtypes`.
- **Rollback qui efface le journal** : journal écrit dans la même transaction.
- **Chargement très lent** : insertion ligne à ligne. Utilisez `method="multi"` et `chunksize`.
- **`NaN` vs `NULL`** : Pandas utilise `NaN`, PostgreSQL attend `NULL`. `to_sql` convertit, mais attention aux colonnes `object`.

## 10. Livrable et commit

```
feat(load): add transactional postgres loader
feat(load): add pipeline run logging
test(load): add idempotency and rollback tests
```

## 11. Question de contrôle / à me transmettre

Envoyez : loader, run_log, la sortie de `checks.sql` après deux exécutions, et la preuve du rollback. **Question** : pourquoi écrire le statut `FAILED` dans une transaction séparée de celle du chargement ?

---

# Phase 7 : Orchestration Python simple

## 1. Phase et objectif

Un point d'entrée `src/main.py` qui enchaîne extraction, transformation, contrôles et chargement, avec gestion des erreurs, journal fichier et code de sortie fiable. Une seule commande : `python -m src.main`.

## 2. Contexte

Un pipeline n'est utile que s'il est relançable par quelqu'un d'autre (ou par un planificateur) et qu'il **signale clairement** son échec. Les planificateurs (cron, GitHub Actions, Airflow plus tard) se fient au code de sortie.

## 3. Notions à comprendre

- **Point d'entrée** : `if __name__ == "__main__":`.
- **Code de sortie** : `sys.exit(0)` succès, non nul échec.
- **`try/except/finally`** : `finally` s'exécute toujours (fermeture, journal).
- **Exceptions personnalisées** : `ExtractionError`, `ValidationError`, `LoadError`.
- **Dataclass de configuration** : `@dataclass` regroupe villes, période, chemins.
- **`argparse`** (optionnel) : options en ligne de commande (`--start-date`, `--dry-run`).
- **Rotation de logs** : `logging.handlers.RotatingFileHandler`.
- **Seuil de qualité** : faire échouer le pipeline si le taux de rejet dépasse un seuil défini.

## 4. Travail à réaliser par vous

**Exercice 1 : Configuration centralisée.** Squelette :

```python
# src/config.py (v1)
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PipelineConfig:
    start_date: str
    end_date: str
    raw_dir: Path
    reject_threshold: float   # e.g. maximum accepted share of rejected rows
    # TODO: add cities, external data paths, retry settings
```

`frozen=True` rend l'objet immuable : on ne peut pas le modifier par accident.

**Exercice 2 : Orchestrateur.**

```python
# src/main.py
import logging
import sys

logger = logging.getLogger(__name__)

def run_pipeline(config) -> None:
    # TODO: start run log, extract, transform, validate, load, end run log
    ...

def main() -> int:
    # TODO: setup logging, build config
    # TODO: try run_pipeline; on known errors log and return 1; on unexpected errors log with logger.exception and return 2
    # TODO: return 0 on success
    ...

if __name__ == "__main__":
    sys.exit(main())
```

**Exercice 3 : Règle d'arrêt.** Faites échouer le pipeline si le taux de rejet dépasse votre seuil, et journalisez le statut `FAILED` avec un message.

**Exercice 4 : Test de bout en bout.** Depuis un clone neuf du dépôt, créez un venv, installez, configurez `.env`, exécutez la commande unique. Puis relancez : le résultat doit être identique.

**Exercice 5 : Échec contrôlé.** Coupez le réseau, ou changez le mot de passe de base : vérifiez le code de sortie (`echo $?`) et le statut dans `ops.pipeline_run_log`.

**Bonus** : option `--cities` pour ne traiter qu'une ville ; option `--dry-run` sans chargement.

## 5. Fichiers concernés

`src/main.py`, `src/config.py`, `src/utils/logging_config.py`, `README.md` (section exécution).

## 6. Commandes à exécuter

```bash
python -m src.main
echo $?                 # code de sortie de la dernière commande (Windows PowerShell : $LASTEXITCODE)
tail -f logs/pipeline.log
```

## 7. Indices progressifs

- *Indice 1* : `logger.exception("message")` journalise la trace complète dans un bloc `except`.
- *Indice 2* : attrapez d'abord vos exceptions personnalisées (`except ExtractionError`), puis seulement en dernier un `except Exception` qui journalise et renvoie un code d'échec. Jamais de `pass`.
- *Indice 3* : si `python -m src.main` échoue sur les imports, vous lancez depuis le mauvais dossier ou il manque un `__init__.py`.

## 8. Critères de validation

- Une commande exécute tout, deux fois de suite, avec le même résultat.
- Succès : code 0. Échec : code non nul et ligne `FAILED` dans le journal.
- Les logs fichier existent et sont lisibles.
- Aucun `except Exception: pass`.
- Fonctionne après un clone neuf.

## 9. Erreurs fréquentes et diagnostic

- **Erreur avalée** : le script affiche une erreur mais renvoie 0. Symptôme : un cron « réussit » alors que rien n'est chargé.
- **Imports relatifs cassés** : lancer `python src/main.py` au lieu de `python -m src.main`.
- **Logs non écrits** : dossier `logs/` absent ou `setup_logging()` appelé trop tard.
- **Handlers dupliqués** : chaque appel à `setup_logging()` ajoute un handler, d'où des lignes en double.

## 10. Livrable et commit

```
feat(config): add centralized pipeline configuration
feat: add pipeline entrypoint with error handling and exit codes
```

## 11. Question de contrôle / à me transmettre

Envoyez : `main.py`, `config.py`, un log d'exécution réussie et un d'échec, et les codes de sortie. **Question** : pourquoi un code de sortie à 0 après une erreur est-il plus dangereux qu'un crash visible ?

---

# Phase 8 : Introduction à dbt

## 1. Phase et objectif

Reconstruire en SQL, avec dbt Core, la chaîne `raw → staging → intermediate → marts`, avec tests et documentation, puis comparer à votre ETL Pandas.

## 2. Contexte

Python excelle pour extraire et nettoyer. Le SQL excelle pour transformer des données déjà dans la base : lisible, testable, versionné, avec un graphe de dépendances. L'approche **ELT** charge d'abord le brut dans la base, puis transforme **dans** la base. dbt organise ces transformations.

## 3. Notions à comprendre

- **ETL vs ELT** : transformer avant de charger (Pandas) contre transformer après (dbt/SQL).
- **Source** : table brute déclarée dans un YAML, référencée avec `{{ source('raw', 'table') }}`.
- **Model** : un fichier `.sql` contenant un `SELECT`. dbt crée la table ou vue.
- **`ref()`** : `{{ ref('autre_modele') }}` référence un autre modèle et construit le graphe de dépendances.
- **Materialization** : `view`, `table`, `incremental`, `ephemeral`.
- **Couches** : *staging* (1 modèle par source, typage et renommage), *intermediate* (jointures, logique réutilisable), *marts* (tables finales pour l'analyse).
- **Tests génériques** : `not_null`, `unique`, `relationships`, `accepted_values`. Tests singuliers : un SQL qui doit renvoyer zéro ligne.
- **`profiles.yml`** : connexion à la base, **hors du dépôt** (dans `~/.dbt/`), avec `{{ env_var('DB_PASSWORD') }}`.
- **Documentation et lineage** : `description:` dans les YAML, graphe généré par `dbt docs`.

## 4. Travail à réaliser par vous

**Exercice 1 : Installer.** Créez un **environnement virtuel séparé** pour dbt (évite les conflits de dépendances), installez `dbt-postgres`, vérifiez `dbt --version`. Expliquez dans `decisions.md` pourquoi un venv séparé.

**Exercice 2 : Initialiser.** `dbt init` dans `dbt_project/`, puis configurez `profiles.yml` hors dépôt, avec des variables d'environnement pour le mot de passe.

**Exercice 3 : Sources.** Déclarez vos tables `raw` dans `models/staging/_sources.yml`. Squelette :

```yaml
version: 2
sources:
  - name: raw
    schema: raw
    tables:
      - name: weather_hourly_raw
      # TODO: declare the other raw tables, add descriptions
```

**Exercice 4 : Modèles staging.** Un modèle par source : typage, renommage, nettoyage léger. Squelette :

```sql
-- models/staging/stg_weather_hourly.sql
select
    -- TODO: cast and rename columns
from {{ source('raw', 'weather_hourly_raw') }}
```

**Exercice 5 : Modèle intermediate.** `int_hourly_city_environment` : jointure météo + air + ville au grain « ville, heure ».

**Exercice 6 : Marts.** Au moins deux : un journalier par ville (agrégations choisies en Phase 0 : moyenne, somme, max), un mensuel. Matérialisez en `table` et placez-les dans le schéma `analytics`.

**Exercice 7 : Tests.** Dans `_models.yml` : `not_null` et `unique` sur les clés, `relationships` vers la dimension ville, `accepted_values` sur un champ catégoriel, plus un test singulier de plausibilité. **Cassez un test volontairement** pour observer l'échec, puis corrigez.

**Exercice 8 : Documentation.** Décrivez chaque modèle et ses colonnes clés.

**Exercice 9 : Exécuter et expliquer.** Lancez `dbt debug`, `dbt run`, `dbt test`, `dbt docs generate`, `dbt docs serve`. Pour chacune, écrivez en deux lignes ce qu'elle a fait.

**Exercice 10 : Comparaison.** Dans `decisions.md`, comparez vos tables Pandas `staging` et les modèles dbt : avantages, limites, ce que vous garderiez dans chaque outil.

## 5. Fichiers concernés

`dbt_project/dbt_project.yml`, `models/staging/_sources.yml`, `stg_*.sql`, `models/intermediate/*.sql`, `models/marts/*.sql`, `_models.yml`, `~/.dbt/profiles.yml` (hors dépôt), `.gitignore` (ajoutez `target/`, `dbt_packages/`, `logs/` de dbt).

## 6. Commandes à exécuter

```bash
cd dbt_project
dbt debug --profiles-dir ~/.dbt
dbt run
dbt run --select staging          # ne lance que les modèles staging
dbt test
dbt docs generate
dbt docs serve
```

Ce que fait chaque commande :

- **`dbt debug`** : vérifie le fichier de projet, le profil et la connexion. Sa réussite ne dit rien de vos modèles.
- **`dbt run`** : compile chaque modèle en SQL, l'exécute dans l'ordre du graphe, et crée tables ou vues dans le schéma cible. Lisez le résumé : `OK`, `ERROR`, `SKIP` (un amont a échoué).
- **`dbt test`** : exécute chaque test comme une requête qui cherche les lignes en défaut. Zéro ligne = `PASS`.
- **`dbt docs generate`** : produit le catalogue et le manifeste (`target/`).
- **`dbt docs serve`** : ouvre un site local avec la documentation et le graphe de dépendances.

## 7. Indices progressifs

**Schéma cible**
- *Indice 1* : dbt crée les modèles dans le schéma du profil, éventuellement préfixé. Pour contrôler : `+schema:` dans `dbt_project.yml`.
- *Indice 2* : sans réglage, dbt concatène schéma du profil et schéma du modèle (`public_analytics`). Cherchez la macro `generate_schema_name` si vous voulez le comportement exact.

**Tests `relationships`**
- *Indice* : la syntaxe a deux arguments : le modèle cible (`ref(...)`) et le champ cible.

**Erreur de compilation**
- *Indice* : `dbt compile` puis ouvrez le SQL généré dans `target/compiled/` : vous voyez exactement ce qui est envoyé à PostgreSQL.

## 8. Critères de validation

- `dbt debug` passe ; `dbt run` et `dbt test` passent.
- Les marts répondent à vos indicateurs de la Phase 0.
- Le graphe de dépendances est visible dans les docs.
- Aucun mot de passe dans le dépôt (`git grep -i password`).
- Vous avez observé un échec de test et sa correction.

## 9. Erreurs fréquentes et diagnostic

- **`profiles.yml` commité** : placez-le hors du dépôt.
- **`Compilation Error: source not found`** : nom de source ou de table mal orthographié dans `_sources.yml`.
- **Conflits de dépendances à l'installation** : `dbt-postgres` dans le venv du projet. D'où le venv séparé.
- **Confusion schéma source / cible** : dbt lit `raw`, mais écrit ailleurs.
- **`dbt test` échoue sur `unique`** : doublon réel dans vos données (donc utile), ou grain mal défini.
- **Dérive des définitions** : règles de qualité écrites différemment en Pandas et en dbt. Alignez-les.

## 10. Livrable et commit

```
feat(dbt): initialize project and declare raw sources
feat(dbt): add staging and intermediate models
feat(dbt): add analytics marts with tests and documentation
```

## 11. Question de contrôle / à me transmettre

Envoyez : vos modèles, `_models.yml`, les sorties de `dbt run` et `dbt test`, et une capture ou description du graphe. **Question** : quelle différence entre `source()` et `ref()`, et que gagne-t-on en utilisant `ref()` plutôt que d'écrire le nom de table en dur ?

---

# Phase 9 : Documentation et qualité

## 1. Phase et objectif

Rendre le projet compréhensible, installable et exécutable par un tiers, à partir du seul README.

## 2. Contexte

Un recruteur ou un collègue lit le README avant le code. Un pipeline sans documentation est un pipeline que personne ne reprend.

## 3. Notions à comprendre

- **README orienté lecteur** : que fait le projet, comment l'installer, comment l'exécuter, que faire en cas de problème.
- **Architecture Decision Records** : une décision, son contexte, ses alternatives, son compromis.
- **Hypothèses et limites** : dire ce que le projet ne fait pas est un signe de maturité.
- **Dictionnaire de données** vivant, aligné sur les tables réelles.

## 4. Travail à réaliser par vous

Rédigez ces sections du `README.md` :

1. Contexte et objectif.
2. Schéma d'architecture (texte).
3. Stack technique.
4. Structure du dépôt.
5. Guide d'installation (prérequis, venv, dépendances, PostgreSQL, `.env`, DDL).
6. Guide d'exécution (pipeline, dbt, tests).
7. Dépannage (au moins 5 erreurs réelles rencontrées et leur solution).
8. Qualité de données (règles `DQ-xx`, actions, métriques).
9. Décisions techniques et compromis.
10. Hypothèses, limites et sources de données (URL, licences, dates).

Mettez à jour `docs/architecture.md`, `docs/data_dictionary.md` (types finaux) et `docs/decisions.md`.

**Test final** : un collègue (ou vous, dans un dossier neuf) suit le README, et seulement le README, de zéro à `dbt test` vert.

Bonus : badges, captures du graphe dbt, section « Résultats ».

## 5. Fichiers concernés

`README.md`, `docs/architecture.md`, `docs/data_dictionary.md`, `docs/decisions.md`.

## 6. Commandes à exécuter

```bash
pytest -v
cd dbt_project && dbt test
git clone <URL> /tmp/fresh-test && cd /tmp/fresh-test   # test du README sur un clone neuf
```

## 7. Indices progressifs

- *Indice 1* : écrivez le guide d'installation en le **suivant** sur un clone neuf, pas de mémoire.
- *Indice 2* : pour le dépannage, relisez vos propres erreurs des phases précédentes.
- *Indice 3* : chaque décision : « on a choisi X plutôt que Y parce que Z, au prix de W ».

## 8. Critères de validation

- Le README permet une installation complète sans aide.
- `pytest` et `dbt test` passent.
- Les limites sont explicitement listées.
- Aucun secret, aucun chemin personnel dans les docs.
- Les types du dictionnaire correspondent aux DDL.

## 9. Erreurs fréquentes et diagnostic

- **Commandes jamais testées** dans le README.
- **Documentation obsolète** après modification du schéma.
- **Ni limites ni sources** : le lecteur ne sait pas ce qu'il peut croire.
- **Trop de texte, pas de structure** : privilégiez titres et blocs de code.

## 10. Livrable et commit

```
docs: complete README with installation, execution and troubleshooting
docs: update architecture, data dictionary and decisions
```

## 11. Question de contrôle / à me transmettre

Envoyez votre README et le compte rendu de votre test sur clone neuf. **Question** : quelles sont les trois principales limites de votre pipeline, et comment un lecteur peut-il les trouver sans lire le code ?

---

# Phase 10 : Démonstration et améliorations

## 1. Phase et objectif

Préparer une démonstration de 5 à 10 minutes, une bibliothèque de requêtes d'analyse, et une feuille de route d'évolutions priorisée.

## 2. Contexte

Un projet de portfolio se juge par ce que l'on peut en raconter : problème, architecture, difficultés rencontrées, résultats, suite.

## 3. Notions à comprendre

- **Récit de démo** : contexte, flux, preuve, résultat, limites.
- **Requêtes d'analyse** : lisibles, commentées, qui répondent aux questions métier de la Phase 0.
- **Priorisation** : valeur apportée contre effort, dépendances.

## 4. Travail à réaliser par vous

**Exercice 1 : Script de démo.** Plan minutaire : (1) problème métier, (2) architecture, (3) exécution de la commande unique, (4) rejets et journal, (5) tables PostgreSQL, (6) dbt (graphe, tests), (7) une analyse finale, (8) limites et suite.

**Exercice 2 : Requêtes d'analyse.** 5 à 8 requêtes dans `sql/queries/analysis.sql`, à partir des marts. Exemples de questions : jours de dépassement d'un seuil de particules par ville, lien entre vent et concentration, comparaison entre villes, évolution mensuelle. Vous les écrivez ; je les relis.

**Exercice 3 : Résultats attendus.** Dans le README : volumétrie finale, taux de rejet, durée d'exécution, trois enseignements issus des données.

**Exercice 4 : Roadmap priorisée.** Classez ces évolutions avec une justification courte (valeur/effort) et un ordre :

| Priorité à vous de définir | Évolution |
|---|---|
| ? | CI GitHub Actions (tests à chaque push) |
| ? | Tests de données avancés (par exemple Great Expectations ou dbt-expectations) |
| ? | Ingestion incrémentale (ne charger que les nouvelles heures) |
| ? | Docker (environnement reproductible) |
| ? | Orchestration (Prefect ou Airflow) |
| ? | Stockage Parquet pour le brut |
| ? | Cloud (base managée, stockage objet) |
| ? | Dashboard (Metabase ou Power BI) |
| ? | CDC (pertinent surtout si les sources sont des bases transactionnelles) |

Aucun de ces outils ne doit être ajouté au socle : ce sont des évolutions facultatives.

**Bonus** : enregistrez la démo en vidéo courte ; ajoutez un diagramme d'architecture.

## 5. Fichiers concernés

`docs/demo_script.md`, `sql/queries/analysis.sql`, `docs/roadmap.md`, `README.md`.

## 6. Commandes à exécuter

```bash
python -m src.main
cd dbt_project && dbt run && dbt test
psql -U pipeline_user -h localhost -d air_weather -f sql/queries/analysis.sql
```

## 7. Indices progressifs

- *Indice 1* : une bonne démo montre un **échec contrôlé** (rejets, journal), pas seulement le cas heureux.
- *Indice 2* : une requête d'analyse commence par la question en commentaire, puis le SQL.
- *Indice 3* : priorisez d'abord ce qui sécurise le projet (CI, tests), ensuite ce qui l'agrandit (incrémental, orchestration).

## 8. Critères de validation

- La démo tient en 10 minutes ou moins, sans improviser.
- Les requêtes d'analyse s'exécutent sur vos marts.
- La roadmap est priorisée et justifiée.
- Le dépôt est propre : pas de secrets, tests verts, historique de commits lisible.

## 9. Erreurs fréquentes et diagnostic

- **Démo trop technique** : commencez par le problème métier.
- **Aucune limite mentionnée** : donne l'impression que vous ne les connaissez pas.
- **Requêtes sur `staging` au lieu des marts** : elles contournent le travail de modélisation.
- **Roadmap fourre-tout** : sans ordre ni justification.

## 10. Livrable et commit

```
docs: add demo script and analysis queries
docs: add improvement roadmap
```

Pensez ensuite à un tag de version : `git tag -a v1.0.0 -m "First complete release"` puis `git push --tags`.

## 11. Question de contrôle / à me transmettre

Envoyez votre script de démo, vos requêtes d'analyse et votre roadmap. **Question** : si vous deviez ajouter une seule évolution demain, laquelle et pourquoi ?

---

# Par où continuer

1. **Terminez la Phase 0 et la Phase 1** si ce n'est pas fait, puis envoyez-moi leurs livrables.
2. Menez ensuite la Phase 2, puis 3 et 4 (indépendantes entre elles).
3. À chaque phase, collez votre code et vos erreurs : je vous répondrai par un diagnostic et une correction minimale.

Je peux aussi regrouper ces phases dans un second document Word, comme pour le plan général. Souhaitez-vous que je le fasse ?











