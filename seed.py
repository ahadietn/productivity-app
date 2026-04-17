from config import app, db
from models import User, Note
from faker import Faker

fake = Faker()

with app.app_context():
    print("Clearing old data...")
    Note.query.delete()
    User.query.delete()

    print("Seeding users...")
    users = []
    for i in range(3):
        user = User(username=fake.user_name() + str(i))
        user.set_password('password123')
        db.session.add(user)
        users.append(user)

    db.session.commit()

    print("Seeding notes...")
    for user in users:
        for _ in range(4):
            note = Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=3),
                user_id=user.id
            )
            db.session.add(note)

    db.session.commit()
    print("Done! Seeded 3 users with 4 notes each.")