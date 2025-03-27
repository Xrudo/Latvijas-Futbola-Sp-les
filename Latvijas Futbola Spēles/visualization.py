import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from models import Match

def create_location_pie_chart():
    os.makedirs('static/graphs', exist_ok=True)
    plot_path = 'static/graphs/locations_pie.png'
    
    try:
        # Get data from database
        query = Match.select()
        df = pd.DataFrame(list(query.dicts()))
        
        if df.empty:
            return None

        # Create pie chart
        plt.figure(figsize=(10, 8))
        locations = df['vieta'].value_counts()
        threshold = 0.05 * len(df)
        main_locations = locations[locations >= threshold]
        other = locations[locations < threshold].sum()
        
        if other > 0:
            main_locations['Citas vietas'] = other
        
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(main_locations)))
        plt.pie(main_locations, labels=main_locations.index, 
                colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Spēļu vietu sadalījums')
        plt.savefig(plot_path, bbox_inches='tight', dpi=100)
        plt.close()
        
        return plot_path
    
    except Exception as e:
        print(f"Error creating pie chart: {e}")
        return None