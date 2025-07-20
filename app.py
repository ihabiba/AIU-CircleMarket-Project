import os
from flask import Flask, json, jsonify, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'AIUESHOP2025'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aiuShop.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/LENOVO/Downloads/aiu e-shop (3)/aiu e-shop/instance/aiuShop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

class Seller(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)  # Assume products table exists
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    customer = db.relationship('Customer', backref='cart_items')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)  # Path to the product image
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)  # Foreign key to Seller

    seller = db.relationship('Seller', backref='products')  # Relationship to Seller
    

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship with Order
    orders = db.relationship('Order', backref='user', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    hostel_block = db.Column(db.String(50), nullable=False)
    room_number = db.Column(db.String(50), nullable=False)
    payment_category = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # Add a status field
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Foreign key to Product

    product = db.relationship('Product', backref='orders')  # Relationship to Product

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    email = session.get('email')
    return render_template('profile.html', username=username, email=email)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('profile'))  # Redirect to the home page or login page

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()  # Adjust the query as needed
    return render_template('shop.html', products=products)

@app.route('/cart')
def cart():
    user_id = session.get('user_id')  # Get the current user's ID
    orders = Order.query.filter_by(user_id=user_id).all()  # Fetch orders for the user

    # Assuming you have a way to get the cart items from the session
    cart_items = session.get('cart', [])  # Example of getting cart items from session
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)  # Calculate total

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount, orders=orders)

@app.route('/shop')
def shop():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('shop.html', products=products)

@app.route('/place-order', methods=['POST'])
def place_order():
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.form.get('full-name')
        student_id = request.form.get('student-id')
        hostel_block = request.form.get('hostel-block')
        room_number = request.form.get('room-number')
        payment_category = request.form.get('payment-category')
        
        # Get the current user's ID from the session
        user_id = session.get('user_id')  # Assuming you store user ID in session

        # Get cart data from the form
        cart_data = request.form.get('cart')
        cart_items = json.loads(cart_data)  # Parse the JSON string into a Python object

        # Create orders for each item in the cart
        for item in cart_items:
            product_id = item['id']  # Assuming each item has an 'id'
            total_amount = item['price'] * item['quantity']  # Calculate total for this item

            # Create a new order for each product
            new_order = Order(
                full_name=full_name,
                student_id=student_id,
                hostel_block=hostel_block,
                room_number=room_number,
                payment_category=payment_category,
                total_amount=total_amount,
                user_id=user_id,  # Associate the order with the user
                product_id=product_id  # Associate the order with the product
            )
            db.session.add(new_order)

        db.session.commit()
        flash('Your order is pending!', 'success')
        return redirect(url_for('cart'))  # Redirect to cart to show order status

@app.route('/admin/view-orders')
def view_orders():
    # Get the current seller's ID from the session
    seller_id = session.get('user_id')  # Assuming seller ID is stored in session

    # Fetch orders for products added by the current seller
    products = Product.query.filter_by(seller_id=seller_id).all()  # Get products for the seller
    product_ids = [product.id for product in products]  # Get the IDs of those products

    # Fetch orders that are associated with the seller's products
    orders = Order.query.filter(Order.product_id.in_(product_ids)).all()

    return render_template('view_orders.html', orders=orders)

@app.route('/admin/confirm-order/<int:order_id>', methods=['POST'])
def confirm_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order.status = 'confirmed'  # Update the order status
        db.session.commit()
        flash('Order has been confirmed!', 'success')  # Flash message for confirmation
        # Notify the user about the order status
        user_id = order.user_id
        user = User.query.get(user_id)
        flash(f'Your order #{order.id} has been confirmed!', 'success')  # Notify user
    return redirect(url_for('view_orders'))  # Redirect to the orders view

