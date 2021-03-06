from action.action import DeployAction, MarchAction, InvadeAction
from environment.GameEnums import *
from utilities.Parser import *
from environment.Encoders import Encoder
import copy
import json
import math


class Environment:

    INVASION_REWARD = 2

    def __init__(self, map_config_file=None, pop_config_file=None, game_status=None, winner=None,
                 country_list=None, border_list=None, continent_list=None, adj_list=None, change=None, reserve_1 = 0, reserve_2 = 0):

        self.reserve_1 = reserve_1
        self.reserve_2 = reserve_2
        self.change = change

        if map_config_file is None or pop_config_file is None:
            self.__game_status = game_status
            self.__winner = winner
            self.__country_list = country_list
            self.__border_list = border_list
            self.__continent_list = continent_list
            self.__adj_list = adj_list
        else:
            self.__game_status = GameStatus.ONGOING
            self.__winner = GamePlayId.NONE
            self.__country_list, self.__border_list, self.__continent_list \
                = self.__readconfigfiles__(map_config_file, pop_config_file)
            for i, continent in enumerate(self.continent_list):
                for country_id in continent.country_list:
                    self.country_list[country_id - 1].continent_id = i+1
            self.__adj_list = self.__make_adj_list()

    def __deepcopy__(self, memodict={}):
        return Environment(game_status=copy.deepcopy(self.__game_status, memodict),
                           winner=copy.deepcopy(self.__winner, memodict),
                           continent_list=copy.deepcopy(self.__continent_list, memodict),
                           country_list=copy.deepcopy(self.__country_list, memodict),
                           border_list=copy.deepcopy(self.__border_list, memodict),
                           adj_list=copy.deepcopy(self.__adj_list, memodict),
                           reserve_1=copy.deepcopy(self.reserve_1, memodict),
                           reserve_2=copy.deepcopy(self.reserve_2, memodict),
                           change=copy.deepcopy(self.change, memodict))

    def __str__(self):
        strg = "country list:\n"
        for country in self.country_list:
            strg += json.dumps(country, cls=Encoder) + "\n"
        strg += "\ncontinent list:\n"
        for continent in self.continent_list:
            strg += json.dumps(continent, cls=Encoder) + "\n"
        strg += "\n" + str(self.game_status) + "\n------------*****-----------" + "\n"
        return strg

    def __make_adj_list(self):
        adj_list = dict()
        for country in self.__country_list:
            adj_list[country.id] = []
        for border in self.__border_list:
            adj_list[border.country1].append(self.country_list[border.country2 - 1])
            adj_list[border.country2].append(self.country_list[border.country1 - 1])
        return adj_list

    def reprJson(self):
        return dict(game_status=self.__game_status.name,
                    winner=self.__winner.name,
                    country_list=self.country_list,
                    border_list=self.border_list,
                    continent_list=self.continent_list,
                    reserve_1=self.reserve_1,
                    reserve_2=self.reserve_2)

    def __readconfigfiles__(self, map_config_file, pop_config_file):
        read_data_map = MapFileParser(map_config_file)
        read_data_pop = PopFileParser(pop_config_file)
        return read_data_pop.obtain_country_list(), read_data_map.obtain_border_list()\
            , read_data_map.obtain_continent_list()

    def __border_exists(self, country1_id, country2_id):
        for border in self.border_list:
            if(border.country1 == country1_id and border.country2 == country2_id) or (border.country1 == country2_id and border.country2 == country1_id):
                return True
        return False

    def __is_owner(self, test_player_id , country_id):
        return self.country_list[country_id - 1].owner_id == test_player_id

    def __game_ended(self,test_player_id):
        for country in self.country_list:
            if country.owner_id != test_player_id:
                return False
        return True

    def __is_continent_new_owner(self,test_player_id , continent_id):
        if self.continent_list[continent_id - 1].owner_id == test_player_id :
            return 0
        for country_id in self.continent_list[continent_id - 1].country_list:
            if self.country_list[country_id -1].owner_id != test_player_id:
                return 0
        return 1

    @property
    def adj_list(self):
        return self.__adj_list

    @property
    def game_status(self):
        return self.__game_status

    @game_status.setter
    def game_status(self, game_status):
        self.__game_status = game_status


    @property
    def winner(self):
        return self.__winner

    @property
    def country_list(self):
        return self.__country_list

    @property
    def border_list(self):
        return self.__border_list

    @property
    def continent_list(self):
        return self.__continent_list

    def deploy_reserve_troops(self, owner_id, target_country_id):
        if not self.__is_owner(owner_id, target_country_id):
            raise ValueError("Can't deploy troops to unowned country : country owner ("
                             + str(self.country_list[target_country_id - 1].owner_id) + ") ,"
                             + "player " + str(owner_id) + ")")

        if owner_id == GamePlayId.P1:
            if self.reserve_1 > 0:
                self.country_list[target_country_id - 1].troops_count += self.reserve_1
                self.change = DeployAction(target_country_id, self.reserve_1)
                self.reserve_1 = 0
            else:
                raise ValueError("no troops to deploy")
        else:
            if self.reserve_2 > 0:
                self.country_list[target_country_id - 1].troops_count += self.reserve_2
                self.change = DeployAction(target_country_id, self.reserve_2)
                self.reserve_2 = 0
            else:
                raise ValueError("no troops to deploy")

    def march_troops(self, owner_id, from_country_id, to_country_id, troops_count):

        if troops_count == 0.9:
            troops_count = self.country_list[from_country_id - 1].troops_count - 1

        if troops_count < 1:
            troops_count = math.floor(self.country_list[from_country_id - 1].troops_count * troops_count)

        if not self.__is_owner(owner_id, from_country_id):
            raise ValueError("Can't march troops from unowned country : country owner ("
                             + str(self.country_list[from_country_id - 1].owner_id) + ") ,"
                             + "player (" + str(owner_id) + ")")
        if not self.__is_owner(owner_id, to_country_id):
            raise ValueError("Can't march troops to unowned country : country owner ("
                             + str(self.country_list[to_country_id - 1].owner_id) + ") ,"
                             + "player (" + str(owner_id) + ")")
        if self.country_list[from_country_id - 1].troops_count - troops_count < 1:
            raise ValueError("Not enough troops to march from ( " + str(from_country_id)
                             + " ) to ( " + str(to_country_id) + " ) troops are in country are "
                             + str(self.country_list[from_country_id - 1].troops_count))
        if not self.__border_exists(from_country_id,to_country_id):
            raise ValueError("Can't march no route from ( " + str(from_country_id)
                             + " ) to ( " + str(to_country_id) + " )")

        self.change = MarchAction(from_country_id, to_country_id, troops_count)
        self.country_list[from_country_id - 1].troops_count -= troops_count
        self.country_list[to_country_id - 1].troops_count += troops_count

    def invade(self, owner_id, from_country_id, to_country_id, troops):

        if troops > 1:
            if self.country_list[to_country_id - 1].troops_count >= troops \
                    or self.country_list[from_country_id - 1].troops_count <= troops:
                raise ValueError("Not enough troops not invade with")

        if troops > 1:
            troops = troops - self.country_list[to_country_id - 1].troops_count

        if troops == 0.9:
            troops = self.country_list[from_country_id - 1].troops_count \
                     - self.country_list[to_country_id - 1].troops_count - 1
        elif troops < 1:
            troops = math.floor((self.country_list[from_country_id - 1].troops_count -
                                 self.country_list[to_country_id - 1].troops_count) * troops)
        if troops < 1:
            raise ValueError("Not enough troops not invade with")

        if self.__is_owner(owner_id, from_country_id) and self.__is_owner(owner_id, to_country_id):
            raise ValueError("Can't invade your own country")
        if not self.__border_exists(from_country_id,to_country_id):
            raise ValueError("Can't invade no route from ( " + str(from_country_id)
                             + " ) to ( " + str(to_country_id) + " )")
        if not self.__is_owner(owner_id, from_country_id):
            raise ValueError("Can't invade from unowned country : country owner ("
                             + str(self.country_list[from_country_id - 1].owner_id) + ") ,"
                             + "player (" + str(owner_id) + ")")

        troops_action = troops + self.country_list[to_country_id - 1].troops_count

        self.country_list[from_country_id - 1].troops_count -= troops + self.country_list[to_country_id - 1].troops_count
        self.country_list[to_country_id - 1].troops_count = troops
        self.country_list[to_country_id - 1].owner_id = owner_id

        continent_id = self.country_list[to_country_id - 1].continent_id
        reward = self.INVASION_REWARD

        if self.__is_continent_new_owner(owner_id, continent_id):
                self.continent_list[continent_id - 1].owner_id = owner_id
                reward += self.continent_list[continent_id - 1].reward

        if self.__game_ended(owner_id):
            self.__game_status = GameStatus.ENDED
            self.__winner = owner_id

        if owner_id == GamePlayId.P1:
            self.reserve_1 += reward
        else:
            self.reserve_2 += reward

        self.change = InvadeAction(from_country_id, to_country_id, troops_action , self.game_status, self.winner, reward)
