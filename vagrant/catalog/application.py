from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    #output = ''
    #output += '<h3>Categories:</h3></br>'
    #for i in category:
    #    output += i.name
    #    output += '</br>'
    return render_template('show-categories.html', category = category)


#Show Items In a given category by passing in the category_id (number)
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items')
def ShowItemsInCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category.id)
    return render_template('show-items-in-category.html', category = category, items = items, category_id = category_id)


#Show a given item by passing in the catalog_item_id
@app.route('/item/<int:catalog_item_id>')
def ShowItem(catalog_item_id):
	item = session.query(CatalogItem).filter_by(id = catalog_item_id).one()
	category = session.query(Category).filter_by(id = item.category_id).one()
	return render_template('show-item.html', item = item, category = category, catalog_item_id = catalog_item_id)


#Add new category
@app.route('/category/new', methods=['GET','POST'])
def addNewCategory():
    #output = ''
    #output += 'Add a new category'
    return render_template('new-category.html')

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
    #output = ''
    #output += 'Edit category '
    #output += str(category_id)
    #output += '</br>'
    #add code to accomidate for urls to edit categories that do not exist
	#change code to not edit the id, but the name
	category = session.query(Category).filter_by(id = category_id).one()
	return render_template('edit-category.html', category = category, category_id = category_id)


#Delete a category
@app.route('/category/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
    #output = ''
    #output += 'Delete category '
	#output += str(category_id)
    #output += '</br>'
    #add code to accomidate for urls to delete categories that do not exist
	category = session.query(Category).filter_by(id = category_id).one()
	return render_template('delete-category.html', category = category, category_id = category_id)


#Add new item
@app.route('/item/new', methods=['GET','POST'])
def addNewItem():
    #output = ''
    #output += 'Add a new item'
    return render_template('new-item.html')


#Edit an item
@app.route('/item/<int:catalog_item_id>/edit', methods=['GET','POST'])
def editItem(catalog_item_id):
    #output = ''
    #output += 'Edit item '
    #output += str(catalog_item_id)
    #output += '</br>'
    #add code to accomidate for urls to edit items that do not exist
	item = session.query(CatalogItem).filter_by(id = catalog_item_id).one()
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(id = item.category_id).one()
	return render_template('edit-item.html', item = item, category = category, catalog_item_id = catalog_item_id, categories = categories)


#Delete an item
@app.route('/item/<int:catalog_item_id>/delete', methods=['GET','POST'])
def deleteItem(catalog_item_id):
    #output = ''
    #output += 'Delete item '
    #output += str(catalog_item_id)
    #output += '</br>'
    #add code to accomidate for urls to delete items that do not exist
	item = session.query(CatalogItem).filter_by(id = catalog_item_id).one()
	return render_template('delete-item.html', catalog_item_id = catalog_item_id, item = item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
