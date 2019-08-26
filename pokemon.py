import pandas as pd
from random import randint
from math import sqrt

df1 = pd.read_csv('doc/database.csv')
df1.set_index('pokemon', inplace=True)

df2 = pd.read_csv('doc/typeTable.csv')
df2.set_index('type', inplace=True)

class Pokemon():
        
    #Constructor
    def __init__(self, name, pokeType, lvl, listSpell):
        pass

    #Methods
    def isKo(self):
        """
           Returns True if Pokemon is KO.
        """
        pass

    def attackPokemon(self, spell):
        """
            Returns spell power and spell type.
           :param 'spell': input string.
        """
        pass

    def takeDamage(self, spellType, spellPower, attacker):
        """
            Void method.
            :param 'spellType': str (return value of attackPokemon() method).
            :param 'spellPower': int (return value of attackPokemon() method).
            :param 'attacker': Pokemon objet. The one that attack.
        """
        pass 
