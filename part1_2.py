import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np
import part_1_1.sw.part1_1 as p1

def rprecision_calc(gt, se_ls):
    means, mins, quartiles_1, medians, quartiles_3, maxs = [], [], [], [], [], []
    for res in [p1.rprecision_metrics(gt, se, 'all') for se in se_ls]:
        means.append(res['mean'])
        mins.append(res['min'])
        quartiles_1.append(res['quartile_1'])
        medians.append(res['median'])
        quartiles_3.append(res['quartile_3'])
        maxs.append(res['max'])
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 
            'Mean(R-precision_Distribution)': means}    
    rpress_df = pd.DataFrame(res, columns=res.keys())
    return rpress_df

def mrr_calc(gt, se_ls):
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 
            'MRR': [p1.mrr(gt, se) for se in se_ls]}
    mrr_df = pd.DataFrame(res, columns=res.keys())
    return mrr_df

def mpak_calc(gt, se_ls, k):
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 
            'Mean(P@{})'.format(str(k)): [p1.mpak(gt, se, k) for se in se_ls]}
    mpak_df = pd.DataFrame(res, columns=res.keys())
    return mpak_df

def mndcg_calc(gt, se_ls, k):
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 
            'Mean(nDCG@{})'.format(str(k)): [p1.mndcg(gt, se, k) for se in se_ls]}
    mndcg_df = pd.DataFrame(res, columns=res.keys())
    return mndcg_df

def calc_final_results(dataset="dataset"):
    gt_table = pd.read_table("{}/part_1_2/part_1_2__Ground_Truth.tsv".format(dataset))
    se1 = pd.read_table("{}/part_1_2/part_1_2__Results_SE_1.tsv".format(dataset))
    se2 = pd.read_table("{}/part_1_2/part_1_2__Results_SE_2.tsv".format(dataset))
    se3 = pd.read_table("{}/part_1_2/part_1_2__Results_SE_3.tsv".format(dataset))
    gt = gt_table.groupby('Query_id')['Relevant_Doc_id'].apply(lambda x: x.tolist()).tolist()
    se1_list = se1.groupby('Query_ID')['Doc_ID'].apply(lambda x: x.tolist()).tolist()
    se2_list = se2.groupby('Query_ID')['Doc_ID'].apply(lambda x: x.tolist()).tolist()
    se3_list = se3.groupby('Query_ID')['Doc_ID'].apply(lambda x: x.tolist()).tolist()
    se_ls = [se1_list, se2_list, se3_list]
    mpak_res = mpak_calc(gt, se_ls, 4)
    mndcg_res = mndcg_calc(gt, se_ls, 4)
    mrr_res = mrr_calc(gt, se_ls)
    rprecision_res = rprecision_calc(gt, se_ls)
    tmp1_res = pd.merge(mpak_res, mndcg_res, on="Search Engine")
    tmp2_res = pd.merge(mrr_res, rprecision_res, on="Search Engine")
    final_res = pd.merge(tmp1_res, tmp2_res, on="Search Engine")
    final_res.sort_values(['Mean(P@4)', "Mean(nDCG@4)", "MRR"], ascending=[False, False, False], inplace=True)
    return final_res

if __name__ == '__main__':
    DATASET_PATH = "dataset"
    OUTPUT_PATH = "part_1_2/output_data"
    final_res = calc_final_results(DATASET_PATH)
    final_res.to_csv("{}/scores.csv".format(OUTPUT_PATH), index=False)
    