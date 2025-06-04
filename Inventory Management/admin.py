from flask import Blueprint,jsonify,request
from flask_login import login_user,logout_user
from werkzeug.security import check_password_hash,generate_password_hash
from models import User,Category,Supplier,Item,db
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

admin_bp = Blueprint('admin', __name__, url_prefix='/api')




@admin_bp.route('/api/register',methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        if not username or not password or not role:
            return jsonify({'message':'Please fill in all forms'}),404

        password_hash = generate_password_hash(password)

        new_user = User(username =username,password =password_hash,role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'Thank you for Registering. Now login!'}),201
    except Exception as e:
        return jsonify({'message':'Invalid server error','error':str(e)}),500

@admin_bp.route('/api/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'message':'Invalid Login'}),404

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            db.session.commit()
            return jsonify({'message':'You have successfully logged in'}),200
        return jsonify({'message':'Try again please'}),404
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@admin_bp.route('/api/logout',methods=['GET'])
def logout():
    try:
        logout_user()
        return jsonify({'message':'You have successfully logged out'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)},500)

@admin_bp.route('/api/category',methods=['POST'])
def category():
    try:
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({'message':'Please add the name of this category'}),404

        user = Category(name=name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'The category has been added to the collection'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/all_category',methods=['GET'])
def all_category():
    try:
        all_category = Category.query.all()
        category_list = [
            {
                "id" :c.id,
                'name': c.name

            }
            for c in all_category
        ]
        return jsonify({'Category':category_list}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/single_category/<int:category_id>',methods=['GET'])
def single_category(category_id):
    try:
        category = Category.query.get(category_id)

        category_data = {
            "id": category.id,
            "name":category.name
        }
        return jsonify({'message':'This is the data for this category','data':category_data}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@admin_bp.route('/api/edit_category/<int:category_id>',methods=['PUT'])
def edit_category(category_id):
    try:
        category = Category.query.get(category_id)
        data = request.get_json()
        category.name = data.get('name',category.name)
        return jsonify({'message':'This category has been updated','data':category.name}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/image_category',methods=['POST'])
def image_category():
    try:
        if 'image' not in request.files:
            return jsonify({'message':'Image not in file'}),404

        file = request.files['Image']
        if file.filename == '':
            return jsonify({'message':'file not found'}),404

        filename = secure_filename(file.filename)
        filepath = os.path.join(admin_bp.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        return jsonify({'message':'Your image has been added'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/delete_category/<int:category_id>',methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message':'This category has been deleted!!'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500


@admin_bp.route('/api/supplier',methods=['POST'])
def supplier():
    try:
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({'message':'Name must be added'}),404

        user = Supplier(name=name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'Supplier has been added'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/all_supplier',methods=['GET'])
def all_supplier():
    try:
        supplier = Supplier.query.all()
        supplier_list = [
            {
                "id":s.id,
                "name":s.name
            }
            for s in supplier
        ]
        return jsonify({'message':'This are all the suppliers','data':supplier_list}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/single_supplier/<int:supplier_id>',methods=['GET'])
def single_supplier(supplier_id):
    try:
        supplier = Supplier.query.get(supplier_id)
        supplier_data = {
            "id":supplier.id,
            "name":supplier.name
        }
        return jsonify({'message':'This is the data for this particular supplier','data':supplier_data}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/edit_supplier/<int:supplier_id>',methods = ['PUT'])
def edit_supplier(supplier_id):
    try:
        supplier = Supplier.query.get(supplier_id)
        data = request.get_json()
        supplier.name = data.get('name',supplier.name)
        return jsonify({'message':'This supplier name has been updated..'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/delete_supplier/<int:supplier_id>',methods=['DELETE'])
def delete_supplier(supplier_id):
    try:
        supplier= Supplier.query.get(supplier_id)
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message':'This supplier has been deleted'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/item',methods=['POST'])
def item():
    try:
        data = request.get_json()
        name = data.get('name')
        quantity = data.get('quantity')
        category_id = data.get('category_id')
        supplier_id = data.get('supplier_id')
        if not name or not quantity or not category_id or not supplier_id:
            return jsonify({'message':'Please fill in all form'}),404

        user = Item(name=name,quantity=quantity,category_id=category_id,supplier_id=supplier_id)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'Item has been added'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/all_item',methods=['GET'])
def all_item():
    try:
        items = Item.query.all()
        item_list = [
            {
                "name":item.name,
                "quantity":item.quantity,
                "category_id":item.category_id,
                "supplier_id":item.supplier_id
            }
            for item in items
        ]
        return jsonify({'message':'This are all the items','data':item_list}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/single_item/<int:item_id>',methods=['GET'])
def single_item(item_id):
    try:
        item = Item.query.get(item_id)
        item_single = {
            "name":item.name,
            "quantity": item.quantity,
            "category_id":item.category_id,
            "supplier_id":item.supplier_id
        }
        return jsonify({'message':'This is a single item','item':item_single}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/edit_item/<int:item_id>',methods=['PUT'])
def edit_item(item_id):
    try:
        item = Item.query.get(item_id)
        data = request.get_json()
        item.name = data.get('name', item.name)
        item.quantity = data.get('quantity',item.quantity)
        item.category_id = data.get('category_id', item.category_id)
        item.supplier_id = data.get('supplier_id',item.supplier_id)
        db.session.commit()
        return jsonify({'message':'Your item has been updated'}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@admin_bp.route('/api/delete_item/<int:item_id>',methods=['DELETE'])
def delete_item(item_id):
    try:
        item = Item.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message':'Your item has been deleted'}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

