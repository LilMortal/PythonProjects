#!/usr/bin/env python3
"""
Dice Rolling Simulator
A comprehensive dice rolling application with multiple game modes and dice types.
Compatible with Python 3.10+
"""

import random
import time
import sys
from typing import List, Tuple, Dict, Optional


class DiceSimulator:
    """Main dice simulator class with various rolling modes and dice types."""
    
    def __init__(self):
        self.roll_history: List[Dict] = []
        self.custom_dice: Dict[str, List[int]] = {}
        
    def roll_standard_dice(self, sides: int = 6, count: int = 1) -> List[int]:
        """Roll standard dice with specified sides and count."""
        if sides < 2:
            raise ValueError("Dice must have at least 2 sides")
        if count < 1:
            raise ValueError("Must roll at least 1 die")
        
        results = [random.randint(1, sides) for _ in range(count)]
        self._add_to_history("Standard", f"{count}d{sides}", results)
        return results
    
    def roll_custom_dice(self, face_values: List[int], count: int = 1) -> List[int]:
        """Roll custom dice with specified face values."""
        if len(face_values) < 2:
            raise ValueError("Custom dice must have at least 2 faces")
        if count < 1:
            raise ValueError("Must roll at least 1 die")
        
        results = [random.choice(face_values) for _ in range(count)]
        self._add_to_history("Custom", f"{count} dice with faces {face_values}", results)
        return results
    
    def roll_advantage_disadvantage(self, sides: int = 20, advantage: bool = True) -> Tuple[List[int], int]:
        """Roll with advantage (take higher) or disadvantage (take lower)."""
        rolls = self.roll_standard_dice(sides, 2)
        result = max(rolls) if advantage else min(rolls)
        mode = "Advantage" if advantage else "Disadvantage"
        self._add_to_history(mode, f"2d{sides}", rolls, result)
        return rolls, result
    
    def roll_with_modifier(self, sides: int = 20, count: int = 1, modifier: int = 0) -> Tuple[List[int], int]:
        """Roll dice and apply a modifier to the total."""
        rolls = self.roll_standard_dice(sides, count)
        total = sum(rolls) + modifier
        self._add_to_history("Modified", f"{count}d{sides}+{modifier}", rolls, total)
        return rolls, total
    
    def roll_drop_lowest(self, sides: int = 6, count: int = 4, drop: int = 1) -> Tuple[List[int], List[int], int]:
        """Roll multiple dice and drop the lowest values."""
        if drop >= count:
            raise ValueError("Cannot drop more dice than rolled")
        
        all_rolls = self.roll_standard_dice(sides, count)
        sorted_rolls = sorted(all_rolls, reverse=True)
        kept_rolls = sorted_rolls[:-drop] if drop > 0 else sorted_rolls
        total = sum(kept_rolls)
        
        self._add_to_history("Drop Lowest", f"{count}d{sides} drop {drop}", all_rolls, total)
        return all_rolls, kept_rolls, total
    
    def roll_exploding_dice(self, sides: int = 6, count: int = 1, explode_on: Optional[int] = None) -> Tuple[List[int], int]:
        """Roll exploding dice (roll again on max value or specified value)."""
        if explode_on is None:
            explode_on = sides
        
        all_rolls = []
        for _ in range(count):
            die_rolls = []
            roll = random.randint(1, sides)
            die_rolls.append(roll)
            
            # Keep rolling while we get the exploding value
            while roll == explode_on:
                roll = random.randint(1, sides)
                die_rolls.append(roll)
            
            all_rolls.extend(die_rolls)
        
        total = sum(all_rolls)
        self._add_to_history("Exploding", f"{count}d{sides} explode on {explode_on}", all_rolls, total)
        return all_rolls, total
    
    def create_custom_dice(self, name: str, face_values: List[int]) -> None:
        """Create and save a custom dice type."""
        if len(face_values) < 2:
            raise ValueError("Custom dice must have at least 2 faces")
        self.custom_dice[name] = face_values
    
    def roll_saved_custom_dice(self, name: str, count: int = 1) -> List[int]:
        """Roll a previously saved custom dice type."""
        if name not in self.custom_dice:
            raise ValueError(f"Custom dice '{name}' not found")
        return self.roll_custom_dice(self.custom_dice[name], count)
    
    def _add_to_history(self, roll_type: str, description: str, rolls: List[int], result: Optional[int] = None) -> None:
        """Add a roll to the history."""
        self.roll_history.append({
            'type': roll_type,
            'description': description,
            'rolls': rolls.copy(),
            'result': result or sum(rolls),
            'timestamp': time.strftime('%H:%M:%S')
        })
    
    def get_statistics(self) -> Dict:
        """Get rolling statistics from history."""
        if not self.roll_history:
            return {}
        
        all_rolls = []
        for entry in self.roll_history:
            all_rolls.extend(entry['rolls'])
        
        return {
            'total_rolls': len(self.roll_history),
            'total_dice': len(all_rolls),
            'average': sum(all_rolls) / len(all_rolls),
            'highest': max(all_rolls),
            'lowest': min(all_rolls),
            'most_common': max(set(all_rolls), key=all_rolls.count)
        }
    
    def clear_history(self) -> None:
        """Clear the roll history."""
        self.roll_history.clear()


