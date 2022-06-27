from flask_sqlalchemy import SQLAlchemy
import logging
import os

DATABASE_URI = os.getenv("DATABASE_URI")

logger = logging.getLogger(__name__)

db_profile = SQLAlchemy()

class Profile(db_profile.Model):
    __tablename__ = 'profile'
    id = db_profile.Column(db_profile.Integer, primary_key=True)
    season = db_profile.Column(db_profile.String(50))
    episode = db_profile.Column(db_profile.String(50))
    character = db_profile.Column(db_profile.String(50))
    scene = db_profile.Column(db_profile.String(50))
    cliffhanger = db_profile.Column(db_profile.String(50))
    user_id = db_profile.Column(db_profile.String(50))

def init_profile_base(app):
    db_profile.init_app(app)
    app.app_context().push()
    db_profile.create_all()

def get_profile_manager():
    profileManager = ProfileManager()
    return profileManager

class ProfileManager:
    def __init__(self):
        self.session = db_profile.session

    def setProfile(self, values, user_id):
         profiles = self.session.query(Profile)
         profile = profiles.filter(Profile.user_id == user_id).first()
         if profile is not None:
             self.session.delete(profile)
         entry_profile = Profile(user_id=user_id,\
             season=values["season"],\
             episode=values["episode"],\
             character=values["character"],\
             scene=values["scene"],\
             cliffhanger=values["cliffhanger"])
         self.session.add(entry_profile)
         self.session.commit()

    def getProfile(self, user_id):
        profiles = self.session.query(Profile)
        profile = profiles.filter(Profile.user_id == user_id).first()
        if not profile:
            return {}
        row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        return row2dict(profile)
