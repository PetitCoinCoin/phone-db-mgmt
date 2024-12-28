## phone-db-mgmt

To run this web app, clone this repo and cd into it. Then:

```
docker compose up -d
```
Then in a browser, go to:
- `http://localhost:8080` to access minimal dashboard page
- `http://localhost:8080/api/docs` for API documentation

#### Testing

To launch tests on backend:
```
docker compose down
docker compose --profile test up -d
```
Then:
```
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r test_requirements.txt
pytest
```
To stop everything after the tests:
```
docker compose --profile test down
```
