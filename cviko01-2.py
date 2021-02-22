from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1

#toto riešenie nie je správne, pretože lockujem síce manipulovanie s inkrementáciou
#prvku poľa aj indexu, ale test na koniec poľa môžu vykonávať obe vlákna, keď na ne dojde rada,
#lebo shared v tej časti ešte nie je locknutý a dá sa k nemu pristúpiť. Tým pádom jedno vlákno
#môže vyhodnotiť podmienku ako nesplnenú, pričom druhé zatiaľ inkrementuje index a tým môže prísť
#k tomu, že sa dostaneme za hranicu poľa a preto podmienka nám túto výnimku pri paralelnom programovaní
#nemusí odchytiť. A presne to sa mi aj stávalo, takmer v každom volaní funkcie counter prišlo k out of range exception

#Dve ďalšie riešenia aj vaic k nim sú v druhom súbore

def counter(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.unlock()
        shared.array[shared.counter] += 1  
        shared.counter += 1
        shared.mutex.unlock()
  


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))
