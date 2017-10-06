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

/**
 * Print program usage to stdout
 */
void printUsage() {
    std::cout
            << "naivebayes - Text classification using Naive Bayes" << std::endl << std::endl
            << "Usage: naivebayes [-i input.csv] [-o output.csv]" << std::endl
            << "    -i, --input\t\tCSV input file" << std::endl
            << "    -o, --output\tOutput file" << std::endl
            << "    -h, --help\t\tDisplay this help message" << std::endl;
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
            {"help",   no_argument,       0, 'h'},
            {0, 0,                        0, 0}
    };

    int optionIndex = 0;
    int c;
    while ((c = getopt_long(argc, argv, "hi:o:", longOptions, &optionIndex)) != -1) {
        switch (c) {
            case 'i':
                g_inputFile = optarg;
                break;
            case 'o':
                g_outputFile = optarg;
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
    if(g_inputFile.empty() || g_outputFile.empty()) {
        printUsage();
        return 0;
    }

    try{
        // Prepare csv variables
        int id;
        int category;
        std::string text;

        // Load information
        io::CSVReader<3> inputCSV(g_inputFile);
        inputCSV.read_header(io::ignore_extra_column, "Id", "Category", "Text");
        std::cout << ">> Loading: " << g_inputFile << std::endl;
        while(inputCSV.read_row(id, category, text)){
            std::vector<std::string> tokens = tokenize(text);
            std::cout << tokens.size() << std::endl;
        }

    } catch (io::error::can_not_open_file exception) {
        std::cerr << "Error opening input file" << std::endl;
        return 1;
    }
    return 0;
}