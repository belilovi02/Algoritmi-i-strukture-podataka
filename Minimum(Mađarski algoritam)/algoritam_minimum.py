import numpy as np

#----------------------------------------------------------------------------------------------------------------
# RED SA NAJMANJE NULA (0)

# Dva koraka:
# 1. Funkcija pronalazi red sa koji sadrži najmanje nula (0)
# 2. Funkcija izabere nultu vrijednost u redu, i označava elemenat (red i kolona) kao False
def minimalno_nula_red(nula_matrica, oznaka_nula):
    # Pronaći red
    min_red = [99999, 1]

    for broj_red in range(nula_matrica.shape[0]):
        if np.sum(nula_matrica[broj_red] == True) > 0 and min_red[0] > np.sum(nula_matrica[broj_red] == True):
            min_red = [np.sum(nula_matrica[broj_red] == True), broj_red]

    # Označiti odabrani red i kolonu kao False
    nula_index = np.where(nula_matrica[min_red[1]] == True)[0][0]
    oznaka_nula.append((min_red[1], nula_index))
    nula_matrica[min_red[1], :] = False
    nula_matrica[:, nula_index] = False

#----------------------------------------------------------------------------------------------------------------
# Pronalazi sve moguće vrijednosti koje funkcija može vratiti (return) za ovaj problem linearne dodjele
def oznaciti_matricu(matrica):

    # Nalazimo red sa najmanje 0 elemenata
    # Pretvara matricu u boolean matricu tako da je 0 = True, a bilo koja druga vrijednost je False
    trenutna_matrica = matrica
    nula_bool_matrica = (trenutna_matrica == 0)
    nula_bool_matrica_kopija = nula_bool_matrica.copy()

    # Bilježi sve moguće pozicije na kojima je rješenje koristeći oznacena_nula
    oznacena_nula = []
    while (True in nula_bool_matrica_kopija):
            minimalno_nula_red(nula_bool_matrica_kopija, oznacena_nula)

    # Odvojeno bilježi indekse redova i kolona
    oznacena_nula_red = []
    oznacena_nula_kolona = []
    for i in range(len(oznacena_nula)):
        oznacena_nula_red.append(oznacena_nula[i][0])
        oznacena_nula_kolona.append(oznacena_nula[i][1])

    # Redovi koji ne sadrže označene 0 elemente i sprema njihove indekse u neoznacen_red
    neoznacen_red = list(set(range(trenutna_matrica.shape[0])) - set(oznacena_nula_red)) 

    oznacene_kolone = []
    provjera_zamjena = True
    while provjera_zamjena:
        provjera_zamjena = False
        for i in range(len(neoznacen_red)):
            red_niz = nula_bool_matrica[neoznacen_red[i], :]
            for j in range(red_niz.shape[0]):
                # Pretraži element neoznacen_red te provjeri ima li neoznačenih 0 elemenata u odgovarajućoj koloni toga reda
                if red_niz[j] == True and j not in oznacene_kolone:
                    # Sprema indeks kolone u oznacene_kolone
                    oznacene_kolone.append(j)
                    provjera_zamjena = True

        for red_broj, kolona_broj in oznacena_nula:
            # Poredi indekse kolona koji su zabilježeni u oznacena_nula i oznacene_kolone
            if red_broj not in neoznacen_red and kolona_broj in oznacene_kolone:
                # Ako postoji kolona sa odgovarajućim indeskom, onda odgovarajući indeks reda se sprema u neoznacen_red
                neoznacen_red.append(red_broj)
                provjera_zamjena = True

    # Redovi sa indeksima koji nisu u neoznaceni_red se spremaju u oznaceni_redovi
    oznaceni_redovi = list(set(range(matrica.shape[0])) - set(neoznacen_red))

    return(oznacena_nula, oznaceni_redovi, oznacene_kolone)

#----------------------------------------------------------------------------------------------------------------
# Ovdje se matrica modifikuje
def namjestena_matrica(matrica, preci_redove, preci_kolone):
    trenutna_matrica = matrica
    nenulti_element = []

    # Pronalazi najmanji element koji nije u oznaceni_redovi i oznacene_kolone
    for red in range(len(trenutna_matrica)):
        if red not in preci_redove:
            for i in range(len(trenutna_matrica[red])):
                if i not in preci_kolone:
                    nenulti_element.append(trenutna_matrica[red][i])
    
    min_broj = min(nenulti_element)

    # Od vrijednosti elemenata iz prethodnog koraka koji nisu u oznaceni_redovi i oznacene_kolone oduzima se najmanji element koji je pronađen u prethodnom koraku
    # Npr. [4, 5, 8, (1), 7] - najmanji element je 1
    # Onda u ovom koraku izgleda ovako [3, 4, 7, 0, 6] jer je oduzeto 1 iz prošlog koraka
    for red in range(len(trenutna_matrica)):
        if red not in preci_redove:
            for i in range(len(trenutna_matrica[red])):
                if i not in preci_kolone:
                    trenutna_matrica[red, i] = trenutna_matrica[red, i] - min_broj

    # Dodati element koji se nalazi i u oznaceni_redovi i u oznacene_kolone u minimalnu vrijednost koraka prije prethodnog
    for red in range(len(preci_redove)):
        for kolona in range(len(preci_kolone)):
            trenutna_matrica[preci_redove[red], preci_kolone[kolona]] = trenutna_matrica[preci_redove[red], preci_kolone[kolona]] + min_broj

    return trenutna_matrica