def print_animated_roll(duration: float = 1.0) -> None:
    """Print an animated dice rolling effect."""
    frames = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for frame in frames:
            print(f"\r🎲 Rolling... {frame}", end="", flush=True)
            time.sleep(0.1)
    print("\r" + " " * 20 + "\r", end="")  # Clear the line


def display_results(rolls: List[int], description: str, total: Optional[int] = None, 
                   additional_info: str = "") -> None:
    """Display roll results in a formatted way."""
    print(f"\n🎲 {description}")
    print(f"   Rolls: {rolls}")
    if total is not None and total != sum(rolls):
        print(f"   Total: {sum(rolls)} → {total}")
    else:
        print(f"   Total: {total or sum(rolls)}")
    if additional_info:
        print(f"   {additional_info}")


def main_menu() -> None:
    """Display the main menu options."""
    print("\n" + "="*50)
    print("🎲 DICE ROLLING SIMULATOR 🎲")
    print("="*50)
    print("1. Roll Standard Dice")
    print("2. Roll with Advantage/Disadvantage")
    print("3. Roll with Modifier")
    print("4. Roll and Drop Lowest")
    print("5. Roll Exploding Dice")
    print("6. Create Custom Dice")
    print("7. Roll Custom Dice")
    print("8. View Roll History")
    print("9. View Statistics")
    print("10. Quick Rolls (Common Games)")
    print("11. Clear History")
    print("0. Exit")
    print("-" * 50)


def quick_rolls_menu() -> None:
    """Display quick roll options for common games."""
    print("\n🎮 QUICK ROLLS FOR COMMON GAMES")
    print("-" * 40)
    print("1. D&D Ability Scores (4d6 drop lowest)")
    print("2. D&D Attack Roll (1d20)")
    print("3. D&D Damage (Various)")
    print("4. Yahtzee (5d6)")
    print("5. Monopoly (2d6)")
    print("6. Risk Attack (3d6)")
    print("7. Farkle (6d6)")
    print("8. Back to Main Menu")


