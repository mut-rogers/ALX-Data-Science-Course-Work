""" 
data_ingestion.py 

This module provides utility functions for performing data extraction for different sources, in this case, 
data sources include SQL DataBase and Web-based CSV files. 

This module includes functions for interacting with the database (Creating DB Engine, Connecting to the DB Engine, and Querying DB) 

The aim of the module is to provide simple and reusable blocks of code for common operations of connecting and/or retrieving data from the database and 
Web-based CSV from our company sources.
"""

from sqlalchemy import create_engine, text
import logging
import pandas as pd
# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('data_ingestion')
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

### START FUNCTION

def create_db_engine(db_path):
    """ 
    This is a utility function that creates a connection to our database 

    Args:
        db_path (str): This is a string containing path to our SQLite database file. 

    Returns:
        Database_Connection (instance): A database connection object
    """

    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine # Return the engine object if it all works well
    except ImportError: #If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    except Exception as e:# If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e
    
def query_data(engine, sql_query):
    """ 
    A utility function to query data from the database 

    Args:
        engine (instance): A DataBase engine instance with connection to the database
        sql_query (str): SQL Statement to be parsed to the DataBase for data extraction 

    Returns:
        df (DataFrame): A dataframe with the extracted data
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e
    
def read_from_web_CSV(URL):
    """ 
    A utility function to extract data from a Web-Based CSV file 

    Args:
        URL (str): A URL pointing to the CSV Web resource 

    Returns:
        df (DataFrame): A dataframe with the extracted data
    """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e
    
### END FUNCTION