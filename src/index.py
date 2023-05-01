from app import app
from config import config

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.run()