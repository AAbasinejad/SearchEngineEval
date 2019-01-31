# SearchEngineV2.0
Search-Engine Evaluation and Near-Duplicates-Detection

### Introduction
------
This project composed of two parts: Search-Engine Evaluation and Near-Duplicates-Detection

### Part 1
------
In this part the quality of three different search engines assessed using only the ground truth and their query results.

#### Part 1-1
In [this part](https://github.com/AAbasinejad/SearchEngineV2.0/blob/master/part1_1.py)using the available data we calculate the following evaluation metrics: P@K, R-Precision, MRR (Mean Reciprocal Rank) and nDCG (normalized discounted cumulative gain).<br/>
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

