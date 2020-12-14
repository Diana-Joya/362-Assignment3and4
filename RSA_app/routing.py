from RSA_app import app, db
from flask import redirect, url_for, render_template, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from RSA_app.forms import RegistrationForm, LoginForm, UpdateContactInfo, UpdateAvailability, AddMenuItem
from RSA_app.database import Restaurant, Businesshours, Menu, Menuitem, Order, Orderitem


@app.route("/", methods=["POST", "GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('user', name=current_user.name))
    form = LoginForm()
    if form.validate_on_submit():
        restaurant_usr = Restaurant.query.filter_by(email=form.email.data).first()
        if restaurant_usr and (form.password.data == restaurant_usr.password):
            login_user(restaurant_usr)
            return redirect(url_for('user', name=restaurant_usr.name))
        else:
            flash('Login Unsuccessful. Please check email & password!', 'danger')
    return render_template("index.html", form=form)


@app.route("/<name>")
def user(name):
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("home.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user', name=current_user.name))
    form = RegistrationForm()
    if form.validate_on_submit():
        restaurant = Restaurant(email=form.restaurant_email.data, password=form.password.data,
                                name=form.restaurant_name.data)
        db.session.add(restaurant)
        db.session.flush()
        mon_hours = Businesshours(restaurant_id=restaurant.restaurant_id, day=0)
        db.session.add(mon_hours)
        db.session.flush()

        tue_hours = Businesshours(restaurant_id=restaurant.restaurant_id, day=1)
        db.session.add(tue_hours)
        db.session.flush()

        wed_hours = Businesshours(restaurant_id=restaurant.restaurant_id, day=2)
        db.session.add(wed_hours)
        db.session.flush()

        th_hours = Businesshours(restaurant_id=restaurant.restaurant_id, day=3)
        db.session.add(th_hours)
        db.session.flush()

        fr_hours = Businesshours(restaurant_id=restaurant.restaurant_id, day=4)
        db.session.add(fr_hours)
        db.session.flush()

        sat_hours = Businesshours(restaurant_id=restaurant.restaurant_id, day=5)
        db.session.add(sat_hours)
        db.session.flush()

        sun_hours = Businesshours(restaurant_id=restaurant.restaurant_id, day=6)
        db.session.add(sun_hours)
        db.session.flush()

        menu = Menu(restaurant_id=restaurant.restaurant_id)
        db.session.add(menu)

        db.session.commit()

        flash('Your Account has been created!', 'success')
        return redirect(url_for('user', name=restaurant.name))
    return render_template("signup.html", form=form)


@app.route("/userpage")
def update_restaurant():
    return render_template("userpage.html")


@app.route("/reservationspage", methods=["POST", "GET"])
def reservations_page():
    form = UpdateAvailability()
    if form.validate_on_submit():
        if form.capacity.data:
            current_user.capacity = form.capacity.data

        schedule = Businesshours.query.filter_by(restaurant_id=current_user.restaurant_id).all()

        for day in schedule:
            if day.day == 0:
                if form.mon_start.data:
                    day.open_time = str(form.mon_start.data)
                if form.mon_end.data:
                    day.close_time = str(form.mon_end.data)
            elif day.day == 1:
                if form.tues_start.data:
                    day.open_time = str(form.tues_start.data)
                if form.tues_end.data:
                    day.close_time = str(form.tues_end.data)
            elif day.day == 2:
                if form.wed_start.data:
                    day.open_time = str(form.wed_start.data)
                if form.wed_end.data:
                    day.close_time = str(form.wed_end.data)
            elif day.day == 3:
                if form.th_start.data:
                    day.open_time = str(form.th_start.data)
                if form.th_end.data:
                    day.close_time = str(form.th_end.data)
            elif day.day == 4:
                if form.fri_start.data:
                    day.open_time = str(form.fri_start.data)
                if form.fri_end.data:
                    day.close_time = str(form.fri_end.data)
            elif day.day == 5:
                if form.sat_start.data:
                    day.open_time = str(form.sat_start.data)
                if form.sat_end.data:
                    day.close_time = str(form.sat_end.data)
            elif day.day == 6:
                if form.sun_start.data:
                    day.open_time = str(form.sun_start.data)
                if form.sun_end.data:
                    day.close_time = str(form.sun_end.data)

        db.session.commit()
        schedule = Businesshours.query.filter_by(restaurant_id=current_user.restaurant_id).all()
        return render_template("reservationSystem.html", schedule=schedule, form=form)

    schedule = Businesshours.query.filter_by(restaurant_id=current_user.restaurant_id).all()
    return render_template("reservationSystem.html", schedule=schedule, form=form)


@app.route("/orderspage")
def orders_page():
    open = Order.query.filter_by(status="open").all()
    accepted = Order.query.filter_by(status="accepted").all()
    return render_template("currentOrders.html", open=open, accepted=accepted)


@app.route("/accept", methods=["POST", "GET"])
def accept_order():
    order_id = request.form['order_to_accept']
    order = Order.query.filter_by(order_id=order_id).first()
    order.status = "accepted"
    db.session.commit()
    return redirect(url_for('orders_page'))


@app.route("/completed", methods=["POST", "GET"])
def complete_order():
    order_id = request.form['order_to_complete']
    order = Order.query.filter_by(order_id=order_id).first()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders_page'))


@app.route("/update-restaurant-info", methods=["POST", "GET"])
def update_db():
    form = UpdateContactInfo()
    if form.validate_on_submit():
        if form.email.data:
            current_user.email = form.email.data
        if form.name.data:
            current_user.name = form.name.data
        if form.address.data:
            current_user.address = form.address.data
        if form.phone.data:
            current_user.phone = form.phone.data
        if form.capacity.data:
            current_user.capacity = form.capacity.data
        if form.type.data:
            current_user.food_type = form.type.data
        if form.cost.data:
            current_user.cost = form.cost.data

        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for("update_restaurant"))
    return render_template("updateInfo.html", form=form)


@app.route("/restaurant-menu")
def restaurant_menu():
    menu = Menu.query.filter_by(restaurant_id=current_user.restaurant_id).first()
    return render_template("menu.html", menu=menu)


@app.route("/delete", methods=["POST", "GET"])
def delete_item():
    item_id = request.form['item_to_delete']
    item = Menuitem.query.filter_by(item_id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('restaurant_menu'))


@app.route("/edit", methods=["POST", "GET"])
def edit_item():
    item_id = request.form['item_to_edit']
    item = Menuitem.query.filter_by(item_id=item_id).first()
    return redirect(url_for('restaurant_menu'))


@app.route("/newItem", methods=["POST", "GET"])
def add_new_item():
    form = AddMenuItem()
    if form.validate_on_submit():
        menu = Menu.query.filter_by(restaurant_id=current_user.restaurant_id).first()
        item = Menuitem(menu_id=menu.menu_id, name=form.name.data, ingredients=form.ing.data,
                                allergens=form.allergens.data, price=form.price.data, available=form.avl.data)
        db.session.add(item)
        db.session.commit()

        flash('You\'ve added a new menu item!', 'success')
        return redirect(url_for('restaurant_menu'))
    return render_template("newMenuItem.html", form=form)


@app.route("/preview-page", methods=["GET"])
def preview():
    menu = Menu.query.filter_by(restaurant_id=current_user.restaurant_id).first()
    menu_id = menu.menu_id
    menuItems = Menuitem.query.filter_by(menu_id=menu_id).all()
    return render_template("PreviewPage.html", items=menuItems)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
