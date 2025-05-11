import pandas as pd
import sys
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch

def generate_visualizations():
    cloud_id = os.environ.get('ELASTIC_ID')
    password = os.environ.get('ELASTIC_PASSWD')
    
    es = Elasticsearch(
        cloud_id=cloud_id,
        basic_auth=("briceno", password)  # Fixed: using basic_auth instead of http_auth
    )
    
    try:
        # Get data
        response = es.search(index="titanic", body={"size": 1000, "query": {"match_all": {}}})
        hits = response['hits']['hits']
        
        if not hits:
            print("No data found in 'titanic' index")
            return
            
        df = pd.DataFrame([hit['_source'] for hit in hits])
        
        # Print available columns for debugging
        print("Available columns:", df.columns.tolist())
        
        # Create visualizations
        plt.figure(figsize=(12, 6))
        
        # Plot 1: Survival by class - check for column name variations
        plt.subplot(1, 2, 1)
        class_col = 'Pclass' if 'Pclass' in df.columns else 'pclass'  # handle case sensitivity
        survival_col = 'Survived' if 'Survived' in df.columns else 'survived'
        
        if class_col in df.columns and survival_col in df.columns:
            df.groupby([class_col, survival_col]).size().unstack().plot(
                kind='bar', stacked=True)
            plt.title('Survival by Class')
        else:
            print(f"Missing required columns: {class_col} or {survival_col}")
        
        # Plot 2: Age distribution
        plt.subplot(1, 2, 2)
        age_col = 'Age' if 'Age' in df.columns else 'age'
        if age_col in df.columns:
            df[age_col].hist(bins=20)
            plt.title('Age Distribution')
        else:
            print(f"Missing age column: {age_col}")
        
        # Save plots
        plt.tight_layout()
        os.makedirs('docs', exist_ok=True)
        plt.savefig('docs/visualizations.png')
        print("Visualizations generated and saved")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    generate_visualizations()
