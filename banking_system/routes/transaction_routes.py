from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Account, Transaction

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.json
    acc = Account.query.filter_by(account_number=data['account']).first()
    acc.balance += data['amount']
    db.session.add(Transaction(type="deposit", amount=data['amount'], to_account_id=acc.id))
    db.session.commit()
    return jsonify({"message": "Deposit successful", "balance": acc.balance})

@transaction_bp.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    data = request.json
    acc = Account.query.filter_by(account_number=data['account']).first()
    if acc.balance >= data['amount']:
        acc.balance -= data['amount']
        db.session.add(Transaction(type="withdraw", amount=data['amount'], from_account_id=acc.id))
        db.session.commit()
        return jsonify({"message": "Withdrawal successful", "balance": acc.balance})
    return jsonify({"message": "Insufficient funds"}), 400

@transaction_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    data = request.json
    from_acc = Account.query.filter_by(account_number=data['from']).first()
    to_acc = Account.query.filter_by(account_number=data['to']).first()
    if from_acc.balance >= data['amount']:
        from_acc.balance -= data['amount']
        to_acc.balance += data['amount']
        db.session.add(Transaction(type="transfer", amount=data['amount'],
                                   from_account_id=from_acc.id, to_account_id=to_acc.id))
        db.session.commit()
        return jsonify({"message": "Transfer successful"})
    return jsonify({"message": "Insufficient funds"}), 400

@transaction_bp.route('/transactions/<account>', methods=['GET'])
@jwt_required()
def history(account):
    acc = Account.query.filter_by(account_number=account).first()
    txs = Transaction.query.filter((Transaction.from_account_id==acc.id) | 
                                   (Transaction.to_account_id==acc.id)).all()
    return jsonify([{"type": t.type, "amount": t.amount, "date": t.date} for t in txs])
