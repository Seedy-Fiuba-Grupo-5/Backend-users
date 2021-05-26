from prod import create_app, db
from flask_cors import CORS

app = create_app()
with app.app_context():
    db.create_all()
CORS(app)
