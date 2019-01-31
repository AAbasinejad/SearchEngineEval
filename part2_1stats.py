import pandas as pd


if __name__ == '__main__':
    CANDIDATES = "ALL_NEAR_DUPLICATE_CANDIDATES_with_LSH__10_30_300__ALL_LYRICS.tsv"
    ND_BRUTE_FORCE = "BRUTE_FORCE__near_duplicate_pairs__ALL_LYRICS.tsv"
    ND_LSH_MH = "APPROXIMATED_NEAR_DUPLICATES_DETECTION__lsh_plus_min_hashing__10_30_300__ALL_LYRICS.tsv"
    DATA_PATH = "part_2_1/output_data/"

    candidates_df = pd.read_table(DATA_PATH+CANDIDATES)
    nd_ls_mh_df = pd.read_table(DATA_PATH+ND_LSH_MH)

    ids_candidates = list(zip(candidates_df.id_set_1, candidates_df.id_set_2))
    ids_nd = list(zip(nd_ls_mh_df.id_set_1, nd_ls_mh_df.id_set_2))

    ids_false_positives_filtered = [x for x in ids_candidates if x not in ids_nd]
    false_positives_df = pd.DataFrame(ids_false_positives_filtered, columns=["id_set_1", "id_set_2"])
    false_positives_df = pd.merge(false_positives_df, candidates_df, left_on=['id_set_1', 'id_set_2'], right_on=['id_set_1', 'id_set_2'])
    false_positives_df.to_csv("{}false_positives.tsv".format(DATA_PATH), sep="\t", index=False)

    print("Near duplicates candidates using LSH = {}".format(candidates_df.shape[0]))
    print("Approximated near duplicates using LSH and MH = {}".format(nd_ls_mh_df.shape[0]))
    print("False positives filtered out = {}".format(false_positives_df.shape[0]))
