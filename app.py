import json
import math
import webbrowser

#pip install plotly
#import pandas as pd
#import plotly.express as px

data = [
    30, 46, 71, 66, 34, 95, 50, 69, 31, 55, 42, 65, 75, 77, 32, 87, 75, 89, 31, 54,
    63, 95, 35, 86, 80, 47, 90, 82, 53, 58, 48, 66, 78, 78, 38, 82, 75, 31, 80, 79,
    48, 94, 77, 64, 38, 95, 46, 70, 30, 60, 50, 68, 34, 73, 98, 98, 33, 84, 98, 92,
    65, 44, 76, 96, 97, 37, 81, 85, 48, 61, 52, 47, 77, 50, 50, 49, 96, 97, 82, 49,
    33, 78, 70, 48, 96, 82, 40, 68, 34, 62, 54, 58, 54, 70, 35, 69, 98, 30, 88, 94,
    35, 51, 46, 92, 37, 38, 80, 54, 40, 39, 38, 54, 77, 62, 90, 39, 55, 50, 67, 31,
    68, 42, 48, 62, 40, 56, 94, 66, 39, 45, 33, 59, 78, 64, 50, 35, 45, 56, 69, 80,
    69, 39, 78, 65, 42, 55, 95, 78, 45, 56, 36, 58, 80, 68, 56, 36, 54, 65, 96, 76,
    74, 67, 93, 66, 44, 55, 82, 72, 54, 80, 94, 48, 34, 73, 61, 46, 76, 82, 64, 64,
    89, 89, 75, 66, 45, 59, 71, 89, 76, 74, 86, 56, 44, 91, 62, 75, 86, 81, 76, 65
]

sortedData = sorted(data)

#Encontrar valor maximo y minimo
def findXmax(data):
    xmax = data[0]
    for number in data:
        if number > xmax:
            xmax = number
    return xmax

def findXmin(data):
    xmin = data[0]
    for number in data:
        if number < xmin:
            xmin = number
    return xmin

#Calcular el número de clases
def findK(data):
    n = len(data)
    k = 1 + 3.3 * math.log10(n)
    return math.ceil(k)


#Calcular la amplitud
def findA(xmax, xmin, k):
    R = (xmax - xmin) + 1
    A = R / k
    return math.ceil(A)

#Construir intervalos de clase
def setIntervals(xmin, A, k):
    intervals = []
    limitI = xmin
    for _ in range(k):
        limitS = limitI + A
        intervals.append((limitI, limitS))
        limitI = limitS
    return intervals

#Contar
def countFrecuency(data, intervals):
    frecuency = [0] * len(intervals)
    for dataX in data:
        for i, (limitI, limitS) in enumerate(intervals):
            if limitI <= dataX < limitS:
                frecuency[i] += 1
                break
    return frecuency

#Calcular media aritmetica
def calcArithmeticMean(table):
    sumFixi = sum(item["fi.xi"] for item in table)
    n = len(data)
    arithmeticMean = sumFixi / n
    return arithmeticMean

#Calcular mediana
def calcMean(intervals, frecuency, n, A):
    acum = 0
    meanInterval = None
    
    for i, fi in enumerate(frecuency):
        acum += fi
        if acum >= n / 2:
            meanInterval = intervals[i]
            fiAnterior = acum - fi  # Frecuencia acumulada anterior
            Li = meanInterval[0]
            Med = Li + ((n / 2 - fiAnterior) / fi) * A
            return Med
    return None
    
#Calcular desviacion estandar y varianza
def calcVarianceAndStandarDeviation(table, n, x):
    sumFixi2 = sum(item["fi.xi^2"] for item in table)
    variance = (sumFixi2 / n) - math.pow(x, 2)
    
    standarDeviation = math.sqrt(variance)
    return variance, standarDeviation

#Calcular moda
def calcModal(intervals, frecuency, A):
    fiMax = max(frecuency)
    modals = []
    error = False

    for modalIndex, fi in enumerate(frecuency):
        if fi == fiMax:
            Li = intervals[modalIndex][0]
            
            fiAnterior = frecuency[modalIndex - 1] if modalIndex > 0 else 0
            #Si modalIndex > que 0, significa que existe una clase anterior, y por lo tanto asigna el valor
            #Si vale 0, significa que estamos en la primera clase y no hay clase anterior, por lo que se asigna 0
            
            fiSiguiente = frecuency[modalIndex + 1] if modalIndex < len(frecuency) - 1 else 0
            #Si modalIndex < que len(frecuency) - 1, significa que hay una clase que sigue y asigna el valor
            #Si vale lo mismo que len(frecuency) - 1, significa que estamos en la última clase y no hay clase siguiente, por lo que se asigna 0

            d1 = fi - fiAnterior
            d2 = fi - fiSiguiente
            
            if d1 == 0 and d2 == 0:
                modal = Li + A
                error = True
                errorString = "Excepción: clases cercanas a la moda tienen la misma frecuencia acumulada, por lo tanto, da una division entre cero.\nSe utiliza otra formula: (Li + A)"
                modals.append(modal)
            else:
                modal = Li + (d1 / (d1 + d2)) * A
                error = False
                errorString = ""
                modals.append(modal)            
    return modals, error, errorString

