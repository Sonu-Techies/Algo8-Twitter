import sqlalchemy

class Database:
    __engine = None
    __connection = None
    __user = 'root'
    __pass = 'mjqJjezWk32MWoNXh3GC'
    __host = 'containers-us-west-83.railway.app'
    __port = 5648
    __db = 'railway'

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def connect(self):
        Database.__engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{Database.__user}:{Database.__pass}@{Database.__host}:{Database.__port}/{Database.__db}")
        Database.__connection = Database.__engine.connect()

    @property
    def connection(self):
        if not Database.__connection:
            raise RuntimeError('No database connection available.')
        return Database.__connection

    @property
    def engine(self):
        if not Database.__engine:
            raise RuntimeError('No database engine initialized.')
        return Database.__engine
