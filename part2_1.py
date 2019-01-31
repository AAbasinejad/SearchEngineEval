from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import re
import binascii
import random
import math
import pandas as pd
from collections import OrderedDict
from multiprocessing import Pool
import tqdm

DATA_PATH = "dataset/part_2_1/lyrics_collection/"
OUTPUT_PATH = "part_2_1/input_data"

def process_file(html_file):
    return (html_file, re.sub(r'\W+', ' ', parse_data(DATA_PATH, html_file)).lower().strip())

def parse_data(data_path, html_file):
    soup = BeautifulSoup(open(data_path+html_file), "html.parser")
    lyric_content = soup.find("body")
    lyrics = ''.join(map(str,lyric_content.contents)).replace('<br/>', ' ')
    return lyrics

def shingle_docs(docs):
    docs_shingles = {}
    set_all_shingles = set()
    for i, lyric_tuple in tqdm.tqdm(enumerate(docs), total=len(docs)):
        words = lyric_tuple[1].split()
        if len(words) > 0:
            set_of_shingles = set()
            for index in range(0, len(words)-2):
                shingle = " ".join([words[index], words[index+1], words[index+2]])
                hashed_shingle =  binascii.crc32(shingle.encode('utf-8')) & 0xffffffff
                set_of_shingles.add(hashed_shingle)
                set_all_shingles.add(hashed_shingle)
            docs_shingles[lyric_tuple[0]] = set_of_shingles
    return docs_shingles, set_all_shingles

def is_prime(number):
    for j in range(2, int(math.sqrt(number)+1)):
        if (number % j) == 0: 
            return False
    return True

def gen_hash_func_parameters(num_hash_functions=100, upper_bound_on_number_of_distinct_terms=100, save=False, output="output"):
    hash_funcs_params = []
    for _ in range(num_hash_functions):
        a = random.randint(1, upper_bound_on_number_of_distinct_terms-1)
        b = random.randint(0, upper_bound_on_number_of_distinct_terms-1)
        p = random.randint(upper_bound_on_number_of_distinct_terms, 10*upper_bound_on_number_of_distinct_terms)
        while is_prime(p) == False:
            p = random.randint(upper_bound_on_number_of_distinct_terms, 10*upper_bound_on_number_of_distinct_terms)
        hash_func = OrderedDict([('a',a), ('b',b), ('p',p), ('n',upper_bound_on_number_of_distinct_terms)])
        hash_funcs_params.append(hash_func)
    hash_funcs_params_df = pd.DataFrame.from_dict(hash_funcs_params)
    if save:
        hash_funcs_params_df.to_csv("{}/{}_hash_functions_file.tsv".format(output, num_hash_functions), 
                                    sep="\t", index=False)
    return hash_funcs_params

def hash_func(params, x):
    return ((params['a']*x+params['b'])%params['p'])%params['n']

def min_hash(shingle):
    hash_funcs_params_df = pd.read_table("part_2_1/input_data/300_hash_functions_file.tsv")
    hash_funcs_params = list(hash_funcs_params_df.T.to_dict().values())
    min_hashes = []
    value = shingle[1]
    key = shingle[0]
    for hash_func_param in hash_funcs_params:
        min_hash = float('inf')
        for shingle_id in value:
            hash_code = hash_func(hash_func_param, shingle_id)
            if hash_code < min_hash:
                min_hash = hash_code
        min_hashes.append(min_hash)
    return tuple([key, min_hashes])

if __name__ == "__main__":
    html_files = sorted([f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))])

    with Pool(processes=8) as pool:
        lyrics = list(tqdm.tqdm(pool.imap(process_file, html_files), total=len(html_files)))
        pool.close()
        pool.join()

    lyrics = [x for x in lyrics if x[1].strip()]
    shingles, set_of_shingles = shingle_docs(lyrics)
    output_hash_params = "part_2_1/input_data"
    hash_params = gen_hash_func_parameters(300, len(set_of_shingles), save=True, output=output_hash_params)
    with Pool(processes=8) as pool:
        min_hashes = list(tqdm.tqdm(pool.imap(min_hash, shingles.items()), total=len(shingles.items())))
        pool.close()
        pool.join()

    min_hashes_df = pd.DataFrame(min_hashes)
    min_hashes_df.to_csv("{}/sets_file__ALL_LYRICS.tsv".format(OUTPUT_PATH), sep="\t", header=False, index=False)