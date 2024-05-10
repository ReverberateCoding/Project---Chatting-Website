from app import db, User, app
with app.app_context():
    db.create_all()
