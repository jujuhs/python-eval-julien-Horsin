from colorama import init, Fore, Style
import numpy as np
from itertools import product
import string

init(convert=True)  # permet de mettre en marche le module colorama


class Ruler:
    def choix_mat(self, S):  # permet de définir la matrice dans le cas simple
        # où toutes les substitutions ont le même cout
        if S == "":
            M = np.zeros(shape=(26, 26))
            for i, j in product(range(25), range(25)):
                if i != j:
                    M[i][j] = 1
            return M
        else:  # si on veut définir une autre matrice pour les coûts
            return S

    def __init__(self, str1, str2, d=1, S="", remplacement_cost=1, insert_cost=1):
        self.str1 = str1  # chaîne 1
        self.str2 = str2  # chaîne 2
        self.str_mod1 = None  # chaîne 1 modifiée pour être alignée avec la 2
        self.str_mod2 = None  # chaîne 2 modifiée pour être alignée avec la 1
        self.n = len(self.str1)  # longeur de la première chaîne de caractère
        self.m = len(self.str2)
        self.distance = None  # distance entre les deux chaînes de caractères
        # coût unitaire d'un non alignement lors du calcul de la distance(on peut paramétrer cet aspect)
        self.d = d
        # on définit la valeur de la distance liée à un remplacement
        self.remplacement_cost = remplacement_cost
        # (on peut paramétrer cet aspect)
        # on définit la distance liée à un gap (on peut paramétrer cet aspect)
        self.insert_cost = insert_cost
        # on définit la matrice des coûts de substitution entre les lettres
        self.mat = self.choix_mat(S)

    def red_text(self, text):
        # fonction pour mettre une chaîne de caractère en rouge
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    def report(self):
        # fonction pour retourner les 2 chaînes modifiées
        return self.str_mod1, self.str_mod2

    # cette méthode renvoie les couts liés à la subsitution des lettres 'x' et 'y'
    def cout_sub(self, x, y):
        # liste de longeur 26 avec les lettres de l'alphabet
        L = list(string.ascii_lowercase)
        lettre_1 = x.lower()
        lettre_2 = y.lower()
        i = L.index(lettre_1)
        j = L.index(lettre_2)
        return self.mat[i][j]  # on renvoit le cout associé à la substition

    def compute(self):  # on va calculer la distance entre les deux chaînes de caractères
        # C est la matrice "des scores" de chaque opération
        C = np.empty(shape=(self.n + 1, self.m + 1))
        # D est la matrice qui note au fur et à mesure
        D = np.zeros(shape=(self.n + 1, self.m + 1))
        # et qu'il faudra remonter pour trouver l'alignement optimal

        C[0][0] = 0  # le cout en haut à gauche est nul
        # dans la matrice D, on associe la valeur 3 à la case en haut à gauche (l'arrêt)
        D[0][0] = 3
        # on associe la valeur 0 quand on vient de la case en diagonale juste avant
        # on associe la valeur 1 quand on vient de la case juste au dessus
        # on associe la valeur 2 quand on vient de la case à gauche

        for i in range(1, self.n + 1):  # coûts et déplacements associés sur la première ligne
            C[i][0] = (i*self.d)
            D[i][0] = 2

        for j in range(1, self.m + 1):  # coûts et déplacements associés sur la première colonne
            C[0][j] = (j*self.d)
            D[0][j] = 1

        # on calcule les coûts pour toutes les cases
        for (i, j) in product(range(1, self.n+1), range(1, self.m+1)):
            cost = [C[i-1][j-1] + self.cout_sub(self.str1[i-1], self.str2[j-1]),
                    C[i][j-1] + self.d,
                    C[i-1][j] + self.d]
            m = min(cost)
            C[i][j] = min(cost)
            # ici, on met 0,1 ou 2 dans la case (i,j) de D, en fonction
            D[i][j] = cost.index(m)
            # de l'opération la moins couteuse

        # ici, on va partir du coin en bas à droite de D
        x, y = (self.n, self.m)
        # et on va remonter les cases jusqu'en au à gauche (la case de valeur 3)
        # en prenant le chemin optimal

        etat = D[x][y]
        new1 = []
        new2 = []
        self.distance = 0
        while etat != 3:  # le critère d'arrêt en haut à gauche

            if etat == 0:  # on test les valeurs pour savoir si on doit remonter en diagonale
                if self.str2[y-1] != self.str1[x-1]:
                    self.distance += self.remplacement_cost
                    # on met un "=" en rouge quand on met un gap
                    new1 = [self.red_text(self.str1[x-1])]+new1
                    new2 = [self.red_text(self.str2[y-1])]+new2
                else:
                    new1 = [self.str1[x-1]]+new1
                    new2 = [self.str2[y-1]]+new2
                x, y = (x-1, y-1)

            elif etat == 1:  # on test les valeurs pour savoir si on doit remonter à la verticale
                new1 = [self.red_text("=")]+new1
                new2 = [self.str2[y-1]]+new2
                x, y = (x, y-1)
                self.distance += self.insert_cost
            else:  # on test les valeurs pour savoir si on doit remonter à l'horizontale
                new2 = [self.red_text("=")]+new2
                new1 = [self.str1[x-1]]+new1
                x, y = (x-1, y)
                self.distance += self.insert_cost
            etat = D[x][y]

        # on met les mots dans les attributs str_mod1 et str_mod2
        self.str_mod1 = "".join(new1)
        self.str_mod2 = "".join(new2)