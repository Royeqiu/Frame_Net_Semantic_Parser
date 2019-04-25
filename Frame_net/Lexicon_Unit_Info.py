class Lexicon_Unit_Info:

    def __init__(self, lu_id, semantic_frame_id, text, pos):
        self.lu_id = lu_id
        self.semantic_frame_id = semantic_frame_id
        self.text = text
        self.pos = pos

    def __eq__(self, other):
        if other.lu_id == self.lu_id:
            return True
        else:
            return False

    def __hash__(self):
        return self.lu_id.__hash__()
