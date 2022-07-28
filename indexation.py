from math import log
import nltk.stem as stemmer
from os import listdir
import pretraitement as pt
index_construit=False
#ajouter un autre module de prétraitement

def doc_rtl(s):
    s=s[0:len(s)-4]
    return " ".join(s.split()[::-1])

def save_index(path,name):
    global poids
    f=open(path+"/"+name,'w')
    for(term,doc),pd in poids.items():
        f.write(term+"\t"+doc+"\t"+str(pd)[:6]+"\n")

def import_index(index_path='G:/PFE master/CODES/Collections/INDEX/INDEX.TXT',\
                 collection_path='G:/PFE master/CODES/Collections/r/arabic_network_collection'):
    global poids
    global terms
    poids={}
    terms=[]
    f=open(index_path,'r')
    line=f.readline()
    while(line!=''):
        elt=line[:-1].split('\t')
        poids[(elt[0],elt[1])]=float(elt[2])
        if(elt[0] not in terms):
            terms.append(elt[0])
        line=f.readline()

    global nb_mot
    nb_mot = len(terms)
    global nb_doc
    nb_doc=len(listdir(collection_path))
               
def indexer(collection_path):
    '''retourne l'index (tf*idf) des documents contenus dans "chemin_collection"'''
    global index_construit
    global terms
    global poids
    if(index_construit==True):
        return   #l'index a déjà été construit (afficher plus tard qqc)
    index_construit=True
    documents=listdir(collection_path)
    
    poids={}
    terms=[]
    freq={}
    for doc in documents:
        f=open(collection_path+'/'+doc,'r')
        text=f.read()
        tokens=pt.tokenize_nd_stem(text)
        for token in tokens:
            freq[(token,doc)]=freq.get((token,doc),0)+1
            if(token not in terms):
                terms.append(token)
        f.close()
    ## calcul des poids
    for (termei,documi),fri in freq.items():
        maxf=0
        ## calcul du max
        for (terme,docum),fr in freq.items():
            if(docum==documi):
                if(maxf<fr):
                    maxf=fr
        ## calcul de nbDoc (nombre de document contenant le terme)
        for (terme,docum),fr in freq.items():
            nbDoc=0
            for docname in documents:
                if((termei,docname) in freq):
                    nbDoc=nbDoc+1
        poids[(termei,documi)]=(fri/maxf)*((log((len(documents)/nbDoc)+1))/log(10))

    save_index('G:/PFE master/CODES/Collections/INDEX','INDEX.TXT')
    global nb_mot
    nb_mot = len(terms)
    global nb_doc
    nb_doc=len(documents)

def str_show_index():#IMPROVE PRINTING LATER
    global poids
    if(index_construit==False):
        affichage="\n"+63*"="+"\n\n"+7*" "+"L'index des termes n'a pas encore été construit\n\n"+63*"="
        return affichage
    poids_trie=sorted(poids.items())
    global nb_mot
    global nb_doc
    affichage="\n====================== LE FICHIER INVERSE =====================\n\n"
    affichage+=63*"="+"\n MOT                     DOCUMENT                        POIDS \n"+63*"="+"\n"

    ter_prec=""
    for((ter,do),pd)in poids_trie:
        s1=26-round((4+round(len(ter)/1.4)+0.5*round(len(ter)/1.4)))
        s2=26-round((4+0.5*round(len(do)/1.4)))
        
        z=str(pd)
        z=z[:6]

        if(ter==ter_prec):
            affichage+=s1*" "+doc_rtl(do)+s2*" "+z+"\n"
        else:
            affichage+=63*'-'+"\n"+" "+ter+s1*" "+doc_rtl(do)+s2*" "+z+"\n"
        ter_prec=ter

    affichage+=63*"-"+"\n\n Le nombre de documents est : "+str(nb_doc)+"\n\n"
    affichage+=" Le nombre de mots est : "+str(nb_mot)+"\n\n"
    affichage+="\n"+63*"="+"\n"
    return affichage
