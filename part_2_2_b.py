import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np
import part_2_2.sw.HW_1_part_2_2_a as pa

def transform_set_ids(x):
    return list(map(int, x.replace("{","").replace("}", "").split(",")))

def merge_min_hashes(x,y):
    return list(np.minimum(x,y))

def estimate_union_size(x, min_hash_sketches):
    set_list = min_hash_sketches.loc[min_hash_sketches.Min_Hash_Sketch_INTEGER_Id.isin(x)]['Min_Hash_Sketch'].tolist()
    merged_min_hash = merge_min_hashes(set_list[0], set_list[1])
    if len(set_list) > 2:
        for i in range(2, len(set_list)):
            merged_min_hash = merge_min_hashes(merged_min_hash, set_list[i])
    return pa.estimate_size(merged_min_hash)


DATASET_PATH = "dataset"
OUTPUT_PATH = "part_2_2/output_data"
min_hash_sketches = pd.read_table("{}/part_2_2/HW_1_part_2_2_dataset__min_hash_sketches.tsv".format(DATASET_PATH))
min_hash_sketches['Min_Hash_Sketch'] = min_hash_sketches['Min_Hash_Sketch'].apply(pa.transform_to_list)
union_set_ids = pd.read_table("{}/part_2_2/HW_1_part_2_2_dataset__SETS_IDS_for_UNION.tsv".format(DATASET_PATH)) 
union_set_ids['list_set_ids'] = union_set_ids.set_of_sets_ids.apply(transform_set_ids)
union_set_ids['ESTIMATED_UNION_SIZE'] = union_set_ids['list_set_ids'].apply(lambda x: estimate_union_size(x, min_hash_sketches))
res = union_set_ids[['Union_Set_id', 'set_of_sets_ids', 'ESTIMATED_UNION_SIZE']]
res.to_csv("{}/OUTPUT_HW_1_part_2_2_b.csv".format(OUTPUT_PATH), index=False)
