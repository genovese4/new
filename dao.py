from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting
import networkx as nx
import mysql.connector

class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        try:
            cnx = DBConnect.get_connection()
            if cnx is None:
                print("Connessione fallita")
                return []

            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * FROM state s"""
            cursor.execute(query)

            result = [State(row["id"], row["Name"], row["Capital"], row["Lat"], row["Lng"], row["Area"], row["Population"], row["Neighbors"]) for row in cursor]

            cursor.close()
            cnx.close()
            return result

        except mysql.connector.Error as err:
            print(f"Errore di connessione al database: {err}")
            return []

    @staticmethod
    def get_all_sightings():
        try:
            cnx = DBConnect.get_connection()
            if cnx is None:
                print("Connessione fallita")
                return []

            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * FROM sighting s ORDER BY `datetime` ASC"""
            cursor.execute(query)

            result = [Sighting(**row) for row in cursor]

            cursor.close()
            cnx.close()
            return result

        except mysql.connector.Error as err:
            print(f"Errore di connessione al database: {err}")
            return []

    @staticmethod
    def get_years_with_sightings():
        try:
            cnx = DBConnect.get_connection()
            if cnx is None:
                print("Connessione fallita")
                return []

            cursor = cnx.cursor()
            query = """SELECT DISTINCT YEAR(`datetime`) as year FROM sighting ORDER BY year DESC"""
            cursor.execute(query)

            result = [row["year"] for row in cursor]

            cursor.close()
            cnx.close()
            return result

        except mysql.connector.Error as err:
            print(f"Errore di connessione al database: {err}")
            return []

    @staticmethod
    def get_shapes_for_year(year):
        try:
            if not isinstance(year, int):
                raise ValueError("L'anno deve essere un intero.")

            cnx = DBConnect.get_connection()
            if cnx is None:
                print("Connessione fallita")
                return []

            cursor = cnx.cursor()
            query = """SELECT DISTINCT shape FROM sighting WHERE YEAR(`datetime`) = %s AND shape IS NOT NULL AND shape != '' ORDER BY shape ASC"""
            cursor.execute(query, (year,))

            result = [row["shape"] for row in cursor]

            cursor.close()
            cnx.close()
            return result

        except mysql.connector.Error as err:
            print(f"Errore di connessione al database: {err}")
            return []
        except ValueError as val_err:
            print(f"Errore di validazione: {val_err}")
            return []

    @staticmethod
    def create_graph_for_year_and_shape(year, shape):
        try:
            if not isinstance(year, int):
                raise ValueError("L'anno deve essere un intero.")
            if not isinstance(shape, str):
                raise ValueError("La forma deve essere una stringa.")

            cnx = DBConnect.get_connection()
            if cnx is None:
                print("Connessione fallita")
                return None

            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * FROM sighting WHERE YEAR(`datetime`) = %s AND shape = %s"""
            cursor.execute(query, (year, shape))

            sightings = [Sighting(**row) for row in cursor]

            cursor.close()
            cnx.close()

            graph = nx.DiGraph()

            for sighting in sightings:
                graph.add_node(sighting.id, state=sighting.state, lat=sighting.latitude, lng=sighting.longitude)

            for i in range(len(sightings)):
                for j in range(i + 1, len(sightings)):
                    if sightings[i].state == sightings[j].state:
                        if sightings[i].longitude < sightings[j].longitude:
                            weight = sightings[j].longitude - sightings[i].longitude
                            graph.add_edge(sightings[i].id, sightings[j].id, weight=weight)
                        elif sightings[i].longitude > sightings[j].longitude:
                            weight = sightings[i].longitude - sightings[j].longitude
                            graph.add_edge(sightings[j].id, sightings[i].id, weight=weight)

            return graph

        except mysql.connector.Error as err:
            print(f"Errore di connessione al database: {err}")
            return None
        except ValueError as val_err:
            print(f"Errore di validazione: {val_err}")
            return None

    @staticmethod
    def get_top_5_heaviest_edges(graph):
        try:
            if not isinstance(graph, nx.DiGraph):
                raise ValueError("L'oggetto fornito non è un grafo orientato.")

            edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:5]
            return [(edge[0], edge[1], edge[2]['weight']) for edge in edges]

        except ValueError as val_err:
            print(f"Errore di validazione: {val_err}")
            return []
        except Exception as e:
            print(f"Errore sconosciuto: {e}")
            return []

@staticmethod
def find_max_score_path(graph):
        try:
            if not isinstance(graph, nx.DiGraph):
                raise ValueError("L'oggetto fornito non è un grafo orientato.")

            def datetime_to_month(dt):
                return dt.month

            paths = {}
            max_score_path = []
            max_score = 0

            nodes = list(graph.nodes(data=True))
            for node_id, data in nodes:
                paths[node_id] = [(node_id, 100)]  # Each node starts with its own score

            for node_id in nx.topological_sort(graph):
                current_path = paths[node_id]
                current_score = sum([score for _, score in current_path])

                for successor in graph.successors(node_id):
                    edge_weight = graph[node_id][successor]['weight']
                    successor_data = graph.nodes[successor]
                    successor_month = datetime_to_month(successor_data['datetime'])
                    last_month = datetime_to_month(graph.nodes[current_path[-1][0]]['datetime'])
                    month_count = sum(1 for _, _, month in current_path if month == successor_month)

                    if month_count < 3 and (successor_month != last_month or len(current_path) == 1):
                        new_score = current_score + 100 + (200 if successor_month == last_month else 0)
                        new_path = current_path + [(successor, new_score)]

                        if new_score > sum([score for _, score in paths[successor]]):
                            paths[successor] = new_path

                            if new_score > max_score:
                                max_score = new_score
                                max_score_path = new_path

            return max_score_path

        except ValueError as val_err:
            print(f"Errore di validazione: {val_err}")
            return []
        except Exception as e:
            print(f"Errore sconosciuto: {e}")
            return []
