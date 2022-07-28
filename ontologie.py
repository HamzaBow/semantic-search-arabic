from nltk.stem import ISRIStemmer
from collections import defaultdict
stemer=ISRIStemmer()
cdic={}
cdic_sh={}
nw_ontology=[]
onto_index={}
index_construit=False

def doc_rtl(s):
    s=s[0:len(s)-4]
    return " ".join(s.split()[::-1])

def reverse_concept(concept):
    c2=[]
    for elt in concept[::-1]:
        if(type(elt)==tuple):
            c2.append(elt[::-1])
            continue
        c2.append(elt)
    return c2

def get_concept_from_line(line,cat='lemme'):
    '''cat : categorie = "stem" or "lemme"'''
    s=line.strip()
    l=s.split()
    l2=[]
    for st in l:
        if(st.startswith('(')):
            liste=st[1:len(st)-1].split(',')
            if(cat=='stem'):
                l2.append(tuple([stemer.stem(e) for e in liste]))
            else:
                l2.append(tuple(liste))
        else:
            if(cat=='stem'):
                l2.append(stemer.stem(st))
            else:
                l2.append(st)
    return l2

def import_ontology_file():
    f=open('G:/PFE master/ACM CSS/Networks_Arabic_v9_synonyms.txt','r')
    lines=f.readlines()
    f.close()
    global cdic #concepts dictionary (id,concept)
    cdic={}
    global cdic_sh
    cdic_sh={}
    global nw_ontology #tuples of two elements each, each element is a concept_id
    nw_ontology=[]

    for i,line in enumerate(lines):
        cdic[i]=get_concept_from_line(line,cat='stem')
        cdic_sh[i]=reverse_concept(get_concept_from_line(line))
        #=============   add a (father,child) tuple
        nb_tabs=line.count('\t')
        for j in range(i,-1,-1):
            if(lines[j].count('\t')<nb_tabs):
                nw_ontology.append((j,i))
                break

##def indexer(poids):
##    global index_construit
##    if(index_construit==True):
##        return
##    index_construit=True
##    global onto_index
##    onto_index=defaultdict(list)
##    for cid in cdic:        #cid : concept identifier
##        for (tr,doc) in poids.keys():
##            for ce in cdic[cid]:        #ce : concept element (one of the elements of the concept
##                if(type(ce)==tuple):
##                    if(tr not in ce):
##                        break
##                else:
##                    if(tr!=ce):
##                        break
##            else:
##                onto_index[(cid,doc)].append(poids[(tr,doc)])
##    for k in onto_index:
##        onto_index[k]=sum(onto_index[k])/len(onto_index[k])

def indexer(poids,documents):
    global index_construit
    if(index_construit==True):
        return
    index_construit=True
    global onto_index
    onto_index={}
    for doc in documents:
        for cid in cdic:
            lpd=[]
            gfound=True
            for elt in cdic[cid]:
                found=False
                if(type(elt)==tuple):
                    for e in elt:
                        if(poids.get((e,doc),0)>0):
                            found=True
                            lpd.append(poids.get((e,doc),0))
                            break
                else:
                    if(poids.get((elt,doc),0)>0):
                        found=True
                        lpd.append(poids.get((elt,doc),0))
                if(found==False):
                    gfound=False
                    break
            if(gfound==True):
                if(len(lpd)!=0):
                    onto_index[(cid,doc)]=lpd
    for k in onto_index:
        onto_index[k]=sum(onto_index[k])/len(onto_index[k])





def str_show_index(first_elt="document"):#IMPROVE PRINTING LATER
    '''si first_elt="document" -> on affiche le document de chaque concept
si first_elt="concept" -> on affiche les documents pour chaque concept'''
    if(index_construit==False):
        affichage="\n"+63*"="+"\n\n"+5*" "+"L'index des concepts n'a pas encore été construit\n\n"+63*"="
        return affichage
    affichage=63*"="+"\n"+21*" "+"L'INDEX DES CONCEPTS\n\n\n "
    if(first_elt=="concept"):
        affichage+="PAR CONCEPT\n"
    else:
        affichage+="PAR DOCUMENTS\n"
    prec=""
    if(first_elt=="concept"):
        for((idc,do),pd)in sorted(onto_index.items()):
            z=str(pd)
            z=z[:6]
            if(cdic_sh[idc].__str__()==prec):
                affichage+=11*" "+"DOCUMENT : "+doc_rtl(do)+"\n"+11*" "+"POIDS = "+z+"\n\n"
            else:
                affichage+=63*"="+"\n\n CONCEPT : "+"("+str(idc)+'):'+cdic_sh[idc].__str__()+"\n\n "+"DOCUMENTS ET POIDS :\n\n"+\
                            11*" "+"DOCUMENT : "+doc_rtl(do)+"\n"+11*" "+"POIDS = "+z+"\n\n"
            prec=cdic_sh[idc].__str__()

    else:#first_elt="document"
        for((idc,do),pd)in sorted(onto_index.items(),key=lambda x:x[0][1]):
            z=str(pd)
            z=z[:6]
            if(do==prec):
                affichage+=11*" "+"("+str(idc)+'):'+cdic_sh[idc].__str__()+"\n"+11*" "+"POIDS = "+z+"\n\n"
            else:
                affichage+=63*"="+"\n\n DOCUMENT : "+doc_rtl(do)+"\n\n "+"CONCEPTS ET POIDS :\n\n"+\
                            11*" "+"("+str(idc)+'):'+cdic_sh[idc].__str__()+"\n"+11*" "+"POIDS = "+z+"\n\n"
            prec=do
    affichage+="\n"+63*"="+"\n"
    return affichage


    





###graphviz ontology must be improved before image generated & snapshot
###f=open('G:/PFE master/ACM CSS/Networks_Arabic_for_graphviz.txt','r')
##source= "digraph G {"
##for tupl in nw_ontology:
##    source+="\n"+'"'+tupl[0]+'"'+" -> "+'"'+tupl[1]+'"'+";"
##source+="\n }"
##fout=open('C:/Users/TEAM 161 User/Desktop/source.gv','w')
##fout.write(source)
##fout.close()
