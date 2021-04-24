from boilerplate import db
from boilerplate.common.models import BaseModel

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey(
                         'users.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey(
                         'roles.id'), primary_key=True)
                     )

user_permission = db.Table('user_permission',
                           db.Column('user_id', db.Integer, db.ForeignKey(
                               'users.id'), primary_key=True),
                           db.Column('permission_id', db.Integer, db.ForeignKey(
                               'permissions.id'), primary_key=True)
                           )


class Users(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), nullable=False, unique=True)
    first_name = db.Column(db.String(300), nullable=False,)
    last_name = db.Column(db.String(300))
    email = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300))
    roles = db.relationship('Roles', secondary=user_role, lazy='subquery',
                            backref=db.backref('users', lazy=True))
    permissions = db.relationship('Permissions', secondary=user_permission, lazy='subquery',
                                  backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<Users %r>' % self.username


class UserDetails(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
