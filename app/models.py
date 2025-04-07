from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# init the database
db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = 'episodes'
    
    # define columns
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)  # could use Date but String works fine for this
    number = db.Column(db.Integer)
    
    # relationships - one to many with appearances
    appearances = db.relationship('Appearance', back_populates='episode', 
                                  cascade='all, delete-orphan')
    
    # many-to-many with guests through appearances
    guests = db.relationship('Guest', secondary='appearances', viewonly=True)
    
    def to_dict(self, detailed=False):
        # basic dict representation
        episode_data = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        
        # add appearance data if requested
        if detailed:
            episode_data['appearances'] = [a.to_dict() for a in self.appearances]
            
        return episode_data


class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    
    # relationships
    appearances = db.relationship('Appearance', back_populates='guest', 
                                cascade='all, delete-orphan')
    episodes = db.relationship('Episode', secondary='appearances', viewonly=True)
    
    def to_dict(self):
        # simple dict representation
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }


# Join table with extra data
class Appearance(db.Model):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 rating
    
    # FKs
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    
    # Relationships
    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')
    
    # make sure rating is between 1-5
    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value
    
    def to_dict(self):
        # we need both the guest and episode info
        return {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id,
            'guest': self.guest.to_dict(),
            'episode': {
                'id': self.episode.id,
                'date': self.episode.date,
                'number': self.episode.number
            }
        }