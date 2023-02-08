import pandas as pd
import numpy as np
import os
import argparse
import pickle
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer

def parse_args():
    '''
    Use argparse to get the input parameters for preprocessing the data`.

    '''

    parser = argparse.ArgumentParser(description = 'preprocessing')
    
    parser.add_argument(
        'columns',
        help = 'Select the columns csv.'
    )

    parser.add_argument(
        'modeling',
        type = str,
        help = 'Select the Modeling Data csv.'
    )

    args = parser.parse_args()

    return args

def main(columns, modeling):
    '''

    This function takes the files and preprocessing them.

    Parameters
    ----------
    columns : csv file
        Full path to PAKDD2010_VariablesList file.
    modeling : txt file
        Full path to PAKDD2010_Modeling_Data file.

    Returns:
    Prepocessed data.     
    '''

    print('Inizialization of prepocesing process... ')

    # Read the csv with the variables description.
    col_descript = pd.read_csv(columns)

    # I take columns names and make a list.
    col_nam = col_descript['Var_Title'].to_list()

    # I rename some columns.
    col_nam[6] = 'GENDER'
    col_nam[43] = 'MATE_EDUCATION_LEVEL'
    col_nam[53] = 'TARGET'

    # Read the csv that I will use.
    df = pd.read_csv(modeling, encoding = 'ISO-8859-1',
    delimiter='\t', header = None, names = col_nam, low_memory = False)
    
    df = df.drop(['MATE_PROFESSION_CODE', 'MATE_EDUCATION_LEVEL', 'EDUCATION_LEVEL', 'RESIDENCIAL_BOROUGH',
    'CITY_OF_BIRTH', 'RESIDENCIAL_PHONE_AREA_CODE','PROFESSIONAL_CITY', 'MONTHS_IN_THE_JOB', 'QUANT_ADDITIONAL_CARDS',
    'PROFESSIONAL_BOROUGH', 'PROFESSIONAL_STATE','RESIDENCIAL_CITY', 'PERSONAL_ASSETS_VALUE', 'POSTAL_ADDRESS_TYPE'], axis = 1)

    df = df.loc[:, df.apply(pd.Series.nunique) != 1]

    num = df.select_dtypes('number').columns
    df_num = df[num]

    cat = df.select_dtypes('object')
    df_cat_list = cat.keys().to_list()
    df_cat = df[df_cat_list]

    df = df.copy()

    # Numerical
    
    # MONTHS_IN_RESIDENCE
    df_mir = df['MONTHS_IN_RESIDENCE']
    df_mir.loc[(df_mir > 199)] = 101
    df_mir.loc[(df_mir > 31)] = 32

    # AGE
    df_num.loc[df_num['AGE'] < 17, 'AGE'] = 17

    # PERSONAL_MONTHLY_INCOME
    df_num['TOTAL_INCOMES'] = pd.DataFrame(df_num['PERSONAL_MONTHLY_INCOME'] + df_num['OTHER_INCOMES'])

    # MARITAL_STATUS
    df_num['MARITAL_STATUS'].loc[(df_num['MARITAL_STATUS'] > 3)] = 3
    
    # NACIONALITY
    df['NACIONALITY'].loc[(df['NACIONALITY'] == 2)] = 1

    # QUANT_DEPENDANTS
    df_num['QUANT_DEPENDANTS'].loc[(df_num['QUANT_DEPENDANTS'] >= 7)] = 7
    df_num['QUANT_DEPENDANTS'].loc[(df_num['QUANT_DEPENDANTS'] >= 10)] = 10

    # PROFESSION_CODE
    df_pc = df_num['PROFESSION_CODE']
    df_pc.loc[(df_pc >= 17)] = 17

    # Categorical

    # APPLICATION_SUBMISSION_TYPE
    df_cat['APPLICATION_SUBMISSION_TYPE'].replace({'0': 'Carga'}, inplace = True)

    # STATE_OF_BIRTH
    df_cat['STATE_OF_BIRTH'].replace({'XX': np.nan, ' ' : np.nan}, inplace = True)

    # RESIDENCIAL_ZIP_3
    df_cat['RESIDENCIAL_ZIP_3'].loc[(df_cat['RESIDENCIAL_ZIP_3']  == '#DIV/0!')] = np.nan

    # PROFESSIONAL_ZIP_3
    df_cat['PROFESSIONAL_ZIP_3'].loc[(df_cat['PROFESSIONAL_ZIP_3']  == '#DIV/0!')] = np.nan

    df = pd.concat([df_num, df_cat], axis = 1)

    df = df.drop(['PERSONAL_MONTHLY_INCOME', 'OTHER_INCOMES'], axis = 1)

    # I set the client_id as the index.
    df = df.set_index('ID_CLIENT')

    # Features
    X = df.drop(['TARGET'], axis = 1)

    # Labels
    y = df['TARGET']

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    train_size = .8,
    random_state = 42,
    stratify = y
    )
    
    # Pipeline for numerical
    pipe_num = Pipeline(steps = [
        ('impute', SimpleImputer(strategy = 'median')),
        ('scaler', StandardScaler())
    ])

    # Pipeline for categorical
    pipe_cat = Pipeline(steps = [
        ('impute', SimpleImputer(strategy = 'most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown = 'ignore', sparse = False, drop = 'if_binary'))
    ])

    # I use ColumnTransformer to takes the tuple of transformers
    full_processor = ColumnTransformer(transformers = [
        ('number', pipe_num, df_num.drop(['ID_CLIENT', 'TARGET', 'PERSONAL_MONTHLY_INCOME', 'OTHER_INCOMES'], axis = 1).keys().to_list() ),
        ('categorical', pipe_cat, df_cat_list)
    ])

    # I use the processor on X_train and X_test, respectively:
    pipe_final = make_pipeline(full_processor)

    # I fit the model.
    pipe_fit = pipe_final.fit(X_train.copy())

    # Save final preprocessing pipeline in a pickle, after fitting it
    with open(os.path.join('./pickles/', 'pipeline_fit.pickle'), 'wb') as f:
        pickle.dump(pipe_fit , f, protocol = pickle.HIGHEST_PROTOCOL)
    
    # I transform the data with the pipelines,
    # and then, make them a dataframe.
    X_train = pipe_fit.transform(X_train)
    X_train = pd.DataFrame(X_train)
    
    # I save the data set split in pickles.
    with open(os.path.join('./pickles/', 'X_train.pickle'), 'wb') as f:
        pickle.dump(X_train, f, protocol = pickle.HIGHEST_PROTOCOL)

    with open(os.path.join('./pickles/', 'y_train.pickle'), 'wb') as f:
        pickle.dump(y_train, f, protocol = pickle.HIGHEST_PROTOCOL)

    print('Preprocessing done.')

if __name__ == '__main__':

    args = parse_args()

    main(args.columns, args.modeling)