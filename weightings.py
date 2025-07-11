import pandas as pd
import numpy as np

stat = pd.read_csv("fdata.csv")


data = [
   "Age","Appearances", "Goals", "Goals per match", "Headed goals",
   "Goals with right foot", "Goals with left foot", "Penalties scored", "Freekicks scored",
   "Shots", "Shots on target", "Shooting accuracy %", "Hit woodwork", "Big chances missed",
   "Clean sheets", "Goals conceded", "Tackles", "Tackle success %", "Last man tackles",
   "Blocked shots", "Interceptions", "Clearances", "Headed Clearance", "Clearances off line",
   "Recoveries", "Duels won", "Duels lost", "Successful 50/50s", "Aerial battles won",
   "Aerial battles lost", "Own goals", "Errors leading to goal", "Assists", "Passes",
   "Passes per match", "Big chances created", "Crosses", "Cross accuracy %", "Through balls",
   "Accurate long balls", "Saves", "Penalties saved", "Punches", "High Claims", "Catches",
   "Sweeper clearances", "Throw outs", "Goal Kicks", "Yellow cards", "Red cards", "Fouls",
   "Offsides"
]
#stat = stat[stat['Appearances'] != 0]
#stat[data] = stat[data].div(stat['Appearances'], axis=0)
#print(stat[data].isnull().any())
stat = stat.dropna(subset=data + ['Wins'])


X = stat[data]
y = stat['Wins']

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=19)
#copied

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.linear_model import ElasticNet

elastic_net = ElasticNet(max_iter=10000)
elastic_net.fit(X_train,y_train)
y_pred = elastic_net.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
mae =mean_absolute_error(y_test,y_pred)
print("this is the mean absolute error",mae)
mse =mean_squared_error(y_test, y_pred)
print("this is the mean squared error",mse)
rscore =r2_score(y_test, y_pred)
print("this is the r2score",rscore)

print("------------------------------")

param_grid = {
    "alpha": np.linspace(0.01,0.05, 1.0, 20),
    "l1_ratio": np.linspace(0.01, 1.0, 20),
}

from sklearn.model_selection import GridSearchCV
elastic_cv =GridSearchCV(estimator= elastic_net,param_grid=param_grid,cv =3 ,scoring='neg_mean_squared_error',n_jobs=-1)
#copied
elastic_cv.fit(X_train,y_train)
y_pred = elastic_cv.predict(X_test)
mae =mean_absolute_error(y_test,y_pred)
print("this is the mean absolute error",mae)
mse =mean_squared_error(y_test, y_pred)
print("this is the mean squared error",mse)
rscore =r2_score(y_test, y_pred)
print("this is the r2score",rscore)

coefs = pd.Series(elastic_cv.best_estimator_.coef_, index=X.columns)
coefs_sorted = coefs.sort_values(ascending=False)
print(coefs_sorted)
