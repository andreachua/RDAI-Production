import pickle
import numpy as np
from sklearn import preprocessing
import python_speech_features as mfcc
import os.path

class speakerIdService:
    def __init__(self):
        self.modelpath = "../demo_models/"

    def extract_features(self, audio,rate):
        mfcc_feature = mfcc.mfcc(audio,rate, 0.015, 0.01,20,nfft = 1024, appendEnergy = True)     
        mfcc_feature = preprocessing.scale(mfcc_feature)
        delta = self.calculate_delta(mfcc_feature)
        combined = np.hstack((mfcc_feature,delta)) 

        return combined

    def calculate_delta(self, array):

        rows,cols = array.shape
        deltas = np.zeros((rows,20))
        N = 2
        for i in range(rows):
            index = []
            j = 1
            while j <= N:
                if i-j < 0:
                    first =0
                else:
                    first = i-j
                if i+j > rows-1:
                    second = rows-1
                else:
                    second = i+j 
                index.append((second,first))
                j+=1
            deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
        return deltas
        
    def predict(self, audio):
        gmm_files = [os.path.join(self.modelpath, fname) for fname in os.listdir(self.modelpath) if fname.endswith('.gmm')]

        # Load Gaussian gender Models
        models = [pickle.load(open(fname,'rb')) for fname in gmm_files]
        speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname in gmm_files]

        sr = audio[0]
        audio = audio[1]
        vector = self.extract_features(audio,sr)

        log_likelihood = np.zeros(len(models))

        for i in range(len(models)):
            gmm = models[i] # check with each model 1-1
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()
        
        winner = np.argmax(log_likelihood)
        selected_model = speakers[winner].split('/')[2]

        return selected_model
    