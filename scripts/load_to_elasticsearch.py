# scripts/load_to_elasticsearch.py (ejemplo básico)
from elasticsearch import Elasticsearch
import pandas as pd
import os

def load_data():
    cloud_id = os.environ.get('ELASTIC_ID')
    password = os.environ.get('ELASTIC_PASSWD')
    
    es = Elasticsearch(
        cloud_id=cloud_id,
        basic_auth=("briceno", password)
    )

    # Cargar datos del Titanic (ejemplo con un CSV)
    df = pd.read_csv("data/Titanic-Dataset.csv")  # Asegúrate de que este archivo existe
    
    # Convertir a formato JSON e indexar en Elasticsearch
    records = df.to_dict(orient='records')
    for i, record in enumerate(records):
        es.index(index="titanic", id=i+1, document=record)

    print(f"Datos cargados: {len(records)} registros en índice 'titanic'")

if __name__ == "__main__":
    load_data()
