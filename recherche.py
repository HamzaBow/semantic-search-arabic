from operator import itemgetter
from math import sqrt
from random import randint
from collections import defaultdict


def doc_rtl(s):
    s=s[0:len(s)-4]
    return " ".join(s.split()[::-1])


                #===============================================#
                #                  USING ONTOLOGY               #
                #===============================================#



def rsv_c(query_concepts,sub_concepts,syn_concepts,docu,onto_index,cdic): #formule de Cosinus (Modèle Vectoriel)
    enum=0
    denom1=0
    denom2=0
    for cid in query_concepts:
        p=onto_index.get((cid,docu),0)
        enum+=p
        denom2+=1
    for cid in syn_concepts:
        p=onto_index.get((cid,docu),0)
        enum+=p*0.6
        denom2+=0.6
    for cid in sub_concepts:
        p=onto_index.get((cid,docu),0)
        enum+=p*0.4
        denom2+=0.4
    for cid in cdic:
        denom1+=pow(onto_index.get((cid,docu),0),2)
    Denom=sqrt(denom1*denom2)
    if(Denom==0):
        return 0
    return (enum/Denom)


def get_query_concepts(query_terms,cdic):
    query_concepts=[]
    for cid in cdic:
        for elt in cdic[cid]:
            if(type(elt)==tuple):
                found=False
                for e in elt:
                    if(e in query_terms):
                        found=True
                        break
                if(found==False):
                    break
            else:
                if(elt not in query_terms):
                    break
        else:
            query_concepts.append(cid)
    return query_concepts

def get_subconcepts(query_concepts,nw_ontology):# what about brother_concepts and others...
    sub_concepts=[]
    for (i,j) in nw_ontology:
        if (i in query_concepts):
            sub_concepts.append(j)
    return sub_concepts



def search_onto(query_terms,onto_index,documents,cdic,nw_ontology):#séparer le fct de recherche et celle de l'affichage
    query_concepts=get_query_concepts(query_terms,cdic)
    sub_concepts=get_subconcepts(query_concepts,nw_ontology)
    sims=[]
    for doc in documents:
        sim=rsv_c(query_concepts,sub_concepts,[],doc,onto_index,cdic)
        if(sim>0):
            sims.append((doc,round(sim,6)))
    return sorted(sims,key=itemgetter(1),reverse=True)

def str_search_onto(results):
    s="\n"+63*"="+"\n"+" "*20+"RECHERCHE AVEC ONTOLOGIE\n\n"
    s+=27*" "+"RESULTAT"+"\n\n"
    for i,(doc,sim) in enumerate(results):
        s+="="*30+" "+str(i+1)+" "+(31-len(str(i+1)))*"="+"\n\n"
        s+=" DOCUMENT :   "+doc_rtl(doc)
        s+="\n\n SIMILARITE :  "+str(round(sim,5))+"\n\n"        
    s+=63*"="
    return s

def get_parent(concept_id,nw_ontology):
    for (i,j) in nw_ontology:
        if(j==concept_id):
            return i
def onto_expdq_str(query_terms,cdic,cdic_sh,nw_ontology):
    query_concepts=get_query_concepts(query_terms,cdic)
    sub_concepts=get_subconcepts(query_concepts,nw_ontology)
    s=63*"="+"\n"+24*" "+"REQUETE ETENDUE\n"+63*"="+3*"\n"+" LES CONCEPTS DE LA REQUETE\n"
    s+="\n"+63*"="+"\n"+" CONCEPT_ID  |  CONCEPT\n"+63*"="+"\n"
    for cid in query_concepts:
        s+=4*" "+str(cid)+(9-len(str(cid)))*" "+"| "+cdic_sh[cid].__str__()+"\n"+63*"-"+"\n"
    s+=3*"\n"+" LES SOUS-CONCEPTS AJOUTEE\n\n"+63*"="+"\n SOUS-CONCEPT|  CONCEPT  |\n"
    s+="     ID      |  PARENT   |\n"+63*"="+"\n"
    for cid in sub_concepts:
        parent=get_parent(cid,nw_ontology)
        s+=4*" "+str(cid)+(9-len(str(cid)))*" "+"| "+4*" "+str(parent)+(7-len(str(parent)))*" "+"| "
        s+=cdic_sh[cid].__str__()+"\n"+63*"-"+"\n"
    return s
    
                #===============================================#
                #            USING ARABIC WORDNET               #
                #===============================================#

