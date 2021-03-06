import copy


class InvadeAction:

    def __init__(self,country_from, country_to, troops, game_status, winner, reward):
        self.country_from = country_from
        self.country_to = country_to
        self.troops = troops
        self.game_status = game_status
        self.winner = winner
        self.reward = reward

    def repJson(self):
        return dict(change=1,
                    type="invade",
                    from_country=self.country_from,
                    to_country=self.country_to,
                    troops=self.troops,
                    reward=self.reward,
                    game_status=self.game_status.name,
                    winner=self.winner.name)

    def __str__(self):
        return str(self.repJson())

    def __deepcopy__(self, memodict={}):
        return InvadeAction(copy.deepcopy(self.country_from),
                            copy.deepcopy(self.country_to),
                            copy.deepcopy(self.troops),
                            copy.deepcopy(self.game_status),
                            copy.deepcopy(self.winner),
                            copy.deepcopy(self.reward))

class MarchAction:

    def __init__(self,country_from, country_to, troops):
        self.country_from = country_from
        self.country_to = country_to
        self.troops = troops

    def repJson(self):
        return dict(change=1,
                    type="march",
                    from_country=self.country_from,
                    to_country=self.country_to,
                    count=self.troops)

    def __str__(self):
        return str(self.repJson())

    def __deepcopy__(self, memodict={}):
        return MarchAction(copy.deepcopy(self.country_from),
                            copy.deepcopy(self.country_to),
                            copy.deepcopy(self.troops))


class DeployAction:

    def __init__(self, country_to, troops):
        self.country_to = country_to
        self.troops = troops

    def repJson(self):
        return dict(change=1,
                    type="deploy",
                    target=self.country_to,
                    count=self.troops)

    def __str__(self):
        return str(self.repJson())

    def __deepcopy__(self, memodict={}):
        return DeployAction(copy.deepcopy(self.country_to),
                            copy.deepcopy(self.troops))


class NoAction:

    def repJson(self):
        return dict(change=0)

    def __str__(self):
        return str(self.repJson())

    def __deepcopy__(self, memodict={}):
        return NoAction()
