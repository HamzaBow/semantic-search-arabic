import nltk.stem as stemmer
import string
import re
stemer = stemmer.ISRIStemmer()

def nettoyer(text_input):
    punct=list(string.punctuation)
    punct.extend(['؛','،','‘',"«","»",'·','؟'])
    tachkil={'ُ','َ','ِ','ْ','ٌ','ٍ','ّ'}
    alifs=['أ','آ','إ','ٱ']
    caracters=list(text_input)
    caracters2=[]
    for c in caracters:
        if(c in punct):
            caracters2.append(" ")
        elif(c in alifs):
            caracters2.append("ا")
        elif not((c in tachkil)or(c in string.digits)):
            caracters2.append(c)
    return ''.join(caracters2)

def tokenize_nd_stem(text):
    stopwords=open('G:/PFE master/CODES/stopwords/arabic_ansi.txt').read().split()
    text2=nettoyer(text)
    tokens=text2.split()
    tokens2=[stemer.stem(token) for token in tokens if ((token not in stopwords)and not(re.search('[a-zA-Z]',token)))]
    return tokens2
