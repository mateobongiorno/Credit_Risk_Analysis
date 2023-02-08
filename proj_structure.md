### Credit Risk analysis unsing Deep Learning by Mateo Bongiorno. 

Below is the full project structure:

```
├── api
│   ├── Dockerfile
│   ├── app.py
│   ├── middleware.py
│   ├── views.py
│   ├── settings.py
│   ├── utils.py
│   ├── static    
│   │   ├── assets
│   │   │   ├── css
│   │   │   └── webfonts
│   │   └── images
│   └── templates
│       ├── results.html
│       └── form.html
├── model
│   ├── data       
│   ├── pickles
│   ├── Dockerfile
│   ├── prepocessing.py
│   ├── train.py
│   ├── requirements.txt
│   ├── ml_service.py
│   └── settings.py
├── notebooks
│   ├── EDA.ipynb      
│   └── Model_Evaluation.ipynb
├── uploads
│   └── forms.csv
├── docker-compose.yml
├── proj_structure.md
└── README.md
```

Let's take a quick overview on each module:

- api: It has all the needed code to implement the communication interface between the users and the service. It uses Flask and Redis to queue tasks to be processed by the machine learning model.
    - `api/app.py`: Setup and launch the Flask api.
    - `api/views.py`: Contains the API endpoints. You must implement the following endpoints:
        - *index*: Displays a frontend in which the user can upload a form and get a prediction from the model.
        - *predict*: POST method which receives a form and sends back the model prediction with the probability and score. This endpoint is useful for integration with other services and platforms given we can access it from any other programming language.
    - `api/middleware`: It has a function that queues jobs into redis and waits for ML model to get a prediction as answer.
    - `api/utils.py`: Implements some extra functions used internally by the api.
    - `api/settings.py`: It has all the API settings.
    - `api/templates`: Here I put the .html files used in the frontend.
    - `api/static`: Here I put the .css, images, etc, used in the frontend.

- model: Implements the logic to get jobs from Redis and process them with the Machine Learning model. When we get the predicted value from the model, we must encole it on Redis again so it can be delivered to the user.
    - `model/data` : Carpet that contain the data to be used in preprocessing, received from ../download.py.
    - `model/ml_service.py`: Runs a thread in which it get jobs from Redis, process them with the model and returns the answers.
    - `model/settings.py`: Settings for the ML model.
    - `model/preprocessing.py`: Here I grouped all feature engineering in a single pipeline to be reused later in the project.
    - `model/train.py`: Train the selected model.
    - `model/pickles` : Carpet that save the pickles received from preprocessing and train to be used in ./ml_service.

- notebooks: Here I have the notebooks where I started with the project doing the EDA and training models.
    - `notebooks/EDA.ipynb`: Notebook with the Feature Engineering.
    - `notebooks/Model_Evaluation.ipynb`: Here I trained some models and got their metrics.

- uploads: Here you can see the forms received as a CSV file.
    - `forms.csv`: CSV file with the forms received.