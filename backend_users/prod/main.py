from prod import create_app, db
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app()

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Backend Users - API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

with app.app_context():
    db.create_all()
CORS(app)
