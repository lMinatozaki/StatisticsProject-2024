import json
import math

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

#Probar cuando todas las clases son iguales y probar cuando todas las clases dan 0

sortedData = sorted(data)

#Entonctrar valor maximo y minimo
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

    for modalIndex, fi in enumerate(frecuency):
        if fi == fiMax:
            Li = intervals[modalIndex][0]
            fiAnterior = frecuency[modalIndex - 1] if modalIndex > 0 else 0
            fiSiguiente = frecuency[modalIndex + 1] if modalIndex < len(frecuency) - 1 else 0

            d1 = fi - fiAnterior
            d2 = fi - fiSiguiente

            modal = Li + (d1 / (d1 + d2)) * A
            modals.append(modal)

    return modals

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
    return None

#Calcular curtosis
def calcKurtosis(P75, P25, P90, P10):
    kurtosis = ((P75 - P25) / (P90 - P10)) * 0.5
    return kurtosis

#Calcular indice de asimetria
def calcAsymmetryIndex(arithmeticMean, mean, standarDeviation):
    if standarDeviation == 0:
        return float('nan')  #Nao nao division entre 0
    asymmetryIndex = 3 * (arithmeticMean - mean) / standarDeviation
    return asymmetryIndex

#Tabla de frecuencia
#Mejorar presentación y acomodar tabla para que se vea mejor
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

def loadTable(name):
    with open(name, 'r') as jsonX:
        tableF = json.load(jsonX)
    return tableF

def saveTable(table, name):
    with open(name, 'w') as jsonX:
        json.dump(table, jsonX)

def menu():
    print("Options")
    print("1. Show frecuency table")
    print("2. Show arithmetic mean")
    print("3. Show mean")
    print("4. Show variance")
    print("5. Show standar deviation")
    print("6. Show modal")
    print("7. Show percentils")
    print("8. Show quartils")
    print("9. Show kurtosis")
    print("10. Show asymmetry index")
    print("11. Exit")

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
    jsonTable = json.dumps(tableF, indent=4)
    arithmeticMean = calcArithmeticMean(tableF)
    mean = calcMean(intervals, frecuency, n, A)
    variance, standarDeviation = calcVarianceAndStandarDeviation(tableF, n, arithmeticMean)
    modal = calcModal(intervals, frecuency, A)
    P90 = calcPercentil(intervals, frecuency, n, A, 90)
    P75 = calcPercentil(intervals, frecuency, n, A, 75)
    P60 = calcPercentil(intervals, frecuency, n, A, 60)
    P50 = calcPercentil(intervals, frecuency, n, A, 50)
    P25 = calcPercentil(intervals, frecuency, n, A, 25)
    P10 = calcPercentil(intervals, frecuency, n, A, 10)
    Q1, Q2, Q3, Q4 = calcQuartil(intervals, frecuency, n, A)
    kurtosis = calcKurtosis(P75, P25, P90, P10)
    asymmetryIndex = calcAsymmetryIndex(arithmeticMean, mean, standarDeviation)

    while True:
        menu()
        option = input("Select an option: ")
        print("**********************************************************")

        if option == '1':
            saveTable(tableF, jsonName)
            print(jsonTable)
            print("**********************************************************")

        elif option == '2':
            print(f"Media Aritmética: {round(arithmeticMean, 2)}")
            print("**********************************************************")

        elif option == '3':
            print(f"Mediana: {round(mean, 2)}")
            print("**********************************************************")

        elif option == '4':
            print(f"Varianza: {round(variance, 2)}")
            print("**********************************************************")

        elif option == '5':
            print(f"Desviación estándar: {round(standarDeviation, 2)}")
            print("**********************************************************")

        elif option == '6':
            print(f"Modas: {modal}")
            print("**********************************************************")

        elif option == '7':
            print(f"P90: {round(P90, 2)}")
            print(f"P75: {round(P75, 2)}")
            print(f"P60: {round(P60, 2)}")
            print(f"P50: {round(P50, 2)}")
            print(f"P25: {round(P25, 2)}")
            print(f"P10: {round(P10, 2)}")
            print("**********************************************************")

        elif option == '8':
            print(f"Q1: {round(Q1, 2)}")
            print(f"Q2: {round(Q2, 2)}")
            print(f"Q3: {round(Q3, 2)}")
            print(f"Q4: {Q4}")
            print("**********************************************************")

        elif option == '9':
            print(f"Curtosis: {round(kurtosis, 4)}")
            print("**********************************************************")

        elif option == '10':
            print(f"Índice de Asimetría: {asymmetryIndex if not math.isnan(asymmetryIndex) else 'No calculable'}")
            print("**********************************************************")

        elif option == '11':
            print("Byebye")
            break

        else:
            print("Error. Choose another option and try again")
            print("**********************************************************")

if __name__ == "__main__":
    main()