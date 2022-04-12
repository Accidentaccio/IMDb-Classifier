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

download('stopwords')
stops = set(stopwords.words('english'))


def text_preprocessing(text):
    
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

    global stops
    chdir(path[0])

    df = read_csv('IMDB Dataset.csv')
    df['Review'] = df['Review'].map(text_preprocessing)

    X_train, X_test, y_train, y_test = train_test_split(df['Review'], df['Sentiment'], test_size=0.33, random_state=10)

    count_vect = CountVectorizer()
    X_train_matrix = count_vect.fit_transform(X_train)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_matrix)

    clf = MultinomialNB()
    clf.fit(X_train_tfidf, y_train)


    ## Test ##
    X_test_matrix = count_vect.transform(X_test)
    X_test_tfidf = tfidf_transformer.transform(X_test_matrix)
    
    predicted = clf.predict(X_test_tfidf)

    
    ## Reports ##
    print(confusion_matrix(y_test,predicted))
    print(classification_report(y_test, predicted))

    dump(clf, './Objects/clf.pkl') 
    dump(count_vect, './Objects/count_vect.pkl')
    dump(tfidf_transformer, './Objects/tfidf_transformer.pkl')



if __name__ == '__main__':
    main()