# FIAR - Five in a Row

Python Flask app + PostgreSQL DB + Gunicorn http server

## Solution bonus parts
- password strength evaluation
- password reset using an e-mail (reset link)
- save games with all turns and allow replay


## Installation and run

1) copy `fiar/config.example.toml` into `fiar/config.toml`
2) edit `fiar/config.toml`, especially mail server

#### Docker: (Gunicorn http server + Flask app) + (PostgreSQL)
```
cd path/to/project/root
docker-compose build    # or podman-compose build
docker-compose up       # or podman-compose up
```

Default server address: `http://127.0.0.1:8000/`

There is default admin account:

- email: `admin@example.com`
- password: `admin`

and two normal accounts:

1)
- email: `hello@example.com`
- password: `hello`

2)
- email: `jello@example.com`
- password: `jello`