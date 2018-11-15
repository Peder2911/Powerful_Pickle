from nltk.stem import WordNetLemmatizer
import re
from sklearn.feature_extraction.text import CountVectorizer

def wnl_nonum(doc):
    wnl = WordNetLemmatizer()
    cv = CountVectorizer()
    ana = cv.build_analyzer()
    
    doc = re.sub('[0-9]','',doc)
    return(wnl.lemmatize(w) for w in ana(doc))

