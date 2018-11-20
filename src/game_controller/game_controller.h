#ifndef GAME_CONTROLLER_H
#define GAME_CONTROLLER_H

/* import libraries */
/******************************************/
#include "./environment/environment.h"
#include "./player/player_factory.h"
#include "./player/player.h"
#include "../graphics_controller/cli_controller/game_set_visualizer.h"
#include "./environment/data_structures.h"
#include <cstdlib> // for system calls

using namespace std;

/* class definition */
/******************************************/
class game_controller
{

	private:
		environment game_environment;
		player *player1;
		player *player2;
		gameplay_id player_turn;

		// some utilities
		void announce_player_turn();

	public:
		/* constructor */
		game_controller(char *map_init_file_dir, char *ownership_init_file_dir, player_type p1_type, player_type p2_type);
		~game_controller();

		/* interface methods */
		void start_new_game();

};

#endif 
