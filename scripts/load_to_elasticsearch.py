import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os

def load_data_to_elasticsearch():
    # Configuración de Elasticsearch
    es = Elasticsearch(
        cloud_id="github_actions:ea01be305c7a4e50871237b16bde813b:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDJiZjliNjZkYWI2YjRlYTY5MWFiMmY1ODMzOGZmNGRjJDQ5NTE2ZTE0NGFhZTQzZjVhZTc5Y2NmMzlkZjg3Y2Iy",  # Reemplazar con tu cloud ID
        http_auth=("briceno", "Luigi123@")  # Reemplazar con tus credenciales
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