def handle_quick_rolls(simulator: DiceSimulator, choice: str) -> None:
    """Handle quick roll selections."""
    print_animated_roll(0.8)
    
    if choice == '1':  # D&D Ability Scores
        all_rolls, kept_rolls, total = simulator.roll_drop_lowest(6, 4, 1)
        display_results(all_rolls, "D&D Ability Score", total, f"Kept: {kept_rolls}")
    
    elif choice == '2':  # D&D Attack Roll
        rolls = simulator.roll_standard_dice(20, 1)
        display_results(rolls, "D&D Attack Roll (1d20)")
    
    elif choice == '3':  # D&D Damage
        print("Common D&D damage rolls:")
        print("a) Dagger (1d4)")
        print("b) Shortsword (1d6)")
        print("c) Longsword (1d8)")
        print("d) Greatsword (2d6)")
        damage_choice = input("Choose damage type (a-d): ").lower()
        
        if damage_choice == 'a':
            rolls = simulator.roll_standard_dice(4, 1)
            display_results(rolls, "Dagger Damage (1d4)")
        elif damage_choice == 'b':
            rolls = simulator.roll_standard_dice(6, 1)
            display_results(rolls, "Shortsword Damage (1d6)")
        elif damage_choice == 'c':
            rolls = simulator.roll_standard_dice(8, 1)
            display_results(rolls, "Longsword Damage (1d8)")
        elif damage_choice == 'd':
            rolls = simulator.roll_standard_dice(6, 2)
            display_results(rolls, "Greatsword Damage (2d6)")
    
    elif choice == '4':  # Yahtzee
        rolls = simulator.roll_standard_dice(6, 5)
        display_results(rolls, "Yahtzee Roll (5d6)")
    
    elif choice == '5':  # Monopoly
        rolls = simulator.roll_standard_dice(6, 2)
        display_results(rolls, "Monopoly Roll (2d6)")
    
    elif choice == '6':  # Risk Attack
        rolls = simulator.roll_standard_dice(6, 3)
        display_results(rolls, "Risk Attack (3d6)")
    
    elif choice == '7':  # Farkle
        rolls = simulator.roll_standard_dice(6, 6)
        display_results(rolls, "Farkle Roll (6d6)")


