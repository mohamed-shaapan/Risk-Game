#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

/* import libraries */
/******************************************/
#include <string>
#include "data_structures.h"
#include "../utilities/file_parser.h"

using namespace std;


/* class definition */
/******************************************/
class environment
{
	private:
		vector<struct country> country_list;
		vector<struct border> border_list;
		vector<struct continent> continent_list;
		int game_status;

	public:
		/* constructor */
		environment(char *init_file_dir);
		~environment();

		/* interface methods */
		int invade(int from_country_id, int to_country_id); // attempts to make move

		// some getters
		vector<struct country> *get_country_list();
		vector<struct border> *get_border_list();
		vector<struct continent> *get_continent_list();
		int get_game_status();
		//environment *get_game_environment();


};

#endif 