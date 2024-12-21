from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todo.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})  # connect_args is for detecting more database errors but in default we can get a error only
