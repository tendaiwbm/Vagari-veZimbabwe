import psycopg2 as pg
from dotenv import load_dotenv,find_dotenv
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR,".env"))

def request_handler(decoratee):
    def wrapper(query):
        returnNone = {"SELECT 0": True}
        connection = pg.connect(user=os.getenv('PG_USER'),password=os.getenv('PG_PASSWORD'),host=os.getenv('PG_HOST'),port=os.getenv('PG_PORT'),database=os.getenv('PG_DATABASE'))
        with connection.cursor() as cursor:
            cursor.execute(query)
            try:
                if returnNone[cursor.statusmessage]:
                    raise ValueError("Ambiguous query")
            except:
                 return cursor.fetchall()
    return wrapper

