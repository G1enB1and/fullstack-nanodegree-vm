from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem, User
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import urllib2

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Project"


# Connect to database
engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False},
                       poolclass=SingletonThreadPool)
Base.metadata.bind = engine

# Create Database Session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    categories = session.query(Category).all()
    return render_template('login.html', STATE=state, categories=categories)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += 'Welcome, '
    output += login_session['username']
    output += '!</br>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 150px; height: 150px; '
    output += 'border-radius: 150px; -webkit-border-radius: 150px; '
    output += '-moz-border-radius: 150px;"> '
    output += '</br> email: ' + login_session['email'] + '</br>'

    # see if user exists, if it doesn't- make a new one.
    user_id = getUserID(login_session['email'])
    if not user_id:
        output += 'First time logging in with this email. </br>'
        output += 'Creating new user in database </br>'
        user_id = createUser(login_session)
        output += '...Done! </br></br>'
    else:
        output += 'Welcome back! </br>'
        output += 'Your email address has been found in our database. </br>'
        output += '</br>'
    login_session['user_id'] = user_id

    downloadUserPicture(login_session['picture'])

    flash("You are now logged in as %s." % login_session['username'])
    return output


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Download a copy of the user picture for use when that user is not logged in.
# Such as to show other users a picture of the user who created an item.
def downloadUserPicture(url):
    file_name = 'static/user_pic_' + str(login_session['user_id']) + '.jpg'
    try:
        request = urllib2.Request(url)
        img = urllib2.urlopen(request).read()
        with open(file_name, 'w') as f:
            f.write(img)
        print('Done! - no exception errors.')
    except:
        print('Exception error while downloading user picture')


# DISCONNECT - Revoke a user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']

    # Execute HTTP GET request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flashMessage = '' + 'Successfully logged out.'
        flash(flashMessage)
        response = redirect(url_for('ShowAllCategoriesItems'))
        return response
    else:
        flashMessage = '' + 'Failed to revoke token for given user.'
        flash(flashMessage)
        response = redirect(url_for('ShowAllCategoriesItems'))
        return response


# Provide an API Endpoint (GET Request)
# to show all items in all categories.
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


# Provide an API Endpoint (GET Request)
# to show all items in a given category.
@app.route('/category/<int:category_id>/JSON')
@app.route('/category/<int:category_id>/items/JSON')
def ShowItemsInCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category.id)
    return jsonify(ItemsInCategory=[i.serialize for i in items])


# Provide an API Endpoint (GET Request)
# to show one item by it's catalog_item_id.
@app.route('/item/<int:catalog_item_id>/JSON')
def ShowItemJSON(catalog_item_id):
    item = session.query(CatalogItem).filter_by(id=catalog_item_id).one()
    return jsonify(Item=[item.serialize])


# Get Category Name from Category ID
def GetCategoryNameFromID(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return category.name


# Show a list of all categories and items
@app.route('/')
@app.route('/catalog')
def ShowAllCategoriesItems():
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    items = session.query(CatalogItem).all()
    return render_template('show-all-categories-items.html',
                           categories=categories, items=items,
                           GetCategoryNameFromID=GetCategoryNameFromID,
                           loggedIn=loggedIn,
                           login_session=login_session)


# Show a list of categories
@app.route('/')
@app.route('/catalog')
def ShowCategories():
    category = session.query(Category).all()
    return render_template('show-all-categories-items.html', category=category)


# Show Items In a given category by passing in the category_id (number)
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items')
def ShowItemsInCategory(category_id):
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category.id)
    return render_template('show-items-in-category.html', category=category,
                           items=items, category_id=category_id,
                           categories=categories, loggedIn=loggedIn,
                           login_session=login_session)


