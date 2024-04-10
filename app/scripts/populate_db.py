import random
from ..repositories.managers import BeverageManager, IngredientManager, OrderManager, SizeManager
from ..controllers import OrderController
from faker import Faker
import traceback




ingredients=['Spinach', 'Bacon', 'Anchovies', 'Artichokes', 'Broccoli', 'Olives', 'Pineapple', 'Cheese', 'Tuna', 'Peppers','Chochos']
beverages=['Coke', 'Pepsi', 'Sprite', 'Fanta', '7up', 'Water', 'Beer', 'Wine', 'Milk', 'Coffee']
sizes=['Small', 'Medium', 'Large', 'Extra Large', 'Family']
fake=Faker('es_CO')

def get_random_price(lower_bound: float, upper_bound: float) -> float:
    return round(random.uniform(lower_bound, upper_bound), 2)

def insert_ingredients():
    for i in range(len(ingredients)):
        IngredientManager.create({"name":ingredients[i], "price":get_random_price(1, 1.75)})

def insert_beverages():
    for i in range(len(beverages)):
        BeverageManager.create({"name":beverages[i], "price":get_random_price(2, 4)})

def insert_sizes():
    for i in range(len(sizes)):
        SizeManager.create({"name":sizes[i], "price":get_random_price(2, 4)})

def get_random_ingredients():
    ingredients= IngredientManager.get_all()
    ingredient_number= random.randint(1, 10)
    chosen_ingredients=[]
    while len(chosen_ingredients)<ingredient_number:
        ingredient= random.choice(ingredients)["_id"]
        if ingredient not in chosen_ingredients:
            chosen_ingredients.append(ingredient)
    return chosen_ingredients

def get_random_sizes():
    sizes= SizeManager.get_all()
    return random.choice(sizes)["_id"]

def get_random_beverages():
    beverages= BeverageManager.get_all()
    beverage_number= random.randint(1, 10)
    chosen_beverages=[]
    while len(chosen_beverages)<beverage_number:
        beverage= random.choice(beverages)["_id"]
        if beverage not in chosen_beverages:
            chosen_beverages.append(beverage)
    return chosen_beverages

def insert_client():
    client={
        'client_name': fake.name(),
        'client_address': fake.address(),
        'client_phone': fake.phone_number(),
        'client_dni': fake.nuip()
    }
    return client

def insert_orders(client_number, order_number):
    orders_controller=OrderController()

    clients=[]
    for _ in range(client_number):
        clients.append(insert_client())
    
    for _ in range(order_number):
        size= get_random_sizes()
        ingredients= get_random_ingredients()
        beverages= get_random_beverages()
        size_price= SizeManager.get_by_id(size).get('price')
        ingredients_names= IngredientManager.get_by_id_list(ingredients)
        beverages_names= BeverageManager.get_by_id_list(beverages)
        order_price=orders_controller.calculate_order_price(size_price, ingredients_names, beverages_names)
        client = clients[random.randint(0, client_number-1)]
        OrderManager.create({
            "size_id":size,
            "client_name":client['client_name'], 
            "client_address":client['client_address'], 
            "client_phone":client['client_phone'], 
            "client_dni":client['client_dni'],
            "date":fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None),
            "total_price":order_price,
            },ingredients_names,beverages_names)
        

def populate_db(client_number, order_number):
    try:
        insert_ingredients()
        insert_beverages()
        insert_sizes()
        insert_orders(client_number, order_number)
        print('Database populated successfully')
    except Exception as e:
        traceback.print_exc()
        print(f'Error populating database: {e}')





