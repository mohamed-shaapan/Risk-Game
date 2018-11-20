#include "game_set_visualizer.h"

/* visualize environment */
/******************************************/
void
game_set_visualizer::display_country_info(struct country *c)
{
	cout << "(id : " << c->id << ")\t";
	cout << "(owner : " << c->owner << ")\t";
	cout << "(troops count : " << c->troops_count << ")" << endl;
}

void
game_set_visualizer::display_game_board(environment *game_set)
{
	cout << "**************************************************************************************" << endl;
	cout << "**************************************************************************************" << endl;
	cout << "\t\t\t\t    COUNTRIES" << endl;
	cout << "**************************************************************************************" << endl;
	cout << "**************************************************************************************" << endl;
	cout << endl;

	vector<struct country>::iterator ptr1;
	for (ptr1 = game_set->get_country_list()->begin(); ptr1 < game_set->get_country_list()->end(); ptr1++) 
	{
		// display country info
		cout << "\t****************************************************************" << endl;
		cout << "\tcountry : ";
		display_country_info(&(*ptr1));
		cout << "\t****************************************************************" << endl;

		// display bordering countries
		vector<struct border>::iterator ptr2;
		for (ptr2 = game_set->get_border_list()->begin(); ptr2 < game_set->get_border_list()->end(); ptr2++) 
		{
			// country on 1st side of border
			if(ptr1->id == ptr2->country1)
			{
				cout << "\tNeighbor : ";
				display_country_info(&game_set->get_country_list()->at(ptr2->country2 - 1));
				continue;
			}
			// country on 2nd side of border
			if(ptr1->id == ptr2->country2)
			{
				cout << "\tNeighbor : ";
				display_country_info(&game_set->get_country_list()->at(ptr2->country1 - 1));
				continue;
			}
		}

		cout << endl;
	}

	// display continents
	//cout << endl << endl;
	cout << "**************************************************************************************" << endl;
	cout << "**************************************************************************************" << endl;
	cout << "\t\t\t\t    CONTINENTS" << endl;
	cout << "**************************************************************************************" << endl;
	cout << "**************************************************************************************" << endl;
	cout << endl;

	vector<struct continent>::iterator ptr3;
	for (ptr3 = game_set->get_continent_list()->begin(); ptr3 < game_set->get_continent_list()->end(); ptr3++) 
	{
		cout << "\t****************************************************************" << endl;
		cout << "\tcontinent : " << "(reward = " << ptr3->reward << ")" << endl;
		cout << "\t****************************************************************" << endl;
		vector<int>::iterator ptr4;
		for (ptr4 = ptr3->country_list.begin(); ptr4 < ptr3->country_list.end(); ptr4++) 
		{
			cout << "\tcountry : ";
			display_country_info(&game_set->get_country_list()->at(*ptr4 - 1));
		}
	}

	cout << endl;
	cout << "**************************************************************************************" << endl;
	cout << "**************************************************************************************" << endl;

}