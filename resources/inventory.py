from flask_restful import Resource, reqparse
from models import db, Inventory

class InventoryResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', required=True, type=int, help='book_id is required')
    parser.add_argument('current_stock', required=True, type=int, help='current_stock is required')