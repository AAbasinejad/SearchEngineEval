# SearchEngineV2.0
Search-Engine Evaluation and Near-Duplicates-Detection

### Introduction
------
This project composed of two parts: Search-Engine Evaluation and Near-Duplicates-Detection

### Part 1
------
In this part the quality of three different search engines assessed using only the ground truth and their query results.

#### Part 1-1
In [this part](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/part1_1.py) using the available data we calculate the following evaluation metrics: P@K, R-Precision, MRR (Mean Reciprocal Rank) and nDCG (normalized discounted cumulative gain).<br/>
First we check how many unique documents and how many queries we have on the ground truth.<br/>

|Number of Queries|Number of Unique Documents|
|---|---|
|222|728|
<br/>
calculation of the metrics mentioned aboved for each search engine:<br/>

**P@K** <br/>

|   |Search Engine|Mean(P@1)|Mean(P@3)|Mean(P@5)|Mean(P@10)|
|---|---|---|---|---|---|
|0|SE_1|0.031532|0.030030|0.027928|0.025676|
|1|SE_2|0.301802|0.295796|0.263063|0.185586|
|2|SE_3|0.238739|0.205706|0.186486|0.143243|
<br/>

**R-Precision Table** <br/>

|   |Search Engine|1|2|3|4|5|6|
|---|---|---|---|---|---|---|---|
|0|SE_1|0.023|0.000|0.000|0.000|0.000|0.667|
|1|SE_2|0.255|0.000|0.000|0.250|0.429|1.000|
|2|SE_3|0.179|0.000|0.000|0.143|0.333|1.000|
<br/>
In the above table the columns have the following meaning:<br/>

1. Mean(R-precision_Distribution)
2. min(R-precision_Distribution)
3. 1_quartile(R-precision_Distribution)
4. MEDIAN(R-precision_Distribution)
5. 3_quartile(R-precision_Distribution)
6. MAX(R-precision_Distribution)
<br/>

**MRR Table** <br/>

|   |Search Engine|MRR|
|---|---|---|
|0|SE_1|0.081414|
|1|SE_2|0.486303|
|2|SE_3|0.395118|
<br/>

**nDCG Table** <br/>

|   |Search Engine|Mean(nDCG@1)|Mean(nDCG@3)|Mean(nDCG@5)|Mean(nDCG@10)|
|---|---|---|---|---|---|
|0|SE_1|0.031532|0.032753|0.036867|0.051712|
|1|SE_2|0.301802|0.319976|0.343172|0.371056|
|2|SE_3|0.238739|0.237409|0.259599|0.299687|

#### Part 1-2
In [this part](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/part1_2.py) we analyse the quality of the three different search engine modules considering the following constraints:<br/>
1. The output is only four results for each search query.
2. These four results are displayed randomly.

First we check how many unique documents and how many queries we have on the ground truth.<br/>

|Number of Queries|Number of Unique Documents|
|---|---|
|198|662|
<br/>
Now, let’s consider the same metrics that we calculated on Part 1.1, then we analyse the results based on our constraints.<br/>

|   |Search Engine|Mean(P@4)|Mean(nDCG@4)|MRR|Mean(R-precision_Distribution)|
|---|---|---|---|---|---|
|2|SE_3|0.289141|0.355537|0.503345|0.264729|
|0|SE_1|0.284091|0.350827|0.498194|0.267304|
|1|SE_2|0.205808|0.253527|0.416848|0.185576|
<br/>

It is possible to see that, overall, Search Engine 3 and Search Engine 1 have better results then Search Engine 2, therefore, we disregard Search Engine 2 and focus on the other two. <br/>
When we compare results, Search Engine 3 has higher mean precistion at 4 and higher mean normalized discounted cumulative gain at 4 and higher mean reciprocal rank, whilst Search Engine 1 has higher mean R-precision.<br/>
Given our two constraints, evaluation measures that take into account the rank position should be ignored, because we do not rank the results (they are displayed randomly). Thus, the measures of MRR and R-precision do not gives us a reliable measure in this case.<br/> 
There could be an argument to use the normalized discounted cumulative gain, they also take into account the rank position, but since we set as 1 the rating of every relevant document we could consider the best ranking for each query given the first 4 results. Although this could gives us some information it is not correct per se. Moreover, the results are close for Search Engine 3 and 1, so we will not consider this evaluation metric in ordet to give a final answer.<br/>
Finally, we are left with the precision at 4 scores. This metric seems suitable for our case, since we consider the precision for 4 results (our first constraint), and by default it does not take into account how the results are ranked (our second constraint). With this in mind, we would recommend Search Engine 3 given our constraints and our objective.<br/>

