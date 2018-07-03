class Store:

    def __init__(self):
        self.data = {}

    def register_new_state(self, uuid, state):
        self.data[uuid] = state

    def update_state(self, uuid, next_state):
        current_state = self.data[uuid]

        self.data[uuid] = {
            **current_state,
            **next_state
        }
