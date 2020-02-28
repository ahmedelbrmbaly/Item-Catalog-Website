
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify

# Database required libraries
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items, User

# Liraries for login
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

# Load  client_secrets
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "PcStore"

# Make connection with database
engine = create_engine('sqlite:///pcstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON Routes
# Main Json


@app.route('/JSON/')
@app.route('/main/JSON/')
def mainJson():
    categories = session.query(Category).order_by(asc(Category.name))
    return jsonify(Category=[category.serialize for category in categories])


# Show category JSON


@app.route('/<int:cat_id>/JSON/')
@app.route('/<int:cat_id>/items/JSON/')
def showItemsJson(cat_id):
    # Select specific category
    category = session.query(Category).filter_by(id=cat_id).one()
    items = session.query(Items).filter_by(cat_id=cat_id)   # Get all its items
    return jsonify(Items=[item.serialize for item in items])


# Main route


@app.route('/')
@app.route('/main/')
def main():

    # Select all records in category table ordered by name
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('main.html', categories=categories, login_session=login_session)


# Login page


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# New category


@app.route('/new', methods=['GET', 'POST'])
def newCat():
    #  Check if user logged
    if 'username' not in login_session:
        return redirect('/login/')
    # When POST request is sent
    if request.method == 'POST':
        # NOTE: edit user here
        newCat = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCat)
        session.commit()
        flash('New Categoryt %s  added' % newCat.name)
        return redirect(url_for('main'))
    # When GET request is sent
    else:
        return render_template('newCat.html')


# Show category route


@app.route('/<int:cat_id>/')
@app.route('/<int:cat_id>/items/')
def showItems(cat_id):
    # Select specific category
    category = session.query(Category).filter_by(id=cat_id).one()
    items = session.query(Items).filter_by(cat_id=cat_id).order_by(
        asc(Items.name))  # Get all its items
    return render_template('show.html', category=category, items=items, user_id=login_session['user_id'])


# New item in a category route


@app.route('/<int:cat_id>/item/new', methods=['GET', 'POST'])
def newItem(cat_id):
    #  Check if user logged
    if 'username' not in login_session:
        return redirect('/login/')
    category = session.query(Category).filter_by(id=cat_id).one()
    # Check if user is authorized
    if login_session['user_id'] != category.user_id:
        return render_template('notAuth.html')
    # When POST request is sent
    if request.method == 'POST':
        newItem = Items(user_id=login_session['user_id'], name=request.form['name'],
                        description=request.form['description'],
                        price=request.form['price'], cat_id=cat_id)  # edit user
        session.add(newItem)
        session.commit()
        flash('New Item %s Item added' % (newItem.name))
        return redirect(url_for('showItems', cat_id=cat_id, category=category))
    # When GET request is sent
    else:
        return render_template('new.html', cat_id=cat_id)


# Edit item in a category route


@app.route('/<int:cat_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(cat_id, item_id):
    #  Check if user logged
    if 'username' not in login_session:
        return redirect('/login/')
    category = session.query(Category).filter_by(id=cat_id).one()
    # Check if user is authorized
    if login_session['user_id'] != category.user_id:
        return render_template('notAuth.html')
    editedItem = session.query(Items).filter_by(id=item_id).one()
    # When POST request is sent
    if request.method == 'POST':
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', cat_id=cat_id))
    # When GET request is sent
    else:
        return render_template('edit.html', item=editedItem)


# Delete item in a category route


@app.route('/<int:cat_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(cat_id, item_id):
    #  Check if user logged
    if 'username' not in login_session:
        return redirect('/login/')
    category = session.query(Category).filter_by(id=cat_id).one()
    # Check if user is authorized
    if login_session['user_id'] != category.user_id:
        return render_template('notAuth.html')

    deleteItem = session.query(Items).filter_by(id=item_id).one()
    # When POST request is sent
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('showItems', cat_id=cat_id))
    # When GET request is sent
    else:
        return render_template('delete.html', item=deleteItem)

# Gconnect Method


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

    # Save session information
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:  # Create new user
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # Output
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Control Functions
# Create new user


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Get user information


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Get user id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Gdisconnect Methos


@app.route('/gdisconnect')
def gdisconnect():

    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        login_session['user_id'] = 0
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# When the project is called as main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.depug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
