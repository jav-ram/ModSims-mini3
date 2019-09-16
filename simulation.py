import sys
import math
import random

INF = sys.maxsize


def generateTime(a, s):
    return s - (1/a) * math.log(random.random())


def simulation(
    servers,  # numero de servers
    Tn,  # Tiempo final
    a  # lambda to generate times
):
    # State
    # ---------------------------------
    t = 0  # tiempo actual
    Na = 0  # Numero de llegadas al sistema
    C = [0] * servers  # Clientes servidos por el i-esimo server
    n = 0  # clientes en el sistema
    i = [INF] * servers  # cliente que es servido por el i-esimo server
    T = [generateTime(a, t)]  # generar la primera llegada
    tA = T[0]  # la siguiente llegada
    tD = [INF] * servers  # el tiempo de la siguiente completacion del i-esimo server
    # ---------------------------------

    # Outputs
    # ---------------------------------
    A = {}
    D = {}

    while True:
        # cases
        if tA == min([tA] + tD):  # if tA is the next event
            t = tA
            Na = Na + 1
            T.append(generateTime(a, t))
            tA = T[-1]
            A[Na] = t
            if n == 0 and all(v == 0 for v in i):  # if it is the first event
                n = 1
                i[0] = Na
                Y = generateTime(a, t)
                tD[0] = t + Y
            # if there are less clients  than servers
            if n < servers:
                # find the empty server
                for index, server in enumerate(i):
                    if server == 0:  # is empty
                        n = n + 1
                        i[index] = Na
                        Y = generateTime(a, t)
                        tD[index] = t + Y
                        break
            # there is no space
            else:
                # add to wait
                n = n + 1
        else:
            for index, ti in enumerate(tD):
                if t == min([tA] + tD):  # if ti is the next event
                    t = ti
                    C[index] = C[index] + 1
                    D[index] = t
                    if n <= servers:  # if there are less clients on sistem than servers
                        for j, server in enumerate(i):
                            if n == j:
                                n = n - 1
                                i[j] = 0
                                tD[index] = INF
                                break
                    else:
                        m = max(i)
                        n = n - 1
                        i[index] = m + 1
                        Y = generateTime(t)
                        tD = y + Y





                    
