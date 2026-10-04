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
  <a href="docs/guide.md"><code>docs/guide.md</code></a>.
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

# 2. Créer et activer l’environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell :
# .venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install --upgrade pip
pip install -r requirements-dev.txt

# 4. Configurer l’environnement
cp .env.example .env

# Éditer ensuite le fichier .env avec vos valeurs locales.
</code></pre>

<h3>Base de données</h3>

<pre><code class="language-bash"># Dans psql, en superutilisateur :
# TODO : adapter les noms à votre environnement local
#
# CREATE ROLE pipeline_user WITH LOGIN PASSWORD '&lt;mot_de_passe_local&gt;';
# CREATE DATABASE air_weather OWNER pipeline_user;

# Création des schémas et tables : respecter l’ordre
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/001_create_schemas.sql
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/002_create_raw_tables.sql
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/003_create_staging_tables.sql
psql -U pipeline_user -h localhost -d air_weather -f sql/ddl/004_create_ops_tables.sql
</code></pre>

<h3>Fichiers externes</h3>

<p>Placez les fichiers suivants dans <code>data/external/</code> :</p>

<ul>
  <li><code>TODO: nom du fichier CSV</code> — référentiel des communes</li>
  <li><code>TODO: nom du fichier Excel</code> — populations</li>
</ul>

<h3>Vérification</h3>

<pre><code class="language-bash">python -m src.utils.db
pytest
</code></pre>

<p>
  La commande de connexion doit confirmer l’accès à PostgreSQL et les tests doivent passer.
</p>

<h3>Configuration : <code>.env</code></h3>

<p>
  Aucune valeur réelle ne doit être versionnée. Les variables attendues figurent dans
  <code>.env.example</code>.
</p>

<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>DB_HOST</code></td>
      <td>Hôte PostgreSQL</td>
    </tr>
    <tr>
      <td><code>DB_PORT</code></td>
      <td>Port PostgreSQL</td>
    </tr>
    <tr>
      <td><code>DB_NAME</code></td>
      <td>Nom de la base de données</td>
    </tr>
    <tr>
      <td><code>DB_USER</code></td>
      <td>Utilisateur PostgreSQL</td>
    </tr>
    <tr>
      <td><code>DB_PASSWORD</code></td>
      <td>Mot de passe, jamais versionné</td>
    </tr>
    <tr>
      <td><code>TODO</code></td>
      <td>Autres variables ajoutées à la configuration</td>
    </tr>
  </tbody>
</table>

<hr>

<h2 id="execution">7. Exécution</h2>

<h3>Pipeline Python</h3>

<pre><code class="language-bash">python -m src.main

# Linux / macOS
echo $?

# Windows PowerShell
$LASTEXITCODE
</code></pre>

<p>
  Le pipeline enchaîne les opérations suivantes :
  extraction → transformation → contrôles qualité → chargement
  <code>raw</code> et <code>staging</code> → journalisation.
</p>

<ul>
  <li>Les logs sont écrits dans <code>logs/</code> — <code>TODO: nom du fichier</code>.</li>
  <li>Chaque exécution est tracée dans <code>ops.pipeline_run_log</code>.</li>
  <li><code>TODO:</code> documenter les options de ligne de commande si elles existent.</li>
</ul>

<h3>dbt</h3>

<p>
  dbt est installé dans un <strong>environnement virtuel séparé</strong>
  afin d’éviter les conflits de dépendances avec le pipeline Python.
</p>

<pre><code class="language-bash">cd dbt_project

dbt debug
dbt run
dbt test
dbt docs generate
dbt docs serve
</code></pre>

<ul>
  <li><code>dbt debug</code> : vérifie la configuration et la connexion.</li>
  <li><code>dbt run</code> : construit les modèles staging, intermediate et marts.</li>
  <li><code>dbt test</code> : exécute les tests de qualité.</li>
  <li><code>dbt docs generate</code> : génère la documentation dbt.</li>
  <li><code>dbt docs serve</code> : ouvre la documentation et le graphe de dépendances.</li>
</ul>

<p>
  Le fichier <code>profiles.yml</code> est hors dépôt :
  <code>~/.dbt/profiles.yml</code>. Il doit récupérer les secrets via
  <code>env_var</code>.
</p>

<p>
  <code>TODO:</code> ajouter un exemple de <code>profiles.yml</code> avec des valeurs factices.
</p>

<h3>Idempotence</h3>

<p>
  Relancer le pipeline doit donner le même résultat.
  <code>TODO:</code> décrire la stratégie réellement retenue :
  <code>truncate + reload</code>, <code>upsert</code> ou une autre méthode,
  ainsi que les vérifications réalisées.
</p>

<hr>

<h2 id="modele-de-donnees">8. Modèle de données</h2>

