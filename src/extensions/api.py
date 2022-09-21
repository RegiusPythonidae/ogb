from flask_restx import Api

api = Api(
    title='Coding API',
    version='1.0',
    prefix='/api',
    doc='/doc/',
    # Other metadata
)

# Import and Add Namespaces
