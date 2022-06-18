from market import app, db
from flask import render_template, flash, redirect, url_for, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from flask_login import login_user, logout_user, login_required, current_user



@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/market", methods=["GET","POST"])
@login_required
def market():
    form_purchase = PurchaseForm()
    form_sell = SellForm()
    if request.method == "POST":
        purchased_item = request.form.get("purchased_item")
        purchased_item_object = Item.query.filter_by(name = purchased_item).first()
        sold_item = request.form.get("sold_item")
        sold_item_object = Item.query.filter_by(name = sold_item).first()

        if purchased_item_object:


            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                db.session.commit()
                flash(f"You have bought {purchased_item} successfully")
            else:
                flash(f"No money enough to buy {purchased_item}")
        if sold_item_object:
            sold_item_object.sell(current_user)
            db.session.commit()
            flash(f"You have sold {sold_item} successfully")

        return redirect(url_for("market"))
    if request.method == "GET":
        purchased_items = current_user.items
        items = Item.query.filter_by(owner = None)
        return render_template("market.html", items=items, form_purchase=form_purchase, purchased_items = purchased_items, form_sell=form_sell )

@app.route("/register", methods = ['GET','POST'])

def register_page():
    form = RegisterForm()

    if form.validate_on_submit():

        user_created = User(username = form.username.data,
                            email_address = form.email_address.data,
                            )
        user_created.set_password(form.password1.data)

        db.session.add(user_created)
        db.session.commit()
        login_user(user_created)
        flash(f"You have already created account successfully, now you are logging on username :{user_created.username}", category="success")
        return redirect(url_for('market'))
    if form.errors: # if there are error s
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user :{err_msg}')
    return render_template('register.html', form = form )

@app.route("/login", methods = ['GET','POST'])

def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        print("aaa")
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user is None or not attempted_user.check_password(form.password.data):
            flash("Username or password Invalid, Please try again !!!",category='danger')
            return redirect(url_for("login_page"))

        login_user(attempted_user)
        flash(f"You have already logged in successfully on username :{attempted_user.username}", category="success")
        return redirect(url_for("market"))


    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out !!!", category="success")
    return redirect(url_for("home_page"))




