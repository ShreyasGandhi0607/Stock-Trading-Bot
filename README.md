# Stock Trading Bot



__Tech Stack__
- [Python 3.12](https://github.com/python)
- [Django](https://github.com/django/django) (`pip install "Django>=5.1,<5.2"`)
- [Django Timescaledb](https://github.com/jamessewell/django-timescaledb) (`pip install django-timescaledb`)
- [Python requests](https://github.com/psf/requests) (`pip install requests`)
- [Jupyter](https://jupyter.org/) (`pip install jupyter`)
- [Psycopg Binary Release](https://pypi.org/project/psycopg/) (`pip install "psycopg[binary]"`)
- [Python Requests](https://github.com/HBNetwork/python-decouple) to load environment variables (e.g. `.env`) with type casting and default values.
- [Polygon.io](https://polygon.io/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github) ([docs](https://polygon.io/docs/stocks/getting-started?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github))


## Getting Started

Download the following:
- [git](https://git-scm.com/)
- [VSCode](https://code.visualstudio.com/) (or [Cursor](https://cursor.com/))
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine via [get.docker.com](https://get.docker.com/) (Linux Install Script)
- [Python](https://www.python.org/downloads/)


Create a Python vitual environment
_macOS/Linux/WSL_
```bash
python3.12 -m venv venv
source venv/bin/activate
```

_windows powershell_
```powershell
c:\Path\To\Python312\python.exe -m venv venv
.\venv\Scripts\activate
```

Install requirements
```bash
(venv) python -m pip install -r requirements.txt
```

Docker Compose Up (for local TimescaleDB and Redis)
```bash
docker compose -f compose.yaml up -d
```
> If you don't have Docker, use [TimescaleDB Cloud](tsdb.co/justin) and [Upstash Redis](https://upstash.com/?utm_source=cfe)

Create `.env` in project root
```bash
mkdir -p ~/dev/stock-trading-bot
echo "" >> .env
```

Add `DATABASE_URL` and `REDIS_URL` to `.env` (these are based on the `compose.yaml` file):
```bash
DATABASE_URL="postgresql://postgres:postgres@localhost:5431/postgres"
REDIS_URL="redis://localhost:6378"
```

