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
    

    def post(self):
        data = InventoryResource.parser.parse_args()

        book_id = Inventory.query.filter_by(book_id = data['book_id']).first()

        if book_id:
            return { "message": "Book_id already exists"}, 422

        inventory = Inventory(**data)

        db.session.add(inventory)

        db.session.commit()

        return {"message": "Inventory created successfully"}, 201
    

    def delete(self, id):
        inventory = Inventory.query.filter_by(id=id).first()

        if inventory is None:
            return {"message": "Inventory not found"}, 404
        
        db.session.delete(inventory)
        db.session.commit()

        return {"message": "Inventory deleted successfully"}, 204
    

    def put(self, id):
        inventory = Inventory.query.filter_by(id=id).first()

        if inventory is None:
            return {"message": "inventory not found"}, 404
        
        data = InventoryResource.parser.parse_args()

        # inventory.book_id = data['book_id']
        inventory.current_stock = data['current_stock']

        db.session.commit()

        return {"message": "Inventory updated successfully"}, 200

