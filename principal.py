import matplotlib.pyplot as plt
from string import *
from tkinter import *
from nltk.stem import ISRIStemmer
import pretraitement as pt
import indexation
import recherche
import wordnet
import ontologie
import experimentation as experm
from operator import itemgetter
from os import listdir
import re

last_q=""
last_awn_queries=[]

last_w_syn=""
last_w_synr=""

last_q_o_awn=""
last_query_synos=[]

#collection_path='G:/PFE master/CODES/Collections/SMALL_TEST_COL'
collection_path="G:/PFE master/CODES/Collections/r/arabic_network_collection"
                #==============================================#
                #       transfer the following results         #
                #==============================================#
def docs_rtl(list_doc):
    l2=[]
    for doc in list_doc:
        s=doc[0:len(doc)-4]
        l2.append(" ".join(s.split()[::-1]))
    return l2

def inv_words(st):
    '''inverse words in a string'''
    l=st.split()
    if(len(l)<=1):
        return st
    ll=[]
    for w in reversed(l):
        ll.append(w)
    return(" ".join(ll))

def inv_w_list(liste):
    '''inverse words in a list of strings'''
    liste2=[inv_words(w) for w in liste]
    return liste2

def car_to_pos(c):
    'convert caracter to part-of-speech'
    pos=''
    if(c=='n'):
        pos="NOUN"
    elif(c=='v'):
        pos="VERB"
    elif(c=='a'):
        pos="ADJECTIVE"
    elif(c=='r'):
        pos="ADVERB"
    elif(c=='s'):
        pos='ADJECTIve SATELLITE'
    else:
        pos='UNKNOWN'
    return pos
        
def show_synsets_from_stem(): #change it to "from word"	#=====    AFFICHER LES SYNSET DU MOT ===================================
    resultat.delete(1.0,END)
    if(var_mot.get()==''):
        resultat.insert(END,"\n"+63*"="+"\n\n"+24*" "+"PAS DE MOT"+"\n\n"+63*"=")
        return
    global last_w_syn
    global last_w_synr
    if(last_w_syn==var_mot.get()):
        resultat.insert(END,last_w_synr)
        return
    last_w_syn=var_mot.get()
    stemer = ISRIStemmer()
    R=wordnet.get_synsets(stemer.stem(var_mot.get()),'lemma')
    #changer show_synsets par "affichage_synsets" (la même chose pour les autres)
    show_synsets="\n"+22*"="+" LES SYNSETS DU MOT "+21*"="+"\n\n"
    show_synsets+="\n WORD : "+var_mot.get()+"\n\n"
    for i,(synid,synset,gloss) in enumerate(R):
        if(synid[-4].isnumeric()):
            pos=synid[-5]
        else:
            pos=synid[-4]
        show_synsets+=26*"-"+" Synset {0} ".format(i+1)+(63-(35+len(str(i+1))))*"-"
        show_synsets+="\n  P-O-S : "+car_to_pos(pos)
        show_synsets+="\n  Synonyms : "+" - ".join(inv_w_list(synset))+" ."
        if(gloss!=''):
            show_synsets+="\n  Gloss: "+inv_words(gloss)
        show_synsets+="\n\n"
    show_synsets+="\n"+63*"="
    last_w_synr=show_synsets
    resultat.insert(END,show_synsets)

def show_docs():
    documents=listdir(collection_path)
    resultat.delete(1.0,END)
    resultat.insert(END,"\n"+15*"="+" LES DOCUMENTS DE LA COLLECTION "+16*"="+"\n\n")
    resultat.insert(END,'\n  '+"\n  ".join(docs_rtl(documents))+'\n\n'+63*'=')
    resultat.insert(END,'\n\n - Le nombre de documents : '+ str(len(documents))+'\n\n')
    resultat.insert(END,' - Adresse de la collection :\n\n'+10*' '+collection_path+'\n')

def import_index():
    indexation.import_index()
    indexation.index_construit=True
    ontologie.import_ontology_file()
    ontologie.indexer(indexation.poids,listdir(collection_path))
    resultat.delete(1.0,END)
    resultat.insert(END,"\n"+63*"="+"\n\n"+15*" "+"les deux index ont été importé\n\n"+63*"=")
    return

