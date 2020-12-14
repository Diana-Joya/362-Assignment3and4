from RSA_app import db
from datetime import datetime
from RSA_app.database import Restaurant, Businesshours, Menu, Menuitem, Order, Orderitem

restaurant = Restaurant(email="Diana@test.com", password="runscript",
                        name="Diana's Gourmet Kitchen")
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

menu = Menu.query.filter_by(restaurant_id=restaurant.restaurant_id).first()
item = Menuitem(menu_id=menu.menu_id, name="Hot Dog", ingredients="Bun, hot dog sausage, ketchup, chips, cheese",
                        allergens="gluten, lactose", price=10.99, available=1)
db.session.add(item)

item2 = Menuitem(menu_id=menu.menu_id, name="Pop Corn", ingredients="Corn, butter, salt",
                        allergens="", price=5.99, available=1)
db.session.add(item2)

item3 = Menuitem(menu_id=menu.menu_id, name="Pizza", ingredients="Wheat crust, cheese, ham, corn, pepperoni",
                        allergens="gluten, lactose", price=15.99, available=1)
db.session.add(item3)
db.session.commit()

print(menu.menu_items)
print(menu.menu_items[0])

order1 = Order(timestamp=datetime.utcnow, restaurant_id=restaurant.restaurant_id)
db.session.add(order1)
orderitem1 = Orderitem(curr_order_id=order1.order_id, menu_item_id=item3.item_id, qty=3)
db.session.add(orderitem1)
orderitem2 = Orderitem(curr_order_id=order1.order_id, menu_item_id=item2.item_id, qty=5)
db.session.add(orderitem2)

db.session.commit()

print(order1.order_items)
print(order1.order_items[0])


