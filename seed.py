import csv
import os
from app import create_app
from app.models import db, Episode, Guest, Appearance

# helper to get abs path
def get_csv_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def seed_database():
    print("Starting database seed...")
    
    app = create_app()
    
    with app.app_context():
        # Reset everything
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating tables...")
        db.create_all()
        
        # Load episodes
        print("Loading episodes...")
        episode_count = 0
        with open(get_csv_path('episodes.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # more compact way to create episode
                episode = Episode(**{
                    'id': int(row['id']),
                    'date': row['date'],
                    'number': int(row['number'])
                })
                db.session.add(episode)
                episode_count += 1
        
        # Load guests
        print("Loading guests...")
        guest_count = 0
        with open(get_csv_path('guests.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # create guest manually this time
                guest = Guest(
                    id=int(row['id']),
                    name=row['name'],
                    occupation=row['occupation']
                )
                db.session.add(guest)
                guest_count += 1
        
        # Try to commit after episodes and guests
        try:
            db.session.commit()
            print(f"Added {episode_count} episodes and {guest_count} guests")
        except Exception as e:
            db.session.rollback()
            print(f"Error loading episodes and guests: {str(e)}")
            return
        
        # Load appearances
        print("Loading appearances...")
        appearance_count = 0
        with open(get_csv_path('appearances.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # use dict unpacking with some field conversion
                    appearance = Appearance(
                        id=int(row['id']),
                        rating=int(row['rating']),
                        episode_id=int(row['episode_id']),
                        guest_id=int(row['guest_id'])
                    )
                    db.session.add(appearance)
                    appearance_count += 1
                except ValueError as e:
                    print(f"Skipping appearance - {str(e)}")
        
        # Commit appearances
        try:
            db.session.commit()
            print(f"Added {appearance_count} appearances")
        except Exception as e:
            db.session.rollback()
            print(f"Error loading appearances: {str(e)}")
            return
        
        print("Database seeding complete!")

if __name__ == "__main__":
    seed_database()