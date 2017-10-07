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
std::string g_textFile;
std::string g_langFile;
std::string g_outputFile;
std::vector<std::string> g_algorithms;

// Algorithms
const std::string ALGO_SPACE = "space";

/**
 * Print program usage to stdout
 */
void printUsage() {
    std::cout
            << "csv2csv - Merge two csv files into one" << std::endl << std::endl
            << "Usage: csv2csv [-t text.csv] [-l lang.csv] [-o output.csv]" << std::endl
            << "    -t, --text\t\tCSV text file" << std::endl
            << "    -l, --lang\t\tCSV language file" << std::endl
            << "    -o, --out\t\tCSV output file" << std::endl
            << "    -a, --algo\t\tAlgorithm id to be performed on the text" << std::endl
            << "        \t\t* space: Add space between word characters" << std::endl
            << "    -h, --help\t\tDisplay this help message" << std::endl;
}

/**
 * Initialize parameters
 * @param argc
 * @param argv
 */
void initParams(int argc, char *argv[]) {

    struct option longOptions[] = {
            {"text", required_argument, 0, 't'},
            {"lang", required_argument, 0, 'l'},
            {"out", required_argument, 0, 'o'},
            {"algo", required_argument, 0, 'a'},
            {"help",   no_argument,       0, 'h'},
            {0, 0,                        0, 0}
    };

    int optionIndex = 0;
    int c;
    while ((c = getopt_long(argc, argv, "t:l:o:ha:", longOptions, &optionIndex)) != -1) {
        switch (c) {
            case 't':
                g_textFile = optarg;
                break;
            case 'l':
                g_langFile = optarg;
                break;
            case 'o':
                g_outputFile = optarg;
                break;
            case 'a':
                g_algorithms.push_back(optarg);
                break;
            case 'h':
            default:
                break;
        }
    }
}

/**
 * Utterance structure
 */
struct utt {
    int m_id;
    int m_category;
    std::string m_text;
};

/**
 * Apply algorithm on the utterance text
 * @param algoId
 * @param map
 */
void applyAlgorithm(std::string algoId, std::map<int, struct utt*> &map) {
    if(algoId == ALGO_SPACE) {
        for(auto entry : map) {
            std::string orgText = entry.second->m_text;
            entry.second->m_text.clear();
            std::stringstream ss;
            for(int index=0; index < orgText.length(); index++) {
                ss << orgText[index];
                if(orgText[index] != ' ') {
                    ss << " ";
                }
            }
            entry.second->m_text = ss.str();
        }
    } else {
        std::cerr << "Algorithm ID: " << algoId << " was not found." << std::endl;
    }
}

int main(int argc, char** argv) {

    // Initialize parameters
    initParams(argc, argv);

    // Handle errors
    if(g_textFile.empty() || g_langFile.empty() || g_outputFile.empty()) {
        printUsage();
        return 0;
    }

    try{

        // Prepare csv variables
        int id;
        int category;
        std::string text;
        std::map<int, struct utt*> map;

        // Load language information
        io::CSVReader<2> langCSV(g_langFile);
        langCSV.read_header(io::ignore_extra_column, "Id", "Category");
        std::cout << ">> Loading: " << g_langFile << std::endl;
        while(langCSV.read_row(id, category)){
            map[id] = new struct utt();
            map[id]->m_id = id;
            map[id]->m_category = category;
        }

        // Load text information
        std::cout << ">> Loading: " << g_textFile << std::endl;
        io::CSVReader<2> textCSV(g_textFile);
        textCSV.read_header(io::ignore_extra_column, "Id", "Text");
        while(textCSV.read_row(id, text)) {
            map[id]->m_text = text;
        }

        // Apply algorithms
        for(std::string algoId : g_algorithms) {
            std::cout << ">> Applying algorithm: " << algoId << std::endl;
            applyAlgorithm(algoId, map);
        }

        // Generate new csv
        std::cout << ">> Generating CSV: " << g_outputFile << std::endl;
        std::ofstream outFile (g_outputFile);
        outFile << "Id,Category,Text" << std::endl;
        for(auto entry : map) {
            outFile << entry.second->m_id << "," << entry.second->m_category << ","
                    << entry.second->m_text << std::endl;
            delete entry.second;
        }
        outFile.close();
    } catch (io::error::can_not_open_file exception) {
        std::cerr << "Error opening input file(s)" << std::endl;
        return 1;
    }
    return 0;
}
