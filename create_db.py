from app import app, db

# Create all tables defined in the models
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