#Calcular percentil
def calcPercentil(intervals, frecuency, n, A, k):
    position = (n * k) / 100
    acum = 0
    percInterval = None
    
    for i, fi in enumerate(frecuency):
        acum += fi
        if acum >= position:
            percInterval = intervals[i]
            fiAnterior = acum - fi  #Frecuencia acumulada anterior
            Li = percInterval[0]
            Pk = Li + ((position - fiAnterior) / fi) * A
            return Pk
    return None

#Calcular cuartil
def calcQuartil(intervals, frecuency, n, A):
    Q1 = calcPercentil(intervals, frecuency, n, A, 25)
    Q2 = calcPercentil(intervals, frecuency, n, A, 50)
    Q3 = calcPercentil(intervals, frecuency, n, A, 75)
    Q4 = max(data)
    return Q1, Q2, Q3, Q4

#Calcular deciles
def calcDeciles(intervals, frecuency, n, A):
    deciles = []
    for j in range(1, 10):
        decil = calcPercentil(intervals, frecuency, n, A, j * 10)
        deciles.append((j, decil))
    return deciles

#Calcular curtosis
def calcKurtosis(P75, P25, P90, P10):
    kurtosis = ((P75 - P25) / (P90 - P10)) * 0.5
    if kurtosis > 0:
        typeK = "leptocurtica"
    elif kurtosis == 0:
        typeK = "mesocurtica"
    else:
        typeK = "platicurtica"
    return kurtosis, typeK

#Calcular indice de asimetria
def calcAsymmetryIndex(arithmeticMean, mean, standarDeviation):
    if standarDeviation == 0:
        return float('nan')  #Nao nao division entre 0
    asymmetryIndex = 3 * (arithmeticMean - mean) / standarDeviation
    if asymmetryIndex == 0:
        typeA = "simétrica"
    elif asymmetryIndex < 0:
        typeA = "sesgo a la izquierda"
    else:
        typeA = "sesgo a la derecha"
    return asymmetryIndex, typeA

#Calcular coeficiente de variacion
def calcCoefficientOfVariation(standarDeviation, arithmeticMean):
    if arithmeticMean == 0:
        return float('nan')  #Nao nao division entre 0
    cv = standarDeviation / arithmeticMean
    return cv

#Calcular rango intercuartil
def calcInterquartileRange(Q1, Q3):
    Ri = Q3 - Q1
    return Ri

#Graficar
def graphHistogram():
#    df = pd.DataFrame(data, columns=['value'])
#    fig = px.histogram(df, x='value', nbins=10, title="Histograma de frecuencias")
#    fig.update_xaxes(title='Valores')
#    fig.update_yaxes(title='Frecuencia')
    filename = "prueba.html"
#    fig.write_html("prueba.html")
    webbrowser.open_new_tab(filename)

#Tabla de frecuencia
def createTable(intervals, frecuency, n):
    table = []
    fa = 0
    for i, (limitI, limitS) in enumerate(intervals):
        fi = frecuency[i]
        fa += fi
        fsr = fi / n  #Frecuencia simple relativa
        far = fa / n  #Frecuencia acumulada relativa
        xi = (limitI + limitS) / 2  #Punto medio
        fixi = fi * xi
        xi2 = xi*xi
        fixi2 = fi * xi2  #Fi*xi^2
        percFsr = fsr * 100
        percFar = far * 100
        classT = {
            "Intervalo": f"[{limitI}, {limitS})",
            "Fi": frecuency[i],
            "Fa": fa,
            "Fsr": round(fsr, 4),
            "Far": round(far, 4),
            "xi": round(xi, 2),
            "fi.xi": round(fixi, 2),
            "fi.xi^2": round(fixi2, 2),
            "Fsr%": percFsr,
            "Far%": percFar
        }
        table.append(classT)
    return table

def printTable(tableF):
    print('-' * 115)
    print(f"{'Intervalo':<20}{'Fi':<10}{'Fa':<10}{'Fsr':<10}{'Far':<10}"
          f"{'xi':<10}{'fi.xi':<15}{'fi.xi^2':<15}{'Fsr%':<10}{'Far%':<10}")
    print('-' * 115)
    for fila in tableF:
        interval = fila['Intervalo']
        fi = fila['Fi']
        fa = fila['Fa']
        fsr = fila['Fsr']
        far = fila['Far']
        xi = fila['xi']
        fixi = fila['fi.xi']
        fixi2 = fila['fi.xi^2']
        percFsr = fsr * 100
        percFar = far * 100
        print(f"{interval:<20}{fi:<10}{fa:<10}{fsr:<10}{far:<10}"
              f"{xi:<10}{fixi:<15}{fixi2:<15}{round(percFsr, 2):<10}{round(percFar, 2):<10}")
    print('-' * 115)

