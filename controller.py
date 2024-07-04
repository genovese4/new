import flet as ft
from model.modello import Model
from UI.view import View

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        # Popolare i menu a tendina all'avvio
        self.populate_year_dropdown()

        # Impostare i gestori di eventi
        self._view.btn_graph.on_click = self.handle_graph
        self._view.ddyear.on_change = self.handle_year_change
        self._view.btn_path.on_click = self.handle_path

    def populate_year_dropdown(self):
        try:
            years = self._model.get_years()
            self._view.ddyear.options = [ft.dropdown.Option(year) for year in years]
            self._view.update_page()
        except Exception as e:
            print(f"Errore nel popolamento del menu a tendina degli anni: {e}")
            self._view.create_alert("Errore nel popolamento degli anni")

    def handle_year_change(self, e):
        try:
            selected_year = self._view.ddyear.value
            shapes = self._model.get_shapes(selected_year)
            self._view.ddshape.options = [ft.dropdown.Option(shape) for shape in shapes]
            self._view.update_page()
        except Exception as e:
            print(f"Errore nel cambio dell'anno selezionato: {e}")
            self._view.create_alert("Errore nel cambio dell'anno selezionato")

    def handle_graph(self, e):
        try:
            selected_year = self._view.ddyear.value
            selected_shape = self._view.ddshape.value
            if not selected_year or not selected_shape:
                self._view.create_alert("Anno o forma non selezionati")
                return

            graph = self._model.create_graph(selected_year, selected_shape)
            if not graph:
                self._view.create_alert("Errore nella creazione del grafo")
                return

            top_5_edges = self._model.get_top_5_heaviest_edges(graph)
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Top 5 Archi di Peso Maggiore:"))
            for edge in top_5_edges:
                self._view.txt_result1.controls.append(ft.Text(f"Arco: {edge[0]} -> {edge[1]}, Peso: {edge[2]}"))
            self._view.update_page()
        except Exception as e:
            print(f"Errore nella gestione del grafo: {e}")
            self._view.create_alert("Errore nella gestione del grafo")

    def handle_path(self, e):
        try:
            selected_year = self._view.ddyear.value
            selected_shape = self._view.ddshape.value
            if not selected_year or not selected_shape:
                self._view.create_alert("Anno o forma non selezionati")
                return

            graph = self._model.create_graph(selected_year, selected_shape)
            if not graph:
                self._view.create_alert("Errore nella creazione del grafo")
                return

            max_score_path = self._model.find_max_score_path(graph)
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text("Cammino di Punteggio Massimo:"))
            for step in max_score_path:
                self._view.txt_result2.controls.append(ft.Text(f"Avvistamento: {step[0]}, Punteggio: {step[1]}"))
            self._view.update_page()
        except Exception as e:
            print(f"Errore nella gestione del cammino: {e}")
            self._view.create_alert("Errore nella gestione del cammino")