def get_positive_int(prompt: str, min_val: int = 1) -> int:
    """Get a positive integer from user input with validation."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"Please enter a number >= {min_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")


def main():
    """Main application loop."""
    simulator = DiceSimulator()
    
    print("Welcome to the Dice Rolling Simulator!")
    print("Roll various types of dice with different game modes.")
    
    while True:
        try:
            main_menu()
            choice = input("Choose an option (0-11): ").strip()
            
            if choice == '0':
                print("\n🎲 Thanks for using Dice Rolling Simulator! 🎲")
                sys.exit(0)
            
            elif choice == '1':  # Standard Dice
                sides = get_positive_int("Number of sides (default 6): ") or 6
                count = get_positive_int("Number of dice (default 1): ") or 1
                
                print_animated_roll()
                rolls = simulator.roll_standard_dice(sides, count)
                display_results(rolls, f"Standard Roll ({count}d{sides})")
            
            elif choice == '2':  # Advantage/Disadvantage
                sides = get_positive_int("Number of sides (default 20): ") or 20
                adv_choice = input("Advantage (a) or Disadvantage (d)? ").lower()
                advantage = adv_choice.startswith('a')
                
                print_animated_roll()
                rolls, result = simulator.roll_advantage_disadvantage(sides, advantage)
                mode = "Advantage" if advantage else "Disadvantage"
                display_results(rolls, f"{mode} Roll (2d{sides})", result)
            
            elif choice == '3':  # Roll with Modifier
                sides = get_positive_int("Number of sides (default 20): ") or 20
                count = get_positive_int("Number of dice (default 1): ") or 1
                modifier = int(input("Modifier (can be negative): ") or "0")
                
                print_animated_roll()
                rolls, total = simulator.roll_with_modifier(sides, count, modifier)
                display_results(rolls, f"Modified Roll ({count}d{sides}+{modifier})", total)
            
            elif choice == '4':  # Drop Lowest
                sides = get_positive_int("Number of sides (default 6): ") or 6
                count = get_positive_int("Number of dice (default 4): ") or 4
                drop = get_positive_int("Number to drop (default 1): ") or 1
                
                if drop >= count:
                    print("Cannot drop more dice than rolled!")
                    continue
                
                print_animated_roll()
                all_rolls, kept_rolls, total = simulator.roll_drop_lowest(sides, count, drop)
                display_results(all_rolls, f"Drop Lowest ({count}d{sides} drop {drop})", 
                              total, f"Kept: {kept_rolls}")
            
            elif choice == '5':  # Exploding Dice
                sides = get_positive_int("Number of sides (default 6): ") or 6
                count = get_positive_int("Number of dice (default 1): ") or 1
                explode_input = input(f"Explode on value (default {sides}): ")
                explode_on = int(explode_input) if explode_input else sides
                
                print_animated_roll()
                rolls, total = simulator.roll_exploding_dice(sides, count, explode_on)
                display_results(rolls, f"Exploding Dice ({count}d{sides} explode on {explode_on})", total)
            
            elif choice == '6':  # Create Custom Dice
                name = input("Enter name for custom dice: ").strip()
                if not name:
                    print("Name cannot be empty!")
                    continue
                
                print("Enter face values separated by spaces (e.g., 1 3 5 7 9):")
                face_input = input("Face values: ")
                try:
                    face_values = [int(x) for x in face_input.split()]
                    simulator.create_custom_dice(name, face_values)
                    print(f"✅ Custom dice '{name}' created with faces: {face_values}")
                except ValueError:
                    print("Invalid face values! Please enter numbers separated by spaces.")
            
            elif choice == '7':  # Roll Custom Dice
                if not simulator.custom_dice:
                    print("No custom dice created yet! Use option 6 to create some.")
                    continue
                
                print("Available custom dice:")
                for name, faces in simulator.custom_dice.items():
                    print(f"  - {name}: {faces}")
                
                dice_name = input("Enter dice name to roll: ").strip()
                if dice_name not in simulator.custom_dice:
                    print(f"Custom dice '{dice_name}' not found!")
                    continue
                
                count = get_positive_int("Number of dice (default 1): ") or 1
                
                print_animated_roll()
                rolls = simulator.roll_saved_custom_dice(dice_name, count)
                display_results(rolls, f"Custom Dice Roll ({dice_name})")
            
            elif choice == '8':  # View History
                if not simulator.roll_history:
                    print("No roll history yet!")
                    continue
                
                print(f"\n📜 ROLL HISTORY (Last {min(10, len(simulator.roll_history))} rolls)")
                print("-" * 60)
                for entry in simulator.roll_history[-10:]:
                    print(f"[{entry['timestamp']}] {entry['type']}: {entry['description']}")
                    print(f"    Rolls: {entry['rolls']} → Result: {entry['result']}")
                    print()
            
            elif choice == '9':  # View Statistics
                stats = simulator.get_statistics()
                if not stats:
                    print("No statistics available yet!")
                    continue
                
                print(f"\n📊 ROLLING STATISTICS")
                print("-" * 30)
                print(f"Total roll sessions: {stats['total_rolls']}")
                print(f"Total dice rolled: {stats['total_dice']}")
                print(f"Average roll value: {stats['average']:.2f}")
                print(f"Highest roll: {stats['highest']}")
                print(f"Lowest roll: {stats['lowest']}")
                print(f"Most common roll: {stats['most_common']}")
            
            elif choice == '10':  # Quick Rolls
                while True:
                    quick_rolls_menu()
                    quick_choice = input("Choose a quick roll (1-8): ").strip()
                    
                    if quick_choice == '8':
                        break
                    elif quick_choice in ['1', '2', '3', '4', '5', '6', '7']:
                        handle_quick_rolls(simulator, quick_choice)
                    else:
                        print("Invalid choice! Please select 1-8.")
            
            elif choice == '11':  # Clear History
                simulator.clear_history()
                print("✅ Roll history cleared!")
            
            else:
                print("Invalid choice! Please select 0-11.")
        
        except KeyboardInterrupt:
            print("\n\n🎲 Thanks for using Dice Rolling Simulator! 🎲")
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
