from flask import render_template, redirect, url_for, abort, flash, request, current_app, session
from flask_login import login_required, current_user, login_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, AddNewProductForm, EditProductForm, BuyForm
from ..auth.forms import SimpleLoginForm
from .. import db
from ..models import Role, User, Product, Purchase
from ..decorators import admin_required
from datetime import datetime, timedelta


@main.route('/', methods=['GET', 'POST'])
def index():
    loginform = SimpleLoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user is not None:
            session.permanent = True
            login_user(user, duration=timedelta(minutes=2))
            return redirect(url_for('.user', username=user.username))
        flash('Invalid username or barcode.')
    return render_template('index.html', loginform=loginform, user=current_user)


@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    buyform = BuyForm()
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.purchases.order_by(Purchase.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['CHOCSHOP_PURCHASES_PER_PAGE'],
        error_out=False)
    purchases = pagination.items

    if buyform.validate_on_submit():
        product = Product.query.filter_by(barcode=buyform.barcode.data).first_or_404()
        purchase = buy(current_user._get_current_object(), product)
        flash('You bought a {}, Your Balance is ${:.2f}'.format(purchase.product.name, float(current_user.balance)))
        return redirect(url_for('.user', username=user.username))
    return render_template('user.html', user=user, purchases=purchases, pagination=pagination, buyform=buyform)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.site = form.site.data
        current_user.building = form.building.data
        current_user.room = form.room.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.site.data = current_user.site 
    form.building.data = current_user.building
    form.room.data = current_user.room 
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.site = form.site.data
        user.building = form.building.data
        user.room = form.room.data
        user.balance = form.balance.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.site.data = user.site 
    form.building.data = user.building
    form.room.data = user.room 
    form.balance.data = user.balance
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/add-product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_new_product():
    form = AddNewProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
            barcode=form.barcode.data,
            current_price=form.current_price.data, url=form.url.data)
        db.session.add(product)
        db.session.commit()
        flash('The product has been added.')
        return redirect(url_for('.add_new_product'))
    return render_template('add_new_product.html', form=form, user=user)

@main.route('/products', methods=['GET', 'POST'])
def product_list():
 #   products = Product.query.order_by(Product.name).all()
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.order_by(Product.name).paginate(
        page,
        per_page=current_app.config['CHOCSHOP_PURCHASES_PER_PAGE'],
        error_out=False)
    products = pagination.items
    return render_template('product_list.html', products=products, user=current_user, pagination=pagination)

@main.route('/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = EditProductForm(product=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.barcode = form.barcode.data
        product.current_price = form.current_price.data
        product.url = form.url.data
        db.session.add(product)
        db.session.commit()
        flash('The product has been modified.')
        return redirect(url_for('.product_list'))
    form.name.data = product.name
    form.barcode.data = product.barcode
    form.current_price.data = product.current_price
    form.url.data = product.url
    return render_template('edit_product.html', form=form, product=product)

def buy(user, product):
    purchase = Purchase(price=product.current_price, buyer=user, timestamp=datetime.utcnow(), product=product)
    user.balance = float(user.balance) - float(purchase.price)
    db.session.add(purchase)
    db.session.add(user)
    db.session.commit()
    return purchase

@main.route('/buy/<int:id>', methods=['GET', 'POST'])
@login_required
def buy_product(id):
    product = Product.query.get_or_404(id)
    purchase = buy(current_user._get_current_object(), product)
    flash('You bought a {}, Your Balance is ${:.2f}'.format(purchase.product.name, float(current_user.balance)))
    return redirect(url_for('.product_list'))


@main.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def user_list():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.name).paginate(
        page,
        per_page=current_app.config['CHOCSHOP_USERS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('user_list.html', users=users, user=current_user, pagination=pagination)

@main.route('/purchases', methods=['GET', 'POST'])
@login_required
@admin_required
def purchase_list():
    page = request.args.get('page', 1, type=int)
    pagination = Purchase.query.order_by(Purchase.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['CHOCSHOP_PURCHASES_PER_PAGE'],
        error_out=False)
    purchases = pagination.items
    return render_template('purchase_list.html', purchases=purchases, user=current_user, pagination=pagination)



