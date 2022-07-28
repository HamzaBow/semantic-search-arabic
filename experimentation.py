import xlsxwriter

def save_experimentation(queries_results,prec5,prec10,prec20,rap5,rap10,rap20,avg_precx,avg_rapx,avg_prec2,avg_rap2,f_mesure):
    workbook = xlsxwriter.Workbook('Experim_results.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0,"Requêtes de test")
    row = 1
    col = 0
    for i,(query,results) in enumerate(queries_results):
        worksheet.write(row, col,"requête "+str(i+1))
        worksheet.write(row, col+1,query)
        row+=1
    row+=2

    
    for i,measure_results in enumerate([prec5,prec10,prec20,rap5,rap10,rap20,avg_precx,avg_rapx,[avg_prec2,avg_rap2,f_mesure]]):
                                       
        if(i==0):
            worksheet.write(row, col,"Précision au rang 5")
        elif(i==1):
            worksheet.write(row, col,"Précision au rang 10")
        elif(i==2):
            worksheet.write(row, col,"Précision au rang 20")
        elif(i==3):
            worksheet.write(row, col,"rappel au rang 5")
        elif(i==4):
            worksheet.write(row, col,"rappel au rang 10")
        elif(i==5):
            worksheet.write(row, col,"rappel au rang 20")
        elif(i==6):
            worksheet.write(row, col,"Précision moyenne des précisions au rang x")
        elif(i==7):
            worksheet.write(row, col,"Rappel moyen des rappels au rang x")
        elif(i==8):
            worksheet.write(row, col,"Mesures pour les modèles")

        row+=1
        if(i<8):
            worksheet.write(row, col,"Requête ")
        worksheet.write(row, col+1,"Modèle basé Ontologie")
        worksheet.write(row, col+2,"Modèle basé AWN")
        worksheet.write(row, col+3,"Modèle basé Ontologie et AWN")
        worksheet.write(row, col+4,"Modèle vectoriel")

        row+=1
        if(i<8):
            for j,qr in enumerate(measure_results):
                worksheet.write(row, col,"Req "+str(j+1))
                for k,qv in enumerate(qr):
                    worksheet.write(row, col+(k+1),qv)
                row+=1
            row+=2
        else:
            for j,qr in enumerate(measure_results):
                if(j==0):
                    worksheet.write(row, col,"Précision")
                if(j==1):
                    worksheet.write(row, col,"Rappel")
                if(j==2):
                    worksheet.write(row, col,"F-mesure")
                for k,qv in enumerate(qr):
                    worksheet.write(row, col+(k+1),qv)
                row+=1
            row+=2
    
    





    workbook.close()
    

        
##
##    requête | formule
##            |
##            |
##
##
##    PREC5
##          ontologie AWN AWN_&_O M_vectoriel
##    req1    
##    req2
##    req3
##    ...
##    req11
##---------------------------------------------
##    PREC10
##          ontologie AWN AWN_&_O M_vectoriel
##    req1    
##    req2
##    req3
##    ...
##    req11
##---------------------------------------------
##    PREC20
##          ontologie AWN AWN_&_O M_vectoriel
##    req1    
##    req2
##    req3
##    ...
##    req11
##---------------------------------------------
##    AVG_PREC
##          ontologie AWN AWN_&_O M_vectoriel
##    req1    
##    req2
##    req3
##    ...
##    req11
##---------------------------------------------
##    DCGp
##          ontologie AWN AWN_&_O M_vectoriel
##    req1    
##    req2
##    req3
##    ...
##    req11
##---------------------------------------------
