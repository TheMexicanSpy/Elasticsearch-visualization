import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os

def load_data_to_elasticsearch():
    try:
         # Obtener credenciales de variables de entorno
        cloud_id = os.getenv('ELASTIC_ID')
        password = os.getenv('ELASTIC_PASSWD')
        
        print(f"Intentando conectar con Cloud ID: {cloud_id[:30]}...")  # Log parcial para debug
        
        es = Elasticsearch(
            cloud_id=cloud_id,
            http_auth=("briceno", password)
        )
        
        # Verificar conexión
        if es.ping():
            print("✅ Conexión exitosa a Elasticsearch!")
        else:
            print("❌ No se pudo conectar a Elasticsearch")
            
    except Exception as e:
        print(f"🚨 Error de conexión: {str(e)}")
        raise

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
