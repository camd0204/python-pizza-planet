from app.plugins import ma
from .models import Beverage, Ingredient, Size, Order, OrderDetail

class SerializerFactory:
    @staticmethod
    def create_serializer(model):
        class_name = model.__name__ + 'Serializer'
        Meta = type('Meta', (), {'model': model, 'load_instance': True})
        dynamic_attrs = {}

        if model == OrderDetail:
            fields = (
                'ingredient_price',
                'ingredient',
                'beverage_price',
                'beverage'
            )
            dynamic_attrs['fields'] = fields
            dynamic_attrs['ingredient'] = ma.Nested(IngredientSerializer)
            dynamic_attrs['beverage'] = ma.Nested(BeverageSerializer)

        elif model == Order:
            fields = (
                '_id',
                'client_name',
                'client_dni',
                'client_address',
                'client_phone',
                'date',
                'total_price',
                'size',
                'detail'
            )
            dynamic_attrs['fields'] = fields
            dynamic_attrs['size'] = ma.Nested(SizeSerializer)
            dynamic_attrs['detail'] = ma.Nested(OrderDetailSerializer, many=True)

        else:
            fields = ('_id', 'name', 'price')
            dynamic_attrs['fields'] = fields

        dynamic_attrs['Meta'] = Meta
        serializer_class = type(class_name, (ma.SQLAlchemyAutoSchema,), dynamic_attrs)
        return serializer_class

# Example usage:
# Create serializer for Beverage model
BeverageSerializer = SerializerFactory.create_serializer(Beverage)

# Create serializer for Ingredient model
IngredientSerializer = SerializerFactory.create_serializer(Ingredient)

# Create serializer for Size model
SizeSerializer = SerializerFactory.create_serializer(Size)

# Create serializer for OrderDetail model
OrderDetailSerializer = SerializerFactory.create_serializer(OrderDetail)

# Create serializer for Order model
OrderSerializer = SerializerFactory.create_serializer(Order)