def construire_index():
    global collection_path
    indexation.indexer(collection_path)
    ontologie.import_ontology_file()
    ontologie.indexer(indexation.poids,listdir(collection_path))
    resultat.delete(1.0,END)
    resultat.insert(END,"\n"+63*"="+"\n\n"+20*" "+"L'index a été construit\n\n"+63*"=")
    return
    
def show_index():
    s=indexation.str_show_index()
    resultat.delete(1.0,END)
    resultat.insert(END,s)

def show_indexc():
    global str_show_index
    if(cindex_show_v.get()==1):
        s=ontologie.str_show_index("concept")
    else:
        s=ontologie.str_show_index()
    resultat.delete(1.0,END)
    resultat.insert(END,s)

def show_expanded_query():
    resultat.delete(1.0,END)
    global last_q
    global last_awn_queries

    global last_q_o_awn
    global last_query_synos
    query_terms=pt.tokenize_nd_stem(var_req.get())
    if(len(query_terms)==0):
        resultat.insert(END,"\n"+63*"="+"\n\n"+24*" "+"PAS DE REQUETE"+"\n\n"+63*"=")
        return
    global rad_v
    if(rad_v.get()==0):#ontologie
        str_show=recherche.onto_expdq_str(query_terms,ontologie.cdic,ontologie.cdic_sh,ontologie.nw_ontology)
    elif(rad_v.get()==1):#arabic wordnet
        if(last_q==var_req.get()):
            queries=last_awn_queries
        else:
            last_q=var_req.get()
            queries=last_awn_queries=wordnet.get_expanded_query(query_terms)
        str_show=wordnet.show_awn_expdq(queries,query_terms)
    elif(rad_v.get()==2):#ontologie et arabic wordnet
        if(last_q_o_awn==var_req.get()):
            query_synos=last_query_synos
        else:
            last_q_o_awn=var_req.get()
            query_synos=query_terms.copy()
            for term in query_terms:
                synos=wordnet.get_synos(term)
                query_synos.extend(synos)
            last_query_synos=query_synos
        str_show=recherche.o_awn_expdq_str(query_terms,query_synos,ontologie.cdic,ontologie.cdic_sh,ontologie.nw_ontology)
    elif(rad_v.get()==3):#aucun expansion
        str_show=63*"="+"\n\n"+24*" "+"PAS D'EXPANSION\n\n"+63*"="
    resultat.insert(END,str_show)

def show_search_results():
    resultat.delete(1.0,END)
    global last_q
    global last_awn_queries

    global last_q_o_awn
    global last_query_synos
    query_terms=pt.tokenize_nd_stem(var_req.get())
    if(len(query_terms)==0):
        resultat.insert(END,"\n"+63*"="+"\n\n"+24*" "+"PAS DE REQUETE"+"\n\n"+63*"=")
        return
    global rad_v
    global collection_path
    if(rad_v.get()==0):#ontologie
        results=recherche.search_onto(query_terms,ontologie.onto_index,listdir(collection_path),ontologie.cdic,ontologie.nw_ontology)
        s=recherche.str_search_onto(results)
    elif(rad_v.get()==1):#arabic wordnet
        if(last_q==var_req.get()):
            queries=last_awn_queries
        else:
            last_q=var_req.get()
            queries=last_awn_queries=wordnet.get_expanded_query(query_terms)
        results,doc_qs=recherche.search_awn(queries,indexation.poids,listdir(collection_path),indexation.terms)
        s=recherche.str_search_awn(results,doc_qs)
    elif(rad_v.get()==2):#ontologie et arabic wordnet
        if(last_q_o_awn==var_req.get()):
            query_synos=last_query_synos
        else:
            last_q_o_awn=var_req.get()
            query_synos=query_terms.copy()
            for term in query_terms:
                synos=wordnet.get_synos(term)
                query_synos.extend(synos)
            last_query_synos=query_synos
        results=recherche.search_o_awn(query_terms,query_synos,ontologie.onto_index,listdir(collection_path),ontologie.cdic,ontologie.nw_ontology)
        s=recherche.str_search_onto(results)
    elif(rad_v.get()==3):#aucun expansion
        results=recherche.search_simple(query_terms,indexation.poids,listdir(collection_path),indexation.terms)
        s=recherche.str_search_simple(results)
    resultat.insert(END,s)
    return
