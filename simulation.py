import sys
import math
import time
import random

INF = sys.maxsize


def generateTime(a):
    return - (1/a) * math.log(random.random())


def simulation(
    servers,  # numero de servers
    Tn,  # Tiempo final
    a,  # lambda for next arrival
    b,  # lambda for next finish
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
    A = []  # List of arrivals times
    Q = []  # List of when it enters server
    D = []  # List of departures times

    while True:
        """ print("entrada: ", len(A))
        print("salida: ", len(D))
        print("ejecución: ", len(list(filter(lambda x: x != 0, list(i)))))
        print("dentro", n)
        input() """
        # cases
        if tA == min([tA] + tD) and tA < Tn:  # if tA is the next event
            # print("First case")
            t = tA
            Na = Na + 1
            to = t + generateTime(a)
            T.append(to)
            tA = to
            A.append(t)
            # if there are less clients  than servers
            if n < servers:
                # find the empty server
                for index, server in enumerate(i):
                    if server == 0:  # is empty
                        Q.append(t)
                        n = n + 1
                        i[index] = Na
                        Y = generateTime(b)
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
                n = n - 1

                if n <= servers:
                    server2finish = tD.index(min(tD))
                    i[server2finish] = 0
                    tD[index] = INF
                elif n > servers:
                    Q.append(t)
                    m = max(i)
                    server2finish = tD.index(min(tD))
                    i[server2finish] = m + 1
                    Y = generateTime(b)
                    tD[index] = t + Y
            else:
                continue

        if min([tA] + tD) > Tn and n > 0:
            td = min(tD)
            nxt = tD.index(min(tD))  # id of i server to finish
            t = td
            n = n - 1
            C[nxt] = C[nxt] + 1
            i[nxt] = 0
            D.append(t)
            if n > servers:
                Q.append(t)
                Y = generateTime(b)
                i[nxt] = max(i) + 1
                tD[nxt] = t + Y

        elif min([tA] + tD) > Tn and n == 0:
            print("Fourth case")
            m = min(tD)
            t = m
            Tp = max(t - Tn, 0)
            return A, D, Tp, C, Q, Na, t

start = time.time()
A, D, Tp, C, Q, Na, t = simulation(10, 86400 / 100, 40, 5)
end = time.time()
print(len(A))
print(len(D))
print(sum(C))
print("Entro:" + str(len(Q)))
print(Na)
print(t)
print(end - start)
