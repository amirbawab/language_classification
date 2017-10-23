#!/bin/bash

CSV_PATH="/tmp/csv"
TOOLS_DIR="$PWD"
KFOLD_DIR="$CSV_PATH/kfold"

# Compare generated csv with the actual answer
function comparecsv() {
    k="$1"
    path="$2"
    python3 "$TOOLS_DIR/comparecsv.py" \
        -s "$KFOLD_DIR/results/$path/out$k" \
        -a "$KFOLD_DIR/valid/test$k" \
        | command grep -i "total"
}

# Vanilla Naive-bayes
function naivebayes() {
    k=$1
    outdir="NB"
    echo "Executing Naive-Bayes for k=$k"
    mkdir -p "$KFOLD_DIR/results/$outdir/"
    python3 "$TOOLS_DIR/naivebayes.py" \
        -i "$KFOLD_DIR/train/train$k" \
        -t "$KFOLD_DIR/test/test$k" \
        -o "$KFOLD_DIR/results/$outdir/out$k" > /dev/null

    comparecsv "$k" "$outdir"
}

# Naive-bayes with filter 1
function naivebayes_f1() {
    k=$1
    outdir="NB*"
    rval="0.004"
    echo "Executing Naive-Bayes for k=$k and r=$rval"
    mkdir -p "$KFOLD_DIR/results/$outdir/"
    python3 "$TOOLS_DIR/naivebayes.py" \
        -i "$KFOLD_DIR/train/train$k" \
        -t "$KFOLD_DIR/test/test$k" \
        -o "$KFOLD_DIR/results/$outdir/out$k" \
        -r "$rval" > /dev/null

    comparecsv "$k" "$outdir"
}

# Naive-bayes with filter 1 and filter 2
function naivebayes_f1_f2() {
    k=$1
    outdir="NB**"
    rval="0.004"
    echo "Executing Naive-Bayes for k=$k, r=$rval and strict mode enabled"
    mkdir -p "$KFOLD_DIR/results/$outdir/"
    python3 "$TOOLS_DIR/naivebayes.py" \
        -i "$KFOLD_DIR/train/train$k" \
        -t "$KFOLD_DIR/test/test$k" \
        -o "$KFOLD_DIR/results/$outdir/out$k" \
        -r "$rval" \
        -s > /dev/null

    comparecsv "$k" "$outdir"
}

# Naive-bayes with filter 1, filter 2, Anagrams
function naivebayes_f1_f2_ad() {
    k=$1
    outdir="NB**+AD"
    echo "Executing Anagram Detection for k=$k"
    mkdir -p "$KFOLD_DIR/results/$outdir"
    python3 "$TOOLS_DIR/anagrams.py" \
        -d "$KFOLD_DIR/train-em/train$k" \
        -t "$KFOLD_DIR/test-em/test$k" \
        -p 2 \
        -o "$KFOLD_DIR/results/$outdir/merge$k" > /dev/null

    python3 "$TOOLS_DIR/manipsubmit.py" \
        -i "$KFOLD_DIR/results/NB**/out$k" \
        -m "$KFOLD_DIR/results/$outdir/merge$k" \
        -o "$KFOLD_DIR/results/$outdir/out$k" > /dev/null
    
    comparecsv "$k" "$outdir"
}

# Naive-bayes with filter 1, filter 2, Anagrams with extention
function naivebayes_f1_f2_ad_f1() {
    k=$1
    outdir="NB**+AD*"
    echo "Executing Anagram [Subsequence] Detection for k=$k"
    mkdir -p "$KFOLD_DIR/results/$outdir"
    python3 "$TOOLS_DIR/anagrams.py" \
        -d "$KFOLD_DIR/train-em/train$k" \
        -t "$KFOLD_DIR/test-em/test$k" \
        -p 1 2 \
        -o "$KFOLD_DIR/results/$outdir/merge$k" > /dev/null

    python3 "$TOOLS_DIR/manipsubmit.py" \
        -i "$KFOLD_DIR/results/NB**/out$k" \
        -m "$KFOLD_DIR/results/$outdir/merge$k" \
        -o "$KFOLD_DIR/results/$outdir/out$k" > /dev/null

    comparecsv "$k" "$outdir"
}

for k in {1..10}
do
    naivebayes $k
    naivebayes_f1 $k
    naivebayes_f1_f2 $k
    naivebayes_f1_f2_ad $k
    naivebayes_f1_f2_ad_f1 $k
    echo "----------------------"
done