<table>
  <thead>
    <tr>
      <th>Schéma</th>
      <th>Table</th>
      <th>Rôle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>raw</code></td>
      <td><code>weather_hourly_raw</code></td>
      <td>Données météorologiques horaires telles que reçues</td>
    </tr>
    <tr>
      <td><code>raw</code></td>
      <td><code>air_quality_hourly_raw</code></td>
      <td>Données de qualité de l’air horaires telles que reçues</td>
    </tr>
    <tr>
      <td><code>raw</code></td>
      <td><code>communes_ref_raw</code></td>
      <td>Référentiel des communes</td>
    </tr>
    <tr>
      <td><code>raw</code></td>
      <td><code>population_ref_raw</code></td>
      <td>Populations légales</td>
    </tr>
    <tr>
      <td><code>staging</code></td>
      <td><code>city</code></td>
      <td>Dimension ville</td>
    </tr>
    <tr>
      <td><code>staging</code></td>
      <td><code>weather_observation</code></td>
      <td>Météo nettoyée et standardisée</td>
    </tr>
    <tr>
      <td><code>staging</code></td>
      <td><code>air_quality_observation</code></td>
      <td>Qualité de l’air nettoyée et standardisée</td>
    </tr>
    <tr>
      <td><code>staging</code></td>
      <td><code>rejected_rows</code></td>
      <td>Lignes rejetées avec le motif du rejet</td>
    </tr>
    <tr>
      <td><code>ops</code></td>
      <td><code>pipeline_run_log</code></td>
      <td>Journal des exécutions du pipeline</td>
    </tr>
    <tr>
      <td><code>analytics</code></td>
      <td><code>TODO: vos marts dbt</code></td>
      <td>Tables analytiques finales</td>
    </tr>
  </tbody>
</table>

<p>
  Les noms ci-dessus sont indicatifs : alignez-les avec vos scripts DDL réels.
</p>

<h3>Grain et clés</h3>

<table>
  <thead>
    <tr>
      <th>Table</th>
      <th>Grain</th>
      <th>Clé primaire</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>staging.weather_observation</code></td>
      <td>Une ville, une heure</td>
      <td><code>TODO</code></td>
    </tr>
    <tr>
      <td><code>staging.air_quality_observation</code></td>
      <td>Une ville, une heure</td>
      <td><code>TODO</code></td>
    </tr>
    <tr>
      <td><code>staging.city</code></td>
      <td>Une ville</td>
      <td><code>TODO</code></td>
    </tr>
  </tbody>
</table>

<p>
  Dictionnaire complet :
  <a href="docs/data_dictionary.md"><code>docs/data_dictionary.md</code></a>.
</p>

<hr>

<h2 id="qualite-de-donnees">9. Qualité de données</h2>

<h3>Règles appliquées</h3>

<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Table</th>
      <th>Dimension</th>
      <th>Règle</th>
      <th>Action en cas d’échec</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>DQ-01</td>
      <td><code>TODO</code></td>
      <td>Complétude</td>
      <td><code>TODO: ex. timestamp non nul</code></td>
      <td>Rejeter la ligne</td>
    </tr>
    <tr>
      <td>DQ-02</td>
      <td><code>TODO</code></td>
      <td>Validité</td>
      <td><code>TODO: ex. PM2.5 ≥ 0</code></td>
      <td>Rejeter la ligne</td>
    </tr>
    <tr>
      <td>DQ-03</td>
      <td><code>TODO</code></td>
      <td>Unicité</td>
      <td><code>TODO: absence de doublon sur la clé</code></td>
      <td><code>TODO</code></td>
    </tr>
    <tr>
      <td>DQ-04</td>
      <td><code>TODO</code></td>
      <td>Cohérence</td>
      <td><code>TODO: ville présente dans la dimension</code></td>
      <td><code>TODO</code></td>
    </tr>
    <tr>
      <td>DQ-05</td>
      <td><code>TODO</code></td>
      <td>Validité</td>
      <td><code>TODO: plage de température plausible</code></td>
      <td><code>TODO</code></td>
    </tr>
    <tr>
      <td>DQ-06</td>
      <td><code>TODO</code></td>
      <td>Volumétrie</td>
      <td><code>TODO: 24 × nombre de jours par ville</code></td>
      <td><code>TODO</code></td>
    </tr>
    <tr>
      <td>DQ-07</td>
      <td><code>TODO</code></td>
      <td><code>TODO</code></td>
      <td><code>TODO</code></td>
      <td><code>TODO</code></td>
    </tr>
    <tr>
      <td>DQ-08</td>
      <td><code>TODO</code></td>
      <td><code>TODO</code></td>
      <td><code>TODO</code></td>
      <td><code>TODO</code></td>
    </tr>
  </tbody>
</table>

<h3>Gestion des rejets</h3>

<p>
  Les lignes invalides sont enregistrées dans <code>staging.rejected_rows</code>
  avec le code de règle, la ligne d’origine et l’identifiant d’exécution.
</p>

<p>
  Le pipeline échoue si le taux de rejet dépasse
  <strong><code>TODO: seuil</code></strong>.
</p>

<h3>Tests dbt</h3>

<p>
  <code>TODO:</code> lister les tests mis en œuvre :
  <code>not_null</code>, <code>unique</code>, <code>relationships</code>,
  <code>accepted_values</code> et les tests singuliers.
</p>

<hr>

<h2 id="tests">10. Tests</h2>

<pre><code class="language-bash">pytest -v

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