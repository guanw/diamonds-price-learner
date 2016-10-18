import numpy as np
import pickle


from sklearn import preprocessing, linear_model

def one_hot_encoder(dataset, index, attributes):
    labelEncoder = preprocessing.LabelEncoder()
    labelEncoder.fit(attributes)
    dataset[:,index] = labelEncoder.transform(dataset[:,index])

def encode_all_strings(dataset):
    shape = ['Emerald', 'Oval', 'Round']
    color = ['G', 'F', 'E']
    clarity = ['VS1', 'VVS2', 'VVS1']
    cut = ['Good', 'Very Good', 'Ideal']

    one_hot_encoder(dataset, 0, shape)
    one_hot_encoder(dataset, 2, cut)
    one_hot_encoder(dataset, 3, color)
    one_hot_encoder(dataset, 4, clarity)

    return dataset

def convert_strings(dataset):
    dataset = dataset.astype(float)
    return dataset


def linear_regression_train(file_name, model_name):
    dataset = np.genfromtxt(file_name, delimiter=",", dtype="str")
    dataset = encode_all_strings(dataset)
    dataset = convert_strings(dataset)

    regr = linear_model.LinearRegression()
    regr.fit(dataset[:,:5], dataset[:,-1])
    pickle.dump(regr, open(model_name, 'wb'))

def test_model(test_file, model_name):
    regr = pickle.load(open(model_name, 'rb'))
    data = np.genfromtxt(test_file, delimiter=",", dtype="str")
    data = encode_all_strings(data)
    data = convert_strings(data)
    res = regr.predict(data)
    print res

if __name__ == "__main__":
    file_name = "./data.csv"
    model_name = 'linear.model'
    test_model('test.csv', model_name)