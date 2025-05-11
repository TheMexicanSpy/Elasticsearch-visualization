import pandas as pd
import sys
import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch

def generate_visualizations():
    # Conexión a Elasticsearch
    cloud_id = os.environ.get('ELASTIC_ID')
    password = os.environ.get('ELASTIC_PASSWD')
    es = Elasticsearch(
        cloud_id= os.environ.get('ELASTIC_ID')
        http_auth=("briceno", os.environ.get('ELASTIC_PASSWD'))  
    )
    
    # Consulta para obtener datos
    query = {
        "size": 1000,
        "query": {"match_all": {}}
    }
    
    response = es.search(index="titanic", body=query)
    hits = response['hits']['hits']
    df = pd.DataFrame([hit['_source'] for hit in hits])
    
    # Crear visualizaciones
    plt.figure(figsize=(12, 6))
    
    # Gráfico 1: Supervivencia por clase
    plt.subplot(1, 2, 1)
    df.groupby(['Pclass', 'Survived']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('Supervivencia por Clase')
    
    # Gráfico 2: Distribución de edades
    plt.subplot(1, 2, 2)
    df['Age'].hist(bins=20)
    plt.title('Distribución de Edades')
    
    # Guardar gráficos
    plt.tight_layout()
    plt.savefig('docs/visualizations.png')
    print("Visualizaciones generadas y guardadas")

if __name__ == "__main__":
    generate_visualizations()
