# Data scraping API (data-scraping-api)

## Description
The project objective is to demonstrate approach of developing data scraping API by means
of FastAPI.

The project target scraping data source is [toscrape.com](http://quotes.toscrape.com/).
The source was specially developed in order to let people train their scraping skills.

## Dependencies
The project uses:
1. **FastAPI** - API web framework;
2. **aiohttp** - requesting data via HTTP/HTTPS;
3. **bs4 (lxml)** - parsing raw HTML text documents.

All used packages are listed in [requirements.txt](requirements.txt).

## Project structure
| №   | Path                           | Description                                                 |
|-----|--------------------------------|-------------------------------------------------------------|
| 1.  | app/                           | Package with all project logic.                             |
| 2.  | app/core/                      | Package that manages configurations.                        |
| 3.  | app/core/config.py             | Environment variables parsing with Starlette approach.      |
| 4.  | app/quotes/                    | Package of implemented scraper itself.                      |
| 5.  | app/quotes/api.py              | API methods for quotes scraper.                             |
| 6.  | app/quoates/core.py            | Scraper functionality, requests, parsing and serialisation. |
| 7.  | app/quotes/examples.py         | Examples of input and output data for API methods.          |
| 8.  | app/quotes/schemas.py          | Structures for input and output data.                       |
| 9.  | app/quotes/tests.py            | Tests for quotes scraper.                                   |
| 10. | app/router/                    | Storing endpoints for specific API versions.                |
| 11. | app/router/api_v1/endpoints.py | Endpoints for API version 1.                                |
| 12. | app/conftest.py                | Configurations for purest module.                           |
| 13. | app/main.py                    | Entrypoint for the scraping-api app.                        |
| 14. | .dockerignore                  | List of ignored files by Docker.                            |
| 15. | .gitignore                     | List of ignored files by GIT.                               |
| 16. | dev.env                        | List of environment variables.                              |
| 17. | Dockerfile                     | Deployment instructions for Docker container.               |
| 18. | LICENSE                        | Description of license conditions.                          |
| 19. | pytest.ini                     | Configuration for test files location.                      |
| 20. | README.md                      | Current file with project documentation.                    |
| 21. | requirements.txt               | List of all python packages used in project.                |

## Tests
Writing tests are a must-have practice in any project. Tests for scrapers have its specifics because scrapers 
deals with dynamic data - data that always changes. So be careful writing tests, they must be more abstract. 

## Code style
The code in this project is written in compliance with [PEP8](https://www.python.org/dev/peps/pep-0008/). 
It is extremely important to stick to code style, it helps other people to understand code better. 
In this project all imports are sorted with [isort](https://github.com/PyCQA/isort) package. 
It helps to keep project clean and clear.

Please be respectful to other developers!

## Deployment

### Virtual environment
Command to build virtual environment under project root, it helps  isolate the project from 
other developments so there are no dependencies collisions:
```bash
python -m venv venv/
```

Activate virtual environment:
```bash
source venv/bin/python
```

Command to install all dependencies from created virtual environment:
```bash
pip install -r requirements.txt
```

Command to run tests:
```bash
pytest
```

Command to run service:
```bash
uvicorn app.main:app
```

More details on uvicorn - [read more](https://www.uvicorn.org) 

### Docker
Command to build image (from the project root folder):
```bash
docker build -t data-craping-api .
```
Command to run service and expose 80 port for access via `http://localhost:4001`
```bash
docker run -d --name data-craping-api -p 4001:80 data-craping-api
```

To see all the configurations and options, go to the Docker image page: 
[uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)
