from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Provide an API Endpoint (GET Request) to show all items in all categories
@app.route('/JSON')
@app.route('/catalog/JSON')
def ShowAllItemsInAllCategoriesJSON():
	items = session.query(CatalogItem).all()
	return jsonify(Catalog=[i.serialize for i in items])


# Provide an API Endpoint (GET Request) to show all categories
@app.route('/categories/JSON')
def ShowCategoriesJSON():
    category = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in category])


# Provide an API Endpoint (GET Request) to show all items in a given category
@app.route('/category/<int:category_id>/JSON')
@app.route('/category/<int:category_id>/items/JSON')
def ShowItemsInCategoryJSON(category_id):
	category = session.query(Category).filter_by(id = category_id).one()
	items = session.query(CatalogItem).filter_by(category_id=category.id)
	return jsonify(ItemsInCategory=[i.serialize for i in items])


#Show a list of all categories
@app.route('/')
@app.route('/catalog')
def ShowCategories():
    category = session.query(Category).all()
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
	if request.method == 'POST':
		newCategory = Category(name = request.form['name'])
		session.add(newCategory)
		session.commit()
		confirmation = '' + 'Successfully added ' + str(newCategory.name) + '.'
		flash(confirmation)
		return redirect(url_for('ShowCategories'))
	else:
		return render_template('new-category.html')


#Edit a category
@app.route('/category/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
	category = session.query(Category).filter_by(id = category_id).one()
	oldCategory = category.name
	if request.method =='POST':
		if request.form['name']:
			category.name = request.form['name']
		session.add(category)
		session.commit()
		confirmation = '' + 'Successfully changed ' + str(oldCategory) + ' to ' + str(category.name) + '.'
		flash(confirmation)
		return redirect(url_for('ShowCategories'))
	else:
		return render_template('edit-category.html', category = category, category_id = category_id)


#Delete a category
@app.route('/category/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
	category = session.query(Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		session.delete(category)
		session.commit()
		confirmation = '' + 'Successfully deleted ' + str(category.name) + '.'
		flash(confirmation)
		return redirect(url_for('ShowCategories'))
	else:
		return render_template('delete-category.html', category = category, category_id = category_id)


#Add new item
@app.route('/item/new', methods=['GET','POST'])
def addNewItem():
	categories = session.query(Category).all()
	if request.method == 'POST':
		category_id = request.form['category_id']
		newItem = CatalogItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], category_id = category_id)
		session.add(newItem)
		session.commit()
		confirmation = '' + str(newItem.name)
		confirmation += ' has been added as a new item in '
		category = session.query(Category).filter_by(id = newItem.category_id).one()
		confirmation += str(category.name) + '.'
		flash(confirmation)
		return redirect(url_for('ShowItemsInCategory', category_id = category_id))
	else:
		return render_template('new-item.html', categories = categories)


#Edit an item
@app.route('/item/<int:catalog_item_id>/edit', methods=['GET','POST'])
def editItem(catalog_item_id):
	item = session.query(CatalogItem).filter_by(id = catalog_item_id).one()
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(id = item.category_id).one()
	if request.method == 'POST':
		category_id = request.form['category_id']
		item.name = request.form['name']
		item.description = request.form['description']
		item.price = request.form['price']
		item.category_id = request.form['category_id']
		session.add(item)
		session.commit()
		confirmation = '' + 'Successfuly edited ' + str(item.name)
		confirmation += ' in ' + str(category.name) + '.'
		flash(confirmation)
		return redirect(url_for('ShowItemsInCategory', category_id = category_id))
	else:
		return render_template('edit-item.html', item = item, category = category, catalog_item_id = catalog_item_id, categories = categories)


#Delete an item
@app.route('/item/<int:catalog_item_id>/delete', methods=['GET','POST'])
def deleteItem(catalog_item_id):
	item = session.query(CatalogItem).filter_by(id = catalog_item_id).one()
	category_id = item.category_id
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		confirmation = '' + str(item.name)
		confirmation += ' has been deleted from '
		category = session.query(Category).filter_by(id = item.category_id).one()
		confirmation += str(category.name) + '.'
		flash(confirmation)
		return redirect(url_for('ShowItemsInCategory', category_id = category_id))
	else:
		return render_template('delete-item.html', catalog_item_id = catalog_item_id, item = item)


if __name__ == '__main__':
	app.secret_key = '26thDS534wmNZ097645Q'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)
