from joblib import dump
from pandas import read_csv
from os import chdir
from sys import path
from gensim.corpora.textcorpus import strip_multiple_whitespaces
from gensim.parsing.preprocessing import strip_punctuation, strip_numeric, strip_short, stem_text
from re import sub, findall
from nltk.corpus import stopwords
from nltk import download
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix, classification_report

## Download the dictionary of nltk's stopwords and put in a set ##
download('stopwords')
stops = set(stopwords.words('english'))


def text_preprocessing(text):
    
    """This function do the preprocessing of a string."""
    
    ## Import global stopwords ##
    global stops

    text = sub(r'(:\)|:-\)|:D|:-D)', 'happy', text)
    text = sub(r'(:\(|:-\()', 'happy', text)
    text = sub(r'o.O', 'incredulous', text)
    text = sub(r'(!!)+', 'bigExlamation', text)
    text = sub(r'!', 'Exlamation', text)
    text = sub(r'\?!\?', 'Doubtful', text)
    for item in findall('[A-Z]+[A-Z]+', text):
        text = sub(item, f'{item.lower()} shout{item.lower()}', text, count=1)
    text = text.lower()
    
    filtered_words = (word for word in text.split() if word not in stops)
    text = ' '.join(filtered_words)
    
    text = strip_punctuation(text)
    text = strip_numeric(text)
    text = strip_short(text, minsize=3)
    text = strip_multiple_whitespaces(text)
    return stem_text(text)

def main():

    ## Import global stopwords ##
    global stops
    
    ## Move terminal in the script's directory ##
    chdir(path[0])

    ## Read .csv file for the training and apply preprocessing to entire column of dataframe ##
    df = read_csv('./IMDB Dataset.csv')
    df['Review'] = df['Review'].map(text_preprocessing)

    ## Split data into train and test, with train 2/3 of the total and test 1/3.
    X_train, X_test, y_train, y_test = train_test_split(df['Review'], df['Sentiment'], test_size=0.33, random_state=10)

    ## Creation of matrix document-term ##
    count_vect = CountVectorizer()
    X_train_matrix = count_vect.fit_transform(X_train)

    ## Creation of array with weights of the words"
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_matrix)

    ## Creation of Naive-Bayes classifier and train it ##
    clf = MultinomialNB()
    clf.fit(X_train_tfidf, y_train)


    ## Test it with the test's dataset ##
    X_test_matrix = count_vect.transform(X_test)
    X_test_tfidf = tfidf_transformer.transform(X_test_matrix)
    ## Predicted the results ##
    predicted = clf.predict(X_test_tfidf)

    
    ## Reports ##
    print(confusion_matrix(y_test,predicted))
    print(classification_report(y_test, predicted))

    ## Save file for later ##
    dump(clf, './Objects/clf.pkl') 
    dump(count_vect, './Objects/count_vect.pkl')
    dump(tfidf_transformer, './Objects/tfidf_transformer.pkl')



if __name__ == '__main__':
    main()