from dao import DAO

class Model:
    def __init__(self):
        self.dao = DAO()

    def get_years(self):
        try:
            return self.dao.get_years_with_sightings()
        except Exception as e:
            print(f"Errore nel recupero degli anni: {e}")
            return []

    def get_shapes(self, year):
        try:
            return self.dao.get_shapes_for_year(year)
        except Exception as e:
            print(f"Errore nel recupero delle forme per l'anno {year}: {e}")
            return []

    def create_graph(self, year, shape):
        try:
            return self.dao.create_graph_for_year_and_shape(year, shape)
        except Exception as e:
            print(f"Errore nella creazione del grafo per l'anno {year} e la forma {shape}: {e}")
            return None

    def get_top_5_heaviest_edges(self, graph):
        try:
            return self.dao.get_top_5_heaviest_edges(graph)
        except Exception as e:
            print(f"Errore nel recupero dei 5 archi di peso maggiore: {e}")
            return []


    def find_max_score_path(self, graph):
        try:
            return self.dao.find_max_score_path(graph)
        except Exception as e:
            print(f"Errore nel trovare il cammino con punteggio massimo: {e}")
            return []