def rsv(lisMot,docu,poids,terms): #formule de Cosinus (Modèle Vectoriel)
    if(len(lisMot)==0):
        return 0
    enum=0
    denom1=0
    denom2=0
    for mot in lisMot:
        if(mot in terms):
            p=poids.get((mot,docu),0)
            enum+=p
            denom2+=1
    for term in terms:
        denom1+=pow(poids.get((term,docu),0),2)
    Denom=sqrt(denom1*denom2)
    if(Denom==0):
        return 0
    return (enum/Denom)

def search_awn(queries,poids,documents,terms):#séparer le fct de recherche et celle de l'affichage
    sims=[]
    nqe=[]
    i=0
    while(i<len(queries)):
        r=randint(0,len(queries)-1)
        if(r in nqe):
            continue
        nqe.append(r)
        for doc in documents:
            sim=rsv(queries[r],doc,poids,terms)
            if(sim>0):
                sims.append((r+1,doc,round(sim,7)))
        i+=1
        if(i==20):
            break
#################################################
    rdic={}#################################################
    doc_qs=defaultdict(list)#################################################
    for (num,doc,sim) in sims:#################################################
        rdic[doc]=rdic.get(doc,0)+sim#################################################
        doc_qs[doc].append(num)#################################################
    return sorted(rdic.items(),key=itemgetter(1),reverse=True),doc_qs#################################################
#################################################
def str_search_awn(results,doc_qs):
    s="\n"+63*"="+"\n"+" "*15+"RECHERCHE AVEC ARABIC WORDNET\n\n"
    s+=27*" "+"RESULTAT"+"\n\n"
    for i,(doc,pd) in enumerate(results):
        s+="="*30+" "+str(i+1)+" "+(31-len(str(i+1)))*"="+"\n\n"
        s+=" DOCUMENT :   "+doc_rtl(doc)+"\n\n NUM_REQUETES :"
        for nq in doc_qs[doc]:
            s+=" ("+str(nq)+")"
        s+="\n\n SIMILARITE :  "+str(round(pd,5))+"\n\n"
    s+=63*"="
    return s

                #===============================================#
                #       USING ARABIC WORDNET AND ONTOLOGY       #
                #===============================================#


def search_o_awn(query_terms,query_synos,onto_index,documents,cdic,nw_ontology):#séparer le fct de recherche et celle de l'affichage
    query_concepts=get_query_concepts(query_terms,cdic)
    concepts_synos=get_query_concepts(query_synos,cdic)
    concepts_synos=list(set(concepts_synos)-set(query_concepts))
    
    sub_concepts=get_subconcepts(query_concepts,nw_ontology)
    sub_concepts=list(set(sub_concepts)-set(query_concepts))
    
    sims=[]
    for doc in documents:
        sim=rsv_c(query_concepts,sub_concepts,concepts_synos,doc,onto_index,cdic)
        if(sim>0):
            sims.append((doc,round(sim,6)))
    return sorted(sims,key=itemgetter(1),reverse=True)

def o_awn_expdq_str(query_terms,query_synos,cdic,cdic_sh,nw_ontology):
    query_concepts=get_query_concepts(query_terms,cdic)
    concepts_synos=get_query_concepts(query_synos,cdic)
    concepts_synos=list(set(concepts_synos)-set(query_concepts))    
    sub_concepts=get_subconcepts(query_concepts,nw_ontology)
    s=63*"="+"\n"+24*" "+"REQUETE ETENDUE\n"+63*"="+3*"\n"+" LES CONCEPTS DE LA REQUETE\n"
    s+="\n"+63*"="+"\n"+" CONCEPT_ID  |  CONCEPT\n"+63*"="+"\n"
    for cid in query_concepts:
        s+=4*" "+str(cid)+(9-len(str(cid)))*" "+"| "+cdic_sh[cid].__str__()+"\n"+63*"-"+"\n"
    s+=3*"\n"+" LES SOUS-CONCEPTS AJOUTEE\n\n"+63*"="+"\n SOUS-CONCEPT|  CONCEPT  |\n"
    s+="     ID      |  PARENT   |\n"+63*"="+"\n"
    for cid in sub_concepts:
        parent=get_parent(cid,nw_ontology)
        s+=4*" "+str(cid)+(9-len(str(cid)))*" "+"| "+4*" "+str(parent)+(7-len(str(parent)))*" "+"| "
        s+=cdic_sh[cid].__str__()+"\n"+63*"-"+"\n"
    s+="\n\n\n LES CONCEPTS GENERES A PARTIR DES SYNONYMES\n"
    s+="\n"+63*"="+"\n"+" CONCEPT_ID  |  CONCEPT\n"+63*"="+"\n"
    for cid in concepts_synos:
        s+=4*" "+str(cid)+(9-len(str(cid)))*" "+"| "+cdic_sh[cid].__str__()+"\n"+63*"-"+"\n"
    return s








                #===============================================#
                #        modèle Vectoriel(formule cosinus)      #
                #===============================================#

