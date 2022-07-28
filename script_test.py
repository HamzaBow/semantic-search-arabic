import matplotlib.pyplot as plt
import pretraitement as pt
import indexation
import recherche
import wordnet
import ontologie

collection_path="G:/PFE master/CODES/Collections/r/arabic_network_collection"

queries_results=[]
f=open('G:/PFE master/CODES/PROJECT/queries.txt','r')
lines=f.readlines()
for line in lines:
    if(line[0]!="\t"):
        queries_results.append([line[:len(line)-1],[]])
    else:
        queries_results[-1][1].append(line[1:len(line)-1])


prec5=[]
prec10=[]
prec20=[]
avg_precx=[]
DCGp=[]
for query,result in queries_results:
    query_terms=pt.tokenize_nd_stem(var_req.get())
    if(len(query_terms)!=0):
        results=recherche.search_onto(query_terms,ontologie.onto_index,listdir(collection_path),ontologie.cdic,ontologie.nw_ontology)
        
    








##a1,a2=[1,2,3,4,6,8],[3,6,4,9,6,5]
##b1,b2=[1,2,3,4,5,8],[6.5,7,5,8,2,4]
##c1,c2=[1,4,6,8],[4,4,2,7]
##
##plt.axis([0,9,1,15])
##plt.title('La courbe Précision-Rappel')
##plt.xlabel('Rappel')
##plt.ylabel('Précision')
##
##plt.plot(a1,a2,'r',label='Modèle basé Ontologie')
##plt.plot(b1,b2,'b',label='Modèle basé Arabic Wordnet')
##plt.plot(c1,c2,'g',label='Modèle basé Ontologie et AWN')
##
##plt.grid(True)
##plt.legend()
##plt.show()
