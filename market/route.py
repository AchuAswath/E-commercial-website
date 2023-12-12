from market import app, db
from flask import render_template, request, redirect, url_for, flash, get_flashed_messages, request
from market.model import Item, User
from market.forms import RegisterForm, LoginForm, purchaseform
from flask_wtf import FlaskForm
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    purchase_form = purchaseform()
    if request.method == 'POST':
        purchased_item = request.form.get('purchase_item')
        P_item_obj = Item.query.filter_by(name=purchased_item).first()
        if P_item_obj:
            P_item_obj.owner_id = current_user.id

            db.session.commit()
            flash(f"You have successfully ordered {P_item_obj.name} for price {P_item_obj.price}")
            return redirect(url_for('product'))
        else:
            flash("You have insufficient balance")

    return render_template('product.html',item_name=Item.query.all(), purchase_form=purchase_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        email_address = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email_address == email_address))

        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            username=request.form.get('name'),
            email_address=request.form.get('email'),
            password_hash=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("product"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email_address = request.form.get('email')
        password_hash = request.form.get('password1')

        result = db.session.execute(db.select(User).where(User.email_address == email_address))
        user = result.scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not (user.password_hash, password_hash):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('product'))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
