# MyCurrency - Currency Exchange API

**MyCurrency** is a currency conversion API that allows you to query exchange rates, convert amounts, and manage currencies. The platform uses multiple exchange rate providers with priority logic and failover in case of error.

---

## Features
**RESTful API** to query exchange rates and perform conversions.
- **Multiple providers** with priority management and resilience.
- **Admin Panel** with Django Admin.
- **Asynchronous tasks** for efficient loading of historical data.
- **Postman Collection included** for testing.

---

## Technologies Used
- **Python 3.11**
- **Django 4 / 5**
- **Django Rest Framework**
- **PostgreSQL / SQLite** (Database)
- **asyncio** (for asynchronous requests)
- **Postman** (for API testing)

---

## 1. Installation and Configuration

### **Clone the Repository**
```
git clone https://github.com/MikelEulate/MyCurrency.git
cd MyCurrency
```

## 2. Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies
```
pip install -r requirements.txt
```

## 4. Configure env vars
```
Create a .env file and add:

DEBUG=True
SECRET_KEY=django-insecure-xa2x7jqn4lpjle@t5uf_uz9(2hmu50rm@f!*3q=zr__t=g%c*g
CURRENCYBEACON_BASE_URL=https://api.currencybeacon.com/v1/latest
CURRENCYBEACON_API_KEY=UFlvJMv0hMu8YvreiNV83Y2SfjD2ywGK
DATABASE_URL=sqlite:///db.sqlite3
POSTGRES_DB=mycurrency_db
POSTGRES_USER=mycurrency_user
POSTGRES_PASSWORD=mycurrency_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## 5. Start Services Needed
```
cd docker-compose
docker-compose up --build
```

## 6. Apply Migrations and Load Initial Data
```
python manage.py migrate

# Run the task to load currencies and providers:
python manage.py load_initial_currencies_and_providers # Load currencies and providers

# Run the task to load test data:
python manage.py load_test_data # Load test data (optional)

# Run the task to load historical rates:
python manage.py load_historical_data # Load historical data (optional)
```



## 7. Start Server
```
python manage.py runserver localhost:8000
```
Access API at http://localhost:8000/



---

---

## API Usage

Main Endpoints
```
| Method | URL                                                                                 | Description                             |
|--------|-------------------------------------------------------------------------------------|-----------------------------------------|
| GET    | /api/exchange-rates/?source_currency=USD&date_from=2024-01-01&date_to=2024-02-01    | Get historical exchange rates           |
| GET    | /api/convert/?source_currency=USD&exchanged_currency=EUR&amount=100&date=2025-02-11 | Convert an amount between currencies    |
| POST   | /api/currencies/                                                                    | Create a new currency                   |
| GET    | /api/currencies/                                                                    | List available currencies               |
| PUT    | /api/currencies/{id}/                                                               | Update a currency                       |
| DELETE | /api/currencies/{id}/                                                               | Delete a currency                       |
| POST   | /api/providers/                                                                     | Create a new provider                   |
| GET    | /api/providers/                                                                     | List available providers                |
| PUT    | /api/providers/{id}/                                                                | Update a provider                       |
| DELETE | /api/providers/{id}/                                                                | Delete a provider                       |
```



## Django Admin
To manage currencies and exchange rates, go to:

http://127.0.0.1:8000/admin/

Default credentials:
```
User: BackBase
Pwd: MyCurrency
```

## Postman Collection
Import the MyCurrency.postman_collection.json file into Postman to test the API.

How to Import in Postman
1. Open Postman.
2. Click on "Import".
3. Select MyCurrency.postman_collection.json.
4. Set the base_url variable to http://localhost:8000/.
5. Use the predefined requests to test the API.

## Tests
To run the unit tests:
```
python manage.py test
```

## Improvements

- Add Dockerfile and docker-compose file for deployment
- Add Jenkinsfile for CI/CD (with stages: build, analyze, test w/ coverage, publish image to registry).
- Add Celery / Kafka for asynchronous tasks management.
- Add Swagger documentation for the API.
- Improve error handling and logging.
- Add more providers for exchange rates.
- Add more features to the API (e.g., user accounts, transactions).
- Create new library repository for backend common code and modules.
