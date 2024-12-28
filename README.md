## phone-db-mgmt

To run this web app, clone this repo and cd into it. Then:

```
docker compose up
```
Then in a browser, go to:
- `http://localhost:8080` to access minimal dashboard page
- `http://localhost:8080/api` for API documentation

#### Testing

To launch tests on backend:
```
docker compose down
docker compose --profile test up
```
Then:
```
cd server
pytest
```
