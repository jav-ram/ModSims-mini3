import sys
import math
import random

INF = sys.maxsize


def generateTime(a):
    return - (1/a) * math.log(random.random())


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
    i = [0] * servers  # cliente que es servido por el i-esimo server
    T = [generateTime(a)]  # generar la primera llegada
    tA = T[0]  # la siguiente llegada
    tD = [INF] * servers  # el tiempo de la siguiente completacion del i-esimo server
    # ---------------------------------

    # Outputs
    # ---------------------------------
    A = []
    D = []

    while True:
        """ print(A)
        print(D)
        print(n) """
        # cases
        if tA == min([tA] + tD) and tA < Tn:  # if tA is the next event
            # print("First case")
            t = tA
            Na = Na + 1
            to = t + generateTime(a)
            T.append(to)
            tA = to

            A.append(t)
            if n == 0 and all(v == 0 for v in i):  # if it is the first event
                n = 1
                i[0] = Na
                Y = generateTime(a)
                tD[0] = t + Y
            # if there are less clients  than servers
            elif n <= servers:
                # find the empty server
                for index, server in enumerate(i):
                    if server == 0:  # is empty
                        n = n + 1
                        i[index] = Na
                        Y = generateTime(a)
                        tD[index] = t + Y
                        break
            # there is no space
            else:
                # add to wait
                n = n + 1
        for index, ti in enumerate(tD):
            if ti == min([tA] + tD) and ti < Tn:  # if ti is the next event
                # print("Second case")
                t = ti
                C[index] = C[index] + 1
                D.append(t)

                if n <= servers:
                    server2finish = tD.index(min(tD))
                    n = n - 1
                    i[server2finish] = 0
                    tD[index] = INF
                else:
                    m = max(i)
                    n = n - 1
                    i[index] = m + 1
                    Y = generateTime(a)
                    tD[index] = t + Y

        if min([tA] + tD) > Tn and n > 0:
            print("Third case")
            td = min(tD)
            nxt = tD.index(min(tD))  # id of i server to finish
            t = td
            n = n - 1
            C[nxt] = C[nxt] + 1
            if n > 0:
                Y = generateTime(a)
                tD[nxt] = t + Y
                D.append(t)

        elif min([tA] + tD) > Tn and n == 0:
            print("Fourth case")
            m = min(tD)
            t = m
            Tp = max(t - Tn, 0)
            return A, D, Tp, C, Na, t

A, D, Tp, C, Na, t = simulation(10, 100, 40)

print(len(A))
print(len(D))
print(sum(C))
print(Na)
print(t)
