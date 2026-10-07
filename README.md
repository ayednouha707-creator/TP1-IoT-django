# gestion_grandeurs — Atelier service web (Django + IoT)

TP de l'atelier service web, classe **SEM31** (AU 2026-2027), enseignant Nizar MAATOUG.
Cette version couvre le TP **du début jusqu'au lancement de l'application MQTT**
(slide 49 : `mqttasgi --host localhost --port 1883 gestion_grandeurs.asgi:application`).

## Contenu

| Étape | Slides | Réalisation |
|---|---|---|
| Projet Django | 8-10 | environnement virtuel, `startproject gestion_grandeurs` |
| Applications | 11-12 | `website`, `grandeurs` |
| Modèles | 20-22 | `Grandeur` (nom, unité, min, max) et `Mesure` (valeur, date, FK grandeur) + migrations |
| Channels / Daphne | 42-44 | serveur ASGI, `ProtocolTypeRouter` (http) |
| MQTT consumer | 45-49 | app `mqtt_topics`, `MyMqttConsumer` abonné à `sensor/temperature`, protocole `mqtt` dans `asgi.py` |

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / Raspberry Pi
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

## Prérequis : Redis et Mosquitto

```bash
# Redis (Windows, Docker)
docker run -d --name redis-server -p 6379:6379 redis

# Mosquitto (Linux)
sudo apt install -y mosquitto mosquitto-clients
# Mosquitto (Windows) : installer depuis https://mosquitto.org/download/ puis
net start mosquitto
```

## Lancement

```bash
# serveur web (http://127.0.0.1:8000/admin/)
python manage.py runserver

# écoute MQTT
mqttasgi --host localhost --port 1883 gestion_grandeurs.asgi:application
```

Test avec un capteur simulé :

```bash
mosquitto_pub -h localhost -t sensor/temperature -m '{"val":80,"dep":"dep1"}'
```

Résultat attendu dans le terminal mqttasgi :

```
MQTT connected....
Received a message at topic: sensor/temperature
With payload b'{"val":80,"dep":"dep1"}'
And QOS: 2
```

## Corrections par rapport aux slides

- `asgi.py` (slide 48) : `DJANGO_SETTINGS_MODULE` vaut `gestion_grandeurs.settings` (et non `gestion_mesures.settings`).
- L'import du consumer est placé après `django.setup()`.

## Remarque Windows

Sous PowerShell, les guillemets du message JSON doivent être échappés :

```powershell
mosquitto_pub -h localhost -t sensor/temperature -m '{\"val\":80,\"dep\":\"dep1\"}'
```

Sous Windows, mqttasgi se connecte et s'abonne correctement (vérifié avec `mosquitto -v` :
`Received SUBSCRIBE … sensor/temperature (QoS 2)` puis `Sending PUBLISH to …`), mais la
réception des messages peut ne pas s'afficher. L'environnement prévu par le TP est Linux
(slide 26) ; sous Linux le consumer reçoit et affiche bien les messages.
