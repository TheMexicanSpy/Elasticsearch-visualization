import pandas as pd
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch

def generate_visualizations():
    cloud_id = os.environ.get('ELASTIC_ID')
    password = os.environ.get('ELASTIC_PASSWD')
    
    es = Elasticsearch(
        cloud_id=cloud_id,
        basic_auth=("briceno", password)
    )
    
    try:
        # Obtener datos
        response = es.search(index="titanic", body={"size": 1000, "query": {"match_all": {}}})
        hits = response['hits']['hits']
        
        if not hits:
            print("No data found in 'titanic' index")
            return
            
        df = pd.DataFrame([hit['_source'] for hit in hits])
        
        # Limpieza de tipos de datos
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')  # Convierte a float
        df['Fare'] = pd.to_numeric(df['Fare'], errors='coerce')
        df['Pclass'] = pd.to_numeric(df['Pclass'], errors='coerce')
        df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
        
        # Eliminar filas con valores faltantes críticos
        df = df.dropna(subset=['Age', 'Pclass', 'Survived'])
        
        print("Datos limpios:")
        print(df.dtypes)  # Verifica los tipos de datos
        
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
        os.makedirs('docs', exist_ok=True)
        plt.savefig('docs/visualizations.png')
        print("✅ Visualizaciones generadas y guardadas")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise  # Esto hará que el workflow falle claramente

if __name__ == "__main__":
    generate_visualizations()
