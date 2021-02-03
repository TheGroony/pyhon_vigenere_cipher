import pymongo

abeceda = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Funkce, která zašifruje zprávy zadanou argumenty
def zasifruj(zprava, heslo):
    # Vytvoří z hesla list pro lepší práci
    zadaneHeslo = list(heslo)
    # Pokud se délka hesla neshoduje s délkou zprávy, heslo se upraví
    if len(zadaneHeslo) != len(zprava):
        # Cyklus, který do hesla přidá tolik znaků, kolik je potřeba, aby se shodovalo s textem
        for i in range(len(zprava) - len(zadaneHeslo)):
            # Za poslední znak se přidá další...
            zadaneHeslo.append(zadaneHeslo[i % len(zadaneHeslo)])
    # Zde se hotové heslo načte do proměnné
    hotoveHeslo = "".join(zadaneHeslo)
    sifra = []
    # Zde se přehodí písmena v abecedě a vytvoří se tak hotová šifra
    for i in range(len(zprava)):
        cisloZnaku = ((abeceda.index(zprava[i]) + abeceda.index(hotoveHeslo[i])) % 26)
        sifra.append(abeceda[cisloZnaku])
    hotovaSifra = "".join(sifra)
    puvodniZprava = desifruj(hotovaSifra, hotoveHeslo)
    print("Váš původní text: " + puvodniZprava)
    print("Vaše kompletní heslo: " + hotoveHeslo)
    print("Zašifrovaný text je: " + hotovaSifra)
    ulozDoDatabaze(zprava, heslo, hotovaSifra)

# Funkce, která uloží info o zprávě do MongoDB databáze
def desifruj(sifra, hotoveHeslo):
    zprava = []
    for i in range(len(sifra)):
        cisloZnaku = ((abeceda.index(sifra[i]) - abeceda.index(hotoveHeslo[i])) % 26)
        zprava.append(abeceda[cisloZnaku])
    puvodniZprava = "".join(zprava)
    return puvodniZprava


def ulozDoDatabaze(zprava, heslo, hotovaSifra):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   databaze = client["Šifry"]
   kolekce = databaze["vigenerova_sifra"]
   zaznam = {"zprava": zprava, "heslo": heslo, "zasifrovane": hotovaSifra}
   x = kolekce.insert_one(zaznam)
   print("\n\nVýpis z databáze:")
   vypis = kolekce.find_one({"zprava": zprava})
   print(vypis)

def main():
    print("Zadejte text, který chcete zašifrovat:")
    text = input()
    print("Zvolte si heslo pro zašifrování:")
    heslo = input()
    zasifruj(text, heslo)

main()