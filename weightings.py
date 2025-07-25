#this is a programme that loads a csv file and using several functions generates a coefficient which can then be used in
#designing a weighted average
#1st step
#we want to load our database using the pandas library
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("fdata.csv")
print(data)

#now that the data has been loaded unto the dataframe we need to clean the data and remove any values where appearances
#which is a heading in our data is equal to zero

#data = data[(data[['Appearances']] != 0).any(axis=1)]
#print(data)
def clean_data_set(df):
    """cleans any data where appearances is equal to zero in our dataframe"""
    df = df[df['Appearances'] != 0].copy()
    #df.columns = df.columns.astype(str)

    return df

#in this code snippet we drop all data in our dataframe where the data in the appearance column is equal to zero.the
#inplace parameter is to execute this change to our data frame
data =clean_data_set(data)
#we call our function and load our data set called fdata which is a csv file

from Realwork import stat
#print(stat)


#here in this piece of code the list stat is saved in a different file to save space and ensure code clarity this is then
#imported using the python import module.
def preprocess_data(data):
    data[stat] = data[stat].fillna(0)

    #X = data[stat].div(data["Appearances"], axis=0)
    X = data[stat].div(90)
    #X = X.fillna(0)

    y = data["Wins"]
    return X, y
#now that we have the data and the columns we want to use w e need to apply elastic net regression
# these specific columns we will create
#another function for this task



    # Load and preprocess the data

    # Scale features
def scale_features(X):
    scaler = StandardScaler()
    X.columns = X.columns.astype(str)
    X_scaled = scaler.fit_transform(X)
    return X_scaled

    # Split data
def split_data(X_scaled,y):
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
    # Initialize Elastic Net and perform grid search
def values():
    param_grid = {
        "alpha": [0.01,0.1, 0.5, 1.0,5,0.8,10],
        "l1_ratio": [0.1,0.2, 0.5,0.7]
    }
    return param_grid

def elastic_net(X_train,y_train,param_grid):
    elastic_net = ElasticNet(max_iter=10000000)
    grid_search = GridSearchCV(elastic_net, param_grid = param_grid, cv=5, scoring="neg_mean_squared_error")
    grid_search.fit(X_train, y_train)
    return grid_search
def best_performance(grid_search):
    # Best parameters
    best_model = grid_search.best_estimator_
    print("Best Parameters:", grid_search.best_params_)
    return best_model
def evaluate_performance(best_model,X_test,y_test):
    # Evaluate performance
    y_pred = best_model.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R-squared:", r2_score(y_test, y_pred))
#code from chatgpt
def get_coefficients(model, feature_names):
    """
    Returns a list of (feature, normalized_weight) tuples with clean float values.
    Also prints the normalized weights (not the raw coefficients).
    """
    coefs = model.coef_
    #this needs to be adjusted
    # Handle multiclass (e.g., logistic regression)
    if coefs.ndim == 2 and coefs.shape[0] > 1:
        coefs = coefs[0]

    coefs = coefs.flatten()
    total = sum(abs(coefs))  # use abs to ensure meaningful relative importance
    weights = coefs / total

    for name, weight in zip(feature_names, weights):
        print((name, float(weight)))
        #needs to be adjusted ends here

    return [(name, float(weight)) for name, weight in zip(feature_names, weights)]




def everything_together(df):
# Step 1: Clean the data
    df = clean_data_set(df)

    # Step 2: Extract features and target
    X, y = preprocess_data(df)

    # Step 3: Scale the features
    X_scaled = scale_features(X)

    # Step 4: Split the data
    X_train, X_test, y_train, y_test = split_data(X_scaled, y)

    # Step 5: Get hyperparameters
    param_grid = values()

    # Step 6: Train the model with grid search
    grid_search = elastic_net(X_train, y_train, param_grid)

    # Step 7: Get the best model
    best_model = best_performance(grid_search)

    # Step 8: Evaluate the model
    evaluate_performance(best_model, X_test, y_test)

    get_coefficients(best_model, stat)


print("--------------THIS IS FOR GENERAL----------------")
everything_together(data)

midfielder = data[data['Position'] == 'Midfielder']
print("------------THIS IS FOR MF-----------------------")
everything_together(midfielder)

gk = data[data['Position'] == 'Goalkeeper']
print("------------THIS IS FOR gk-----------------------")
everything_together(gk)

dfn = data[data['Position'] == 'Defender']
print("------------THIS IS FOR DF-----------------------")
everything_together(dfn)


st = data[data['Position'] == 'Forward']
print("------------THIS IS FOR FW-----------------------")
everything_together(st)


d=data[['Saves', 'Clean sheets']].corr()
print(d)





