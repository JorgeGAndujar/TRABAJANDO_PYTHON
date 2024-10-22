# IMPORTAR DENTRO DE LA PROPIA FUNCIÓN
def main():
    from modulo import cubo
    numero = int(input('Ingrese número?'))
    y = cubo(numero)
    print("Cubo: ", y)
main()