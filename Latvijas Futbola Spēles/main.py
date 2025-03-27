from flask import Flask, render_template, request, send_file
from models import Match
from visualization import create_location_pie_chart
from io import BytesIO
import pandas as pd
from peewee import fn
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)

@app.route('/')
def index():
    try:
        tournament_filter = request.args.get('turnirs', '')
        
        # Get filtered matches
        query = Match.select().order_by(Match.datums.desc())
        if tournament_filter:
            query = query.where(Match.turnirs.contains(tournament_filter))
        
        matches = list(query.dicts())
        
        # Calculate stats
        stats = {
            'total': Match.select().count(),
            'wins': Match.select().where(Match.iznākums == 'uzvara').count(),
            'draws': Match.select().where(Match.iznākums == 'neizšķirts').count(),
            'losses': Match.select().where(Match.iznākums == 'zaudējums').count()
        }
        
        return render_template('index.html',
                            matches=matches,
                            stats=stats,
                            current_filter=tournament_filter)
    
    except Exception as e:
        logging.error(f"Index error: {str(e)}")
        return render_template('error.html', error_message="Datu ielādes kļūda"), 500

@app.route('/graphs')
def show_graph():
    try:
        chart_path = create_location_pie_chart()
        if not chart_path:
            return render_template('error.html', 
                                error_message="Nevarēja ģenerēt grafiku"), 500
            
        return render_template('graphs.html', graph_image=chart_path)
    
    except Exception as e:
        logging.error(f"Graph error: {str(e)}")
        return render_template('error.html', 
                            error_message="Grafika ģenerēšanas kļūda"), 500

@app.route('/download')
def download_data():
    try:
        query = Match.select().dicts()
        df = pd.DataFrame(list(query))
        
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="futbola_dati.xlsx"
        )
    
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return render_template('error.html',
                            error_message="Lejupielādes kļūda"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)