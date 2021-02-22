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

#V tomto súbore su dve riešenia. Prvé je to, ako kód teraz funguje a druhé dostanem tak, že zakomentujem súčasný lock-unlock lockujúci celý while-cyklus a odkomentujem zakomentovaný (1 lock a na 2 miestach unlock)

#Pri prvom riešení prebehol chod programu bez chýb a výstup bol správny - samé jednotky. Bolo to súčasne aj najrýchlejším riešením so správnym výstupom, aké som objavil.
#Najrýchlejším je zrejme pre to, že k zamknutiu a odomknutiu zámku dochádza len raz pri každom zavolaní funkcie counter. Z pohľadu paralelného programovania si myslím, že nejde
#o najsprávnejšie riešenie, pretože druhé vlákno sa k úprave poľa dostane až po tom, čo ho celé spraví to prvé, ak som tomu pochopil správne. Pretože prvé si lockne shared na celý čas a
#unlockne až po dobehnutí celého while-u

#Druhé riešenie tiež vyhodilo zakaždým správny výstup a to samé jednotky. Trvalo však o trochu dlhšie, čo pripisujem tomu, že k locknutiu a unlocknutiu príde nie len raz pri zavolaní
#funkcie counter, ale v nej pri každom jednom opakovaní kódu vo while. Z pohľadu paralelného programovania si však myslím, že je to správnejšie riešenie, pretože ak vo while dôjde
#k zmene vlákien, môže sa tak stať akurát po unlocknutí shared a to druhé vlákno teda nemusí čakať, než vlastne dobehne celý while v prvom vlákne a môže pokračovať v práci ono

#Obe riešenia sú správne preto, že sa lockuje aj manipulovanie s indexom poľa, nie len pred zmenou hodnoty poľa, ako to bolo v riešení na prednáške. Tým pádom som zabezpečil
#to, že každý prvok bude zväčšený a index posunutý v rámci jedného vlákna a to druhé do toho porcesu nie je schopné zasiahnuť, kým prvý neukončí svoju procedúru pripočítania jednotky
#do poľa, aj posunutie indexu a neunlockne shared pre iné vláka. Rovanko ani prvé do toho nebude šiahať druhému a tým pádaom nevzniknú vynechané prvky, ani dva a viac krát inkrementované prvky

#Kód som použil Váš z prednášky a manipuloval len s umiestňovaním zámku a sledoval správanie programu, keďže ste nám to pri tomto prvom cviku povolili
#Tretie riešenie je v samostatnom subore a tam je aj popísané

def counter(shared):
    shared.mutex.lock()
    while True:
        #shared.mutex.lock()
        if shared.counter >= shared.end:
            #shared.mutex.unlock()
            break
        shared.array[shared.counter] += 1  
        shared.counter += 1
        #shared.mutex.unlock()
    shared.mutex.unlock()


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))
