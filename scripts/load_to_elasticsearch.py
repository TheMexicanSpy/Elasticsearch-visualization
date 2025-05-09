import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os

def load_data_to_elasticsearch():
    # Configuración de Elasticsearch
    es = Elasticsearch(
        cloud_id="tu-cloud-id",  # Reemplazar con tu cloud ID
        http_auth=("elastic", "tu-password")  # Reemplazar con tus credenciales
    )
    
    # Leer el dataset
    df = pd.read_csv('data/sample_dataset.csv')
    
    # Preparar los datos para bulk insert
    actions = [
        {
            "_index": "titanic",
            "_source": row.to_dict()
        }
        for _, row in df.iterrows()
    ]
    
    # Insertar datos en Elasticsearch
    success, _ = bulk(es, actions)
    print(f"Successfully loaded {success} documents to Elasticsearch")

if __name__ == "__main__":
    load_data_to_elasticsearch()