##=========================== Phase de test ======================================

def precisionx(col_results,q_results,rank):
    if(len(q_results)<rank):
        return len(set(q_results)&set(col_results))/len(q_results)
    return len(set(q_results[:rank])&set(col_results))/rank
def rappelx(col_results,q_results,rank):
    return len(set(q_results[:rank])&set(col_results))/len(col_results)

def experiment():
    global queries_results
    queries_results=[]
    f=open('G:/PFE master/CODES/PROJECT/queries.txt','r')
    lines=f.readlines()
    for line in lines:
        if(line[0]!="\t"):
            queries_results.append([line[:len(line)-1],[]])
        else:
            queries_results[-1][1].append(line[1:len(line)-1])

    global prec5
    global prec10
    global prec20
    
    global rap5
    global rap10
    global rap20
    
    prec5=[]
    prec10=[]
    prec20=[]

    rap5=[]
    rap10=[]
    rap20=[]

    global avg_precx
    global avg_rapx
    avg_precx=[]
    avg_rapx=[]
    
    for query,col_results in queries_results:
        query_terms=pt.tokenize_nd_stem(query)
        if(len(query_terms)==0):
            continue

        #Ontology
        results=recherche.search_onto(query_terms,ontologie.onto_index,listdir(collection_path),ontologie.cdic,ontologie.nw_ontology)
        q_results=[doc for doc,sim in results]
        linep5=[precisionx(col_results,q_results,5)]
        linep10=[precisionx(col_results,q_results,10)]
        linep20=[precisionx(col_results,q_results,20)]

        liner5=[rappelx(col_results,q_results,5)]
        liner10=[rappelx(col_results,q_results,10)]
        liner20=[rappelx(col_results,q_results,20)]

        #AWN
        queries=last_awn_queries=wordnet.get_expanded_query(query_terms)
        results,doc_qs=recherche.search_awn(queries,indexation.poids,listdir(collection_path),indexation.terms)
        q_results=[doc for doc,sim in results]
        linep5.append(precisionx(col_results,q_results,5))
        linep10.append(precisionx(col_results,q_results,10))
        linep20.append(precisionx(col_results,q_results,20))

        liner5.append(rappelx(col_results,q_results,5))
        liner10.append(rappelx(col_results,q_results,10))
        liner20.append(rappelx(col_results,q_results,20))

        #AWN & Ontology
        query_synos=query_terms.copy()
        for term in query_terms:
            synos=wordnet.get_synos(term)
            query_synos.extend(synos)
        results=recherche.search_o_awn(query_terms,query_synos,ontologie.onto_index,listdir(collection_path),ontologie.cdic,ontologie.nw_ontology)        
        q_results=[doc for doc,sim in results]
        linep5.append(precisionx(col_results,q_results,5))
        linep10.append(precisionx(col_results,q_results,10))
        linep20.append(precisionx(col_results,q_results,20))

        liner5.append(rappelx(col_results,q_results,5))
        liner10.append(rappelx(col_results,q_results,10))
        liner20.append(rappelx(col_results,q_results,20))

        #Recherche Simple
        results=recherche.search_simple(query_terms,indexation.poids,listdir(collection_path),indexation.terms)
        q_results=[doc for doc,sim in results]
        linep5.append(precisionx(col_results,q_results,5))
        linep10.append(precisionx(col_results,q_results,10))
        linep20.append(precisionx(col_results,q_results,20))

        liner5.append(rappelx(col_results,q_results,5))
        liner10.append(rappelx(col_results,q_results,10))
        liner20.append(rappelx(col_results,q_results,20))

        prec5.append(linep5)
        prec10.append(linep10)
        prec20.append(linep20)
        avg_precx.append([round(sum(x)/len(x),2) for x in zip(linep5,linep10,linep20)])

        rap5.append(liner5)
        rap10.append(liner10)
        rap20.append(liner20)
        avg_rapx.append([round(sum(x)/len(x),2) for x in zip(liner5,liner10,liner20)])
        
    #calculer
    global avg_prec2
    global avg_rap2
    avg_prec2=[0,0,0,0]
    avg_rap2=[0,0,0,0]
    
    for line in avg_precx:
        for i,val in enumerate(line):
            avg_prec2[i]+=val
    avg_prec2=[round(val/12,2) for val in avg_prec2]

    for line in avg_rapx:
        for i,val in enumerate(line):
            avg_rap2[i]+=val
    avg_rap2=[round(val/12,2) for val in avg_rap2]

    global f_mesure
    f_mesure=[(2*x*y)/(x+y) for x,y in zip(avg_prec2,avg_rap2)]
    experm.save_experimentation(queries_results,prec5,prec10,prec20,rap5,rap10,rap20,avg_precx,avg_rapx,avg_prec2,avg_rap2,f_mesure)
    
    resultat.delete(1.0,END)
    resultat.insert(END,"Prec5\n"+prec5.__str__()+"\n\n")
    resultat.insert(END,"Prec10\n"+prec10.__str__()+"\n\n")
    resultat.insert(END,"Prec20\n"+prec20.__str__()+"\n\n")

    resultat.insert(END,"rap5\n"+rap5.__str__()+"\n\n")
    resultat.insert(END,"rap10\n"+rap10.__str__()+"\n\n")
    resultat.insert(END,"rap20\n"+rap20.__str__()+"\n\n")

    resultat.insert(END,"avg_precx\n"+avg_precx.__str__()+"\n\n")
    resultat.insert(END,"avg_rapx\n"+avg_rapx.__str__()+"\n\n")

    resultat.insert(END,"avg_prec2\n"+avg_prec2.__str__()+"\n\n")
    resultat.insert(END,"avg_rap2\n"+avg_rap2.__str__()+"\n\n")

    resultat.insert(END,"f_mesure\n"+f_mesure.__str__()+"\n\n")


