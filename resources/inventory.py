from flask_restful import Resource, reqparse
from models import db, Inventory

class InventoryResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True, type=int, help='book_id is required')
    parser.add_argument('current_stock', required=True, type=int, help='current_stock is required')


    def get(self, id=None):
        if id:
            inventory = Inventory.query.filter_by(id=id).first()
            
            if inventory == None:
                return { 'message': 'Inventory not found'},404 
            
            return inventory.as_dict()
        
        else:
            inventories = Inventory.query.all()
            return [inventory.as_dict() for inventory in inventories]
    