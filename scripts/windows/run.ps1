.\venv\Scripts\activate.ps1
$env:FLASK_APP = "manage"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = 1
flask run