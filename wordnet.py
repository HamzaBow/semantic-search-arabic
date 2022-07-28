import nltk.stem as stemmer
from itertools import product
import sqlite3 as sq

def get_synsets(word,cat="lemma"):
    '''returns list of tuples :(synsetid,[synonyms],gloss)
cat="stem" or "lemma" : category of words returned'''
    con=sq.connect('arabicwordnetExtendedBino.sqlite')
    cur=con.cursor()
    cur.execute('select wordid from form where value="{0}"'.format(word))
    res=[tup[0] for tup in cur.fetchall()]
    synids=[] #synsets identifiers (synsetid)
    for s in res:
        cur.execute('select synsetid from word where wordid="{0}"'.format(s))
        synids.append([tup[0] for tup in cur.fetchall()])
    results=[] #structure : every element = (synsetid:([values],gloss))
    for synid in synids:
        cur.execute('select value from word where synsetid="{0}"'.format(synid[0]))
        synset=cur.fetchall()
        cur.execute('select gloss from item where itemid="{0}"'.format(synid[0]))
        gloss=cur.fetchall()[0]
        results.append((synid[0],[w[0] for w in synset],gloss[0]))
    con.close()
    if(cat=='stem'):
        stemer=stemmer.ISRIStemmer()
        results2=[]
        for (synid,synonyms,gloss) in results:
            synonyms2=[]
            for synonym in synonyms:
                parts=synonym.split()#treat the case where synonym has more than 1 word. exp:"يذهب إلى"
                if(len(parts)>1):
                    stem=stemer.stem(max(parts,key=len))
                else:
                    stem=stemer.stem(synonym)  
                synonyms2.append(stem)
            results2.append((synid,synonyms2,gloss))
        return results2
    return results

def get_synos(stem):
    'return list of all synonyms of stem'
    synos=[]
    synsets=get_synsets(stem,'stem')
    for synset in synsets:
        for syno in synset[1]:   #synset[1] = liste des synonyms du synset
            if(syno not in synos):                    
                synos.append(syno)
    return synos

def get_expanded_query(query_terms):
    ''' returns a list of queries'''
    #appliquer les prétratement à la requête ("terms" est la liste des stem
    #changer ça par:tokenise,supp ponc,symb,
    #stopwords, tachkil and stemming
    query_sets=[]
    for term in query_terms:
        synonyms=[] # ensemble des synonymes de "term"
        synonyms.append(term)
        synsets=get_synsets(term,'stem')
        for synset in synsets:
            for synonym in synset[1]:   #synset[1] = liste des synonyms du synset
                if(synonym not in synonyms):                    
                    synonyms.append(synonym)
        query_sets.append(synonyms) #ajouter l'ensemble des synonyms de "term"
    queries=list(product(*query_sets)) #queries contient la liste de toutes les combinaison possible des termes de la requête
    return queries

def show_awn_expdq(queries,init_q):
    'show the expanded query i.e set of queries generated from synonyms'
    s="\n"+19*"="+" Expansion de la requête "+19*"="+"\n\n"
    s+="\n Requête : "+init_q.__str__()+"\n\n"

    for i,query in enumerate(queries):
        s+=26*"-"+" Requête {0} ".format(i+1)+(63-(36+len(str(i+1))))*"-"
        s+="\n\n  ("+" , ".join(query)+" )\n\n"
    return s
