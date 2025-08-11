import random
from typing import Dict, List


class CombatSimulation:
    """Main combat simulation controller"""

    def __init__(self, character_manager):
        self.char_manager = character_manager
        from combat_engine import CombatEngine  # Fixed: import here
        self.combat_engine = CombatEngine()

    def simulate_combat(self, player_name: str, enemies: List[Character],
                        max_rounds: int = 100, detailed_log: bool = True) -> Dict:
        """
        Simulate combat between player and enemies
        Returns combat result and statistics
        """
        player = self.char_manager.get_character(player_name)
        if not player:
            return {"error": f"Player character '{player_name}' not found"}

        # Reset all participants to full health/mana
        player.reset_to_full()
        for enemy in enemies:
            enemy.reset_to_full()

        self.combat_engine.clear_log()
        self.combat_engine._detailed_log = detailed_log

        # Combat setup
        all_participants = [player] + enemies
        self.combat_engine.log(f"=== COMBAT START ===")
        self.combat_engine.log(f"Player: {player}")
        self.combat_engine.log(f"Enemies: {len(enemies)}")
        for i, enemy in enumerate(enemies, 1):
            self.combat_engine.log(f"  {i}. {enemy}")
        self.combat_engine.log("")

        round_count = 0

        # Main combat loop
        while round_count < max_rounds:
            round_count += 1

            # Check win conditions
            living_enemies = [e for e in enemies if e.is_alive]
            if not player.is_alive:
                result = CombatResult.DEFEAT
                break
            elif not living_enemies:
                result = CombatResult.VICTORY
                break

            if detailed_log:
                self.combat_engine.log(f"--- Round {round_count} ---")

            # Determine turn order (only living participants)
            living_participants = [p for p in all_participants if p.is_alive]
            turn_order = self.combat_engine.determine_turn_order(
                living_participants)

            # Execute turns
            for character in turn_order:
                if not character.is_alive:
                    continue

                if character == player:
                    # Player attacks random living enemy
                    if living_enemies:
                        target = random.choice(living_enemies)
                        attack_result = self.combat_engine.attack(
                            player, target)
                        if detailed_log:
                            self.combat_engine.log(attack_result["message"])

                        # Update living enemies list
                        living_enemies = [e for e in enemies if e.is_alive]
                else:
                    # Enemy attacks player
                    if player.is_alive:
                        attack_result = self.combat_engine.attack(
                            character, player)
                        if detailed_log:
                            self.combat_engine.log(attack_result["message"])

                # Process end-of-turn effects
                self.combat_engine.process_turn(character)

                # Check if combat ended this turn
                if not player.is_alive or not any(e.is_alive for e in enemies):
                    break
        else:
            # Max rounds reached
            result = CombatResult.ONGOING
            self.combat_engine.log(
                f"Combat ended after {max_rounds} rounds (timeout)")

        # Final results
        living_enemies = [e for e in enemies if e.is_alive]

        self.combat_engine.log(f"\n=== COMBAT END ===")
        self.combat_engine.log(f"Result: {result.value.upper()}")
        self.combat_engine.log(f"Rounds: {round_count}")
        self.combat_engine.log(
            f"Player HP: {player.current_hp}/{player.max_hp}")
        self.combat_engine.log(
            f"Enemies remaining: {len(living_enemies)}/{len(enemies)}")

        return {
            "result": result,
            "rounds": round_count,
            "player_final_hp": player.current_hp,
            "player_max_hp": player.max_hp,
            "enemies_defeated": len(enemies) - len(living_enemies),
            "total_enemies": len(enemies),
            "combat_log": self.combat_engine.get_combat_log()
        }
