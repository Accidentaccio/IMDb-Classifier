from joblib import load
from pandas import DataFrame, read_csv, ExcelWriter
from os import chdir, listdir
from sys import path
from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from Addestramento_Classificatore import text_preprocessing

## Move terminal in the script's directory ##
chdir(path[0])

## Load classifier ##
clf = load('./Objects/clf.pkl')
count_vect = load('./Objects/count_vect.pkl')
tfidf_transformer = load('./Objects/tfidf_transformer.pkl')

## Download the dictionary for nltk's classifier ##
download('vader_lexicon')

## Creation of SentimentIntensityAnalyzer ##
sa = SentimentIntensityAnalyzer()

movies_results = []

## Loop for predict every movie ##
for file in listdir('./Reviews'):

    ## Read file of a movie ##
    df = read_csv(f'./Reviews/{file}')

    ## Apply preprocessing to entire column of dataframe ##
    df['Reviews'] = df['Reviews'].map(text_preprocessing)

    ## Prediction ##
    X_test_matrix = count_vect.transform(df['Reviews'])
    X_test_tfidf = tfidf_transformer.transform(X_test_matrix)
    predicted = clf.predict(X_test_tfidf)

    ## Get number of reviews for a film ##
    number_reviews = df.count()[0]

    ## Average of ratings ##
    average = 0
    for item in df['Rating']:
        average += item
    average /= number_reviews

    
    ## Convert in tuple because predicted is numpy array ##
    positives = tuple(predicted).count('positive')
    positive_rate = (positives/number_reviews)*100

    ## nltk sentiment analyzer ##
    positive_rate_nltk = 0
    for item in df['Reviews']:
        positive_rate_nltk += sa.polarity_scores(item)['pos']
    positive_rate_nltk = (positive_rate_nltk/number_reviews)*100

    ## Dictionary with the information of a film ##
    dictionary = {
        'Movie' : file.replace('.csv', ''),
        'Rating' : f'{round(average, 2)}/10',
        'Reviews' : number_reviews,
        'Positive rate' : f'{round(positive_rate, 2)}%',
        'Positive rate nltk' : f'{round(positive_rate_nltk, 2)}%'
    }

    movies_results.append(dictionary)

## Creation of dataframe ##
df = DataFrame(movies_results)

## Print dataframe sorted and save it in a excel's file ##
excel_file = ExcelWriter('./Results/Results_Sorted.xlsx', engine='xlsxwriter')

df = df.sort_values(by = 'Rating', ascending=False)
df.to_excel(excel_file, sheet_name='Marvel_Analysis', index=False)
print(df)

df = df.sort_values(by = 'Positive rate', ascending=False)
df.to_excel(excel_file, sheet_name='Marvel_Analysis', startcol=7, index=False)
print(df)

df = df.sort_values(by = 'Positive rate nltk', ascending=False)
df.to_excel(excel_file, sheet_name='Marvel_Analysis', startcol=14, index=False)
print(df)

excel_file.save()