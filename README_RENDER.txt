CoRH - Déploiement sur Render

Build Command : pip install -r requirements.txt
Start Command : python server.py

Important :
- server.py utilise HOST=0.0.0.0 et le PORT fourni par Render.
- SQLite fonctionne, mais sans disque persistant les données peuvent être réinitialisées après redéploiement/redémarrage.
- Pour garder les données, ajoute un Persistent Disk sur Render et adapte DB_PATH vers ce disque.
