
def pegardado2():
    import csv
    with open("../server/lista_csv.csv",encoding='utf-8') as f:
        reader = csv.reader(f)
        lista = list(reader)
    return lista
pegardado2()