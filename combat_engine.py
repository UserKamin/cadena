import random
from typing import Dict, List
from models import Character


class CombatEngine:
    """Handles turn-based combat simulation"""

    def __init__(self):
        self.combat_log: List[str] = []

    def calculate_hit_chance(self, attacker: Character, defender: Character) -> float:
        """Calculate hit chance based on attacker DEX vs defender DEX"""
        # Base 50% + (attacker_dex - defender_dex) * 3%
        # Clamped between 5% and 95%
        base_chance = 0.5
        dex_difference = attacker.dexterity - defender.dexterity
        hit_chance = base_chance + (dex_difference * 0.03)
        return max(0.05, min(0.95, hit_chance))

    def calculate_damage(self, attacker: Character) -> int:
        """Calculate base damage from STR with some randomization"""
        base_damage = attacker.strength
        # Add some variance: 80% to 120% of base damage
        variance = random.uniform(0.8, 1.2)
        return max(1, int(base_damage * variance))

    def attack(self, attacker: Character, defender: Character) -> Dict:
        """Perform an attack and return result details"""
        if not attacker.is_alive:
            return {"hit": False, "damage": 0, "message": f"{attacker.name} is defeated and cannot attack!"}

        hit_chance = self.calculate_hit_chance(attacker, defender)
        hit_roll = random.random()

        if hit_roll <= hit_chance:
            damage = self.calculate_damage(attacker)
            actual_damage = defender.take_damage(damage)

            message = f"{attacker.name} hits {defender.name} for {actual_damage} damage!"
            if not defender.is_alive:
                message += f" {defender.name} is defeated!"

            return {
                "hit": True,
                "damage": actual_damage,
                "message": message,
                "hit_chance": hit_chance
            }
        else:
            return {
                "hit": False,
                "damage": 0,
                "message": f"{attacker.name} misses {defender.name}!",
                "hit_chance": hit_chance
            }

    def determine_turn_order(self, participants: List[Character]) -> List[Character]:
        """Sort participants by AGI (highest first), with random tiebreaker"""
        return sorted(participants, key=lambda x: (x.agility, random.random()), reverse=True)

    def process_turn(self, character: Character):
        """Process end-of-turn effects (mana regeneration)"""
        if character.is_alive:
            mana_regen = character.regenerate_mana()
            if mana_regen > 0 and hasattr(self, '_detailed_log') and self._detailed_log:
                self.log(f"{character.name} regenerates {mana_regen} mana.")

    def log(self, message: str):
        """Add message to combat log"""
        self.combat_log.append(message)

    def clear_log(self):
        """Clear the combat log"""
        self.combat_log.clear()

    def get_combat_log(self) -> List[str]:
        """Get copy of combat log"""
        return self.combat_log.copy()
