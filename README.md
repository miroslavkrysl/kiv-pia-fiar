# FIAR - Five in a Row

Python Flask app + PostgreSQL DB + Gunicorn http server

## Installation and run

#### Docker: (Gunicorn http server + Flask app) + (PostgreSQL)
```
cd path/to/project/root
npm install
npm run gulp bundle
docker-compose build    # or podman-compose build
docker-compose up       # or podman-compose up
```

Default server address: `http://127.0.0.1:8000/`