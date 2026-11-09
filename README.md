# 🌦️ Observatoire Météo

API REST développée en Python dans le cadre de ma formation de développeuse en intelligence artificielle.

## Présentation

L'Observatoire Météo permet de gérer des villes, de consulter leurs conditions météorologiques actuelles grâce à Open-Meteo et d'enregistrer les relevés dans une base SQLite.

## Technologies utilisées

- **Python** — langage de programmation
- **FastAPI** — création de l'API REST
- **Requests** — requêtes HTTP vers Open-Meteo
- **Pydantic** — validation des données
- **SQLModel / SQLAlchemy** — accès à la base via un ORM
- **SQLite** — stockage des villes et relevés
- **Uvicorn** — serveur ASGI
- **Swagger UI** — documentation interactive

## Fonctionnalités

- Ajouter une ville avec ses coordonnées géographiques
- Consulter la liste des villes
- Rechercher une ville par identifiant
- Récupérer la température et la vitesse du vent actuelles
- Enregistrer les relevés météorologiques
- Calculer des statistiques simples
- Gérer les erreurs HTTP

## Architecture du projet

```text
app/
├── main.py
├── core/
│   ├── config.py
│   └── database.py
├── models/
│   ├── ville.py
│   └── releve.py
├── repositories/
│   ├── ville_repository.py
│   └── releve_repository.py
├── services/
│   ├── ville_service.py
│   └── meteo_service.py
└── api/
    ├── deps.py
    └── v1/
        ├── router.py
        ├── routes/
        │   ├── villes.py
        │   └── meteo.py
        └── schemas/
            ├── ville.py
            └── meteo.py
```

Les responsabilités sont réparties entre les **routes** (requêtes HTTP), les **services** (logique métier) et les **repositories** (accès à SQLite).

## Installation

Cloner le dépôt, puis ouvrir un terminal à sa racine.

Créer un environnement virtuel :

```powershell
python -m venv .venv
```

Activer l'environnement sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

## Démarrage

```powershell
python -m uvicorn app.main:app --reload
```

Documentation Swagger : http://127.0.0.1:8000/docs

La base SQLite et ses tables sont créées automatiquement au démarrage si elles n'existent pas.

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/villes` | Liste les villes |
| POST | `/villes` | Ajoute une ville |
| GET | `/villes/{ville_id}` | Consulte une ville |
| GET | `/meteo/{ville_id}` | Récupère et enregistre la météo actuelle |

### Exemple d'ajout de ville

Requête `POST /villes` :

```json
{
  "nom": "Saint-Quentin",
  "latitude": 49.8489,
  "longitude": 3.2876
}
```

Réponse attendue : **201 Created**.

Pour consulter sa météo, utiliser ensuite `GET /meteo/{ville_id}` avec l'identifiant attribué par SQLite.

## Codes HTTP

| Code | Signification |
|---|---|
| 200 | Requête réussie |
| 201 | Ville créée |
| 404 | Ville introuvable |
| 409 | Ville déjà enregistrée |
| 422 | Données de requête invalides |
| 502 | Erreur de récupération des données météo |

## Statistiques

Le script `statistiques.py` permet de consulter :

- Le nombre total de relevés
- La température moyenne par ville
- La température minimale
- La température maximale

Exécution depuis la racine du projet :

```powershell
python statistiques.py
```

Des relevés doivent avoir été enregistrés au préalable.

## Remarques

- Les données météo proviennent de l'API **Open-Meteo**.
- Une connexion Internet est nécessaire pour récupérer les données.
- Le fichier local `meteo.db` est exclu du dépôt Git.
- Au premier démarrage, ajouter des villes via Swagger avant de consulter leur météo.

---

**Projet Fil Rouge — Observatoire Météo**  
Formation Développeuse en Intelligence Artificielle — Novembre 2026
