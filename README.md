# Data Analytics Test Task

A Django-based web application for uploading, validating, parsing, and aggregating data from CSV and Excel files.

## Technology Stack

- Python 3.13
- Django 5.2
- Pandas, Openpyxl
- Pytest, pytest-cov
- Ruff
- Poetry / pip

## Setup Instructions

1. Clone the repository and navigate to the project directory:
```bash
git clone [https://github.com/vlchshn/test-task-publicisgroupe.git](https://github.com/vlchshn/test-task-publicisgroupe.git)
cd test-task-publicisgroupe
```

2. Install dependencies:

Using Poetry:
```bash
poetry install
poetry shell
```

Using pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Apply database migrations:
```bash
python manage.py migrate
```

4. Create an admin user (authentication is required to access the dashboard):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

## Testing

The project uses `pytest` for testing business logic and validations.

To run the test suite and check code coverage:
```bash
pytest --cov=analytics --cov-report=term-missing
```

## Linting and Formatting

The codebase complies with standard Python styling rules via `ruff`. 

To check code style:
```bash
ruff check .
```

To format code automatically:
```bash
ruff format .
```

## Task Assets

The original task requirements and sample data files (`Template 1` and `test`) used for application testing are located in the `task_data/` directory.