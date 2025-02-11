import time

from flask import current_app

from example.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)


class SocialToken(db.Model):
    __tablename__ = "social_token"

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String, nullable=True)
    expires_at = db.Column(db.Float, nullable=True)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def is_expired(self):
        return time.time() > (self.expires_at or 0)

    @property
    def safe_access_token(self):
        if self.is_expired:
            with current_app.app_context():
                # It is better if we keep in the model itself or maybe in another a new field called
                # adapter which is the adapter used by this token to renew the access token instead of
                # hardcoding the adapter name here. It is not SOLID but it has been done like this for simplicity
                google_adapter = current_app.extensions["google_adapter"]

                token_store = google_adapter.refresh_access_token(self.refresh_token)
                self.access_token = token_store.access_token
                self.expires_at = time.time() + token_store.expires_in
                db.session.commit()

        return self.access_token
