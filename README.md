Our problem is a Dialog Language Classification task. The goal is to devise a machine learning algorithm to analyze short conversations, and automatically classify them according to the language of the conversation. There are five languages in the corpus: {0: Slovak, 1: French, 2: Spanish, 3: German, 4: Polish}

This is a project for COMP-551 Applied Machine Learning. For this task, we would be implementing Naive Bayes and kNN from scratch, and trying other ML algorithms using scikit-learn.

##### To run kNN from scratch:
To run non-optimized knn (vectorization term frequency ratio and distance computation is row-wise)

    python knn.py -f <train_set> -t <test_set> -k <k_value> -o <file_to_output_predictions> -l <file_to_log_to>

To run optimized knn (threaded, CountVectorizer for vectorization, distance computation is matrix level)

    python knn.py -optimize -f <train_set> -t <test_set> -k <k_value> -o <file_to_output_predictions> -l <file_to_log_to>

##### To run kNN using scikit:
python knn-library.py -f <train_set> -t <test_set> -k <k_value> -o <file_to_output_predictions>
