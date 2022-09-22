.\venv\Scripts\activate.ps1
$env:FLASK_APP = "manage"
flask db migrate
flask db upgrade