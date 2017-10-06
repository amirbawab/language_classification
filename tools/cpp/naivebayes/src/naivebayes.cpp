#include <iostream>
#include <unistd.h>
#include <getopt.h>
#include <string.h>
#include <algorithm>
#include <fstream>
#include <map>
#include <vector>
#include <sstream>
#include <csv.h>

// Global vars
std::string g_inputFile;
std::string g_outputFile;
std::string g_cacheFile;
std::string g_loadCacheFile;
std::string g_sentence;

// Cache types
const std::string CACHE_WORD = "word";
const std::string CACHE_CATEGORY = "category";

/**
 * Print program usage to stdout
 */
void printUsage() {
    std::cout
            << "naivebayes - Text classification using Naive Bayes" << std::endl << std::endl
            << "Usage: naivebayes [-i input.csv] [-o output.csv]" << std::endl
            << "    -i, --input     CSV input file" << std::endl
            << "    -c, --cache     Cache calculated probabilities to a file" << std::endl
            << "    -l, --loadcache Load cache probabilities from file" << std::endl
            << "    -o, --output    Output file" << std::endl
            << "    -s, --sentence  Sentence to evaluate" << std::endl
            << "    -h, --help      Display this help message" << std::endl;
}

/**
 * Initialize parameters
 * @param argc
 * @param argv
 */
void initParams(int argc, char *argv[]) {

    struct option longOptions[] = {
            {"input", required_argument, 0, 'i'},
            {"output", required_argument, 0, 'o'},
            {"cache", required_argument, 0, 'c'},
            {"loadcache", required_argument, 0, 'l'},
            {"sentence", required_argument, 0, 's'},
            {"help",   no_argument,       0, 'h'},
            {0, 0,                        0, 0}
    };

    int optionIndex = 0;
    int c;
    while ((c = getopt_long(argc, argv, "hi:o:c:l:s:", longOptions, &optionIndex)) != -1) {
        switch (c) {
            case 'i':
                g_inputFile = optarg;
                break;
            case 'o':
                g_outputFile = optarg;
                break;
            case 'c':
                g_cacheFile = optarg;
                break;
            case 'l':
                g_loadCacheFile = optarg;
                break;
            case 's':
                g_sentence = optarg;
                break;
            case 'h':
            default:
                break;
        }
    }
}

/**
 * Convert a string to a vector of tokens
 * @param text
 * @return vector of words
 */
std::vector<std::string> tokenize(std::string text) {
    std::vector<std::string> tokens;
    char *cstr = new char[text.length() + 1];
    strcpy(cstr, text.c_str());
    char * pch;
    pch = strtok (cstr," \t");
    while (pch != NULL) {
        tokens.push_back(pch);
        pch = strtok (NULL, " ,.-");
    }
    delete [] cstr;
    return tokens;
}

int main(int argc, char** argv) {

    // Initialize parameters
    initParams(argc, argv);

    // Handle errors
    if((g_loadCacheFile.empty() && g_inputFile.empty()) || g_outputFile.empty()) {
        printUsage();
        return 0;
    }

    try{

        // Naive Bayes variables
        std::map<int, unsigned long> categoryCounter;
        std::map<std::string, std::map<int, unsigned long>> wordGivenCategoryCounter;
        std::map<int, unsigned long> wordsInCategoryCounter;
        std::map<std::string, std::map<int, double>> pWordGivenCategory;
        std::map<int, double> pCategory;
        unsigned long totalUtt = 0;

        if(g_loadCacheFile.empty()) {

            // Prepare csv variables
            int id;
            int category;
            std::string text;

            // Load information
            std::cout << ">> Loading: " << g_inputFile << std::endl;
            io::CSVReader<3> inputCSV(g_inputFile);
            inputCSV.read_header(io::ignore_extra_column, "Id", "Category", "Text");
            while(inputCSV.read_row(id, category, text)){

                // Convert string to tokens
                std::vector<std::string> tokens = tokenize(text);
                for(std::string word : tokens) {

                    // The number of times a word occurs in a category
                    wordGivenCategoryCounter[word][category]++;
                }

                // The number of utterances in this category
                categoryCounter[category]++;

                // Increment the total number of utterance
                totalUtt++;

                // THe number of words in this category
                wordsInCategoryCounter[category] += tokens.size();
            }

            // Start calculating the probabilities
            const int BIAS = 1;
            std::cout << ">> Computing P(Wi|Cj)" << std::endl;
            for(auto &wordEntry : wordGivenCategoryCounter) {
                for(auto &categoryEntry : categoryCounter) {
                    pWordGivenCategory[wordEntry.first][categoryEntry.first] = (double)
                                                                                       (BIAS +  wordGivenCategoryCounter[wordEntry.first][categoryEntry.first]) /
                                                                               (wordsInCategoryCounter[categoryEntry.first] + wordGivenCategoryCounter.size());
                }
            }

            std::cout << ">> Computing P(Cj)" << std::endl;
            for(auto entry : categoryCounter) {
                pCategory[entry.first] = (double) entry.second / totalUtt;
            }
        } else {
            // Prepare csv variables
            std::string word;
            int category;
            std::string type;
            double probability;

            // Load information
            std::cout << ">> Loading probabilities from cache: "<< g_loadCacheFile << std::endl;
            io::CSVReader<4> cacheCSV(g_loadCacheFile);
            cacheCSV.read_header(io::ignore_extra_column, "Word", "Category", "Probability", "Type");
            while(cacheCSV.read_row(word, category, probability, type)) {
                if(type == CACHE_CATEGORY) {
                    pCategory[category] = probability;
                } else if(type == CACHE_WORD) {
                    pWordGivenCategory[word][category] = probability;
                } else {
                    std::cerr << "Unknown type " << type << std::endl;
                }
            }
        }

        // Cache results if requested
        if(!g_cacheFile.empty()) {
            std::cout << ">> Caching computed probabilities at: " << g_cacheFile << std::endl;
            std::ofstream cacheFile(g_cacheFile);

            // If cache file was opened
            if(cacheFile.is_open()) {
                cacheFile << "Word,Category,Probability,Type" << std::endl;

                // Cache probabilities for the categories
                for(auto entry : pCategory) {
                    cacheFile << "," << entry.first << "," << entry.second << "," << CACHE_CATEGORY << std::endl;
                }

                // Cache probabilities for words given categories
                for(auto wordEntry : pWordGivenCategory) {
                    for(auto categoryEntry : wordEntry.second) {
                        cacheFile << wordEntry.first << "," << categoryEntry.first << ","
                                  << categoryEntry.second << "," << CACHE_WORD << std::endl;
                    }
                }
                cacheFile.close();
            } else {
                std::cerr << "Could not open cache file: " << g_cacheFile << std::endl;
            }
        }

        // Evaluate a sentence
        if(!g_sentence.empty()) {
            std::cout << ">> Evaluating sentence: " << g_sentence << std::endl;

            // Convert sentence to tokens
            std::vector<std::string> tokens = tokenize(g_sentence);
            for(auto entry : pCategory) {
                double val = entry.second;
                for(std::string token : tokens) {
                    if(pWordGivenCategory.find(token) != pWordGivenCategory.end()) {
                        val *= pWordGivenCategory[token][entry.first];
                    }
                }
                std::cout << "P(S | " << entry.first << ") = " << val << std::endl;
            }
        }

    } catch (io::error::can_not_open_file exception) {
        std::cerr << "Error opening input file" << std::endl;
        return 1;
    }
    return 0;
}