from flask import request, render_template
from flask import current_app as app

from .inference import inference

@app.route('/', methods = ['GET'])
def load_home_page():
    
    # Return home page
    return render_template('index.html')


@app.route('/', methods = ['POST'])
def run_prediction():
            
    # Get category of prediction
    category = inference()

    # Render the result template
    return render_template('result.html', category = category)
