from flask_dir import db


class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, onupdate=db.func.now())
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    # For soft delete function
    deleted_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(300))
