# MedReports

This project is a minimal Django application for managing medical reports. It uses a custom `User` model with a `role` field that can be either `doctor` or `hospital`.

## Setup

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv env
source env/bin/activate
```

2. Install dependencies:

```bash
pip install -r medreports/requirements.txt
```

3. Run migrations and create a superuser:

```bash
python medreports/manage.py migrate
python medreports/manage.py createsuperuser
```

4. Start the development server:

```bash
python medreports/manage.py runserver
```

After starting the server you can access the signup page at `/accounts/signup/` to create new doctor or hospital users.
