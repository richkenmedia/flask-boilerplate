from sqlalchemy import event

from boilerplate import db
from boilerplate.common.models import BaseModel


role_permissions = db.Table('role_permissions',
                            db.Column('role_id', db.Integer, db.ForeignKey(
                                'roles.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey(
                                'permissions.id'), primary_key=True)
                            )


class Roles(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(300))
    permissions = db.relationship('Permissions', secondary=role_permissions, lazy='subquery',
                                  backref=db.backref('roles', lazy=True))

    def __repr__(self):
        return '<Roles %r>' % self.name
