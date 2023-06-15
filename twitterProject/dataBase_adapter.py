import logging
from dataclasses import dataclass

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)


    

@dataclass
class RDSSQlAlchemyConnector:
    """
    RDS Sql Alchemy Connector
    """
    __engine = None
    __connection = None
    __user = 'root'
    __pass = 'mjqJjezWk32MWoNXh3GC'
    __host = 'containers-us-west-83.railway.app'
    __port = 5648
    __db = 'railway'

    def get_declarative_base(self):
        """
        Get Declarative Base for sql Alchemy
        """
        return declarative_base()

    def get_engine(self):
        """
        Get Engine for sql Alchemy
        """

        logger.info("Creating a database connection")
        engine = create_engine(f"mysql+mysqlconnector://{RDSSQlAlchemyConnector.__user}:{RDSSQlAlchemyConnector.__pass}@{RDSSQlAlchemyConnector.__host}:{RDSSQlAlchemyConnector.__port}/{RDSSQlAlchemyConnector.__db}")
        return engine

    def pg_session(self, engine):
        """
        Get Session for sql Alchemy
        """

        rds_session = sessionmaker(engine)()
        return rds_session

    def get_metadata(self):
        """
        Get MetaData for Sql Alchemy
        """

        metadata = MetaData(schema=self.schema)
        metadata.reflect(bind=self.get_engine())
        return metadata
    
def my_sqlA_alchemy_executor():
    engine = RDSSQlAlchemyConnector().get_engine()
    base = RDSSQlAlchemyConnector().get_declarative_base()
    metadata = RDSSQlAlchemyConnector().get_metadata()

