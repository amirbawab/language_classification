#!/bin/bash

CSV_PATH="/tmp/csv"
TOOLS_DIR="/tmp/tools"
KFOLD_DIR="$CSV_PATH/kfold"

for k in {1..10}
do

    # VANILLA NAIVE-BAYES
    echo "Executing Naive-Bayes for k=$k"
    python "$TOOLS_DIR/naivebayes.py" \
        -i "$KFOLD_DIR/train/train$k" \
        -t "$KFOLD_DIR/test/test$k" \
        -o "$KFOLD_DIR/results/NB/out$k" > /dev/null

    python "$TOOLS_DIR/comparecsv.py" \
        -s "$KFOLD_DIR/results/NB/out$k" \
        -a "$KFOLD_DIR/valid/test$k" \
        | command grep -i "total"


    echo "------------------------------------"
    
done