### Part 2
------
In this part we deal with three data mining problems: (1) near-duplicate detection; (2) the set-estimation problem and (3) the unions-size estimation problem.<br/>

**Part 2-1** <br/>
In [this section](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/part2_1.py) we find, in an approximated way, all near-duplicate documents in a dataset of lyrics of songs. For this, two documents has been considered as near-duplicates if the Jaccard similarity between their associated set of shingles is ≥ 0.85.<br/>
Before running the program we parsed the data and removed documents where the lyrics were empty, from this, out of 87041 song lyrics, we got a total of 86216 that were considered for near-duplicate detection.<br/>

**value of 'r' and 'b'** <br/>
To determine the values of 'r' and 'b' we have the following set of equations and constraints:<br/>

(1) ![Eq-1](http://latex.codecogs.com/gif.latex?n%20%3D%20r%20%5Ctimes%20b) <br/>
(2) ![Eq-2](http://latex.codecogs.com/gif.latex?p%20%3D%201%20-%20%281%20-%20j%5Er%29%5Eb)

<br/>
- Contraint 1: Each set of shingles, that represents an original document, must be sketched in
a Min-Hashing sketch of length 300. <br/>
- Contraint 2: It is acceptable to have as a near-duplicates candidate a pair of documents with
Jaccard=0.85, with probability 0.97.

From Contraint 1 and Constraint 2, and equations 1 and 2, we get:<br/>

(3) ![Eq-3](http://latex.codecogs.com/gif.latex?b%20%5Ctimes%20r%20%3D%20300) <br/>
(4) ![Eq-4](http://latex.codecogs.com/gif.latex?1%20-%20%281%20-%200.85%5Er%29%5Eb%20%5Cge%200.97)

<br/>
Finally, we can choose the value r = 10 and b = 30, which gives us: <br/>

(5) ![eq-5](http://latex.codecogs.com/gif.latex?1%20-%20%281%20-%200.85%5E%7B10%7D%29%5E%7B30%7D%20%3D%200.9986084)

<br/>
Hence, we choose r = 10 and b = 30. <br/>

**Near Duplicates** <br/>
Using locality sensitive hashing, and r = 10, and b = 30 we found 8974 near-duplicate candidates,
you can find the actual candidates [here](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/ALL_NEAR_DUPLICATE_CANDIDATES_with_LSH__10_30_300__ALL_LYRICS.tsv). <br/>
Using locality sensitive hashing with min hashing, and r = 10, and b = 30, we found 1795 approx-
imated near-duplicates, you can find the actual near-duplicates [here](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/APPROXIMATED_NEAR_DUPLICATES_DETECTION__lsh_plus_min_hashing__10_30_300__ALL_LYRICS.tsv). <br/>
The number of false positives on the set of near-duplicate candidates that were filtered out after
getting the approximated near-duplicates is 7179. You can find the actual false positives at [`false_positives.tsv`](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/false_positives.tsv). <br/>
The code to generate the shingles and min-hashes from the set of documents can be found at [`part2_1.py`](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/part2_1.py). <br/>
and the code to get the false positives and other statistics can be found at [`part2_1stats.py`](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/part2_1stats.py). <br/>

**Part 2-2** <br/>
In this section we deal with the last two problems: set-size estimation and unions-size estimation. <br/>

**Set Size Estimation** <br/>
The problem is the following: given a min-hash sketch of a set **X** and the size of the universe set (we call it **U**), we have to estimate the size of **X**. <br/>
We know that the Jaccard similarity (JS) between two sets **A** and **B** is given by: <br/>

(6) ![Eq-6](http://latex.codecogs.com/gif.latex?JS%28A%2CB%29%3D%20%5Cfrac%7B%7CA%20%5Ccap%20B%7C%7D%7B%7CA%20%5Ccup%20B%7C%7D)
<br/>
Moreover, if ![](http://latex.codecogs.com/gif.latex?A%20%5Csubset%20B) we have that the ![](http://latex.codecogs.com/gif.latex?A%20%5Ccup%20B%20%3D%20A), and ![](http://latex.codecogs.com/gif.latex?A%20%5Ccap%20B%20%3D%20A), so ![](http://latex.codecogs.com/gif.latex?JS%28A%2CB%29%20%3D%20%5Cfrac%7B%7CA%7C%7D%7B%7CB%7C%7D) if ![](http://latex.codecogs.com/gif.latex?A%20%5Csubset%20B). <br/>
