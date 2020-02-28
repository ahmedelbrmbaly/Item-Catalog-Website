# Items Catalog
This is a website to  provide a list of items within a variety of categories, as well as provide a user registration and authentication system.
It was created by using two main technologies `flask` and `sqlalchemy`
To make the site with a meaning I created it like a **_Pc Store_**.

## Prerequisites
* Python version 2.7
* Sqlalchemy
* SQLite3 (preferred)

## How it works
1. Open terminal
2. Go to the containing directory
3. Make sure That you have ` pcstore.db`  if not write these two commands
  * `python database_setup.py` to make the database
  * `pyhthon items.py` to fill the database with items (preferred)
4. Type this commnad `python project.py`  
5. Go to this link `localhost:5000` in your preferred internet browser

## Main Features
1. `JSON` endpoints
  * `http://localhost:5000/JSON/` shows all categories information
  * `http://localhost:5000/<int:category_id>/JSON/` shows all category information

2. Authentication & Authorization
  * Site uses `Google sign in `
  * Login link is shown in main page when there is no login
  * Log out link is shown in main page when user is logged
  * Visitors can only see categories information. They can't add new category or item neither editing or deleting any items
  * Users can add new category and edit and delete only the items they added
  * If a visitors tries to reach any page - by using its URL- that isn't for public, he will be redirected automatically to login page
  * If a user tries to get access to data that don;t belong to him, he will be redirected automatically to notAuth page
3. All `CRUD` Functions are used
  * Anyone Can `Read` all site information
  * Any user can `Create` a new category
  * Category's user can `Create` new item, `Update` existing item or `Delete` it.
4. Data is saved in SQL database
5. Code is written compliant with the Python `PEP 8` style guide

## Notes
* If there is a problem with login and log out, Delete your browser cache and it will work again.


## Upcoming Features
1. `Css` styling will be implemented
2. Better UI and UX will be implemented
2. When user log out he will be redirected to main page
(I didn't do that to submit the project as fast as possible)  


## License
**_Items Catalog_** is free and open source .
