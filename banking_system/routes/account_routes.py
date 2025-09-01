from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Account
import datetime

account_bp = Blueprint('account', __name__)

@account_bp.route('/account', methods=['POST'])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    account_number = "ACC" + str(int(datetime.datetime.now().timestamp()))
    account = Account(account_number=account_number, user_id=user_id)
    db.session.add(account)
    db.session.commit()
    return jsonify({"message": "Account created", "account_number": account_number})
