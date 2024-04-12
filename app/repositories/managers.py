from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column, desc, func

from .models import Beverage,Ingredient, Order, OrderDetail, Size, db
from .serializers import (BeverageSerializer,IngredientSerializer, OrderSerializer,
                          SizeSerializer, ma)

months=['January','February','March','April','May','June','July','August','September','October','November','December']
class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages:Optional[List[Beverage]] = None):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        if beverages:
            cls.session.add_all((OrderDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                                 for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()

class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
    
class ReportManager:
    session=db.session
    @classmethod
    def get_top_ingredient(cls):
        top_ingredient_query=cls.session.query(Ingredient.name,
                                               func.count(OrderDetail.ingredient_id).label('total')).join(OrderDetail).group_by(Ingredient.name).order_by(desc('total')).all()
        top_ingredient={}
        if top_ingredient_query:
            top_ingredient={
                'name':top_ingredient_query[0][0],
                'total':top_ingredient_query[0][1]
            }
        return top_ingredient
    
    @classmethod
    def get_top_customers(cls):
        top_customers_query=cls.session.query(Order.client_name,
                                              func.count(Order._id).label('total')).group_by(Order.client_name).order_by(desc('total')).limit(3).all()
        top_customers = []
        for customer_data in top_customers_query:
            customer = {
                'name': customer_data[0],
                'total': customer_data[1]
            }
            top_customers.append(customer)

        print(top_customers)
        return top_customers
    
    @classmethod
    def get_most_earning_month(cls):
        
        most_earning_month_query=cls.session.query(func.extract('month',Order.date).label('month'),
                                                   func.sum(Order.total_price).label('total')).group_by(func.extract('month',Order.date)).order_by(desc('total')).all()
        most_earning_month={}
        if most_earning_month_query:
            month_to_show=months[most_earning_month_query[0][0]-1]
            most_earning_month={
                'month':month_to_show,
                'total':most_earning_month_query[0][1]
            }
        return most_earning_month
        