##
##    a1,a2=[1,2,3,4,6,8],[3,6,4,9,6,5]
##    b1,b2=[1,2,3,4,5,8],[6.5,7,5,8,2,4]
##    c1,c2=[1,4,6,8],[4,4,2,7]
##
##    plt.axis([0,9,1,15])
##    plt.title('La courbe Précision-Rappel')
##    plt.xlabel('Rappel')
##    plt.ylabel('Précision')
##
##    plt.plot(a1,a2,'r',label='Modèle basé Ontologie')
##    plt.plot(b1,b2,'b',label='Modèle basé Arabic Wordnet')
##    plt.plot(c1,c2,'g',label='Modèle basé Ontologie et AWN')
##
##    plt.grid(True)
##    plt.legend()
##    plt.show()












##=========================== l'interface graphique ==============================    
from tkinter import *
fen=Tk()
fen.geometry('1020x685+200+5')
f,h,w=("Cambria",12),2,16
h2,w2=h-2,w-1

fen.title("RECHERCHE SEMANTIQUE")
txt_req=Label(fen,text="Requête :",font=f)
txt_mot=Label(fen,text="Mot :",font=f)

var_req=StringVar()
var_mot=StringVar()

entr_req=Entry(fen,textvariable=var_req)
entr_mot=Entry(fen,textvariable=var_mot)

entr_req.config(font=("consolas",12))
entr_mot.config(font=("consolas",12))

btn_col="light goldenrod"


butt_synsets=Button(fen,text="Synsets",bg=btn_col,height=h2,width=w2,font=f,command=show_synsets_from_stem)
butt_aff_doc=Button(fen,text="Liste de tous\nles documents",bg=btn_col,height=h2,width=w2,font=f,command=show_docs)
#butt_stat=Button(fen,text="???about???",bg="light blue",height=h,width=w,font=f)
butt_index=Button(fen,text="Afficher l'Index\ndes termes",bg="light blue",height=h,width=w,font=f,command=show_index)

butt_quit=Button(fen,text="Quitter",bg="dark gray",height=h,width=w,font=f,command=fen.destroy)
butt_experiment=Button(fen,text="Experimentations",bg="dark gray",height=h,width=w,font=f,command=experiment)
butt_gen_index=Button(fen,text="Contruire\nl'Index",bg="light blue",height=h,width=w,font=f,command=construire_index)
butt_import_index=Button(fen,text="Importer\nl'Index",bg="light blue",height=h,width=w,font=f,command=import_index)
fra = Frame(fen,width=600,height=450)
fra.grid_propagate(False)
fra.grid_rowconfigure(0,weight=1)
fra.grid_columnconfigure(0,weight=1)

