from boilerplate import db
from boilerplate.common.models import BaseModel


function_permissions = db.Table('function_permissions',
                                db.Column('function_id', db.Integer, db.ForeignKey(
                                    'functions.id'), primary_key=True),
                                db.Column('permission_id', db.Integer, db.ForeignKey(
                                    'permissions.id'), primary_key=True)
                                )


class Functions(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    slug = db.Column(db.String(40))
    permissions = db.relationship('Permissions', secondary=function_permissions, lazy='subquery',
                                  backref=db.backref('funcitons', lazy=True))

    def __repr__(self):
        return '<Functions %r>' % self.name
