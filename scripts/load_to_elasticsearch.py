import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os

def load_data_to_elasticsearch():
    try:
        # Obtener variables de entorno CON verificación
        cloud_id = os.environ.get('ELASTIC_ID')
        password = os.environ.get('ELASTIC_PASSWD')
        
        # Verificación explícita
        if not cloud_id:
            raise ValueError("ELASTIC_ID no está definido")
        if not password:
            raise ValueError("ELASTIC_PASSWD no está definido")
        
        print("Iniciando conexión a Elasticsearch...")
        print(f"Cloud ID (primeros 10 chars): {cloud_id[:10]}...")  # Solo primeros caracteres por seguridad
        
        es = Elasticsearch(
            cloud_id=cloud_id,
            http_auth=("briceno", password),
            timeout=30
        )
        
        if not es.ping():
            raise ConnectionError("No se pudo conectar a Elasticsearch")
            
        print("✅ Conexión exitosa!")
        return es
        
    except Exception as e:
        print(f"🚨 Error crítico: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
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