@app.route('/admin/decline-order/<int:order_id>', methods=['POST'])
def decline_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order.status = 'declined'  # Update the order status
        db.session.commit()
        flash('Order has been declined!', 'danger')  # Flash message for decline
        # Notify the user about the order status
        user_id = order.user_id
        user = User.query.get(user_id)
        flash(f'Your order #{order.id} has been declined!', 'danger')  # Notify user
    return redirect(url_for('view_orders'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        customer = Customer.query.filter_by(email=email).first()
        seller = Seller.query.filter_by(email=email).first()
        
        if customer and check_password_hash(customer.password, password):
            session['role'] = 'customer'
            session['username'] = customer.username
            session['email'] = customer.email  # Store email in session
            session['user_id'] = customer.id
            flash(f'Welcome, {customer.username}!', 'success')
            return redirect(url_for('profile'))  # Redirect to profile page
        elif seller and check_password_hash(seller.password, password):
            session['role'] = 'seller'
            session['username'] = seller.username
            session['email'] = seller.email  # Store email in session
            session['user_id'] = seller.id
            return redirect(url_for('admin'))  # Redirect to profile page
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/role-selection', methods=['POST'])
def role_selection():
    role = request.form.get('role')
    if role == 'customer':
        return redirect(url_for('register', role='customer'))
    elif role == 'seller':
        return redirect(url_for('register', role='seller'))
    else:
        return redirect(url_for('index'))

@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if role == 'customer':
            if Customer.query.filter_by(email=email).first():
                flash('Email already registered as customer', 'danger')
            else:
                hashed_password = generate_password_hash(password)
                new_customer = Customer(username=username, email=email, password=hashed_password)
                db.session.add(new_customer)
                db.session.commit()
                
                # Store user information in the session
                session['username'] = new_customer.username
                session['email'] = new_customer.email
                
                return redirect(url_for('login'))  # Redirect to the profile page
        elif role == 'seller':
            if Seller.query.filter_by(email=email).first():
                flash('Email already registered as seller', 'danger')
            else:
                hashed_password = generate_password_hash(password)
                new_seller = Seller(username=username, email=email, password=hashed_password)
                db.session.add(new_seller)
                db.session.commit()
                
                # Store user information in the session
                session['username'] = new_seller.username
                session['email'] = new_seller.email
                p
                return redirect(url_for('login'))  # Redirect to the profile page
    return render_template('register.html', role=role)

@app.route('/dashboard/<role>')
def dashboard(role):
    if 'role' in session:
        if session['role'] == role:
            return f"Welcome to the {role} dashboard, {session['username']}!"
        else:
            return redirect(url_for('dashboard', role=session['role']))
    else:
        return redirect(url_for('login'))

@app.route('/add-product', methods=['POST'])
def add_product():
    if 'role' in session and session['role'] == 'seller':
        name = request.form.get('product-name')
        description = request.form.get('description')
        price = request.form.get('product-price')
        image_url = request.form.get('product-image-url')  # Get the image URL from the form

        # Get the seller's ID from the session
        seller_id = session['user_id']

        # Validate the image URL (optional)
        if image_url:
            new_product = Product(
                name=name,
                description=description,
                price=float(price),
                image_path=image_url,
                seller_id=seller_id  # Associate the product with the seller
            )
            db.session.add(new_product)
            db.session.commit()
        else:
            flash('Please provide a valid image URL.', 'danger')

        return redirect(url_for('admin'))
    else:
        flash('You must be logged in as a seller to add products.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin/edit_product', methods=['GET'])
def edit_product():
    # Get the current seller's ID from the session
    seller_id = session.get('user_id')  # Assuming seller ID is stored in session

    # Fetch only the products that belong to the logged-in seller
    products = Product.query.filter_by(seller_id=seller_id).all()
    return render_template('edit_product.html', products=products)

@app.route('/admin/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    # Get the current seller's ID from the session
    seller_id = session.get('user_id')  # Assuming seller ID is stored in session

    # Fetch the product from the database
    product = Product.query.get_or_404(product_id)

    # Check if the product belongs to the logged-in seller
    if product.seller_id != seller_id:
        flash('You do not have permission to delete this product.', 'danger')
        return redirect(url_for('edit_product_page'))

    # If the product belongs to the seller, delete it
    db.session.delete(product)
    db.session.commit()
    flash('Product removed successfully!', 'success')
    return redirect(url_for('edit_product_page'))
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)