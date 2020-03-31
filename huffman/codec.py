class Node:  # classe des feuilles
    def __init__(self, valeur, fg, fd=None):
        self.valeur = valeur  # le poids du noeud
        # dans ce cas, il n'y a pas d'enfant (c'est une feuille)
        if fd == None:
            self.name = fg  # l'attribut name regroupe les noms des enfants
            self.fg = None
            self.fd = None

        else:
            self.name = fg.name+fd.name
            self.fg = fg
            self.fd = fd

    def __repr__(self):
        return f'{self.valeur},{self.name}'


class TreeBuilder(Node):
    def __init__(self, text):
        self.text = text
        self.lst = list(self.text)
        self.l_feuille = []

    def occur(self):
        occur = {}  # on va stocker les lettres en clé et leur nombre d'apparition en valeur associée
        for i in self.lst:
            if i not in occur:  # si la lettre est pas présent, on l'ajoute au dico
                occur[i] = 1
            else:
                # si la lettre est déjà présente, on incrémente de 1 le nombre d'apparition
                occur[i] += 1
        # on crée une liste rangée par ordre croissant d'apparition
        letters = sorted(occur.items(), key=lambda t: t[1])
        return letters

    def tree(self):
        # liste contenant à chaque fois un doublet (lettre, nombre d'apparition)
        Letters = self.occur()
        # et classé par ordre croissant
        Tot_feuilles = []
        for i in Letters:
            # on crée les feuilles (tout en bas de l'arbre)s
            Tot_feuilles.append(Node(i[1], i[0]))

        # on va regrouper les feuilles en noeud, jusqu'à avoir un seul noeud
        while len(Tot_feuilles) > 1:
            # on prend les deux noeuds avec le moins d'apparition
            f1 = Tot_feuilles[0]
            f2 = Tot_feuilles[1]
            v = f1.valeur + f2.valeur  # le poids du noeud composé des deux noeuds

            new_noeud = Node(v, f1, f2)  # on crée notre nouveau noeud

            # on retire les deux anciens noeuds de la liste des noeuds à traiter
            del Tot_feuilles[1]
            del Tot_feuilles[0]
            j = 0
            # puis on va placer ce nouveau noeud pour en fonction de son poids
            while j < len(Tot_feuilles) and Tot_feuilles[j].valeur <= new_noeud.valeur:
                j += 1
            if j == 0:
                Tot_feuilles.append(new_noeud)
            else:
                Tot_feuilles.insert(j, new_noeud)
        return Tot_feuilles[0]  # on renvoie le noeud principal
        # à partir du ce noeud (appelé racine), on peut accéder à tout l'arbre


class Codec:
    def __init__(self, racine):
        self.racine = racine  # le noeud le plus haut
        self.dic = {}
        self.create()

    # on créer le dictionnaire de codage (lettre:code avec huffman)
    def create(self, noeud=None, code=""):
        # de manière recursive

        if noeud == None:  # on commence en haut de l'arbre
            noeud = self.racine

        if len(noeud.name) == 1:  # cas de base
            self.dic[noeud.name] = code
        else:
            code1 = code + "0"  # 0 si on va vers le fils de gauche
            code2 = code + "1"  # 1 si on va vers le fils de droite
            # recursivité jusqu'à atteindre une feuille
            return self.create(noeud.fg, code1), self.create(noeud.fd, code2)

    def encode(self, text):
        codage = str()
        for i in text:
            codage = codage + self.dic[i]  # on code chaque lettre
        return codage

    def decode(self, code):
        # pour décoder, on part de la racine et on descends, jusqu'à tomber sur une feuille
        decodage = str()
        i = 0
        while i < len(code):
            noeud = self.racine  # on repart de la racine
            while len(noeud.name) > 1:
                # on regarde si on doit aller à gauche ou à droite
                if code[i] == "0":
                    noeud = noeud.fg
                else:
                    noeud = noeud.fd
                i += 1
            decodage = decodage + noeud.name
        return decodage