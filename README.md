# Air & Weather Pipeline

Pipeline de données local croisant **météo** et **qualité de l'air** pour 8 villes françaises sur 12 mois, au grain horaire. Il extrait des données d'API REST et de fichiers CSV/Excel, les nettoie avec Python/Pandas, les charge dans PostgreSQL (`raw` → `staging`), puis construit des tables analytiques avec dbt.

> **Statut** : `TODO: en cours / v1.0.0`
> Les passages marqués `TODO` sont à compléter avec vos résultats réels. Ne laissez aucun `TODO` avant la publication.

---

## Sommaire

1. [Contexte et objectifs](#1-contexte-et-objectifs)
2. [Architecture](#2-architecture)
3. [Stack technique](#3-stack-technique)
4. [Structure du dépôt](#4-structure-du-dépôt)
5. [Sources de données](#5-sources-de-données)
6. [Installation](#6-installation)
7. [Exécution](#7-exécution)
8. [Modèle de données](#8-modèle-de-données)
9. [Qualité de données](#9-qualité-de-données)
10. [Tests](#10-tests)
11. [Dépannage](#11-dépannage)
12. [Décisions techniques et compromis](#12-décisions-techniques-et-compromis)
13. [Hypothèses et limites](#13-hypothèses-et-limites)
14. [Résultats](#14-résultats)
15. [Évolutions possibles](#15-évolutions-possibles)

---

## 1. Contexte et objectifs

**Besoin métier (TODO: reprendre votre exercice 1 de la Phase 0, 5 à 8 lignes).**
Exemple de forme : une agence régionale souhaite suivre la météo et la pollution (PM2.5, PM10, NO2, ozone) pour repérer les épisodes de pollution et leurs liens avec les conditions météorologiques.

**Questions analytiques :**

- TODO: question 1 (ex. : quels jours la concentration de PM2.5 dépasse-t-elle un seuil, et quelle était la météo ?)
- TODO: question 2
- TODO: question 3

**Périmètre :**

| Élément | Valeur |
|---|---|
| Villes | 8 villes françaises (TODO: liste) |
| Période | TODO: ex. 2025-01-01 → 2025-12-31 |
| Grain brut | une ville, une heure |
| Fuseau de référence | TODO: ex. UTC en base, heure locale à l'analyse |

---

## 2. Architecture

```
SOURCES                    EXTRACTION            STOCKAGE BRUT            TRANSFORMATION (Python)
API météo (JSON)    ───►   src/extract/   ───►   data/raw/ (échantillons) ──►  src/transform/
API air (JSON)      ───►   src/extract/                                        src/quality/
CSV communes        ───►   src/extract/   ───►   data/external/                (nettoyage, validation,
Excel populations   ───►   src/extract/                                          jointures, rejets)
                                                          │
                                                          ▼
                                                 CHARGEMENT (src/load/)
                                                          │
                                                          ▼
 PostgreSQL :  raw  ───►  staging  ───►  (dbt) staging / intermediate  ───►  analytics (marts)
                              │
                              └── staging.rejected_rows (lignes rejetées + motif)
               ops.pipeline_run_log (journal des exécutions)

ORCHESTRATION : python -m src.main   │   LOGS : logs/   │   TESTS : pytest + dbt test
```

**Flux en deux temps :**

1. **ETL Python** (extraction, nettoyage, validation, chargement) alimente `raw` et `staging`.
2. **ELT dbt** reprend les tables `raw` comme sources et reconstruit la chaîne en SQL jusqu'aux marts.

Détails dans [`docs/architecture.md`](docs/architecture.md).

---

## 3. Stack technique

| Domaine | Outil |
|---|---|
| Langage | Python 3.TODO |
| Appels HTTP | `requests` |
| Manipulation de données | `pandas`, `openpyxl` |
| Accès base de données | `SQLAlchemy`, `psycopg` |
| Base de données | PostgreSQL TODO (version) |
| Transformation SQL | dbt Core + `dbt-postgres` |
| Configuration | `python-dotenv` |
| Tests | `pytest` |
| Versionnage | Git, GitHub |

---

## 4. Structure du dépôt

```
air-weather-pipeline/
├── README.md
├── .gitignore
├── .env.example            # modèle de configuration (valeurs factices)
├── requirements.txt        # dépendances d'exécution
├── requirements-dev.txt    # dépendances de développement (tests)
├── pyproject.toml
├── data/
│   ├── raw/                # échantillons bruts d'API (non versionnés)
│   ├── external/           # CSV / Excel téléchargés (non versionnés)
│   └── processed/
├── logs/                   # journaux d'exécution (non versionnés)
├── sql/
│   ├── ddl/                # création schémas et tables
│   └── queries/            # contrôles et requêtes d'analyse
├── src/
│   ├── config.py
│   ├── main.py             # point d'entrée du pipeline
│   ├── extract/            # API, CSV, Excel
│   ├── transform/          # nettoyage et mise en forme
│   ├── load/               # chargement PostgreSQL et journal
│   ├── quality/            # règles de qualité et profilage
│   └── utils/              # base de données, logging
├── tests/
├── docs/                   # architecture, dictionnaire, décisions
└── dbt_project/            # modèles dbt (staging, intermediate, marts)
```

---

## 5. Sources de données

> À compléter avec vos observations de la Phase 0. Vérifiez chaque URL, licence et limite dans la documentation officielle avant de publier.

| Source | Type | URL | Licence / conditions | Date de téléchargement | Limites connues |
|---|---|---|---|---|---|
| Météo historique | API REST (JSON) | TODO | TODO | n/a | TODO |
| Qualité de l'air | API REST (JSON) | TODO | TODO | n/a | TODO (profondeur d'historique, plage de dates) |
| Référentiel des communes | CSV | TODO | TODO | TODO | TODO |
| Populations légales | Excel | TODO | TODO | TODO | TODO |

Les fichiers CSV et Excel ne sont **pas** versionnés. Téléchargez-les depuis les URL ci-dessus et placez-les dans `data/external/` (voir [Installation](#6-installation)).

---

## 6. Installation

### Prérequis

- Python 3.TODO ou supérieur
- PostgreSQL TODO ou supérieur, en cours d'exécution
- Git

### Étapes

```bash
# 1. Cloner le dépôt
git clone <URL_DU_DEPOT>
cd air-weather-pipeline

# 2. Créer et activer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate            # Windows PowerShell : .venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install --upgrade pip
pip install -r requirements-dev.txt

# 4. Configurer l'environnement
cp .env.example .env                 # puis éditer .env avec vos valeurs locales
```

### Base de données

```bash
# Dans psql, en superutilisateur : TODO adapter à vos noms
#   CREATE ROLE pipeline_user WITH LOGIN PASSWORD '<mot_de_passe_local>';
#   CREATE DATABASE air_weather OWNER pipeline_user;

# Création des schémas et tables (ordre important)
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/001_create_schemas.sql
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/002_create_raw_tables.sql
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/003_create_staging_tables.sql
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/004_create_ops_tables.sql
```

### Fichiers externes

Placez dans `data/external/` :

- `TODO: nom du fichier CSV` (communes)
- `TODO: nom du fichier Excel` (populations)

### Vérification

```bash
python -m src.utils.db               # doit confirmer la connexion
pytest                               # les tests doivent passer
```

### Configuration (`.env`)

Aucune valeur réelle n'est versionnée. Les variables attendues sont listées dans `.env.example` :

| Variable | Description |
|---|---|
| `DB_HOST` | hôte PostgreSQL |
| `DB_PORT` | port PostgreSQL |
| `DB_NAME` | nom de la base |
| `DB_USER` | utilisateur |
| `DB_PASSWORD` | mot de passe (jamais versionné) |
| `TODO` | autres variables ajoutées par votre configuration |

---

## 7. Exécution

### Pipeline Python

```bash
python -m src.main
echo $?          # 0 = succès, non nul = échec (PowerShell : $LASTEXITCODE)
```

Le pipeline enchaîne : extraction → transformation → contrôles qualité → chargement `raw` et `staging` → journalisation.
Les logs sont écrits dans `logs/` (TODO: nom du fichier). Chaque exécution est tracée dans `ops.pipeline_run_log`.

TODO: documenter les options de ligne de commande si vous en avez ajouté.

### dbt

dbt s'installe dans un **environnement virtuel séparé** (voir [décisions](#12-décisions-techniques-et-compromis)).

```bash
cd dbt_project
dbt debug                # vérifie la configuration et la connexion
dbt run                  # construit staging, intermediate et marts
dbt test                 # exécute les tests de qualité
dbt docs generate        # génère la documentation
dbt docs serve           # ouvre la documentation et le graphe de dépendances
```

Le fichier `profiles.yml` est **hors dépôt** (`~/.dbt/profiles.yml`) et lit le mot de passe via `env_var`.
TODO: ajouter ici un exemple de `profiles.yml` avec des valeurs factices.

### Idempotence

Relancer le pipeline donne le même résultat : TODO: décrire votre stratégie (truncate + reload, upsert) et ce que vous avez vérifié.

---

## 8. Modèle de données

| Schéma | Table | Rôle |
|---|---|---|
| `raw` | `weather_hourly_raw` | météo horaire telle que reçue |
| `raw` | `air_quality_hourly_raw` | qualité de l'air horaire telle que reçue |
| `raw` | `communes_ref_raw` | référentiel des communes |
| `raw` | `population_ref_raw` | populations légales |
| `staging` | `city` | dimension ville |
| `staging` | `weather_observation` | météo nettoyée |
| `staging` | `air_quality_observation` | qualité de l'air nettoyée |
| `staging` | `rejected_rows` | lignes rejetées avec motif |
| `ops` | `pipeline_run_log` | journal des exécutions |
| `analytics` | `TODO: vos marts dbt` | tables analytiques finales |

> Noms indicatifs : alignez-les sur vos DDL réels.

**Grain et clés :**

| Table | Grain | Clé primaire |
|---|---|---|
| `staging.weather_observation` | une ville, une heure | TODO |
| `staging.air_quality_observation` | une ville, une heure | TODO |
| `staging.city` | une ville | TODO |

Dictionnaire complet : [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## 9. Qualité de données

### Règles appliquées

| ID | Table | Dimension | Règle | Action en cas d'échec |
|---|---|---|---|---|
| DQ-01 | TODO | complétude | TODO (ex. timestamp non nul) | rejeter la ligne |
| DQ-02 | TODO | validité | TODO (ex. PM2.5 ≥ 0) | rejeter la ligne |
| DQ-03 | TODO | unicité | TODO (pas de doublon sur la clé) | TODO |
| DQ-04 | TODO | cohérence | TODO (ville existante dans la dimension) | TODO |
| DQ-05 | TODO | validité | TODO (plage de température plausible) | TODO |
| DQ-06 | TODO | volumétrie | TODO (24 × nombre de jours par ville) | TODO |
| DQ-07 | TODO | TODO | TODO | TODO |
| DQ-08 | TODO | TODO | TODO | TODO |

### Gestion des rejets

Les lignes invalides sont écrites dans `staging.rejected_rows` avec le code de la règle, la ligne d'origine et l'identifiant d'exécution. Le pipeline échoue si le taux de rejet dépasse **TODO: seuil**.

### Tests dbt

TODO: lister vos tests (`not_null`, `unique`, `relationships`, `accepted_values`, tests singuliers).

---

## 10. Tests

```bash
pytest -v                      # tests Python (aucun accès réseau requis)
cd dbt_project && dbt test     # tests de données dbt
```

| Zone | Ce qui est testé |
|---|---|
| Extraction API | succès, retry, erreurs HTTP, JSON invalide (requêtes simulées) |
| Lecture de fichiers | codes INSEE conservés en texte, colonnes standardisées |
| Transformation | TODO: au moins 3 règles de qualité |
| Chargement | TODO: idempotence, rollback |

---

## 11. Dépannage

> Complétez avec **les erreurs que vous avez réellement rencontrées**. Les lignes ci-dessous sont des points de départ à vérifier et à adapter.

| Symptôme | Cause probable | Solution |
|---|---|---|
| `ModuleNotFoundError` | environnement virtuel non activé | `source .venv/bin/activate` |
| `password authentication failed` | mot de passe erroné dans `.env` ou rôle sans `LOGIN` | vérifier `.env` et `\du` dans `psql` |
| `Peer authentication failed` | connexion par socket locale | utiliser `-h localhost` |
| Codes INSEE à 4 chiffres | lecture en entier (zéros perdus) | lire la colonne avec `dtype=str` |
| `FileNotFoundError` sur un CSV/Excel | fichier absent de `data/external/` | télécharger selon la section Sources |
| Le pipeline renvoie 0 malgré une erreur | exception avalée | TODO: votre cas réel |
| `dbt debug` échoue | `profiles.yml` absent ou variable d'environnement manquante | TODO: votre cas réel |
| TODO | TODO | TODO |

---

## 12. Décisions techniques et compromis

Chaque décision suit la forme : *choix, alternative écartée, raison, compromis*. Détails dans [`docs/decisions.md`](docs/decisions.md).

| Décision | Alternative | Raison | Compromis |
|---|---|---|---|
| Heures stockées en `timestamptz` (UTC) | `timestamp` sans fuseau | éviter l'ambiguïté du changement d'heure | TODO |
| Couche `raw` tolérante, `staging` stricte | contraintes strictes partout | un défaut de la source ne doit pas bloquer l'ingestion brute | TODO |
| `truncate + reload` au départ | upsert dès le début | simplicité et idempotence immédiate | TODO |
| dbt dans un venv séparé | même venv que le pipeline | éviter les conflits de dépendances | TODO |
| TODO: choix des villes / période | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |

---

## 13. Hypothèses et limites

**Hypothèses :**

- TODO: ex. les coordonnées envoyées aux API représentent correctement la ville.
- TODO: ex. le référentiel des communes est à jour à la date de téléchargement.

**Limites connues :**

- TODO: ex. une ville est représentée par un point (une coordonnée), pas par une zone.
- TODO: ex. les données de qualité de l'air sont issues de modèles, pas de stations de mesure (à vérifier dans la documentation de la source).
- TODO: ex. ingestion complète à chaque exécution, pas d'incrémental.
- TODO: ex. pipeline local, sans planification.

---

## 14. Résultats

> À renseigner après une exécution complète.

| Indicateur | Valeur |
|---|---|
| Lignes extraites (météo / air) | TODO |
| Lignes valides / rejetées | TODO |
| Taux de rejet | TODO |
| Durée d'exécution | TODO |
| Modèles dbt / tests dbt | TODO |

**Enseignements tirés des données :** TODO (2 à 3 constats issus de vos marts).

---

## 15. Évolutions possibles

Évolutions facultatives, hors du socle initial, classées par priorité (TODO: ajuster selon votre analyse valeur/effort) :

1. CI GitHub Actions (tests à chaque push)
2. Tests de données avancés
3. Ingestion incrémentale
4. Docker
5. Orchestration (Prefect ou Airflow)
6. Stockage Parquet pour la zone brute
7. Déploiement cloud
8. Dashboard (Metabase ou Power BI)

---

## Licence et crédits

TODO: licence du code. Les données restent soumises aux licences de leurs sources respectives (voir [Sources de données](#5-sources-de-données)).
#   A i r - W e a t h e r - P i p e l i n e  
 