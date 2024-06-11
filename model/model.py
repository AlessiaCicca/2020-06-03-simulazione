import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo=nx.DiGraph()
        self.nodi=[]
        self.giocatori=DAO.getGiocatori()
        self._idMap = {}
        self.dict={}
        self._solBest = []
        self._costBest = 0
        for v in self.giocatori:
            self._idMap[v.PlayerID] = v


    def creaGrafo(self,goal):
        self.nodi = DAO.getNodi(goal)
        self.grafo.add_nodes_from(self.nodi)
        self.addEdges()
        return self.grafo

    def addEdges(self):
         self.grafo.clear_edges()
         allEdges = DAO.getConnessioni()
         for connessione in allEdges:
             nodo1=self._idMap[connessione.g1]
             nodo2=self._idMap[connessione.g2]
             if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                 if (connessione.t1>connessione.t2):
                     if self.grafo.has_edge(nodo1, nodo2) == False:
                         peso=connessione.t1-connessione.t2
                         self.grafo.add_edge(nodo1, nodo2, weight=int(peso))
                 if (connessione.t2>connessione.t1):
                     if self.grafo.has_edge(nodo2,nodo1)==False:
                         peso=connessione.t2-connessione.t1
                         self.grafo.add_edge(nodo2, nodo1, weight=int(peso))



    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def migliori(self):
        dizionario={}
        lista=[]
        for nodo in self.grafo.nodes:
            dizionario[nodo]=self.grafo.out_degree(nodo)
        dizio=sorted(dizionario.items(), key=lambda item: item[1], reverse=True)
        for archi in self.grafo.out_edges(dizio[0][0]):
            lista.append((archi[1],self.grafo[archi[0]][archi[1]]["weight"]))
        listaOrdinata=sorted(lista,  key=lambda x: x[1], reverse=True)
        return listaOrdinata,dizio[0]

    def getBestPaht(self, numeroGiocatori):
        self._solBest = []
        self._costBest = 0
        parziale = []
        for v in self.grafo.nodes:
            parziale.append(v)
            self.ricorsione(parziale,numeroGiocatori)
            parziale.pop()
        return self._solBest, self._costBest

    def ricorsione(self, parziale,numeroGiocatori):
        # Controllo se parziale è una sol valida, ed in caso se è migliore del best
        if len(parziale)==numeroGiocatori:
            if self.gradoTitolarita(parziale) > self._costBest:
                self._costBest = self.gradoTitolarita(parziale)
                self._solBest = copy.deepcopy(parziale)
            return

        for v,_ in self.grafo.in_edges(parziale[-1]):
            #Qui u è il nodo precedente collegato al nodo corrente parziale[-1].
             if v not in parziale:
                    parziale.append(v)
                    self.ricorsione(parziale, numeroGiocatori)
                    parziale.pop()

    def gradoTitolarita(self, parziale):
        peso = 0
        for nodo in parziale:
            vittorie = self.grafo.out_degree(nodo)
            perdite = self.grafo.in_degree(nodo)
            peso += vittorie - perdite
        return peso
