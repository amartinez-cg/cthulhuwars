from .player import Player
from .color import TextColor, NodeColor
from .unit import Unit, UnitType, UnitState, Faction, Monster, GreatOldOne
from .zone import Zone, GateState

# Yellow Sign
# Starts in Europe

class YellowSign(Player):
    def __init__(self, home_zone, board, name='The Yellow Sign'):
        super(YellowSign, self).__init__(Faction.yellow_sign, home_zone, board, name)
        self._undead = set()
        self._byakhee = set()
        self._hastur = None
        self._king_in_yellow = None

        self._undead_in_play = 0
        self._byakhee_in_play = 0
        self._king_in_yellow_in_play = 0
        self._hastur_in_play = 0
        self._spell_the_third_eye = False
        self._spell_he_who_is_not_to_be_named = False
        self._spell_shriek_of_the_byakhee = False
        self._spell_zingaya = False
        self._spell_passion = False
        self._spell_the_screaming_dead = False
        self._color = TextColor.YELLOW

        self._node_color = NodeColor.YELLOW

    def player_setup(self):
        super(YellowSign, self).player_setup()
        n_undead = 6
        n_byakhee = 4

        for _ in range(n_undead):
            new_u = Undead(self, self._pool)
            self.add_unit(new_u)
            self._undead.add(new_u)

        for _ in range(n_byakhee):
            new_b = Byakhee(self, self._pool)
            self.add_unit(new_b)
            self._byakhee.add(new_b)

        self._hastur = Hastur(self, self._pool)
        self.add_unit(self._hastur)
        self._goo.add(self._hastur)
        self._monsters.add(self._hastur)

        self._king_in_yellow = KingInYellow(self, self._pool)
        self.add_unit(self._king_in_yellow)
        self._goo.add(self._king_in_yellow)
        self._monsters.add(self._king_in_yellow)

    def determine_combat_power(self, units):
        total_combat_power = 0
        n_undead = 0
        n_byakhee = 0
        for unit in units:
            assert isinstance(unit, Unit)
            total_combat_power += unit.combat_power
            if unit.unit_type is UnitType.undead:
                n_undead += 1
            if unit.unit_type is UnitType.byakhee:
                n_byakhee += 1

        if n_undead > 0:
            total_combat_power -= 1
        if n_byakhee > 0:
            total_combat_power += 1

        return total_combat_power

class Undead(Monster):
    def __init__(self, unit_parent, unit_zone, unit_cost=1):
        super(Undead, self).__init__(unit_parent, unit_zone, UnitType.undead, combat_power=1, cost=unit_cost,
                                     base_movement=1,
                                     unit_state=UnitState.in_reserve)
    '''
    @property
    def combat_power(self):
        total = 0
        units = list(set(self.faction.my_units_in_zone(self.unit_zone)))
        for unit in units:
            if unit.unit_type is UnitType.undead and unit.unit_state is UnitState.in_play:
                total += 1
            units.remove(unit)
        self.set_combat_power(total-1)
        return total
    '''

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, id(self))],
            "params": [("string", "dso", "cultist.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition

class Byakhee(Monster):
    def __init__(self, unit_parent, unit_zone, unit_cost=2):
        super(Byakhee, self).__init__(unit_parent, unit_zone, UnitType.byakhee, combat_power=1, cost=unit_cost,
                                      base_movement=1,
                                      unit_state=UnitState.in_reserve)
    '''
    @property
    def combat_power(self):
        total = 0
        units = list(set(self.faction.my_units_in_zone(self.unit_zone)))
        for unit in units:
            if unit.unit_type is UnitType.byakhee and unit.unit_state is UnitState.in_play:
                total += 1
            units.remove(unit)
        self.set_combat_power(total+1)
        return total
    '''

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, id(self))],
            "params": [("string", "dso", "cultist.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition

class Hastur(GreatOldOne):
    def __init__(self, unit_parent, unit_zone, unit_cost=10):
        super(Hastur, self).__init__(unit_parent, unit_zone, UnitType.hastur, combat_power=5, cost=unit_cost,
                                      base_movement=1,
                                      unit_state=UnitState.in_reserve)
    @property
    def combat_power(self):
        return 5

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, id(self))],
            "params": [("string", "dso", "cultist.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition

class KingInYellow(GreatOldOne):
    def __init__(self, unit_parent, unit_zone, unit_cost=4):
        super(KingInYellow, self).__init__(unit_parent, unit_zone, UnitType.king_in_yellow, combat_power=0,
                                      cost=unit_cost,
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
