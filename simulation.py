import sys
import math
import time
import random
import numpy as np

INF = sys.maxsize


def get_min_servers(start, tests):
    for i in range(tests):
        print('With ', i + start, ' ant servers')
        A, D, Tp, C, Q, Na, t = simulation(i + start, 1440, 2400, 600)
        print(Na)
        print(A[-1], Q[-1], D[-1])
        print(A[0], Q[0], D[0])
        waiting = sum(np.subtract(Q, A))
        print('Waiting time: ', waiting)
        print('average waiting time: ', waiting / Na)


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
        elif min(tD) == min([tA] + tD) and min([tA] + tD) < Tn:  # if tD is the next event
            ti = min(tD)
            index = tD.index(min(tD))
            t = ti
            C[index] = C[index] + 1
            D.append(t)
            n = n - 1
            if n < servers:
                i[index] = 0
                tD[index] = INF
            else:
                Q.append(t)
                m = max(i)
                i[index] = m + 1
                Y = generateTime(b)
                tD[index] = t + Y

        elif min([tA] + tD) > Tn and n > 0:
            td = min(tD)
            nxt = tD.index(min(tD))  # id of i server to finish
            t = td
            n = n - 1
            C[nxt] = C[nxt] + 1
            D.append(t)
            if n > servers:
                Q.append(t)
                Y = generateTime(b)
                i[nxt] = max(i) + 1
                tD[nxt] = t + Y
            else:
                i[nxt] = 0
                tD[nxt] = INF

        elif min([tA] + tD) > Tn and n == 0:
            print("Fourth case")
            t = t + abs(t - D[-1])
            Tp = max(t - Tn, 0)
            return A, D, Tp, C, Q, Na, t, i

start = time.time()
A, D, Tp, C, Q, Na, t, i = simulation(10, 86400 / 100, 40, 5)
end = time.time()
print('time: ', t)
working = sum(np.subtract(D, Q)) / 10
idle = t - working
waiting = sum(np.subtract(Q, A))
print('Working time: ', working)
print('IDLE time: ', idle)
print('Waiting time: ', waiting)
print('average waiting time: ', waiting / Na)
print("Requests: " + str(len(Q)))

print(end - start)
# get_min_servers(4, 5)
print(i)
