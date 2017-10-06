# Text Classification using Naive Bayes

## Build tool
```
cd $REPO/tools/cpp/
cmake .
make naivebayes
```

## Usage

Use the `-h` flag to learn more about the options `naivebayes` provides
```
naivebayes -h
```

**NOTE: Use the [csv2csv](csv2csv) tool to generate a valid csv input file**

### Example 1
Load input training set and evaluate a sentence
```
./naivebayes -i input.csv -s "bonjour à tous"
```

### Example 2
Cache the compute Naive Bayes probabilities to a csv file
```
./naivebayes -i input.csv -c cache.csv
```

### Example 3
Load cached probabilities from file and evaluate a sentence
```
./naivebayes -l cache.csv -s "bonjour à tous"
```
