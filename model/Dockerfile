FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/

WORKDIR /src

ADD preprocessing.py ./
ADD data/PAKDD2010_VariablesList.csv ./
ADD data/PAKDD2010_Modeling_Data.txt ./
ADD train.py ./
ADD pickles ./

RUN python3 preprocessing.py ./data/PAKDD2010_VariablesList.csv ./data/PAKDD2010_Modeling_Data.txt
RUN python3 train.py ./pickles/X_train.pickle ./pickles/y_train.pickle

FROM base as build
ENTRYPOINT ["python3", "/src/ml_service.py"]