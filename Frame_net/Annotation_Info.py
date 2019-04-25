class Annotation_Info:

    def __init__(self,lu_id,text):

        self.lu_id = lu_id
        self.text = text
        self.annotations_labels = []

    def set_text(self,text):
        self.text = text

    def add_annotation_label(self, annotation_label):
        self.annotations_labels.append(annotation_label)

class Annotation_Info_DB:

    def __init__(self,id,lu_id,text):
        self.id = id
        self.lu_id = lu_id
        self.text = text
        self.annotations_labels = []

    def set_text(self,text):
        self.text = text

    def add_annotation_label(self, annotation_label):
        self.annotations_labels.append(annotation_label)

    def get_annotation_labels(self):
        return self.annotations_labels

    def get_text(self):
        return self.text