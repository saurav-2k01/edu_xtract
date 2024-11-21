

class InvalidKeyIDError(Exception):
    pass

class Session:
    def __init__(self, key_id: str = None):
        self.key_id = key_id
        self.filepath = None
        self.output_filepath = None
        self.output_filename = None
        self.xtract = None


class Session_Manager:
    def __init__(self):
        self.sessions = dict()

    def create_session(self, key_id: str = None):
        if key_id is not None:
            session = Session(key_id)
            self.sessions[key_id] = session
            return session
        else:
            raise InvalidKeyIDError("Key_id cannot be None")

    def destroy_session(self, key_id: str = None):
        if key_id is not None:
            if key_id in self.sessions:
                del self.sessions[key_id]
            else:
                raise InvalidKeyIDError("key_id is not in session")
        else:
            raise InvalidKeyIDError("key_id cannot be None")

    def get_session(self, key_id: str = None):
        if key_id is not None and key_id in self.sessions:
            return self.sessions[key_id]
        else:
            raise InvalidKeyIDError(f"Session with key_id '{key_id}' does not exists.")


    def get_session_count(self):
        return len(self.sessions)



