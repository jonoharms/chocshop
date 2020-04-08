from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, AddNewProductForm, EditProductForm
from .. import db
from ..models import Role, User, Product, Purchase
from ..decorators import admin_required
from datetime import datetime

@main.route('/')
def index():
    purchases = Purchase.query.order_by(Purchase.timestamp.desc()).all()

    return render_template('index.html', purchases=purchases)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


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
    products = Product.query.order_by(Product.name).all()
    return render_template('product_list.html', products=products, user=current_user)

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

@main.route('/buy/<int:id>', methods=['GET', 'POST'])
@login_required
def buy_product(id):
    product = Product.query.get_or_404(id)
    purchase = Purchase(price=product.current_price, buyer=current_user._get_current_object(), timestamp=datetime.utcnow(), product=product)
    current_user.balance = float(current_user.balance) - float(purchase.price)
    db.session.add(purchase)
    db.session.add(current_user._get_current_object())
    db.session.commit()
    flash('Product Bought, Your Balance is ${:.2f}'.format(float(current_user.balance)))
    return redirect(url_for('.product_list'))




