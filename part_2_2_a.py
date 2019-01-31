import pandas as pd
import numpy as np

def transform_to_list(x):
    return list(map(int, x.replace("[","").replace("]", "").split(",")))

def estimate_size(x):
    min_hash_size = len(x)
    zero_counts = min_hash_size-np.count_nonzero(x)
    jc = zero_counts/min_hash_size
    est_size = int(jc*1123581321)
    return est_size

DATASET_PATH = "dataset"
OUTPUT_PATH = "part_2_2/output_data"
data = pd.read_table("{}/part_2_2/HW_1_part_2_2_dataset__min_hash_sketches.tsv".format(DATASET_PATH))
data['Min_Hash_Sketch'] = data['Min_Hash_Sketch'].apply(transform_to_list)
data['ESTIMATED_ORIGINAL_SET_SIZE'] = data['Min_Hash_Sketch'].apply(estimate_size)
res = data[['Min_Hash_Sketch_INTEGER_Id', 'ESTIMATED_ORIGINAL_SET_SIZE']]
res.to_csv("{}/OUTPUT_HW_1_part_2_2_a.csv".format(OUTPUT_PATH), index=False)