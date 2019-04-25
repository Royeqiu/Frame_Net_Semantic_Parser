import Semantic_Parser
predicted_lexicon_result, predicted_lexicon_id_result, predicted_semantic_frame_result, predicted_semantic_role_result = Semantic_Parser.get_result('Can you give me a box of wine')
for i,result in enumerate(predicted_semantic_role_result):
    print(predicted_lexicon_result[i])
    print(predicted_lexicon_id_result[i])
    print(predicted_semantic_frame_result[i])
    print(result)