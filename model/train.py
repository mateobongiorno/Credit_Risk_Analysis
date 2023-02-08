import os
import argparse
import pickle
from xgboost import XGBClassifier

def parse_args():
    '''
    Use argparse to get the input parameters for preprocessing the data`.
    '''
    parser = argparse.ArgumentParser(description = 'Train your model.')
    parser.add_argument(
        'data_preprocessed',
        type = str,
        help = 'Full path to the X_train pickle file, where is alocated the preprocessed data.'
    )

    parser.add_argument(
        'target',
        type = str,
        help = 'Full path to the y_train pickle file.'
    )

    args = parser.parse_args()

    return args

def main(data_preprocessed, target):
    '''
    This function train a machine learning model using XGBoost algorithm. The only input argument it
    should receive is the path to our preprocessed file.

    Parameters
    ----------
    data_preprocessed : pickle file
        Full path to X_train pickle file.
    target(y_train) : pickle file
        Full path to y_train pickle file.
    Returns:
    pred_class: Binary class prediction of the target variable.
       
    '''
    print('Start training the model...')

    # Load the X_train pickle
    with open(data_preprocessed, 'rb') as f:
        X_train = pickle.load(f) 

    # Load the y_train pickle
    with open(target, 'rb') as f:
        y_train = pickle.load(f)

    # I make a xgb model and train it
    xgb_model = XGBClassifier()
    model_fit = xgb_model.fit(X_train, y_train)

    # Save fitted XGBClassifier model
    with open(os.path.join('./pickles/', 'model_fit.pickle'), 'wb') as f:
         pickle.dump(model_fit, f, protocol = pickle.HIGHEST_PROTOCOL)

    print('Model is now trained.')

if __name__ == '__main__':

    args = parse_args()

    main(args.data_preprocessed, args.target)
