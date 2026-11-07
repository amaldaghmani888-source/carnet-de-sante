# Carnet de santé de la femme — prototype

Application web locale de démonstration créée avec Python/Flask et SQLite.

## Démarrage sous Windows (VS Code)
1. Décompresser le ZIP et ouvrir le dossier dans VS Code.
2. Ouvrir le terminal intégré.
3. Créer un environnement virtuel :
   `py -m venv .venv`
4. Activer :
   `.venv\\Scripts\\activate`
5. Installer les dépendances :
   `pip install -r requirements.txt`
6. Lancer :
   `python app.py`
7. Ouvrir dans le navigateur : `http://127.0.0.1:5000`

## Pages disponibles
Accueil, Profil (modification), Carnet médical (ajout d'entrées), Suivi du cancer du sein, Carnet de vaccination,
Rendez-vous (ajout), Rappels (ajout), Conseils santé, Documents, Paramètres.

## Important
- Les données pré-remplies sont fictives, uniquement pour démonstration.
- Ce prototype n'est pas un système médical validé et n'est pas prêt à héberger des données de santé réelles.
- Avant un déploiement réel, ajouter authentification sécurisée, contrôle d'accès, chiffrement, sauvegardes,
  journalisation, consentement, validation clinique et conformité à la législation marocaine applicable
  (notamment protection des données personnelles et exigences relatives aux données de santé).
- Changer `app.secret_key` avant tout déploiement.
