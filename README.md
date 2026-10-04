<h1>🌤️ Air &amp; Weather Pipeline</h1>

<p>
  Pipeline de données local croisant les données de <strong>météo</strong> et de
  <strong>qualité de l’air</strong> pour huit villes françaises sur douze mois,
  au grain horaire.
</p>

<p>
  Le projet extrait des données depuis des API REST ainsi que des fichiers CSV/Excel,
  les nettoie avec Python et Pandas, les charge dans PostgreSQL
  (<code>raw</code> → <code>staging</code>), puis construit des tables analytiques avec dbt.
</p>

<p>
  <strong>Statut :</strong> <code>TODO: en cours / v1.0.0</code><br>
  Les passages marqués <code>TODO</code> sont à compléter avec vos résultats réels.
  Ne laissez aucun <code>TODO</code> avant publication.
</p>

<hr>

<h2>Sommaire</h2>

<ol>
  <li><a href="#contexte-et-objectifs">Contexte et objectifs</a></li>
  <li><a href="#architecture">Architecture</a></li>
  <li><a href="#stack-technique">Stack technique</a></li>
  <li><a href="#structure-du-depot">Structure du dépôt</a></li>
  <li><a href="#sources-de-donnees">Sources de données</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#execution">Exécution</a></li>
  <li><a href="#modele-de-donnees">Modèle de données</a></li>
  <li><a href="#qualite-de-donnees">Qualité de données</a></li>
  <li><a href="#tests">Tests</a></li>
  <li><a href="#depannage">Dépannage</a></li>
  <li><a href="#decisions-techniques-et-compromis">Décisions techniques et compromis</a></li>
  <li><a href="#hypotheses-et-limites">Hypothèses et limites</a></li>
  <li><a href="#resultats">Résultats</a></li>
  <li><a href="#evolutions-possibles">Évolutions possibles</a></li>
</ol>

<hr>

<h2 id="contexte-et-objectifs">1. Contexte et objectifs</h2>

<h3>Besoin métier</h3>

<p>
  <strong>TODO :</strong> reprendre votre exercice 1 de la Phase 0, en 5 à 8 lignes.
</p>

<p>
  Exemple : une agence régionale souhaite suivre les conditions météorologiques et
  les niveaux de pollution atmosphérique (PM2.5, PM10, NO2 et ozone), afin
  d’identifier les épisodes de pollution et leurs liens avec la météo.
</p>

<h3>Questions analytiques</h3>

<ul>
  <li><strong>TODO :</strong> Quels jours la concentration de PM2.5 dépasse-t-elle un seuil, et quelles étaient les conditions météorologiques associées ?</li>
  <li><strong>TODO :</strong> Question analytique n°2.</li>
  <li><strong>TODO :</strong> Question analytique n°3.</li>
</ul>

<h3>Périmètre</h3>

<table>
  <thead>
    <tr>
      <th>Élément</th>
      <th>Valeur</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Villes</td>
      <td>8 villes françaises (<code>TODO: liste</code>)</td>
    </tr>
    <tr>
      <td>Période</td>
      <td><code>TODO: ex. 2025-01-01 → 2025-12-31</code></td>
    </tr>
    <tr>
      <td>Grain brut</td>
      <td>Une ville, une heure</td>
    </tr>
    <tr>
      <td>Fuseau de référence</td>
      <td><code>TODO: ex. UTC en base, heure locale à l’analyse</code></td>
    </tr>
  </tbody>
</table>

<hr>

<h2 id="architecture">2. Architecture</h2>

<pre><code>SOURCES                    EXTRACTION            STOCKAGE BRUT            TRANSFORMATION (Python)

API météo (JSON)    ───►   src/extract/   ───►   data/raw/                ──►  src/transform/
API air (JSON)      ───►   src/extract/                                        src/quality/
CSV communes        ───►   src/extract/   ───►   data/external/                nettoyage, validation,
Excel populations   ───►   src/extract/                                          jointures, rejets
                                                          │
                                                          ▼
                                                 CHARGEMENT (src/load/)
                                                          │
                                                          ▼
PostgreSQL : raw ───► staging ───► dbt staging / intermediate ───► analytics (marts)
                             │
                             └── staging.rejected_rows
                                 lignes rejetées + motif

ops.pipeline_run_log : journal des exécutions

ORCHESTRATION : python -m src.main
LOGS          : logs/
TESTS         : pytest + dbt test
</code></pre>

<h3>Flux en deux temps</h3>

<ol>
  <li>
    <strong>ETL Python :</strong> extraction, nettoyage, validation et chargement
    vers les schémas <code>raw</code> et <code>staging</code>.
  </li>
  <li>
    <strong>ELT dbt :</strong> réutilisation des tables brutes ou de staging
    comme sources, puis transformations SQL jusqu’aux tables analytiques finales.
  </li>
</ol>

<p>
  Voir également :
  <a href="docs/architecture.md"><code>docs/architecture.md</code></a>.
</p>

<hr>

<h2 id="stack-technique">3. Stack technique</h2>

<table>
  <thead>
    <tr>
      <th>Domaine</th>
      <th>Outil</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Langage</td>
      <td>Python 3.<code>TODO</code></td>
    </tr>
    <tr>
      <td>Appels HTTP</td>
      <td><code>requests</code></td>
    </tr>
    <tr>
      <td>Manipulation de données</td>
      <td><code>pandas</code>, <code>openpyxl</code></td>
    </tr>
    <tr>
      <td>Accès base de données</td>
      <td><code>SQLAlchemy</code>, <code>psycopg</code></td>
    </tr>
    <tr>
      <td>Base de données</td>
      <td>PostgreSQL <code>TODO: version</code></td>
    </tr>
    <tr>
      <td>Transformation SQL</td>
      <td>dbt Core + <code>dbt-postgres</code></td>
    </tr>
    <tr>
      <td>Configuration</td>
      <td><code>python-dotenv</code></td>
    </tr>
    <tr>
      <td>Tests</td>
      <td><code>pytest</code></td>
    </tr>
    <tr>
      <td>Versionnage</td>
      <td>Git, GitHub</td>
    </tr>
  </tbody>
</table>

<hr>

<h2 id="structure-du-depot">4. Structure du dépôt</h2>

<pre><code>air-weather-pipeline/
├── README.md
├── .gitignore
├── .env.example            # Modèle de configuration avec valeurs factices
├── requirements.txt        # Dépendances d’exécution
├── requirements-dev.txt    # Dépendances de développement et de tests
├── pyproject.toml
├── data/
│   ├── raw/                # Échantillons bruts d’API, non versionnés
│   ├── external/           # CSV / Excel téléchargés, non versionnés
│   └── processed/
├── logs/                   # Journaux d’exécution, non versionnés
├── sql/
│   ├── ddl/                # Création des schémas et tables
│   └── queries/            # Contrôles et requêtes d’analyse
├── src/
│   ├── config.py
│   ├── main.py             # Point d’entrée du pipeline
│   ├── extract/            # API, CSV, Excel
│   ├── transform/          # Nettoyage et mise en forme
│   ├── load/               # Chargement PostgreSQL et journalisation
│   ├── quality/            # Règles de qualité et profilage
│   └── utils/              # Base de données, logging
├── tests/
├── docs/                   # Architecture, dictionnaire, décisions
└── dbt_project/            # Modèles dbt : staging, intermediate, marts
</code></pre>


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
#   A i r - W e a t h e r - P i p e l i n e 
 
 