#----------------------------------------------------------------------------------------------------------------
# Linearni algoritam
def madjarski_algoritam(matrica):
    dimenzija = matrica.shape[0]
    trenutna_matrica = matrica

    # Od svakog reda i kolone se oduzima njena najmanja vrijednost
    for red_broj in range(matrica.shape[0]):
        trenutna_matrica[red_broj] = trenutna_matrica[red_broj] - np.min(trenutna_matrica[red_broj])

    for kolona_broj in range(matrica.shape[1]):
        trenutna_matrica[:, kolona_broj] = trenutna_matrica[:, kolona_broj] - np.min(trenutna_matrica[:, kolona_broj])
    broj_nula = 0

    while broj_nula < dimenzija:
        pozicija_rjesenja, oznaceni_redovi, oznacene_kolone = oznaciti_matricu(trenutna_matrica)
        broj_nula = len(oznaceni_redovi) + len(oznacene_kolone)
        
        if broj_nula < dimenzija:
            trenutna_matrica = namjestena_matrica(trenutna_matrica, oznaceni_redovi, oznacene_kolone)

    return pozicija_rjesenja

#----------------------------------------------------------------------------------------------------------------
def izracun_odogovora(matrica, pozicija):
    total = 0
    matrica_rjesenje = np.zeros((matrica.shape[0], matrica.shape[1]))
    for i in range(len(pozicija)):
        total += matrica[pozicija[i][0], pozicija[i][1]]
        matrica_rjesenje[pozicija[i][0], pozicija[i][1]] = matrica[pozicija[i][0], pozicija[i][1]]

    return total, matrica_rjesenje

#----------------------------------------------------------------------------------------------------------------
# Pronađe sve najmanje elemente u matrici(redovi i kolone) te ih sabere
def main():

    #matrica_potrosnje = np.array([[7, 1, 8, 4, 6, 5, 2, 9, 3, 1],
     #                            [4, 5, 8, 10, 7, 6, 2, 1, 9, 3],
      #                           [5, 6, 8, 9, 5, 1, 7, 3, 10, 2],
       #                          [6, 8, 5, 4, 6, 10, 6, 4, 3, 2],
        #                         [9, 5, 6, 4, 7, 4, 13, 2, 8, 6],
         #                        [7, 1, 8, 4, 6, 5, 2, 9, 3, 10],
          #                       [6, 8, 5, 4, 6, 10, 6, 4, 3, 2],
           #                      [5, 6, 8, 9, 5, 1, 7, 3, 10, 2],
            #                     [4, 5, 8, 10, 7, 6, 2, 1, 9, 3],
             #                    [9, 5, 6, 4, 7, 14, 3, 2, 8, 6]])
    matrica_potrosnje = np.random.randint(low = 1, high = 9, size = (5,5))              
    x = '                              '
    y = '                             '

    print("********************************POČETNA MATRICA********************************\n")
    print(x , matrica_potrosnje[0])
    print(x , matrica_potrosnje[1])
    print(x , matrica_potrosnje[2])
    print(x , matrica_potrosnje[3])
    print(x , matrica_potrosnje[4], "\n")      


    pozicija_rjesenja = madjarski_algoritam(matrica_potrosnje.copy())
    rjesenje, matrica_rjesenje = izracun_odogovora(matrica_potrosnje, pozicija_rjesenja)

    print("********************************NOVA MATRICA********************************\n")
    #print(f"Najmanji mogući iznos je: {rjesenje:.0f}\n\nNova matrica izgleda ovako:\n{matrica_rjesenje}")

    print("                         ", "Najmanje moguće rjesenje:", rjesenje , y, "\n")

    print(y, matrica_rjesenje[0])
    print(y, matrica_rjesenje[1])
    print(y, matrica_rjesenje[2])
    print(y, matrica_rjesenje[3])
    print(y, matrica_rjesenje[4], "\n")

if __name__ == '__main__':
        main()
                




