#Imports
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pickle

import operator

class EggWaver:
    def __init__(self):
        self.model = None

    def train_model(self, data_x, data_y, ml_type, test_size = 0.2, random_state = None, **kwargs):
        #Setting default values
        if not "verbose" in kwargs:
           kwargs["verbose"] = 2
        if not "n_jobs" in kwargs:
           kwargs["n_jobs"] = -1

        #Splitting the data
        train_x, test_x, train_y, test_y = train_test_split(data_x, data_y)

        #Fitting model
        if ml_type == "RandomForestClassifier":
            self.model = RandomForestClassifier(**kwargs)

        self.model.fit(train_x, train_y)

        #Getting the prediction
        predict = model.predict(test_x)

        return {'classification_report': classification_report(test_y, predict),
                'confusion_matrix': confusion_matrix(test_y, predict)}

    def predict_chunk(self, data_x, chunk_size = 1):
        #Does the model exists?
        if self.model is None:
            raise Exception("Model not found")

        #Getting the prediction
        predict = self.model.predict_proba(data_x)

        #Getting the probability of each chunk based on the prediction of each individual point
        ret = []
    
        for beg in range(0, len(data_x.index), chunk_size):
            #Averaging the next chunk_size data points
            chunk_proba = predict[beg : min(beg + chunk_size, len(data_x.index)), ].mean(axis = 0)

            ret.append(chunk_proba)
        
        return ret

    def precision_chunk(self, true_y, pred_y):
        #Getting chunk_size
        chunk_size = int(len(true_y) / len(pred_y))

        #Getting expected results per chunk
        expected = []

        for beg in range(0, len(true_y), chunk_size):
            count = {}

            for point_index in range(beg, min(beg + chunk_size, len(true_y))):
                point = str(true_y[point_index])

                if not point in count:
                    count[point] = 0

                count[point] += 1

            expected.append(max(count.items(), key=operator.itemgetter(1))[0])

        #Returning
        return {'classification_report': classification_report(expected, pred_y),
                'confusion_matrix': confusion_matrix(expected, pred_y)}

    def save_model(self, file_object):
        #Does the model exists?
        if self.model is None:
            raise Exception("Model not found")

        #Saving model
        pickle.dump(self.model, file_object)

    def load_model(self, file_object):
        #Loading model
        self.model = pickle.load(file_object)