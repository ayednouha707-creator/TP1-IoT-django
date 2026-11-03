from django.utils.dateparse import parse_datetime

from asgiref.sync import sync_to_async
import json

from django.apps import apps
from proto import message

@sync_to_async
def persist_mesure(message):
   
    
    Grandeur = apps.get_model('grandeurs', 'Grandeur')
    Messure = apps.get_model('grandeurs', 'Mesure')

    message=json.loads(message)

    grandeur = Grandeur.objects.get(nom="Temperature")
    print(f"persist_mesure: {message}")
    Messure.objects.create(
        valeur=float(message["valeur"]),
        date_prise=parse_datetime(message["date_prise"]),
        grandeur=grandeur
    )


buffer = []

@sync_to_async
def persist_mesure_bulk(message):
    from grandeurs.models import Grandeur, Mesure

    message = json.loads(message)  

    global buffer

    buffer.append(
        Mesure(
            valeur=float(message["valeur"]),
            date_prise=parse_datetime(message["date_prise"])
            )
    )

    if len(buffer) >= 100:
        Mesure.objects.bulk_create(buffer)
        print(f"Inserted {len(buffer)}rows")
        buffer.clear()
        