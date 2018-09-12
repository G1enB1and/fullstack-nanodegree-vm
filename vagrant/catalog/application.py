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
    output += '<h3>Categories:</h3></br>'
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
    output = '<h3>'
    output += category.name
    output += ':</h3></br>'

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


#Add new category
@app.route('/category/new', methods=['GET','POST'])
def addNewCategory():
    output = ''
    output += 'Add a new category'
    return output

#    if request.method == 'POST':
#        newCategory = Category(name = request.form['name'])
#        session.add(newCategory)
#        session.commit()
#        output = ''
#        output += 'Added '
#        output += newCategory
#        output += '.'
#        return output
#    else:
#        output = ''
#        output += 'Failed to add new category because POST method was not used.'
#        return output

#Edit a category
@app.route('/category/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
    output = ''
    output += 'Edit category '
    output += str(category_id)
    output += '</br>'
    #add code to accomidate for urls to edit categories that do not exist
    return output


#Delete a category
@app.route('/category/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
    output = ''
    output += 'Delete category '
    output += str(category_id)
    output += '</br>'
    #add code to accomidate for urls to delete categories that do not exist
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
