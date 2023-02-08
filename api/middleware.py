import json
import time
from uuid import uuid4
import redis
import settings

# Connect to Redis and assign to variable `db`
db = redis.Redis(
    port = settings.REDIS_PORT,
    db = settings.REDIS_DB_ID,
    host = settings.REDIS_IP
)

def model_predict(form_name):
    """
    Receives an form name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    form_name : str
        Name for the form uploaded by the user.

    Returns
    -------
    prediction, probability : tuple(str, float)
        Model predicted prediction as a string and the corresponding score(probability) as a number.
    """

    pred = None
    prob = None

    # Assign an unique ID for this job and add it to the queue.
    job_id = str(uuid4())

    # Create a dict with the job data and the id to send through Redis.
    job_dict =     {
        'id': job_id,
        'form' : form_name
    }

    # Json to string
    job_data = json.dumps(job_dict)

    # Send the job to the model service using Redis
    db.lpush(settings.REDIS_QUEUE, job_data)

    # Loop until we received the response from our ML model
    while True:

        # Attempt to get model predictions using job_id
        rpse = db.get(job_id)

        if rpse is None:
            time.sleep(settings.API_SLEEP)
            continue
        else:
            rpse = json.loads(rpse)
            pred = rpse['prediction']            
            prob = rpse['probability']
            # Delete the job from Redis after we get the results
            # Then exit the loop
            db.delete(job_id)
            break
    return pred, prob