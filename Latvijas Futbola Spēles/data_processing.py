# data_processing.py
import pandas as pd
from models import Match, initialize_db
from datetime import datetime

def parse_result(result):
    if pd.isna(result) or result.strip() == '':
        return 0, 0, None
    try:
        home, away = map(int, result.split(':'))
        if home > away:
            outcome = 'uzvara'
        elif home == away:
            outcome = 'neizšķirts'
        else:
            outcome = 'zaudējums'
        return home, away, outcome
    except:
        return 0, 0, None

def process_data():
    db = initialize_db()
    
    # Load and clean data
    df = pd.read_csv('data.csv', encoding='utf-8')
    df.columns = [col.strip() for col in df.columns]
    
    # Clear existing data
    Match.delete().execute()
    
    # Insert new data
    for _, row in df.iterrows():
        goli_par, goli_pret, iznākums = parse_result(row['Rezultāts'])
        
        Match.create(
            datums=row['Datums'],
            turnirs=row['Turnīrs'],
            vieta=row['Vieta'],
            pretinieks=row['Pretinieks'],
            rezultats=row['Rezultāts'],
            vartu_guveji=row['Latvijas vārtu guvēji'] if 'Latvijas vārtu guvēji' in row else None,
            goli_par=goli_par,
            goli_pret=goli_pret,
            iznākums=iznākums
        )

if __name__ == '__main__':
    process_data()