def search_simple(query_terms,poids,documents,terms):#séparer le fct de recherche et celle de l'affichage
    sims=[]
    for doc in documents:
        sim=rsv(query_terms,doc,poids,terms)
        if(sim>0):
            sims.append((doc,round(sim,6)))
    return sorted(sims,key=itemgetter(1),reverse=True)



def str_search_simple(results):
    '''results : les résultat de la requête
it returns the string of results to show in GUI'''
    s="\n"+63*"="+"\n"+" "*20+"    RECHERCHE SIMPLE\n\n"
    s+="="*63+"\n DOCUMENT                          SIMILARITE\n"+"="*63+"\n"
    for elt in results:
        s+=" "+doc_rtl(elt[0])+" "+15*"-"+" "+str(elt[1])+"\n"
    s+="\n"+63*"="
    return s

             #=====================================================#
             # eliminate non relevant synsets and redundancy later #
             #=====================================================#












###this function is for returning the results for each query apart
##def search_awn(queries,poids,documents,terms):#séparer le fct de recherche et celle de l'affichage
##    global last_fct
##    last_fct="Recherche avec Arabic WordNet"
##    results=[] # stores the results for all queries
##    for query in queries[:15]: # must change "15" later
##        sims=[]
##        for doc in documents:
##            sims.append((doc,round(rsv(query,doc,poids,terms),5)))
##        results.append((query,sorted(sims,key=itemgetter(1),reverse=True)[:10]))#must change "10" later
##    return results


##def search_onto(query_terms,poids,onto_index,cdic,nw_ontology):
##    query_concepts=get_query_concepts(query_terms,cdic)
##    sub_concepts=get_subconcepts(query_concepts,nw_ontology)
##    results=[]
##    for (cid,doc),pd in sorted(onto_index.items(),key=itemgetter(1),reverse=True):
##        if(cid in query_concepts):
##            results.append((cid,doc,pd))
##        if(cid in sub_concepts):
##            results.append((cid,doc,pd*0.4))###############change the 0.5 later ###################
##    rdic={}
##    doc_cs=defaultdict(list)
##    for (cid,doc,pd) in results:
##        rdic[doc]=rdic.get(doc,0)+pd
##        doc_cs[doc].append(cid)
##    return sorted(rdic.items(),key=itemgetter(1),reverse=True),doc_cs


##def search_o_awn(query_terms,query_synos,poids,onto_index,cdic,nw_ontology):
##    query_concepts=get_query_concepts(query_terms,cdic)
##    concepts_synos=get_query_concepts(query_synos,cdic)
##    concepts_synos=list(set(concepts_synos)-set(query_concepts))
##    
##    sub_concepts=get_subconcepts(query_concepts,nw_ontology)
##    sub_concepts=list(set(sub_concepts)-set(query_concepts))
##    results=[]
##    for (cid,doc),pd in sorted(onto_index.items(),key=itemgetter(1),reverse=True):
##        if(cid in query_concepts):
##            results.append((cid,doc,pd))
##        if(cid in concepts_synos):
##            results.append((cid,doc,pd*0.6))
##        if(cid in sub_concepts):
##            results.append((cid,doc,pd*0.3))###############change the 0.5 later ###################
##    rdic={}
##    doc_cs=defaultdict(list)
##    for (cid,doc,pd) in results:
##        rdic[doc]=rdic.get(doc,0)+pd
##        doc_cs[doc].append(cid)
##    return sorted(rdic.items(),key=itemgetter(1),reverse=True),doc_cs
##
