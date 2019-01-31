# SearchEngineV2.0
Search-Engine Evaluation and Near-Duplicates-Detection

### Introduction
------
This project composed of two parts: Search-Engine Evaluation and Near-Duplicates-Detection

### Part 1
------
In this part the quality of three different search engines assessed using only the ground truth and their query results.

#### Part 1-1
Using the available data we calculate the following evaluation metrics: P@K, R-Precision, MRR (Mean Reciprocal Rank) and nDCG (normalized discounted cumulative gain).<br/>
First we check how many unique documents and how many queries we have on the ground truth.<br/>
|Number of Queries|Number of Unique Documents|
|---|---|
|222|728|
<br>/
calculattion of the metrics mentioned aboved for each search engine:<br/>

**P@K**<br/>

|   |Search Engine|Mean(P@1)|Mean(P@3)|Mean(P@5)|Mean(P@10)|
|---|---|---|---|---|---|
|0|SE_1|0.031532|0.030030|0.027928|0.025676|
|1|SE_2|0.301802|0.295796|0.263063|0.185586|
|2|SE_3|0.238739|0.205706|0.186486|0.143243|
<br/>

**R-Precision Table**
|   |Search Engine|Mean(R-precision_Distribution)|min(R-precision_Distribution)|1_quartile(R-precision_Distribution)|MEDIAN(R-precision_Distribution)|3_quartile(R-precision_Distribution)|MAX(R-precision_Distribution)|
|---|---|---|---|---|---|---|---|
|0|SE_1|   |   |   |   |   |   |
|1|SE_2|   |   |   |   |   |   |
|2|SE_3|   |   |   |   |   |   |
