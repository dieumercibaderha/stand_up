import requests

# URL de l'API ou du site web auquel tu veux accéder
url = 'http://127.0.0.1:8000/api/list_user/?format=json'

# Faire une requête GET
response = requests.get(url)

# Vérifier que la requête a réussi
if response.status_code == 200:
    # Traiter la réponse (par exemple, afficher le contenu)
    print(response.json())
else:
    print(f"Erreur : {response.json()}")
    

[{'id': 1, 'password': 'pbkdf2_sha256$600000$bkp3M556rF8fN2jeqATp0U$CQKWMXZsgYhiwDSzLTvCw+oIniagBkhQiMJBxBRpYwo=', 'last_login': '2024-11-19T08:59:16.024300Z', 'is_superuser': False, 'username': 'BADERHA', 'first_name': 'MAHAMULI', 'last_name': 'DI', 'email': 'dieumercibaderha1@gmail.com', 'is_staff': False, 'is_active': True, 'date_joined': '2024-11-19T08:59:00.217536Z', 'Photo': 'http://127.0.0.1:8000/Images/Images/CEPHA_SHOW_cgZsK8V.jpg', 'statut': 'IT', 'Organisation': 'STAND_UP', 'Lieu': 'GOMA', 'Nom': 'BADERHA', 'Dates': '2024-11-19T08:59:01.644759Z', 'Etat_civil': 'marié', 'Stand_up': True, 'Matricule': 'ADMIN', 'groups': [], 'user_permissions': []}, {'id': 2, 'password': 'pbkdf2_sha256$600000$tytQkLVnLA3Q6X4k9YxXpa$TI6bt+azYVij0g+K9aVZtjVIj2T8AW112yDaCsp8NHg=', 'last_login': None, 'is_superuser': False, 'username': 'SENET2024BBL-RECO', 'first_name': 'BADERHA', 'last_name': 'LEO', 'email': 'dieumercibaderha1@gmail.com', 'is_staff': False, 'is_active': True, 'date_joined': '2024-11-19T09:04:48.151742Z', 'Photo': 'http://127.0.0.1:8000/Images/Images/COCO1_oBeQiCG.jpg', 'statut': 'RECO', 'Organisation': 'BCZ', 'Lieu': 'GOMA', 'Nom': 'BADERHA2', 'Dates': '2024-11-19T09:04:53.568254Z', 'Etat_civil': 'Célibataire', 'Stand_up': False, 'Matricule': 'SENET2024BBL-RECO', 'groups': [], 'user_permissions': []}]
