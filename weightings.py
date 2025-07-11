#this is a programme that loads a csv file and using several functions generates a coefficient which can then be used in
#designing a weighted average
#1st step
#we want to load our database using the pandas library
import pandas as pd
data = pd.read_csv("fdata.csv")
print(data)

#now that the data has been loaded unto the dataframe we need to clean the data and remove any values where appearances
#which is a heading in our data is equal to zero

#data = data[(data[['Appearances']] != 0).any(axis=1)]
#print(data)
def clean_data_set(df):
    df = df[df['Appearances'] != 0].copy()
    return df


#in this code snippet we drop all data in our dataframe where the data in the appearance column is equal to zero.the
#inplace parameter is to execute this change to our data frame
data =clean_data_set(data)
print(data)

#this code snippet is inspired by stack overflow

