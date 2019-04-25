from Frame_net import FrameNet_Data,Doc_Annotation
from NLP import NLP_Tool
nlp = NLP_Tool.NLP_Tool()
annotation = Doc_Annotation.Doc_Annotation()
frameNet= FrameNet_Data.FrameNet( load_ori_frame=False, load_ori_lu=False)
frameNet.load_lu('data/lu.txt')
frameNet.load_frame('data/frame.txt')
annotation.load_annotation()
one_semantic_frame_count = 0
no_annotation_count = 0
total = 0
for lexicon_count,key in enumerate(frameNet.lex_dic.keys()):
    total += 1
    if len(frameNet.lex_dic[key])==1:
        one_semantic_frame_count += 1
        continue
    for lu in frameNet.lex_dic[key]:
        annotation_id = lu['lu_id']
        if len(annotation.lu_annotation[annotation_id]['annotation']) == 0:
            no_annotation_count += 1
            continue
print(total)
print(one_semantic_frame_count)
print(no_annotation_count)