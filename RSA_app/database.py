import os
import datetime
from RSA_app import db, login_manager
from flask_login import UserMixin

# Load Users
@login_manager.user_loader
def load_user(rid):
    return Restaurant.query.get(int(rid))


class Restaurant(db.Model, UserMixin):
    restaurant_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    food_type = db.Column(db.String(100))
    cost = db.Column(db.String(5))
    capacity = db.Column(db.Integer, default=0)
    schedule = db.relationship('Businesshours', backref="restaurant", lazy=True)
    menu = db.relationship('Menu', backref="restaurant", lazy=True)
    orders = db.relationship('Order', backref="restaurant", lazy=True)

    def __repr__(self):
        return f"Restaurant('{self.restaurant_id}','{self.name}','{self.email}')"

    def get_id(self):
        return self.restaurant_id


class Businesshours(db.Model):
    schedule_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'))
    day = db.Column(db.Integer, nullable=False)
    open_time = db.Column(db.String(20), default="None")
    close_time = db.Column(db.String(20), default="None")


class Menu(db.Model):
    menu_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'))
    menu_items = db.relationship('Menuitem', backref="menu", lazy=True)


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    status = db.Column(db.Unicode, default="open")
    order_items = db.relationship('Orderitem', backref="order", lazy=True)


class Menuitem(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(200))
    allergens = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Integer, default=1)


class Orderitem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True)
    curr_order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menuitem.item_id'), nullable=False)
    qty = db.Column(db.Integer, default=1)


