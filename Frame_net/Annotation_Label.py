class Annotation_Label:

    def __init__(self,text_id,start_offset,end_offset,semantic_role):
        self.text_id = text_id
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.semantic_role = semantic_role

    def get_annotation_label_obj(self):
        annotation_label_dict = dict()
        annotation_label_dict['name'] = self.semantic_role
        annotation_label_dict['start'] = self.start_offset
        annotation_label_dict['end'] =  self.end_offset
        return annotation_label_dict

