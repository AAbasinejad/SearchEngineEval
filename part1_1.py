import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np

def pak(ground_truth, predicted, k):
    '''
    Calculates the precision at K between two lists
    
    Parameters
    ----------
    ground_truth : list of ints
        List of ids to be predicted (order does not matter)
    predicted : list of ints
        List of predicted ids (order does matter)
    k : int
        Rank threshold to calculate the precision at.
        
    Returns
    ----------
    pak : double
        Precision at K give the ground truth and the predicted results
    '''
    predicted_at_k = set(predicted[:k])
    inter = predicted_at_k.intersection(set(ground_truth))
    pak = len(inter)/k
    return pak

def mpak(ground_truth, predicted, k):
    '''
    Calculates the mean of precision at K between two lists of lists
    
    Parameters
    ----------
    ground_truth : list of list of ints
        List of list of ids to be predicted (order does not matter)
    predicted : list of list of ints
        List of list of predicted ids (order does matter)
    k : int
        Rank threshold to calculate the precision at.
        
    Returns
    ----------
    mpak : double
        Mean precision at K given the ground truth and the predicted results
    '''
    mapk = np.mean([pak(gt, p, k) for gt, p in zip(ground_truth, predicted)])
    return mapk

def rprecision(ground_truth, predicted):
    '''
    Calculates the R precision between two lists
    
    Parameters
    ----------
    ground_truth : list of ints
        List of ids to be predicted (order does not matter)
    predicted : list of ints
        List of predicted ids (order does matter)
        
    Returns
    ----------
    rprecision : double
        rprecision given the ground truth and the predicted results
    '''
    k = len(ground_truth)
    rprecision = pak(ground_truth, predicted, k)
    return rprecision

def rprecision_metrics(ground_truth, predicted, metric="all"):
    '''
    Calculates the metrics for the R precision between two lists
    
    Parameters
    ----------
    ground_truth : list of list of ints
        List of list of ids to be predicted (order does not matter)
    predicted : list of lifst ints
        List of list of predicted ids (order does matter)
    metric : str
        The metric to be calculated, it should be one among 
            ('mean', 'min', 'max', 'quartile_1', 'median', 'quartile_3', 'max', 'all')
        
    Returns
    ----------
    score : double or dict
        The result of calculating the specified metric using the rprecision score
        If metric == 'all' it returns a dictionary with the key being the metric and the
            value the score for the specific metric
    '''
    def quartile_1(x):
        return(np.percentile(x, 25))
    def quartile_3(x):
        return(np.percentile(x, 75))
    
    dist = [rprecision(gt, p) for gt, p in zip(ground_truth, predicted)]
    dispatcher = {
        'mean': np.mean,
        'min': np.min,
        'max': np.max,
        'median': np.median,
        'quartile_1': quartile_1,
        'quartile_3': quartile_3
    }
    if metric == 'all':
        score = {
            'mean': dispatcher['mean'](dist),
            'min': dispatcher['min'](dist),
            'max': dispatcher['max'](dist),
            'median': dispatcher['median'](dist),
            'quartile_1': dispatcher['quartile_1'](dist),
            'quartile_3': dispatcher['quartile_3'](dist)
        }
    else:
        score = dispatcher[metric](dist)
    return score



def mrr(ground_truth, predicted):
    '''
    Calculates the mean reciprocal rank between a ground_truth and a predicted result
    
    Parameters
    ----------
    ground_truth : list of list of ints
        List of list of ids to be predicted (order does not matter)
    predicted : list of list of ints
        List of list of predicted ids (order does matter)
        
    Returns
    ----------
    mrr : double
        Mean reciprocal rank between the predicted results and the ground truth
    '''
    mrr = np.mean([next((1/(i+1) for i in range(len(p)) if p[i] in gt), 0) \
                   for gt, p in zip(ground_truth, predicted)])
    return mrr

def dcg_k(relevances, k):
    
    '''
    Calculates the discounted cumulative gain for a list of ranked relevances at rank k
    
    Parameters
    ----------
    relevances : list of ints
        List of relevances (order does matter)
    k : int
        Rank threshold to calculate the dcg at.
        
    Returns
    ----------
    dcg : double
        The dcg for the given ranked relevances
    '''
    rels = relevances[:k]
    dcg = rels[0] + sum([rels[i]/np.log2(i+1) for i in range(1,len(rels))])
    return dcg


def ndcg(ground_truth, predicted, k):
    '''
    Calculates the normalized discounted cumulative gain between a ground thuth and a predicted result
    at rank k
    
    Parameters
    ----------
    ground_truth : list of ints
        List of ids to be predicted (order does not matter)
    predicted : list of ints
        List of predicted ids (order does matter)
    k : int
        Rank threshold to calculate the ndcg at.
        
    Returns
    ----------
    ndcg : double
        The ndcg between two lists
    '''
    relevances = [1 if p in ground_truth else 0 for p in predicted]
    dcg_q = dcg_k(relevances, k)
    idcg = dcg_k(sorted(relevances, reverse=True), k)
    ndcg = 0 if idcg == 0 else dcg_q/idcg
    return ndcg


