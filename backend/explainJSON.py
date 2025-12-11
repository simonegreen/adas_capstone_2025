from featureMapping import explain_features
# from backend.featureMapping import explain_features
import asyncio
import json

res = asyncio.run(explain_features(['history', 'local_resp', 'resp_pkts']))
feat_dict = res.final_output.model_dump()
feat_json = json.dumps(feat_dict, indent=2)

with open("final_features_expl.json", "w", ) as file:
  json.dump(feat_dict, file, ensure_ascii=False, indent=4)

# print("dict type:", type(feat_dict))
# print("dict:", feat_dict)
# print("JSON type:", type(feat_json))
# print("JSON:", feat_json)
# print("list type:", type(feat_dict['features']))
# print("list only:", feat_dict['features'])
