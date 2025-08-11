from typing import Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class CombatResult(Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"
    ONGOING = "ongoing"


@dataclass
class Character:
    """Character class with all stats and combat properties"""
    name: str
    level: int = 1
    title: str = ""

    # Base stats
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    wisdom: int = 10
    agility: int = 10
    constitution: int = 10

    # Combat properties (calculated from base stats)
    current_hp: Optional[int] = None
    current_mana: Optional[int] = None

    def __post_init__(self):
        """Initialize calculated properties after object creation"""
        if self.current_hp is None:
            self.current_hp = self.max_hp
        if self.current_mana is None:
            self.current_mana = self.max_mana

    @property
    def max_hp(self) -> int:
        """HP = Constitution * 2"""
        return self.constitution * 2

    @property
    def max_mana(self) -> int:
        """Mana = Intelligence"""
        return self.intelligence

    @property
    def mana_regen(self) -> int:
        """Mana regeneration per turn = Wisdom"""
        return self.wisdom

    @property
    def is_alive(self) -> bool:
        """Check if character is still alive"""
        return self.current_hp > 0

    def heal(self, amount: int) -> int:
        """Heal character and return actual amount healed"""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp

    def take_damage(self, damage: int) -> int:
        """Apply damage and return actual damage taken"""
        actual_damage = min(damage, self.current_hp)
        self.current_hp = max(0, self.current_hp - damage)
        return actual_damage

    def regenerate_mana(self) -> int:
        """Regenerate mana based on wisdom, return amount regenerated"""
        old_mana = self.current_mana
        self.current_mana = min(
            self.max_mana, self.current_mana + self.mana_regen)
        return self.current_mana - old_mana

    def spend_mana(self, amount: int) -> bool:
        """Try to spend mana, return True if successful"""
        if self.current_mana >= amount:
            self.current_mana -= amount
            return True
        return False

    def reset_to_full(self):
        """Reset HP and mana to maximum"""
        self.current_hp = self.max_hp
        self.current_mana = self.max_mana

    def get_display_name(self) -> str:
        """Get formatted display name with title and level"""
        title_part = f"{self.title} " if self.title else ""
        return f"{title_part}{self.name} (Lv.{self.level})"

    def to_dict(self) -> Dict:
        """Convert character to dictionary for saving"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        """Create character from dictionary"""
        return cls(**data)

    def __str__(self) -> str:
        return (f"{self.get_display_name()}\n"
                f"STR:{self.strength} DEX:{self.dexterity} INT:{self.intelligence} "
                f"WIS:{self.wisdom} AGI:{self.agility} CON:{self.constitution}\n"
                f"HP:{self.current_hp}/{self.max_hp} MP:{self.current_mana}/{self.max_mana}")
