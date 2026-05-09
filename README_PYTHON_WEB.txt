CoRH - Version web avec Python

Cette version contient :
- index.html : interface HTML/CSS/JavaScript
- server.py : backend Python local
- corh_web.sqlite3 : base SQLite creee automatiquement au premier lancement

Lancer l'application web avec Python :

1. Ouvrir PowerShell dans ce dossier.
2. Executer :

   python server.py

3. Le navigateur s'ouvre sur :

   http://127.0.0.1:8000

Important :
- Si vous ouvrez index.html directement, l'application utilise localStorage.
- Si vous lancez python server.py, les donnees sont stockees dans SQLite.
- Sur Netlify, Python ne fonctionne pas directement. Netlify publie seulement la partie statique index.html.

Comptes de test :
- Responsable RH : admin / admin123
- Employe : sara / 1234