# Show a given item by passing in the catalog_item_id
@app.route('/item/<int:catalog_item_id>')
def ShowItem(catalog_item_id):
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    item = session.query(CatalogItem).filter_by(id=catalog_item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    user = session.query(User).filter_by(id=item.user_id).one()
    user_pic = 'user_pic_' + str(user.id) + '.jpg'
    return render_template('show-item.html', item=item, category=category,
                           catalog_item_id=catalog_item_id,
                           categories=categories, loggedIn=loggedIn,
                           login_session=login_session, user=user,
                           user_pic=user_pic)


# Add new category
@app.route('/category/new', methods=['GET', 'POST'])
def addNewCategory():
    # Redirect user to login if they are not logged in
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        confirmation = '' + 'Successfully added ' + str(newCategory.name)
        confirmation += ' to categories.'
        flash(confirmation)
        return redirect(url_for('ShowAllCategoriesItems'))
    else:
        loggedIn = "True"
        return render_template('new-category.html', categories=categories,
                               loggedIn=loggedIn, login_session=login_session)


# Edit a category
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    # Redirect user to login if they are not logged in
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session['user_id']:
        output = '' + 'You are not authorized to edit this category. '
        output += 'Please create your own category in order to edit.'
        flash(output)
        return redirect(url_for('ShowItemsInCategory',
                                category_id=category.id))
    if request.method == 'POST':
        if request.form['name']:
            oldCategory = category.name
            category.name = request.form['name']
        session.add(category)
        session.commit()
        confirmation = '' + 'Successfully changed ' + str(oldCategory) + ' to '
        confirmation += str(category.name) + '.'
        flash(confirmation)
        return redirect(url_for('ShowItemsInCategory',
                                category_id=category.id))
    else:
        loggedIn = "True"
        categories = session.query(Category).all()
        return render_template('edit-category.html', category=category,
                               category_id=category_id, categories=categories,
                               loggedIn=loggedIn, login_session=login_session)


# Delete a category
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    # Redirect user to login if they are not logged in
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session['user_id']:
        output = '' + 'You are not authorized to delete this category. '
        output += 'Please create your own category in order to delete.'
        flash(output)
        return redirect(url_for('ShowItemsInCategory',
                                category_id=category.id))
    if request.method == 'POST':
        items = session.query(CatalogItem).filter_by(category_id=category.id)
        for i in items:
            item = session.query(CatalogItem).filter_by(id=i.id).one()
            session.delete(item)
        session.delete(category)
        session.commit()
        confirmation = '' + 'Successfully deleted ' + str(category.name)
        confirmation += ' from categories. We will remember you '
        confirmation += str(category.name)[:3] + '...something...'
        flash(confirmation)
        return redirect(url_for('ShowAllCategoriesItems'))
    else:
        loggedIn = "True"
        categories = session.query(Category).all()
        return render_template('delete-category.html', category=category,
                               category_id=category_id, categories=categories,
                               loggedIn=loggedIn, login_session=login_session)


# Add new item
@app.route('/item/new', methods=['GET', 'POST'])
def addNewItem():
    # Redirect user to login if they are not logged in
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category_id = request.form['category_id']
        newItem = CatalogItem(name=request.form['name'],
                              description=request.form['description'],
                              price=request.form['price'],
                              category_id=category_id,
                              user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        confirmation = '' + str(newItem.name)
        confirmation += ' has been added to '
        category = (session.query(Category).
                    filter_by(id=newItem.category_id).one())
        confirmation += str(category.name)
        confirmation += '. I have a good feeling about this one!'
        flash(confirmation)
        return redirect(url_for('ShowItem', catalog_item_id=newItem.id))
    else:
        loggedIn = "True"
        categories = session.query(Category).all()
        return render_template('new-item.html', categories=categories,
                               loggedIn=loggedIn, login_session=login_session)


# Edit an item
@app.route('/item/<int:catalog_item_id>/edit', methods=['GET', 'POST'])
def editItem(catalog_item_id):
    # Redirect user to login if they are not logged in
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CatalogItem).filter_by(id=catalog_item_id).one()
    if item.user_id != login_session['user_id']:
        output = '' + 'You are not authorized to edit this item. '
        output += 'Please create your own item in order to edit.'
        flash(output)
        return redirect(url_for('ShowItem', catalog_item_id=item.id))
    category = session.query(Category).filter_by(id=item.category_id).one()
    if request.method == 'POST':
        category_id = request.form['category_id']
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.category_id = request.form['category_id']
        session.add(item)
        session.commit()
        confirmation = '' + 'Behold! The new and improved ' + str(item.name)
        confirmation += ' in ' + str(category.name) + ' has been edited!'
        flash(confirmation)
        return redirect(url_for('ShowItem', catalog_item_id=item.id))
    else:
        loggedIn = "True"
        categories = session.query(Category).all()
        return render_template('edit-item.html', item=item,
                               category=category,
                               catalog_item_id=catalog_item_id,
                               categories=categories, loggedIn=loggedIn,
                               login_session=login_session)


# Delete an item
@app.route('/item/<int:catalog_item_id>/delete', methods=['GET', 'POST'])
def deleteItem(catalog_item_id):
    # Redirect user to login if they are not logged in
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CatalogItem).filter_by(id=catalog_item_id).one()
    if item.user_id != login_session['user_id']:
        output = '' + 'You are not authorized to delete this item. '
        output += 'Please create your own item in order to delete.'
        flash(output)
        return redirect(url_for('ShowItem', catalog_item_id=item.id))
    if request.method == 'POST':
        category_id = item.category_id
        session.delete(item)
        session.commit()
        confirmation = '' + 'Poof! ' + str(item.name)
        confirmation += ' has been deleted from '
        category = session.query(Category).filter_by(id=item.category_id).one()
        confirmation += str(category.name) + '. I never liked that one anyway.'
        flash(confirmation)
        return redirect(url_for('ShowItemsInCategory',
                                category_id=category_id))
    else:
        loggedIn = "True"
        categories = session.query(Category).all()
        return render_template('delete-item.html',
                               catalog_item_id=catalog_item_id,
                               item=item, loggedIn=loggedIn,
                               categories=categories,
                               login_session=login_session)


