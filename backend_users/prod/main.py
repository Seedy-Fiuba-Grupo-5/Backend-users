from prod import create_app, db
from flask_cors import CORS
# from flask_swagger_ui import get_swaggerui_blueprint

app = create_app()

with app.app_context():
    db.create_all()
CORS(app)