def loadTable(name):
    with open(name, 'r') as jsonX:
        tableF = json.load(jsonX)
    return tableF

def saveTable(table, name):
    with open(name, 'w') as jsonX:
        json.dump(table, jsonX)

def menu():
    print("*" * 35)
    print("*   STATISTICS PROJECT Ver. 1.0   *")
    print("*" * 35)
    print("*             OPTIONS             *")
    print("*" * 35)
    print("1. Show frecuency table")
    print("2. Show arithmetic mean")
    print("3. Show mean")
    print("4. Show variance")
    print("5. Show standar deviation")
    print("6. Show modal")
    print("7. Show percentiles")
    print("8. Show quartiles")
    print("9. Show deciles")
    print("10. Show kurtosis")
    print("11. Show asymmetry index")
    print("12. Show coefficient of variation")
    print("13. Show interquartile range")
    print("14. Graph histogram")
    print("15. Exit")

def main():
    jsonName = 'frecuencyTable.json'
    n = len(data)
    xmax = findXmax(data)
    xmin = findXmin(data)
    k = findK(data)
    A = findA(xmax, xmin, k)
    intervals = setIntervals(xmin, A, k)
    frecuency = countFrecuency(data, intervals)
    tableF = createTable(intervals, frecuency, n)
    #jsonTable = json.dumps(tableF, indent=4)
    arithmeticMean = calcArithmeticMean(tableF)
    mean = calcMean(intervals, frecuency, n, A)
    variance, standarDeviation = calcVarianceAndStandarDeviation(tableF, n, arithmeticMean)
    modal, error, errorString = calcModal(intervals, frecuency, A)
    P90 = calcPercentil(intervals, frecuency, n, A, 90)
    P75 = calcPercentil(intervals, frecuency, n, A, 75)
    P60 = calcPercentil(intervals, frecuency, n, A, 60)
    P50 = calcPercentil(intervals, frecuency, n, A, 50)
    P25 = calcPercentil(intervals, frecuency, n, A, 25)
    P10 = calcPercentil(intervals, frecuency, n, A, 10)
    Q1, Q2, Q3, Q4 = calcQuartil(intervals, frecuency, n, A)
    kurtosis, typeK = calcKurtosis(P75, P25, P90, P10)
    asymmetryIndex, typeA = calcAsymmetryIndex(arithmeticMean, mean, standarDeviation)
    cv = calcCoefficientOfVariation(standarDeviation, arithmeticMean)
    Ri = calcInterquartileRange(Q1, Q3)
    deciles = calcDeciles(intervals, frecuency, n, A)

    while True:
        menu()
        print("*" * 35)
        option = input("Select an option: ")
        print("*" * 35)

        if option == '1':
            print("TABLA DE DISTRIBUICION DE FRECUENCIAS")
            print("*" * 35)
            saveTable(tableF, jsonName)
            #print(jsonTable)
            printTable(tableF)
            
        elif option == '2':
            print(f"Media Aritmética: {round(arithmeticMean, 2)}")

        elif option == '3':
            print(f"Mediana: {round(mean, 2)}")

        elif option == '4':
            print(f"Varianza: {round(variance, 2)}")

        elif option == '5':
            print(f"Desviación estándar: {round(standarDeviation, 2)}")

        elif option == '6':
            print(f"Modas: {modal}")
            if error == True:
                print(errorString)

        elif option == '7':
            print("PERCENTILES")
            print("*" * 35)
            print(f"P90: {round(P90, 2)}")
            print(f"P75: {round(P75, 2)}")
            print(f"P60: {round(P60, 2)}")
            print(f"P50: {round(P50, 2)}")
            print(f"P25: {round(P25, 2)}")
            print(f"P10: {round(P10, 2)}")

        elif option == '8':
            print("CUARTILES")
            print("*" * 35)
            print(f"Q1: {round(Q1, 2)}")
            print(f"Q2: {round(Q2, 2)}")
            print(f"Q3: {round(Q3, 2)}")
            print(f"Q4: {Q4}")

        elif option == '9':
            print("DECILES")
            for j, decil in deciles:
                print(f"D{j}: {round(decil, 2)}")

        elif option == '10':
            print(f"Curtosis: {round(kurtosis, 4)}")
            print(f"Tipo de curtosis: {typeK}")

        elif option == '11':
            print(f"Índice de Asimetría: {asymmetryIndex if not math.isnan(asymmetryIndex) else 'No calculable'}")
            print(f"Distribución: {typeA}")

        elif option == '12':
            print(f"Coeficiente de variación: {cv if not math.isnan(asymmetryIndex) else 'No calculable'}")

        elif option == '13':
            print(f"Rango intercuartil: {Ri}")

        elif option == '14':
            print(f"Grafica: ")
            graphHistogram()

        elif option == '15':
            print("Byebye")
            break

        else:
            print("Error. Choose another option and try again")

if __name__ == "__main__":
    main()