# Show a list of all categories and items after canceling new category
@app.route('/cancel-new-category')
@app.route('/catalog/cancel-new-category')
def ShowCategoriesAfterCancelNewCategory():
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    items = session.query(CatalogItem).all()
    flashMessage = '' + ' No new category was made. Probably would have '
    flashMessage += 'been a failure anyway.'
    flash(flashMessage)
    return render_template('show-all-categories-items.html',
                           categories=categories, items=items,
                           GetCategoryNameFromID=GetCategoryNameFromID,
                           loggedIn=loggedIn, login_session=login_session)


# Show Items In a given category by passing in the category_id (number)
# after canceling an edit.
@app.route('/category/<int:category_id>/cancel-edit/')
@app.route('/category/<int:category_id>/items/cancel-edit/')
def ShowCategoryAfterCancelEdit(category_id):
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category.id)
    flashMessage = '' + 'Cancel? Fine. Don\'t worry, your precious '
    flashMessage += category.name + ' wasn\'t edited.'
    flash(flashMessage)
    return render_template('show-items-in-category.html', category=category,
                           items=items, category_id=category_id,
                           categories=categories, loggedIn=loggedIn,
                           login_session=login_session)


# Show Items In a given category by passing in the category_id (number)
# after canceling a delete.
@app.route('/category/<int:category_id>/cancel-delete/')
@app.route('/category/<int:category_id>/items/cancel-delete/')
def ShowCategoryAfterCancelDelete(category_id):
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category.id)
    flashMessage = '' + 'You win this time ' + category.name + '. '
    flash(flashMessage)
    return render_template('show-items-in-category.html', category=category,
                           items=items, category_id=category_id,
                           categories=categories, loggedIn=loggedIn,
                           login_session=login_session)


# Show a list of all categories and items after canceling new item
@app.route('/cancel-new-item')
@app.route('/catalog/cancel-new-item')
def ShowCategoriesAfterCancelNewItem():
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    items = session.query(CatalogItem).all()
    flashMessage = '' + ' No new item was made. Why don\'t you just cancel my'
    flashMessage += ' hopes and dreams while you\'re at it?'
    flash(flashMessage)
    return render_template('show-all-categories-items.html',
                           categories=categories, items=items,
                           GetCategoryNameFromID=GetCategoryNameFromID,
                           loggedIn=loggedIn,
                           login_session=login_session)


# Show a given item by passing in the catalog_item_id after canceling an edit
@app.route('/item/<int:catalog_item_id>/cancel-edit/')
def ShowItemAfterCancelEdit(catalog_item_id):
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    item = session.query(CatalogItem).filter_by(id=catalog_item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    flashMessage = '' + 'Phew! That was close! You almost altered reality '
    flashMessage += 'itself. Not to fear, ' + item.name + ' remains unchanged.'
    flash(flashMessage)
    return redirect(url_for('ShowItem', catalog_item_id=item.id))


# Show a given item by passing in the catalog_item_id after canceling a delete
@app.route('/item/<int:catalog_item_id>/cancel-delete/')
def ShowItemAfterCancelDelete(catalog_item_id):
    # Check if user is logged in
    if 'username' not in login_session:
        loggedIn = "False"
    else:
        loggedIn = "True"
    categories = session.query(Category).all()
    item = session.query(CatalogItem).filter_by(id=catalog_item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    flashMessage = '' + 'I was hoping I could test out my data blaster on '
    flashMessage += 'that one... ' + item.name + ' lives another day.'
    flash(flashMessage)
    return redirect(url_for('ShowItem', catalog_item_id=item.id))


if __name__ == '__main__':
    app.secret_key = '26thDS534wmNZ097645Q'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
