from flask import Blueprint,jsonify,request
from models import db, Item
import sys
import os

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/api/user/items',methods=['GET'])
def get_all_items():
    try:
        items = Item.query.all()
        items_all = [
            {
                "name":item.name,
                "quantity":item.quantity,
                "category_id":item.category_id,
                "supplier_id":item.supplier_id
            }
            for item in items
        ]
        return jsonify({'message':'This are all the items we have in our inventory','data':items_all}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@user_bp.route('/api/user/items/<int:items_id>',methods=['GET'])
def get_single_item(items_id):
    try:
        item = Item.query.get(items_id)
        single_item = {
            "name":item.name,
            "quantity":item.quantity,
            "category_id":item.category_id,
            "supplier_id":item.supplier_id
        }
        return jsonify({'message':'This is a single item','data':single_item}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500


@user_bp.route('/api/user/search',methods=['GET'])
def search_item():
    try:
        query = request.args.get('q','')
        if query.strip() == '':
            return jsonify({'message': 'Query parameter "q" is required and cannot be empty'}), 400

        items = Item.query.filter(Item.name.ilike(f'%{query}%')).all()
        result = [
            {
                "id":item.id,
                "name":item.name,
                "quantity":item.quantity,
                "category_id":item.category_id,
                "supplier_id":item.supplier_id
            }
            for item in items
        ]
        return jsonify({'message':'This is your item that you searched for','data':result}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@user_bp.route('/api/user/buy/<int:item_id>',methods=['POST'])
def buy_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'message':'Item not found'}),404

        if item.quantity<=0:
            return jsonify({'message':'item out of stock'}),404

        item.quantity-=1
        db.session.commit()
        return jsonify(
            {'message': f'You have successfully bought {item.name}', 'remaining_quantity': item.quantity}), 200
    except Exception as e:
        return jsonify({'message': 'Server error', 'error': str(e)}), 500



