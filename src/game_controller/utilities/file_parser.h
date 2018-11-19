#ifndef FILE_PARSER_H
#define FILE_PARSER_H

/* import libraries */
/******************************************/
#include <fstream> // read write file
#include <iostream> // read write screen
#include <vector>
#include <string>
#include <cstring>
#include "io_handler.h"
#include "../environment/data_structures.h" // data structures of environment

using namespace std;

/* class definition */
/******************************************/
class file_parser
{
	public:
		file_parser(char *init_file_dir);
		void obtain_border_list(vector<struct border> *border_list);
		void obtain_continent_list(vector<struct continent> *continent_list);
		// some getters
		int get_country_count();
		int get_border_count();
		int get_continent_count();

	private:
		// attributes
		vector<string> init_file_lines; // buffered init file as vectors of lines
		int country_count = 0;
		int border_count = 0;
		int continent_count = 0;

		// utility functions
		vector<string> tokenize(string target_line); // splits string by delimiter
		int parse_count(int line_number); // gets count for specific attribute (country, border, continent)
		
};

#endif 