def mndcg(ground_truth, predicted, k):
    '''
    Calculates the mean of ndcg between two lists of lists
    
    Parameters
    ----------
    ground_truth : list of list of ints
        List of list of ids to be predicted (order does not matter)
    predicted : list of list of ints
        List of list of predicted ids (order does matter)
    k : int
        Rank threshold to calculate the ndcg at.
        
    Returns
    ----------
    mndcg : double
        Mean ndcg at K given the ground truth and the predicted results
    '''
    mndcg = np.mean([ndcg(gt, p, k) for gt, p in zip(ground_truth, predicted)])
    return mndcg

def create_mpak(gt, se_ls, save=True, output="output"):
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 
            'Mean(P@1)': [mpak(gt, se, 1) for se in se_ls],
            'Mean(P@3)': [mpak(gt, se, 3) for se in se_ls], 
            'Mean(P@5)': [mpak(gt, se, 5) for se in se_ls], 
            'Mean(P@10)': [mpak(gt, se, 10) for se in se_ls]}
    pak_df = pd.DataFrame(res, columns=res.keys())
    if save:
        pak_df.to_csv("{}/p_at_k.csv".format(output), index=False)
    else:
        return pak_df

def create_rprecision(gt, se_ls, save=True, output="output"):
    means, mins, quartiles_1, medians, quartiles_3, maxs = [], [], [], [], [], []
    for res in [rprecision_metrics(gt, se, 'all') for se in se_ls]:
        means.append(res['mean'])
        mins.append(res['min'])
        quartiles_1.append(res['quartile_1'])
        medians.append(res['median'])
        quartiles_3.append(res['quartile_3'])
        maxs.append(res['max'])
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 
            '1': [ '%.3f' % m for m in means ],
            '2': [ '%.3f' % m for m in mins ], 
            '3': [ '%.3f' % q for q in quartiles_1 ],
            '4': [ '%.3f' % m for m in medians ],
            '5': [ '%.3f' % q for q in quartiles_3 ],
            '6': [ '%.3f' % m for m in maxs ]}
    rpress_df = pd.DataFrame(res, columns=res.keys())
    if save:
        rpress_df.to_csv("{}/R-Precision.csv".format(output), index=False)
    else:
        return rpress_df
    
def create_mrr(gt, se_ls, save=True, output="output"):
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 'MRR': [mrr(gt, se) for se in se_ls]}
    mrr_df = pd.DataFrame(res, columns=res.keys())
    if save:
        mrr_df.to_csv("{}/MRR.csv".format(output), index=False)
    else:
        return mrr_df
    
def create_ndcg(gt, se_ls, save=True, output="output"):
    res = {'Search Engine':['SE_1', 'SE_2', 'SE_3'], 
            'Mean(nDCG@1)': [mndcg(gt, se, 1) for se in se_ls],
            'Mean(nDCG@3)': [mndcg(gt, se, 3) for se in se_ls], 
            'Mean(nDCG@5)': [mndcg(gt, se, 5) for se in se_ls], 
            'Mean(nDCG@10)': [mndcg(gt, se, 10) for se in se_ls]}
    ndcg_df = pd.DataFrame(res, columns=res.keys())
    if save:
        ndcg_df.to_csv("{}/nDCG.csv".format(output), index=False)
    else:
        return ndcg_df


if __name__ == '__main__':
    DATASET_PATH = "dataset"
    OUTPUT_PATH = "part_1_1/output_data"
    gt_table = pd.read_table("{}/part_1_1/part_1_1__Ground_Truth.tsv".format(DATASET_PATH))
    se1 = pd.read_table("{}/part_1_1/part_1_1__Results_SE_1.tsv".format(DATASET_PATH))
    se2 = pd.read_table("{}/part_1_1/part_1_1__Results_SE_2.tsv".format(DATASET_PATH))
    se3 = pd.read_table("{}/part_1_1/part_1_1__Results_SE_3.tsv".format(DATASET_PATH))
    gt_list = gt_table.groupby('Query_id')['Relevant_Doc_id'].apply(lambda x: x.tolist()).tolist()
    se1_list = se1.groupby('Query_ID')['Doc_ID'].apply(lambda x: x.tolist()).tolist()
    se2_list = se2.groupby('Query_ID')['Doc_ID'].apply(lambda x: x.tolist()).tolist()
    se3_list = se3.groupby('Query_ID')['Doc_ID'].apply(lambda x: x.tolist()).tolist()
    se_ls = [se1_list, se2_list, se3_list]
    create_mpak(gt_list, se_ls, save=True, output=OUTPUT_PATH)
    create_rprecision(gt_list, se_ls, save=True, output=OUTPUT_PATH)
    create_mrr(gt_list, se_ls, save=True, output=OUTPUT_PATH)
    create_ndcg(gt_list, se_ls, save=True, output=OUTPUT_PATH)