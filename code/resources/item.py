import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This filed can't be left blank!"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        # print("item executed", item)
        if item:
            return item.json() 
        return None

    def post(self, name):
        # print("item post self.get", self.get(name))
        if ItemModel.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()  
        
        item =  ItemModel(name, **data)
        print( 'item in item post' ,item.name)

        try:
            item.save_to_db()
        except:
            return {'Message': 'An error occurred inserting the item.'}, 500

        return item.json(), 201
   
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
     
        return {'Message': 'Item Deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
      
        if item is None:
           item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()  
                  
class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}