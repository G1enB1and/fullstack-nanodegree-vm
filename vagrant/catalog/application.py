from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def HelloWorld():
    category = session.query(Category).filter_by(id = 3).one()
    items = session.query(CatalogItem).filter_by(category_id=category.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
