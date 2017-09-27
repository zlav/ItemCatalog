#! /usr/bin/ python
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session
import random, string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

#Connect to Database and create database session
engine = create_engine('sqlite:///shoppingcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#JSON APIs to view Catalog Information
@app.route('/catalog/<int:category_id>/items/JSON')
def categoryListJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    catItem = session.query(Item).filter_by(id = item_id).one()
    return jsonify(catItem = catItem.serialize)

@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories = [r.serialize for r in categories])


#Show the catalog
@app.route('/')
@app.route('/catalogpublic/')
@app.route('/catalog/')
def showCatalog():
  catalog = session.query(Category).order_by(asc(Category.name))
  items = session.query(Item).order_by(Item.id.desc()).limit(10) 
  if 'username' not in login_session:
      print "help"
      return render_template('catalogpublic.html', catalog = catalog, items = items)
  print(login_session['username'])
  return render_template('catalog.html', catalog = catalog, items = items)

#Create a new category
@app.route('/catalog/new/', methods=['GET','POST'])
def newCategory():
  if 'username' not in login_session:
      print "help"
      return redirect('/login')
  if request.method == 'POST':
      newCategory = Category(name = request.form['name'], user_id=login_session['user_id'])
      session.add(newCategory)
      flash('New Category %s Successfully Created' % newCategory.name)
      session.commit()
      return redirect(url_for('showCatalog'))
  else:
      return render_template('newCategory.html')

#Edit a restaurant
@app.route('/category/<int:category_id>/edit/', methods = ['GET', 'POST'])
def editCategory(category_id):
  editedCategory = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedCategory.name = request.form['name']
        flash('Category Successfully Edited %s' % editedCategory.name)
        return redirect(url_for('showItems', category_id = category_id))
  else:
    return render_template('editCategory.html', category = editedCategory)


#Delete a restaurant
@app.route('/category/<int:category_id>/delete/', methods = ['GET','POST'])
def deleteCategory(category_id):
  categoryToDelete = session.query(Category).filter_by(id = category_id).one()
  itemsInCategory = session.query(Item).filter_by(category_id = categoryToDelete.id)
  if request.method == 'POST':
    for item in itemsInCategory:
        session.delete(item)
    session.delete(categoryToDelete)
    flash('%s and Its Items Successfully Deleted ' % categoryToDelete.name)
    session.commit()
    return redirect(url_for('showCatalog'))
  else:
    return render_template('deleteCategory.html',category = categoryToDelete)

#Show a categories Items
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/publicitems/')
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    creator = getUserInfo(category.user_id).first()

    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicitems.html', creator = creator, items = items, category = category)
    else:
        print('items')
        return render_template('items.html', creator = creator, items = items, category = category)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/iteminfo')
def showInfo(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).first()
    return render_template('iteminfo.html', item = item, category_id = category_id)

#Create a new item
@app.route('/catalog/<int:category_id>/items/new/',methods=['GET','POST'])
def newItem(category_id):
  category = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
      newItem = Item(name = request.form['name'], description = request.form['description'], price = request.form['price'], category_id = category_id)
      session.add(newItem)
      session.commit()
      flash('New Item, %s Successfully Created' % (newItem.name))
      return redirect(url_for('showItems', category_id = category_id))
  else:
      return render_template('newitem.html', category_id = category_id)

#Edit an item
@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):

    editedItem = session.query(Item).filter_by(id = item_id).one()
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit() 
        flash('Item Successfully Edited')
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('edititem.html', category_id = category_id, item_id = item_id, item = editedItem)


#Delete an item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods = ['GET','POST'])
def deleteItem(category_id, item_id):
    category = session.query(Category).filter_by(id = category_id).first()
    itemToDelete = session.query(Item).filter_by(id = item_id).one() 
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('deleteItem.html', category_id = category_id, item = itemToDelete)

@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

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
        response = make_response(json.dumps('Current user is already connected.'),
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
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
 
    login_session['user_id'] = user_id 

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done! %s" %data['name'])
    return output

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id)
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect', methods=['POST'])
def fbconnect():

    #Check if the states match, if not exit
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("User AToken: "+ access_token)
    #Exchange client Token for long lived server token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    
    #Retrieve User Information and strip the expire tag
    token = json.loads(result)["access_token"].split("&")[0]
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email,picture' % token
    h = httplib2.Http()
    result = h.request(url,'GET')[1]
    login_session['access_token'] = token

    #Assing data to the login_session variable
    data = json.loads(result)
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['picture'] = data["picture"]["data"]["url"]
    login_session['provider'] = 'facebook'
    #Check if user is already registered
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
 
    login_session['user_id'] = user_id 

    #Output to the main page
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done! %s" %data['name'])
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id'] 
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h= httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

@app.route('/disconnect')
def disconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']

        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        flash("You have successfully logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in to begin with.")
        return redirect(url_for('showCatalog'))

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
  
