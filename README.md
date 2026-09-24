# ISTIR-IRIS

Application de bureau (Windows / Linux / macOS) permettant de se connecter aux postes de l'ISTIC et de l'ESIR via SSH, avec un terminal intégré et un explorateur de fichiers SFTP, le tout dans une interface graphique unique.

ISTIR-IRIS : ISTIC & ESIR Infrastructure Remote Interface System.

**Version actuelle : 1.1.2-dev**

## Fonctionnalités

- Détection automatique de la connexion au VPN de l'ISTIC (surveillance de l'interface réseau).
- Sélection d'une salle puis d'un poste depuis une liste préconfigurée.
- Connexion SSH avec authentification par mot de passe, terminal interactif intégré (xterm.js) via un vrai PTY.
- Panneau SFTP rétractable pour parcourir, télécharger et envoyer des fichiers sur le poste distant, sans quitter l'application.
- Thème clair / sombre.
- Interface responsive avec menu latéral escamotable.

## Prérequis

- Python 3.10 ou supérieur.
- Un accès au VPN de l'ISTIC actif au moment de la connexion SSH.
- Windows, Linux ou macOS.

## Installation

Cloner le dépôt puis installer les dépendances :

```bash
pip install -r data/requirements.txt
```

Le fichier `requirements.txt` gère automatiquement les dépendances spécifiques à chaque plateforme (`pywinpty` sous Windows, `ptyprocess` sous Linux/macOS).

## Lancement

Depuis la racine du projet :

```bash
python main.py
```

L'application ouvre une fenêtre native. Sélectionnez une salle et un poste, renseignez votre identifiant et votre mot de passe, puis cliquez sur "Se connecter".

## Notes techniques

- La détection du VPN vérifie qu'une interface réseau possède une adresse IP dans le sous-réseau `148.60.9.0/24`.
- La connexion SSH principale s'appuie sur le binaire `ssh` du système, piloté via un pseudo-terminal (PTY), pour permettre une authentification interactive identique à un terminal classique.
- La connexion SFTP utilise `paramiko` en parallèle, avec le même mot de passe, pour rester entièrement multiplateforme sans dépendre d'une version particulière d'OpenSSH.

## État du projet

Version en développement actif (1.1.0-dev). Les fonctionnalités de base (VPN, SSH, SFTP, thèmes) sont fonctionnelles ; des ajustements d'ergonomie et de robustesse sont encore en cours.