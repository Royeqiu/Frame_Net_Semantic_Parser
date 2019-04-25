class Frame_Info:

    def __init__(self, lu_id, semantic_frame_id, semantic_frame_name, pos,latent_id):
        self.lu_id = lu_id
        self.semantic_frame_id = semantic_frame_id
        self.semantic_frame_name = semantic_frame_name
        self.pos = pos

        self.latent_id = []
        for id in latent_id:
            self.latent_id.append(id)

    def __eq__(self, other):
        if other.semantic_frame_id == self.semantic_frame_id:
            return True
        else:
            return False

    def __hash__(self):
        return self.semantic_frame_id.__hash__()

    def get_content(self):
        return self.lu_id, self.semantic_frame_id, self.semantic_frame_name, self.pos

