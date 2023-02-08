import os
import settings
import csv
from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)
from middleware import model_predict

router = Blueprint('app_router', __name__, template_folder = 'templates', static_folder='static')

@router.route('/', methods = ['GET', 'POST']) 
def index():
    '''
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can upload the form.
    When it receives an dict from the UI, it also calls our ML model to
    get and display the predictions in the result page.
    '''
    if request.method == 'GET':
        return render_template('form.html')

    if request.method == 'POST':
        form = request.form.to_dict()

        path = os.path.join(settings.UPLOAD_FOLDER, 'forms.csv') 
        if os.path.exists(path): 
            with open(path,'a') as f:
                w = csv.DictWriter(f, form.keys())
                w.writerow(form)
        else:
            with open(path,'a') as f:
                w = csv.DictWriter(f, form.keys())
                w.writeheader()
                w.writerow(form)
        
        # Calls this function to predict from middleware
        pred, prob = model_predict(form)

        context = {
            'prediction': pred,
            'probability': prob
        }

       # Define the treshold as 0.27
        if float(context['probability']) >= 0.27:
            context['prediction'] = 1
        else:
            context['prediction'] = 0

        return render_template('result.html', context = context)

@router.route('/predict', methods = ['POST'])
def predict():

    rpse = {
        'prediction': None,
        'probability': None
     }

    # If user sends an invalid request return `rpse` dict with 
    # default values HTTP 400 Bad Request code
    if request.method != 'POST':
        return jsonify(rpse), 400
    
    form_dict = request.form.to_dict()
    
    pred, prob = model_predict(form_dict)

    rpse = {
        'prediction': pred,
        'probability': prob
    }

    return jsonify(rpse)  