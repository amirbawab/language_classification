# Language classification
### by team 2045

Our problem is a Dialog Language Classification task. The goal is to devise a machine learning algorithm to analyze short conversations, and automatically classify them according to the language of the conversation. There are five languages in the corpus: {0: Slovak, 1: French, 2: Spanish, 3: German, 4: Polish}

This is a project for COMP-551 Applied Machine Learning. For this task, we would be implementing Naive Bayes and kNN from scratch, and trying other ML algorithms using scikit-learn.

## Commands
*All scripts used in this section are available under `tools/python/` directory*

### Generate csv files

#### Generate an enhanced training set csv
*Merge `train_set_x.csv` and `train_set_y.csv` into a single file. Furthermore, convert all characters to lower case and place a single whitespace between each two consecutive characters*
```
python csv2csv.py \
    -t train_set_x.csv \
    -l train_set_y.csv \
    -o train_set_xy_1.csv \
    -a no_space lower space
```

*Merge `train_set_x.csv` and `train_set_y.csv` into a single file. Furthermore, convert all characters to lower case, remove all whitespaces and sort each sentence lexically*
```
python csv2csv.py \
    -t train_set_x.csv \
    -l train_set_y.csv \
    -o train_set_xy_2.csv \
    -a no_space lower sort_lex
```

*Create an enhanced `test_set_x.csv` file. In the new file, remove all whitespaces and sort each sentence lexically*
```
python maniptest.py \
    -i test_set_x.csv \
    -o test_set_x_1.csv \
    -a no_space sort_lex
```

### kNN
##### To run kNN from scratch:
*To run non-optimized knn (vectorization term frequency ratio and distance computation is row-wise)*
```
python knn.py \
    -f train_set_xy_1.csv \
    -t test_set_x.csv \
    -k <k_value> \
    -o <file_to_output_predictions> \
    -l <file_to_log_to>
```
*To run optimized knn (threaded, CountVectorizer for vectorization, distance computation is matrix level)*
```
python knn.py \
    -optimize \
    -f train_set_xy_1.csv \
    -t test_set_x.csv \
    -k <k_value> \
    -o <file_to_output_predictions> \
    -l <file_to_log_to>
```
##### To run kNN using scikit:
```
python knn-library.py \
    -f train_set_xy_1.csv \
    -t test_set_x.csv \
    -k <k_value> \
    -o <file_to_output_predictions>
```

### Naive-Bayes
#### To run Naive-Bayes
*Wihtout filters*
```
python naivebayes.py \
    -i train_set_xy_1.csv \
    -t test_set_x.csv \
    -o NB.csv
```

*With first filter*
```
python naivebayes.py \
    -i train_set_xy_1.csv \
    -t test_set_x.csv \
    -r 0.004 \
    -o NB*.csv
```

*With first and second filters*
```
python naivebayes.py \
    -i train_set_xy_1.csv \
    -t test_set_x.csv \
    -r 0.004 \
    -s \
    -o NB**.csv
```

### Anagram Detection
#### To run Anagram Detection
*Without extension*
```
python anagrams.py \
    -d train_set_xy_2.csv \
    -t test_set_x_1.csv \
    -p 2 \
    -o AD.csv
```

*With extension*
```
python anagrams.py \
    -d train_set_xy_2.csv \
    -t test_set_x_1.csv \
    -p 1 2 \
    -o AD*.csv
```
#### To merge Anagram Detection into Naive-Bayes
```
python manipsubmit.py \
    -i NB**.csv \
    -m AD*.csv \
    -o NB**+AD*.csv
```

### Compare 2 CSV files (Header: Id,Category)
```
python comparecsv.py \
    -s new-submit.csv \
    -a old-submit.csv
```
*Note: This script is useful to compare locally the output difference between a previously submitted csv file and a new generated one.*
