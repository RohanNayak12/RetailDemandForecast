from flask import Flask, render_template, request
import sys
from pathlib import Path
from src.retailDemand.pipeline.stage05_model_pred import ModelPredictorPipeline

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    try:
        store_id = int(request.form['store_id'])
        date = request.form['date']
        
        pipeline = ModelPredictorPipeline(store_id, date)
        result = pipeline.main()
        
        return render_template('index.html', prediction=result)
        
    except ValueError:
        return render_template('index.html', error_message=f"Store ID {request.form.get('store_id')} not found")
    except Exception as e:
        return render_template('index.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
