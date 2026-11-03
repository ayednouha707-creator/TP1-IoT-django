import json
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, db
from asgiref.sync import sync_to_async
from django.apps import apps
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# ---------------------------------------------------------------------------
# Firebase Realtime Database (Admin SDK avec la clé du compte de service)
# La clé firebase-key.json est à la racine du projet (à côté de manage.py)
# et elle est dans .gitignore -> JAMAIS sur GitHub.
# ---------------------------------------------------------------------------
FIREBASE_KEY = Path(settings.BASE_DIR) / "firebase-key.json"
FIREBASE_DB_URL = "https://gestion-grandeur-2a6fa-default-rtdb.firebaseio.com/"
FIREBASE_NODE = "mesures"  # noeud dans la Realtime DB

# initialisé UNE seule fois
if not firebase_admin._apps:
    firebase_admin.initialize_app(
        credentials.Certificate(str(FIREBASE_KEY)),
        {"databaseURL": FIREBASE_DB_URL},
    )


def _parse(message):
    """Accepte un str JSON ou un dict, et la clé 'valeur' ou 'value'."""
    data = json.loads(message) if isinstance(message, str) else message
    valeur = float(data.get("valeur", data.get("value")))
    date = parse_datetime(data.get("date_prise", "") or "") or timezone.now()
    return valeur, date


# ---------------------------------------------------------------------------
# 1) SQLite (Django ORM) - une mesure à la fois
# ---------------------------------------------------------------------------
@sync_to_async
def persist_mesure(message):
    Grandeur = apps.get_model('grandeurs', 'Grandeur')
    Mesure = apps.get_model('grandeurs', 'Mesure')

    valeur, date = _parse(message)
    grandeur = Grandeur.objects.get(nom="Temperature")
    mesure = Mesure.objects.create(valeur=valeur, datePrise=date, grandeur=grandeur)
    print(f"[SQLite] saved ✔ {mesure}")
    return mesure


# ---------------------------------------------------------------------------
# 2) SQLite (Django ORM) - par paquets de 100
# ---------------------------------------------------------------------------
buffer = []


@sync_to_async
def persist_mesure_bulk(message):
    Grandeur = apps.get_model('grandeurs', 'Grandeur')
    Mesure = apps.get_model('grandeurs', 'Mesure')

    valeur, date = _parse(message)
    grandeur = Grandeur.objects.get(nom="Temperature")
    buffer.append(Mesure(valeur=valeur, datePrise=date, grandeur=grandeur))

    if len(buffer) >= 100:
        Mesure.objects.bulk_create(buffer)
        print(f"[SQLite] inserted {len(buffer)} rows")
        buffer.clear()


# ---------------------------------------------------------------------------
# 3) Firebase Realtime Database
# ---------------------------------------------------------------------------
@sync_to_async
def persist_mesure_firebase(message):
    valeur, date = _parse(message)
    data = {
        "grandeur": "Temperature",
        "valeur": valeur,
        "date_prise": date.isoformat(),
    }
    ref = db.reference(FIREBASE_NODE).push(data)   # push = nouvelle clé unique
    print(f"[Firebase] saved ✔ {ref.key} -> {data}")
    return ref.key
