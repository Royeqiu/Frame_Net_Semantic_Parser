from utl import Feature_Extractor
fe = Feature_Extractor.Feature_Extractor()
extract_functions = [fe.get_tokens_tag,fe.get_tokens_dep]
function_len = len(extract_functions)

nlp = None

def get_frame_feature_lists(tokens):
    data_lists = []
    for function in extract_functions:
        data_lists.append(function(tokens))
    return data_lists