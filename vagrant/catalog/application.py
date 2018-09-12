from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Show a list of all categories
@app.route('/')
@app.route('/catalog')
def ShowCategories():
    category = session.query(Category).all()
    output = ''
    for i in category:
        output += i.name
        output += '</br>'
    return output


#Show Items In a given category by passing in the category_id (number)
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items')
def ShowItemsInCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
    return output


#Show a given item by passing in the catalog_item_id
@app.route('/item/<int:catalog_item_id>')
def ShowItem(catalog_item_id):
    item = session.query(CatalogItem).filter_by(id = catalog_item_id).one()
    category = session.query(Category).filter_by(id = item.category_id).one()
    output = ''
    output += item.name
    output += '</br>'
    output += item.description
    output += '</br>'
    output += item.price
    output += '</br>'
    output += category.name
    output += '</br>'
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
