import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_grafo(self,e):
        grafo = self._model.creaGrafo(float(self._view.txt_goal.value))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        self._view.update_page()

    def handle_top(self, e):
        battuti, vincitore=self._model.migliori()
        self._view.txt_result.controls.append(ft.Text(f"TOP PLAYER: {vincitore[0]} "))
        self._view.txt_result.controls.append(ft.Text(f"AVVERSARI BATTUTI:"))
        for giocatore in battuti:
            self._view.txt_result.controls.append(ft.Text(f"{giocatore[0]} | {giocatore[1]}"))
        self._view.update_page()

    def handle_dream(self, e):
        soluzione,peso=self._model.getBestPaht(int(self._view.txt_giocatori.value))
        self._view.txt_result.controls.append(ft.Text(f"Il dream team ha grado di titolarità pari a {peso} e include"))
        for giocatore in soluzione:
            self._view.txt_result.controls.append(ft.Text(f"{giocatore}"))
        self._view.update_page()
