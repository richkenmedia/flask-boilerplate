
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, get_raw_jwt
)

from flask_dir import jwt


blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


class Logout(Resource):
    @jwt_required
    def delete(self):
        try:
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            return {
                "status": {
                    "code": 200,
                    "message": "Successfully logged out"
                },
                "results": []
            }, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500
