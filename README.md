# 📋 Système de Gestion de Factures Django

Un système complet de gestion de factures construit avec **Django**, conçu pour faciliter la création, le suivi et la gestion des factures clients. Le projet inclut la génération de PDF, la gestion des clients, et un système de paiement intégré.

---

## 📑 Table des matières

- [Caractéristiques principales](#caractéristiques-principales)
- [Architecture du projet](#architecture-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure de la base de données](#structure-de-la-base-de-données)
- [API et URLs](#api-et-urls)
- [Déploiement](#déploiement)
- [Technologies utilisées](#technologies-utilisées)
- [Contribution](#contribution)

---

## ✨ Caractéristiques principales

### 🎯 Gestion des Factures

- ✅ Création de factures avec articles multiples
- ✅ Génération automatique de PDF téléchargeables
- ✅ Suivi du statut de paiement (payée/non payée)
- ✅ Mise à jour en masse du statut de paiement
- ✅ Trois types de factures : Reçu, Facture Pro-forma, Facture standard
- ✅ Historique complet des modifications
- ✅ Recherche et filtrage en temps réel
- ✅ Export des données

### 👥 Gestion des Clients

- ✅ Création et modification de profils clients
- ✅ Stockage des informations complètes (nom, email, téléphone, adresse, etc.)
- ✅ Suivi des factures par client
- ✅ Calcul automatique du total des factures par client
- ✅ Validation des données (email unique, format téléphone)
- ✅ Profils clients détaillés avec informations personnelles
- ✅ Gestion d'adresses complètes

### 📊 Articles et Lignes de Facture

- ✅ Ajout de multiples articles par facture
- ✅ Calcul automatique des totaux (quantité × prix unitaire)
- ✅ Validation des prix et quantités
- ✅ Formset Django pour gestion facile des articles
- ✅ Édition rapide des articles

### 🔐 Sécurité et Authentification

- ✅ Authentification obligatoire pour tous les utilisateurs
- ✅ Restriction d'accès aux superutilisateurs
- ✅ Logging complet des actions
- ✅ Protection CSRF intégrée
- ✅ Validation des formulaires côté serveur
- ✅ Tokens CSRF pour les requêtes AJAX
- ✅ Chiffrement des données sensibles

### 🌍 Internationalisation

- ✅ Support du français et de l'anglais
- ✅ Traductions complètes de l'interface
- ✅ Localisation des dates et formats
- ✅ Interface multilingue dynamique

### 📱 Interface Utilisateur

- ✅ Design responsive avec Bootstrap 5
- ✅ Pagination des listes
- ✅ Messages de confirmation/erreur
- ✅ Tableaux de bord avec statistiques
- ✅ Single Page Application (SPA) avec AngularJS
- ✅ Navigation fluide sans rechargement de page
- ✅ Animations et transitions douces

### ⚙️ Fonctionnalités Avancées

- ✅ Tâches asynchrones avec Celery
- ✅ Cache Redis pour optimisation
- ✅ Compression des fichiers statiques
- ✅ Support Docker et Docker Compose
- ✅ Configuration multi-environnements (développement/production)
- ✅ API REST pour intégration
- ✅ Webhooks et notifications
- ✅ Système de logs structuré

---

## 🏗️ Architecture du projet

```
django-invoice/
├── django_invoice/              # Configuration principale Django
│   ├── settings.py             # Paramètres globaux
│   ├── local.py                # Configuration développement
│   ├── production.py           # Configuration production
│   ├── urls.py                 # Routage principal
│   ├── wsgi.py                 # Application WSGI
│   ├── asgi.py                 # Application ASGI
│   └── celery.py               # Configuration Celery
│
├── fact_app/                    # Application principale
│   ├── models.py               # Modèles de données (Customer, Invoice, Article)
│   ├── views.py                # Vues et logique métier
│   ├── forms.py                # Formulaires Django
│   ├── urls.py                 # Routage de l'application
│   ├── admin.py                # Configuration admin Django
│   ├── decorators.py           # Décorateurs personnalisés
│   ├── signals.py              # Signaux Django
│   ├── utils.py                # Fonctions utilitaires
│   ├── tests.py                # Tests unitaires
│   ├── api.py                  # API REST endpoints
│   ├── api_urls.py             # Routage API
│   ├── spa_views.py            # Vue SPA principale
│   └── migrations/             # Migrations de base de données
│
├── templates/                   # Fichiers HTML
│   ├── base.html               # Template de base
│   ├── spa.html                # Template SPA principal
│   ├── index.html              # Page d'accueil traditionelle
│   ├── add_customer.html       # Formulaire client
│   ├── add_invoice.html        # Formulaire facture
│   ├── invoice.html            # Détail facture
│   ├── invoice-pdf.html        # Template PDF
│   └── admin/                  # Templates admin personnalisés
│
├── static/                      # Fichiers statiques
│   ├── style.css               # Feuilles de style principal
│   ├── script.js               # Scripts Javascript utilitaires
│   ├── images/                 # Images et icônes
│   └── spa/                    # Application SPA AngularJS
│       ├── app.module.js       # Définition du module AngularJS
│       ├── app.routes.js       # Configuration du routage
│       ├── controllers/        # Contrôleurs AngularJS
│       │   ├── dashboard.controller.js
│       │   ├── invoices.controller.js
│       │   └── customers.controller.js
│       ├── services/           # Services AngularJS
│       │   └── api.service.js  # Service API
│       └── views/              # Templates Vue AngularJS
│           ├── dashboard.html
│           ├── invoices.html
│           └── customers.html
│
├── locale/                      # Fichiers de traduction
│   └── fr/LC_MESSAGES/         # Traductions français
│
├── scripts/                     # Scripts utilitaires
│   ├── create_dev_superuser.py # Création superutilisateur dev
│   └── create_superuser.ps1    # Script PowerShell
│
├── docker-compose.yml          # Configuration Docker Compose
├── Dockerfile                  # Configuration Docker
├── requirements.txt            # Dépendances Python
├── manage.py                   # Utilitaire Django
└── README.md                   # Ce fichier
```

---

## 🎨 Architecture SPA (Single Page Application)

L'application utilise une architecture **Single Page Application (SPA)** moderne avec **AngularJS** côté client, offrant une expérience utilisateur fluide sans rechargements de page.

### Structure de la SPA

```
static/spa/
├── app.module.js          # Module principal AngularJS
├── app.routes.js          # Configuration du routeur
├── controllers/           # Logique métier côté client
│   ├── dashboard.controller.js    # Contrôleur du tableau de bord
│   ├── invoices.controller.js     # Contrôleur des factures
│   └── customers.controller.js    # Contrôleur des clients
├── services/              # Services réutilisables
│   └── api.service.js     # Abstraction de l'API REST
└── views/                 # Templates HTML AngularJS
    ├── dashboard.html     # Vue du tableau de bord
    ├── invoices.html      # Vue de la liste des factures
    └── customers.html     # Vue de la liste des clients
```

### Points d'entrée de la SPA

**URL Principale** : `http://localhost:8000/#!/`

La SPA est accessible via les routes suivantes :

| Route              | Description          | Contrôleur               |
| ------------------ | -------------------- | ------------------------ |
| `#!/`              | Tableau de bord      | DashboardController      |
| `#!/invoices`      | Liste des factures   | InvoicesController       |
| `#!/invoices/:id`  | Détail d'une facture | InvoiceDetailController  |
| `#!/customers`     | Liste des clients    | CustomersController      |
| `#!/customers/:id` | Détail d'un client   | CustomerDetailController |

### Flux de données SPA

```
┌─────────────────┐
│  AngularJS SPA  │
│   (Frontend)    │
└────────┬────────┘
         │ AJAX
         ▼
┌─────────────────┐
│   API REST      │
│  (fact_app)     │
└────────┬────────┘
         │ ORM
         ▼
┌─────────────────┐
│  Base de données│
│  (PostgreSQL)   │
└─────────────────┘
```

### Avantages de l'architecture SPA

✅ **Expérience utilisateur fluide** : Pas de rechargement de page
✅ **Performances** : Chargement des données en arrière-plan
✅ **Responsive** : Interface agile et réactive
✅ **Réutilisabilité** : API partagée entre frontend et backend
✅ **Maintenabilité** : Séparation claire des responsabilités
✅ **Extensibilité** : Facile d'ajouter de nouvelles fonctionnalités

---

## 📋 Prérequis

### Système

- Python 3.9 ou supérieur
- PostgreSQL 12+ (pour production)
- Redis 6.2+ (pour Celery)
- Git

### Logiciels optionnels

- Docker et Docker Compose (pour déploiement containerisé)
- wkhtmltopdf (pour génération PDF avancée)

---

## 🚀 Installation

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/donaldte/django-invoice.git
cd django-invoice
```

### Étape 2 : Créer un environnement virtuel

**Linux/Mac :**

```bash
python3.9 -m venv venv
source venv/bin/activate
```

**Windows :**

```bash
python3.9 -m venv venv
venv\Scripts\activate
```

### Étape 3 : Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Étape 4 : Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
# Django
SECRET_KEY=votre-clé-secrète-très-sécurisée
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_invoice
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (optionnel)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe
```

### Étape 5 : Initialiser la base de données

```bash
python manage.py migrate
```

### Étape 6 : Créer un superutilisateur

```bash
python manage.py createsuperuser
```

Ou utiliser le script fourni :

```bash
python scripts/create_dev_superuser.py
```

### Étape 7 : Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### Étape 8 : Lancer le serveur de développement

```bash
python manage.py runserver
```

Accédez à l'application : **http://localhost:8000**

---

## ⚙️ Configuration

### Configuration Django (settings.py)

**Applications installées :**

- Django Admin
- Django Auth
- Django Sessions
- Django Messages
- WhiteNoise (compression statiques)
- Django Celery Beat (tâches planifiées)
- fact_app (application principale)

**Middleware :**

- SecurityMiddleware
- WhiteNoiseMiddleware (compression)
- LocaleMiddleware (i18n)
- SessionMiddleware
- CsrfViewMiddleware
- AuthenticationMiddleware
- MessageMiddleware

**Langues supportées :**

- Français (fr)
- Anglais (en)

### Configuration Celery

Celery est configuré pour les tâches asynchrones :

```python
# django_invoice/celery.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

Lancer le worker Celery :

```bash
celery -A django_invoice worker -l info
```

Lancer le beat scheduler :

```bash
celery -A django_invoice beat -l info
```

---

## 📖 Utilisation

### Accès à l'application

1. **Connexion** : Accédez à `/admin/` et connectez-vous avec vos identifiants superutilisateur
2. **Tableau de bord** : Vous serez redirigé vers la page d'accueil avec la liste des factures

### Interface SPA Moderne

L'application propose une **Single Page Application (SPA)** moderne accessible via `/spa/` ou directement `http://localhost:8000/#!/`.

#### Avantages de l'interface SPA

- **Navigation fluide** : Pas de rechargement de page
- **Interface responsive** : Fonctionne parfaitement sur desktop, tablette et mobile
- **Recherche en temps réel** : Filtrage instantané des données
- **Chargement rapide** : Cache côté client et requêtes optimisées
- **Expérience utilisateur améliorée** : Transitions fluides et animations

#### Routes SPA

**Tableau de bord** : `http://localhost:8000/#!/`

- Vue d'ensemble des statistiques
- Dernières factures
- Informations clés

**Factures** : `http://localhost:8000/#!/invoices`

- Liste complète des factures
- Recherche et filtrage
- Actions rapides (édition, suppression, PDF)

**Clients** : `http://localhost:8000/#!/customers`

- Gestion complète des clients
- Profils détaillés
- Historique des factures

### Gestion des Clients (via SPA)

**Ajouter un client :**

1. Accédez à `#!/customers`
2. Cliquez sur "Ajouter un client"
3. Remplissez le formulaire avec les informations du client :
   - Nom complet
   - Email (unique)
   - Téléphone
   - Adresse complète
   - Genre (M/F)
   - Âge
   - Ville
   - Code postal
4. Cliquez sur "Enregistrer"

**Modifier un client :**

1. Accédez à `#!/customers`
2. Sélectionnez le client à modifier
3. Cliquez sur "Modifier"
4. Mettez à jour les informations
5. Cliquez sur "Enregistrer"

**Consulter le détail d'un client :**

1. Accédez à `#!/customers`
2. Cliquez sur le client
3. Consultez :
   - Informations personnelles
   - Nombre total de factures
   - Total dû
   - Factures associées

**Supprimer un client :**

1. Accédez à `#!/customers`
2. Sélectionnez le client
3. Cliquez sur "Supprimer"
4. Confirmez la suppression

### Gestion des Factures (via SPA)

**Créer une facture :**

1. Accédez à `#!/invoices`
2. Cliquez sur "Ajouter une facture"
3. Remplissez le formulaire :
   - **Client** : Sélectionnez dans la liste
   - **Date** : Sélectionnez la date de facturation
   - **Type** : Choisissez parmi :
     - Reçu (R)
     - Facture Pro-forma (P)
     - Facture (I)
   - **Articles** : Ajoutez des articles :
     - Nom du produit/service
     - Quantité
     - Prix unitaire
   - **Commentaires** : Ajoutez des notes (optionnel)
4. Cliquez sur "Créer la facture"

**Consulter une facture :**

1. Accédez à `#!/invoices`
2. Cliquez sur une facture
3. Consultez :
   - Détails de la facture
   - Informations du client
   - Liste des articles avec totaux
   - Statut de paiement
   - Commentaires

**Télécharger en PDF :**

1. Ouvrez une facture
2. Cliquez sur "Télécharger PDF"
3. Le fichier PDF sera généré et téléchargé automatiquement
4. Le PDF inclut :
   - Données de la facture
   - Informations du client
   - Détail des articles
   - Total à payer
   - Commentaires

**Mettre à jour le statut de paiement :**

1. Ouvrez une facture dans `#!/invoices`
2. Cochez la case "Marquée comme payée"
3. Le statut s'update en temps réel
4. L'historique des modifications est conservé

**Rechercher des factures :**

1. Accédez à `#!/invoices`
2. Utilisez la barre de recherche en haut
3. Tapez :
   - Nom du client
   - Numéro de facture
   - Montant
4. Les résultats s'actualisent en temps réel

**Mise à jour en masse :**

1. Accédez à `#!/invoices`
2. Sélectionnez plusieurs factures
3. Choisissez l'action :
   - Marquer comme payée
   - Marquer comme non payée
   - Supprimer
4. Cliquez sur "Appliquer"

### Interface Classique (Fallback)

Si vous préférez l'interface traditionnelle avec rechargement de page, accédez à `/` pour utiliser les vues Django classiques.

---

## 🗄️ Structure de la base de données

### Modèle Customer (Client)

```python
- id (PK)
- name (CharField, max 132)
- email (EmailField, unique)
- phone (CharField, max 20)
- address (CharField, max 255)
- sex (CharField, choices: M/F)
- age (PositiveIntegerField, nullable)
- city (CharField, max 64)
- zip_code (CharField, max 16)
- created_date (DateTimeField, auto)
- updated_date (DateTimeField, auto)
- save_by (ForeignKey → User)
```

**Méthodes utiles :**

- `get_total_invoices()` : Retourne le total des factures du client
- `get_paid_invoices()` : Retourne le nombre de factures payées

### Modèle Invoice (Facture)

```python
- id (PK)
- customer (ForeignKey → Customer)
- save_by (ForeignKey → User)
- invoice_date_time (DateTimeField, auto)
- total (DecimalField, 12 chiffres, 2 décimales)
- last_updated_date (DateTimeField, auto)
- paid (BooleanField, default=False)
- invoice_type (CharField, choices: R/P/I)
- comments (TextField, max 1000, nullable)
```

**Méthodes utiles :**

- `get_total` (property) : Calcule le total à partir des articles
- `mark_as_paid()` : Marque la facture comme payée
- `mark_as_unpaid()` : Marque la facture comme non payée
- `get_article_count()` : Retourne le nombre d'articles

### Modèle Article (Ligne de facture)

```python
- id (PK)
- invoice (ForeignKey → Invoice)
- name (CharField, max 255)
- quantity (PositiveIntegerField)
- unit_price (DecimalField, 12 chiffres, 2 décimales)
- created_at (DateTimeField, auto)
```

**Méthodes utiles :**

- `get_total` (property) : Calcule le total (quantité × prix unitaire)

---

## 🔗 API et URLs

### URLs Principales

#### Factures

| Méthode  | URL                             | Vue                        | Description           |
| -------- | ------------------------------- | -------------------------- | --------------------- |
| GET      | `/`                             | HomeView                   | Liste des factures    |
| GET      | `/invoices/<id>/`               | InvoiceDetailView          | Détail d'une facture  |
| GET      | `/invoices/<id>/pdf/`           | get_invoice_pdf            | Télécharger PDF       |
| GET/POST | `/invoices/<id>/update-status/` | UpdateInvoiceStatusView    | Modifier le statut    |
| GET/POST | `/invoices/<id>/delete/`        | DeleteInvoiceView          | Supprimer une facture |
| GET/POST | `/invoices/add/`                | AddInvoiceView             | Créer une facture     |
| POST     | `/invoices/bulk-update-status/` | bulk_update_invoice_status | Mise à jour en masse  |

#### Clients

| Méthode  | URL                       | Vue                | Description         |
| -------- | ------------------------- | ------------------ | ------------------- |
| GET      | `/customers/`             | CustomerListView   | Liste des clients   |
| GET/POST | `/customers/add/`         | AddCustomerView    | Ajouter un client   |
| GET/POST | `/customers/<id>/update/` | UpdateCustomerView | Modifier un client  |
| GET/POST | `/customers/<id>/delete/` | DeleteCustomerView | Supprimer un client |

---

## � API REST

L'application propose une **API REST complète** pour intégration avec d'autres systèmes ou applications mobiles.

### Authentification API

Toutes les requêtes API nécessitent une authentification Django :

```bash
# Authentification via session
curl -X GET http://localhost:8000/api/invoices/ \
  -b "sessionid=votre_sessionid"

# Ou avec credentials
curl -X GET http://localhost:8000/api/invoices/ \
  -u username:password
```

### Endpoints API

#### Factures

**Liste des factures**

```bash
GET /api/invoices/
```

Paramètres de requête :

- `q` (string) : Recherche par nom de client ou ID

Exemple :

```bash
curl http://localhost:8000/api/invoices/?q=Dupont
```

Réponse :

```json
{
  "results": [
    {
      "id": 1,
      "customer_id": 1,
      "customer_name": "Jean Dupont",
      "invoice_date_time": "2025-01-15T10:30:00",
      "total": "1500.00",
      "paid": false,
      "invoice_type": "I",
      "invoice_type_display": "Facture",
      "comments": "Paiement à 30 jours"
    },
    {
      "id": 2,
      "customer_id": 2,
      "customer_name": "Marie Martin",
      "invoice_date_time": "2025-01-14T14:20:00",
      "total": "2300.50",
      "paid": true,
      "invoice_type": "P",
      "invoice_type_display": "Facture Pro-forma",
      "comments": ""
    }
  ]
}
```

**Détail d'une facture**

```bash
GET /api/invoices/{id}/
```

Réponse :

```json
{
  "id": 1,
  "customer_id": 1,
  "customer_name": "Jean Dupont",
  "invoice_date_time": "2025-01-15T10:30:00",
  "total": "1500.00",
  "paid": false,
  "invoice_type": "I",
  "invoice_type_display": "Facture",
  "comments": "Paiement à 30 jours",
  "articles": [
    {
      "id": 1,
      "name": "Prestation consulting",
      "quantity": 5,
      "unit_price": "250.00",
      "total": "1250.00"
    },
    {
      "id": 2,
      "name": "Frais de déplacement",
      "quantity": 1,
      "unit_price": "250.00",
      "total": "250.00"
    }
  ]
}
```

#### Clients

**Liste des clients**

```bash
GET /api/customers/
```

Paramètres de requête :

- `q` (string) : Recherche par nom ou email

Réponse :

```json
{
  "results": [
    {
      "id": 1,
      "name": "Jean Dupont",
      "email": "jean.dupont@example.com",
      "phone": "+33612345678",
      "address": "123 Rue de la Paix",
      "sex": "M",
      "age": 35,
      "city": "Paris",
      "zip_code": "75001",
      "created_date": "2025-01-10T08:00:00"
    }
  ]
}
```

**Détail d'un client**

```bash
GET /api/customers/{id}/
```

Réponse :

```json
{
  "id": 1,
  "name": "Jean Dupont",
  "email": "jean.dupont@example.com",
  "phone": "+33612345678",
  "address": "123 Rue de la Paix",
  "sex": "M",
  "age": 35,
  "city": "Paris",
  "zip_code": "75001",
  "created_date": "2025-01-10T08:00:00",
  "total_invoices": "3500.00",
  "paid_invoices": 2,
  "invoices": [
    {
      "id": 1,
      "invoice_date_time": "2025-01-15T10:30:00",
      "total": "1500.00",
      "paid": false
    },
    {
      "id": 2,
      "invoice_date_time": "2025-01-14T14:20:00",
      "total": "2000.00",
      "paid": true
    }
  ]
}
```

### Intégration JavaScript/AngularJS

L'application SPA utilise un service `ApiService` pour communiquer avec l'API :

```javascript
// services/api.service.js
angular.module("invoiceApp").service("ApiService", [
  "$http",
  function ($http) {
    this.listInvoices = function (params) {
      return $http.get("/api/invoices/", { params: params });
    };

    this.getInvoice = function (id) {
      return $http.get("/api/invoices/" + id + "/");
    };

    this.listCustomers = function (params) {
      return $http.get("/api/customers/", { params: params });
    };

    this.getCustomer = function (id) {
      return $http.get("/api/customers/" + id + "/");
    };
  },
]);
```

Utilisation dans les contrôleurs :

```javascript
// controllers/invoices.controller.js
angular.module("invoiceApp").controller("InvoicesController", [
  "ApiService",
  function (ApiService) {
    const vm = this;

    vm.loading = true;
    vm.invoices = [];
    vm.q = "";

    vm.load = function () {
      vm.loading = true;
      ApiService.listInvoices({ q: vm.q })
        .then(function (response) {
          vm.invoices = response.data.results;
        })
        .catch(function (error) {
          console.error("Erreur lors du chargement", error);
        })
        .finally(function () {
          vm.loading = false;
        });
    };

    vm.onSearch = function () {
      vm.load();
    };

    // Charger les données au démarrage
    vm.load();
  },
]);
```

---

## �🐳 Déploiement

### Avec Docker Compose

**Prérequis :**

- Docker
- Docker Compose

**Lancer l'application :**

```bash
docker-compose up -d
```

**Services lancés :**

- **web** : Application Django (port 8000)
- **db** : PostgreSQL (port 5432)
- **redis** : Redis (port 6379)
- **celery** : Worker Celery

**Arrêter l'application :**

```bash
docker-compose down
```

**Voir les logs :**

```bash
docker-compose logs -f web
```

### Déploiement en Production

**1. Préparer le serveur :**

```bash
# Mettre à jour le système
sudo apt-get update && sudo apt-get upgrade -y

# Installer les dépendances
sudo apt-get install -y python3.9 python3-pip postgresql redis-server nginx
```

**2. Cloner et configurer :**

```bash
git clone https://github.com/donaldte/django-invoice.git
cd django-invoice
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Configurer les variables d'environnement :**

```bash
# Créer .env avec les paramètres de production
DEBUG=False
SECRET_KEY=votre-clé-très-sécurisée
DJANGO_ALLOWED_HOSTS=votre-domaine.com
```

**4. Migrations et collecte statiques :**

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

**5. Configurer Gunicorn :**

```bash
pip install gunicorn
gunicorn django_invoice.wsgi:application --bind 0.0.0.0:8000
```

**6. Configurer Nginx :**

Voir le fichier `ngnix.conf` fourni dans le projet.

**7. Configurer Systemd (optionnel) :**

Créer `/etc/systemd/system/django-invoice.service` :

```ini
[Unit]
Description=Django Invoice Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/django-invoice
ExecStart=/path/to/django-invoice/venv/bin/gunicorn django_invoice.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activer le service :

```bash
sudo systemctl enable django-invoice
sudo systemctl start django-invoice
```

---

## 🛠️ Technologies utilisées

### Backend

- **Django 4.1+** : Framework web Python
- **PostgreSQL** : Base de données relationnelle
- **Redis** : Cache et broker de messages
- **Celery** : Tâches asynchrones
- **Gunicorn** : Serveur WSGI
- **pdfkit** : Génération de PDF

### Frontend

- **Bootstrap 5** : Framework CSS
- **HTML5** : Markup
- **CSS3** : Styles
- **JavaScript** : Interactivité

### DevOps

- **Docker** : Containerisation
- **Docker Compose** : Orchestration
- **Nginx** : Serveur web reverse proxy
- **WhiteNoise** : Compression statiques

### Outils

- **python-decouple** : Gestion des variables d'environnement
- **psycopg2** : Adaptateur PostgreSQL
- **django-celery-beat** : Tâches planifiées
- **django-redis** : Cache Redis

---

## 📝 Logging

L'application utilise le logging Python standard. Les logs sont configurés dans `logging_config.py`.

**Niveaux de log :**

- **DEBUG** : Informations détaillées pour le diagnostic
- **INFO** : Confirmations que tout fonctionne
- **WARNING** : Avertissements pour les problèmes potentiels
- **ERROR** : Erreurs graves
- **CRITICAL** : Erreurs très graves

**Exemples d'événements loggés :**

- Création/modification/suppression de clients
- Création/modification/suppression de factures
- Génération de PDF
- Erreurs de validation
- Accès non autorisés

---

## 🧪 Tests

Exécuter les tests :

```bash
python manage.py test
```

Exécuter les tests avec couverture :

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## 🔒 Sécurité

### Bonnes pratiques implémentées

✅ **Authentification** : Tous les utilisateurs doivent être connectés
✅ **Autorisation** : Seuls les superutilisateurs peuvent accéder
✅ **CSRF Protection** : Tokens CSRF sur tous les formulaires
✅ **SQL Injection** : Utilisation de l'ORM Django
✅ **XSS Protection** : Échappement automatique des templates
✅ **Validation** : Validation côté serveur de tous les formulaires
✅ **Secrets** : Utilisation de variables d'environnement
✅ **HTTPS** : Recommandé en production

### Recommandations supplémentaires

- Utiliser HTTPS en production
- Configurer les en-têtes de sécurité (HSTS, CSP)
- Mettre à jour régulièrement les dépendances
- Utiliser un WAF (Web Application Firewall)
- Effectuer des audits de sécurité réguliers

---

## 📞 Support et Contribution

### Signaler un bug

Créez une issue sur GitHub avec :

- Description du problème
- Étapes pour reproduire
- Résultat attendu vs résultat obtenu
- Environnement (OS, Python, Django version)

### Contribuer

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👨‍💻 Auteur

**Donald Tè** - [GitHub](https://github.com/donaldte)

---

## 📚 Ressources utiles

- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation Celery](https://docs.celeryproject.org/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation Redis](https://redis.io/documentation)
- [Documentation Docker](https://docs.docker.com/)

---

## 🎯 Feuille de route

- [ ] Intégration de paiement (Stripe, PayPal)
- [ ] Rapports et statistiques avancées
- [ ] Export en Excel/CSV
- [ ] API REST complète
- [ ] Application mobile
- [ ] Notifications par email
- [ ] Système de devis
- [ ] Gestion des taxes
- [ ] Numérotation automatique des factures
- [ ] Rappels de paiement automatiques

---

**Dernière mise à jour** : 2024
**Version** : 1.0.0
