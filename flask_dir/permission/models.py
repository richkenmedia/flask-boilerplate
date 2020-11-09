from flask_dir import db
from flask_dir.common.models import BaseModel


class Permissions(BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True, unique=True)

    def __repr__(self):
        return '<Permissions %r>' % self.name
