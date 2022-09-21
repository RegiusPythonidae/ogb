from flask_restx import Api


api = Api(
    api_blueprint,
    title='Coding API',
    version='1.0',
    # Other metadata
)

# Import and Add Namespaces