resultat=Text(fra,height=25,width=25,wrap=WORD,bg="white",relief="sunken")
resultat.config(font=("consolas",12))
resultat.grid(row=0,column=0,sticky="nsew",padx=2,pady=2)


scrollbar = Scrollbar(fra, command=resultat.yview)
scrollbar.grid(row=0,column=1,sticky='nsew')
resultat['yscrollcommand']=scrollbar.set

txt_mot.grid(row=0,column=0,padx=5,pady=2)
txt_req.grid(row=0,column=1,padx=5,pady=2)

entr_mot.grid(row=1,column=0,padx=10,pady=2)
entr_req.grid(row=1,column=1,padx=10,pady=2,sticky='ew')

#==================== Radio buttons & Search Btn ===========================
rbt_fra=Frame(fen)
rbt_fra.grid_propagate(True)
rbt_fra.grid_rowconfigure(0,weight=1)
rbt_fra.grid_columnconfigure(0,weight=1)
rad_v=IntVar()

rbt1=Radiobutton(rbt_fra,text="Expansion avec Ontologie de Domaine.",variable=rad_v,value=0)
rbt2=Radiobutton(rbt_fra,text="Expansion avec Arabic Wordnet.",variable=rad_v,value=1)
rbt3=Radiobutton(rbt_fra,text="Expansion avec l'Ontologie et Arabic Wordnet.\t\t\t\t\t",variable=rad_v,value=2)
rbt4=Radiobutton(rbt_fra,text="Aucune Expansion.",variable=rad_v,value=3)
butt_rech=Button(rbt_fra,text="Rechercher",bg=btn_col,height=h,width=w-1,font=f,command=show_search_results)
butt_show_expd_q=Button(rbt_fra,text="Afficher\nRequête étendue",bg=btn_col,height=h2,width=w2,font=f,command=show_expanded_query)

rbt1.grid(row=0,column=0,sticky="w",padx=0)
rbt2.grid(row=1,column=0,sticky="w",padx=0)
rbt3.grid(row=2,column=0,sticky="w",padx=0)
rbt4.grid(row=3,column=0,sticky="w",padx=0)
butt_rech.grid(row=2,column=1,rowspan=2,padx=10,pady=0,sticky='e')
butt_show_expd_q.grid(row=0,column=1,rowspan=2,padx=5,pady=5)
#===============================================================================
#==================== Radio buttons & btn for showing concepts index ===========
rci_fra=Frame(fen)
rci_fra.grid_propagate(True)
rci_fra.grid_rowconfigure(0,weight=1)
rci_fra.grid_columnconfigure(0,weight=1)
cindex_show_v=IntVar()

rci1=Radiobutton(rci_fra,text="par document.",variable=cindex_show_v,value=0)
rci2=Radiobutton(rci_fra,text="par concept.",variable=cindex_show_v,value=1)
butt_indexc=Button(rci_fra,text="Afficher l'Index\ndes concepts",bg="light blue",height=h,width=w,font=f,command=show_indexc)

butt_indexc.grid(row=0)
rci1.grid(row=1,sticky="w")
rci2.grid(row=2,sticky="w")
#===============================================================================
butt_synsets.grid(row=2,column=0,padx=5,pady=5,sticky='n')
butt_aff_doc.grid(row=1,column=2,padx=20,pady=5)
butt_index.grid(row=3,column=2,padx=5,pady=5)
butt_quit.grid(row=6,column=2,padx=5,pady=5,sticky='s')
butt_experiment.grid(row=6,column=0,padx=5,pady=5,sticky='s')
butt_gen_index.grid(row=3,column=0,padx=5,pady=5)
butt_import_index.grid(row=4,column=0,padx=5,pady=5)
fra.grid(row=3,column=1,padx=5,pady=5,rowspan=4)
rbt_fra.grid(row=2,column=1,padx=5,pady=5)
rci_fra.grid(row=4,column=2,padx=5,pady=5)

fen.mainloop()
