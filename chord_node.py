
class ChordNode:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.predecessor = None
        self.successor = self  # Inicialmente, apunta a sí mismo

    def find_successor(self, id):
        """Encuentra el sucesor de un ID dado en el anillo"""
        # Caso base: Si el ID está en el rango entre el ID del nodo y su sucesor
        if self.id < id <= self.successor.id:
            return self.successor
        
        # Si el ID está fuera del rango del nodo actual, enviar al sucesor
        if self.id < id or id <= self.successor.id:
            return self.successor.find_successor(id)

        # Buscar en los nodos conocidos
        closest_node = self.find_closest_preceding_node(id)
        return closest_node.find_successor(id)

    def find_closest_preceding_node(self, id):
        """Encuentra el nodo más cercano que precede al ID dado"""
        # Itera sobre la lista de nodos conocidos para encontrar el nodo más cercano
        closest_node = self
        for node in self.nodes:
            if (self.id < node.id < id) or (self.id < node.id and id <= self.successor.id):
                closest_node = node
        return closest_node

    def notify(self, predecessor_id):
        """Actualiza el nodo predecesor"""
        # Lógica para manejar la notificación de predecesores.
        pass