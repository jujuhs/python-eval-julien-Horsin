class Node:
    def __init__(self,valeur, fg, fd=None):
        self.valeur = valeur
        if fd == None:
            self.name = fg
            self.fg = None
            self.fd = None

        else:
            self.name = fg.name+fd.name
            self.fg = fg
            self.fd = fd
    def __repr__(self):
        return f'{self.valeur},{self.name}'


class TreeBuilder:
    def __init__(self, text):
        self.text = text
        self.lst = list(self.text)
        self.l_feuille=[]
        
    def occur(self):
        occur={} # on va stocker les lettres en clé et leur nombre d'apparition en valeur associée
        for i in self.lst:
            if i not in occur: #si la lettre est pas présent, on l'ajoute au dico
                occur[i]=1
            else:
                occur[i]+=1 # si la lettre est déjà présente, on incrémente de 1 le nombre d'apparition
        letters = sorted(occur.items(), key=lambda t: t[1]) #on crée une liste rangée par ordre croissant d'apparition
        return letters


    def arbre(self):
        Letters = self.occur()
        Tot_feuilles = []
        for i in Letters:
            Tot_feuilles.append(Node(i[1],i[0]))
        while len(Tot_feuilles) > 1:
            f1 = Tot_feuilles[0]
            f2 = Tot_feuilles[1]
            v =f1.valeur + f2.valeur
            
            new_feuilles = Node(v, f1, f2)
            del Tot_feuilles[1]
            del Tot_feuilles[0]
            j=0
            while j<len(Tot_feuilles) and Tot_feuilles[j].valeur <= new_feuilles.valeur:
                    j+=1
            if j==0:
                Tot_feuilles.append(new_feuilles)
            else:
                Tot_feuilles.insert(j, new_feuilles)
        return Tot_feuilles[0]




   

class Codec:

 
    def __init__(self, racine):
        self.racine = racine
        self.dic={}

        
    def create(self, noeud=None,code=""):
        if noeud==None:
            noeud = self.racine

        if len(noeud.name)==1:
            self.dic[noeud.name]=code
        else:
            code1 = code +"0"
            code2 = code + "1"
            return self.create(noeud.fg,code1),self.create(noeud.fd,code2)

    def encode(self,text):
        codage =str()
        for i in text:
            codage = codage + self.dic[i]
        return codage
    def decode(self,code):
        decodage =str()
        i=0
        while i<len(code):
            noeud = self.racine
            while len(noeud.name) > 1:
                if code[i]=="0":
                    noeud = noeud.fg
                else:
                    noeud = noeud.fd
                i+=1
            decodage = decodage + noeud.name
        return decodage
            

            
        




text = "a dead dad ceded a bad babe a beaded abaca bed"
sol="1000011101001000110010011101100111001001000111110010011111011111100010001111110100111001001011111011101000111111001"

# on analyse les fréquences d'occurrence dans text
# pour fabriquer un arbre binaire
builder = TreeBuilder(text)
a= builder.arbre()
#print(a.fg.name)
#print(a.fd)
codec = Codec(a)
codec.create()
#print(codec.dic)
encoded = codec.encode(text)
print(encoded)
print(codec.decode(encoded))
