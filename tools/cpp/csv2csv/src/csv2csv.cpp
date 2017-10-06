#include <iostream>
#include <unistd.h>
#include <getopt.h>
#include <string.h>
#include <algorithm>
#include <csv.h>

// Gloabl vars
std::string g_textFile;
std::string g_langFile;
std::string g_outputFile;

/**
 * Print program usage to stdout
 */
void printUsage() {
    std::cout
            << "csv2csv - Merge two csv files into one" << std::endl << std::endl
            << "Usage: csv2csv [-t text.csv] [-l lang.csv] [-o output.csv]" << std::endl
            << "    -t, --text\t\t\tCSV text file" << std::endl
            << "    -l, --lang\t\t\tCSV language file" << std::endl
            << "    -o, --out\t\t\tCSV output file" << std::endl
            << "    -h, --help\t\t\tDisplay this help message" << std::endl;
}

/**
 * Initialize parameters
 * @param argc
 * @param argv
 * @param doc
 * @param res
 */
void initParams(int argc, char *argv[]) {

    struct option longOptions[] = {
            {"text", required_argument, 0, 't'},
            {"lang", required_argument, 0, 'l'},
            {"out", required_argument, 0, 'o'},
            {"help",   no_argument,       0, 'h'},
            {0, 0,                        0, 0}
    };

    int optionIndex = 0;
    int c;
    while ((c = getopt_long(argc, argv, "t:l:o:h", longOptions, &optionIndex)) != -1) {
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
            case 'h':
            default:
                break;
        }
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

    return 0;
}