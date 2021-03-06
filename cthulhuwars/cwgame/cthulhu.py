"""
 The Great Cthulhu
 Starts in South Pacific
"""

from .player import Player
from .color import TextColor, NodeColor
from .unit import Unit, UnitType, UnitState, Faction, Monster, GreatOldOne
from .zone import Zone, GateState
from .diceRoller import DiceRoller

class Cthulhu(Player):
    def __init__(self, home_zone, board, name='Great Cthulhu'):
        super(Cthulhu, self).__init__(Faction.cthulhu, home_zone, board, name)
        self._deep_ones = set()
        self._shoggoth = set()
        self._starspawn = set()
        self._cthulhu = None
        self._immortal = False
        self._spell_dreams = False
        self._spell_yha_nthlei = False
        self._spell_devolve = False
        self._spell_regenerate = False
        self._spell_absorb = False
        self._spell_submerge = False
        self._color = TextColor.GREEN
        self._node_color = NodeColor.GREEN

        '''
        probability_dict overrides the probabilities in the Player class
        these are used to govern the weighted choices for actions in the 'wc'
        PlayerLogic methods
        '''
        self.probability_dict = {
            'capture': 0.1,
            'build': 0.2,
            'move': 0.2,
            'summon': 0.2,
            'recruit': 0.1,
            'combat': 0.2,
            'awaken': 0,
            'special': 0
        }
        self._brain.set_probabilities(self.probability_dict)

    def player_setup(self):
        super(Cthulhu, self).player_setup()
        n_deep_ones = 4
        n_shoggoth = 2
        n_starspawn = 2
        for _ in range(n_deep_ones):
            new_do = DeepOne(self, self._pool)
            self.add_unit(new_do)
            self._deep_ones.add(new_do)
            self._monsters.add(new_do)

        for _ in range(n_shoggoth):
            new_s = Shoggoth(self, self._pool)
            self.add_unit(new_s)
            self._shoggoth.add(new_s)
            self._monsters.add(new_s)

        for _ in range(n_starspawn):
            new_ss = Starspawn(self, self._pool)
            self.add_unit(new_ss)
            self._starspawn.add(new_ss)
            self._monsters.add(new_ss)

        self._cthulhu = GreatCthulhu(self, self._pool)
        self.add_unit(self._cthulhu)
        self._goo.add(self._cthulhu)
        self._monsters.add(self._cthulhu)

    def summon_deep_one(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for deep_one in self._deep_ones:
                if deep_one.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Deep One has surfaced!' + TextColor.ENDC)
                        deep_one.set_unit_state(UnitState.in_play)
                        deep_one.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_shoggoth(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for shog in self._shoggoth:
                if shog.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Shoggoth oozes forth!' + TextColor.ENDC)
                        shog.set_unit_state(UnitState.in_play)
                        shog.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_starspawn(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for ss in self._starspawn:
                if ss.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Starspawn reveals itself!' + TextColor.ENDC)
                        ss.set_unit_state(UnitState.in_play)
                        ss.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_cthulhu(self, unit_zone):
        unit_cost = 10
        if self._immortal:
            unit_cost = 4
        if self._home_zone.gate_state is not GateState.noGate:
            if self.power >= unit_cost:
                cthulhu = self._cthulhu
                assert isinstance(cthulhu, Unit)
                if cthulhu.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'The Great Cthulhu has emerged!' + TextColor.ENDC)
                        cthulhu.set_unit_state(UnitState.in_play)
                        cthulhu.set_unit_zone(self._home_zone)
                        self._immortal = True
                        self.draw_elder_sign()
                        return True
        return False

    def summon_action(self, monster, unit_zone):
        assert isinstance(monster, Unit)
        if monster.unit_state is UnitState.in_reserve:
            if monster.unit_type is UnitType.cthulhu:
                return self.summon_cthulhu(unit_zone)
            if monster.unit_type is UnitType.deep_one:
                return self.summon_deep_one(unit_zone)
            if monster.unit_type is UnitType.shoggoth:
                return self.summon_shoggoth(unit_zone)
            if monster.unit_type is UnitType.star_spawn:
                return self.summon_starspawn(unit_zone)
        return False

class DeepOne(Monster):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(DeepOne, self).__init__(unit_parent, unit_zone, UnitType.deep_one, combat_power=1, cost=unit_cost,
                                      base_movement=1,
                                      unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, id(self))],
            "params": [("string", "dso", "cultist.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition


class Shoggoth(Monster):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Shoggoth, self).__init__(unit_parent, unit_zone, UnitType.shoggoth, combat_power=2, cost=unit_cost,
                                       base_movement=1,
                                       unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, id(self))],
            "params": [("string", "dso", "cultist.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition


class Starspawn(Monster):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Starspawn, self).__init__(unit_parent, unit_zone, UnitType.star_spawn, combat_power=3, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, id(self) )],
            "params": [("string", "dso", "cultist.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition


class GreatCthulhu(GreatOldOne):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(GreatCthulhu, self).__init__(unit_parent, unit_zone, UnitType.cthulhu, combat_power=6, cost=unit_cost,
                                           base_movement=1,
                                           unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, id(self))],
            "params": [("string", "dso", "cthulhu_goo.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition
