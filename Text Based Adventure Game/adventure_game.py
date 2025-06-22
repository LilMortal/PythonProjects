#!/usr/bin/env python3
"""
Fantasy Quest: A Text-Based Adventure Game
==========================================
A complete single-file adventure game with combat, inventory, and multiple story paths.
Compatible with Python 3.10+
"""

import random
import sys
import time
from typing import Dict, List, Optional, Tuple


class Player:
    """Player character with stats, inventory, and progression tracking."""
    
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.defense = 5
        self.gold = 50
        self.inventory = []
        self.level = 1
        self.experience = 0
        self.location = "village"
        
    def add_item(self, item: str) -> None:
        """Add an item to the player's inventory."""
        self.inventory.append(item)
        print(f"✅ Added {item} to your inventory!")
        
    def use_item(self, item: str) -> bool:
        """Use an item from inventory if available."""
        if item in self.inventory:
            if item == "Health Potion":
                heal_amount = min(50, self.max_health - self.health)
                self.health += heal_amount
                self.inventory.remove(item)
                print(f"💚 You healed {heal_amount} health! Current health: {self.health}")
                return True
            elif item == "Magic Sword":
                self.attack += 10
                print("⚔️ Your attack increased by 10!")
                return True
        return False
        
    def gain_experience(self, exp: int) -> None:
        """Add experience and handle level ups."""
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level += 1
            self.max_health += 20
            self.health = self.max_health
            self.attack += 5
            self.defense += 2
            print(f"🌟 Level up! You are now level {self.level}!")
            print(f"📈 Stats increased: Health +20, Attack +5, Defense +2")
            
    def show_stats(self) -> None:
        """Display player statistics."""
        print("\n" + "="*40)
        print(f"🧙 {self.name} - Level {self.level}")
        print(f"❤️  Health: {self.health}/{self.max_health}")
        print(f"⚔️  Attack: {self.attack}")
        print(f"🛡️  Defense: {self.defense}")
        print(f"💰 Gold: {self.gold}")
        print(f"⭐ Experience: {self.experience}/{self.level * 100}")
        if self.inventory:
            print(f"🎒 Inventory: {', '.join(self.inventory)}")
        else:
            print("🎒 Inventory: Empty")
        print("="*40)


class Enemy:
    """Enemy class with combat capabilities."""
    
    def __init__(self, name: str, health: int, attack: int, defense: int, 
                 gold_reward: int, exp_reward: int):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward


class Game:
    """Main game class handling all game logic and story progression."""
    
    def __init__(self):
        self.player = None
        self.game_over = False
        self.enemies = {
            "goblin": Enemy("Goblin", 40, 12, 2, 25, 50),
            "orc": Enemy("Orc", 80, 18, 5, 50, 100),
            "dragon": Enemy("Ancient Dragon", 200, 35, 10, 500, 1000),
            "bandit": Enemy("Forest Bandit", 60, 15, 3, 35, 75),
            "skeleton": Enemy("Undead Skeleton", 50, 14, 4, 30, 60)
        }
        
    def typewriter_print(self, text: str, delay: float = 0.03) -> None:
        """Print text with typewriter effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    def get_player_choice(self, options: List[str]) -> int:
        """Get valid player choice from a list of options."""
        while True:
            try:
                print("\nWhat do you choose?")
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                
                choice = int(input("\nEnter your choice (number): "))
                if 1 <= choice <= len(options):
                    return choice - 1
                else:
                    print(f"❌ Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("❌ Please enter a valid number!")
                
    def combat(self, enemy_name: str) -> bool:
        """Handle combat between player and enemy. Returns True if player wins."""
        enemy = Enemy(**self.enemies[enemy_name].__dict__)
        
        print(f"\n⚔️ COMBAT: {self.player.name} vs {enemy.name}!")
        print(f"🔥 {enemy.name} appears with {enemy.health} health!")
        
        while enemy.health > 0 and self.player.health > 0:
            # Player turn
            print(f"\n--- Your turn ---")
            actions = ["Attack", "Use Health Potion", "Run Away"]
            if "Health Potion" not in self.player.inventory:
                actions.remove("Use Health Potion")
                
            action = self.get_player_choice(actions)
            
            if actions[action] == "Attack":
                damage = max(1, self.player.attack - enemy.defense + random.randint(-3, 3))
                enemy.health -= damage
                print(f"💥 You deal {damage} damage to {enemy.name}!")
                if enemy.health <= 0:
                    print(f"🎉 You defeated the {enemy.name}!")
                    break
                    
            elif actions[action] == "Use Health Potion":
                self.player.use_item("Health Potion")
                
            elif actions[action] == "Run Away":
                if random.random() < 0.7:  # 70% chance to escape
                    print("💨 You successfully ran away!")
                    return False
                else:
                    print("❌ You couldn't escape!")
            
            # Enemy turn
            if enemy.health > 0:
                damage = max(1, enemy.attack - self.player.defense + random.randint(-2, 2))
                self.player.health -= damage
                print(f"💢 {enemy.name} deals {damage} damage to you!")
                print(f"❤️ Your health: {self.player.health}/{self.player.max_health}")
                
                if self.player.health <= 0:
                    print("💀 You have been defeated!")
                    return False
        
        # Victory rewards
        if enemy.health <= 0:
            self.player.gold += enemy.gold_reward
            self.player.gain_experience(enemy.exp_reward)
            print(f"💰 You earned {enemy.gold_reward} gold!")
            return True
            
        return False
        
    def intro(self) -> None:
        """Game introduction and character creation."""
        print("🏰" + "="*50 + "🏰")
        self.typewriter_print("    Welcome to FANTASY QUEST!")
        self.typewriter_print("    A Text-Based Adventure Game")
        print("🏰" + "="*50 + "🏰")
        
        print("\n🌟 You are about to embark on an epic adventure...")
        print("💫 Create your character to begin!")
        
        while True:
            name = input("\n🧙 Enter your character's name: ").strip()
            if name and len(name) <= 20:
                break
            print("❌ Please enter a valid name (1-20 characters)")
            
        self.player = Player(name)
        
        print(f"\n🎭 Welcome, {name}!")
        self.typewriter_print("You are a brave adventurer in the mystical kingdom of Aetheria.")
        self.typewriter_print("Dark forces threaten the land, and only you can restore peace...")
        
        self.player.show_stats()
        input("\n📖 Press Enter to begin your adventure...")
        
    def village_scene(self) -> None:
        """Starting village scene with multiple paths."""
        print("\n" + "🏘️ " + "="*30 + " 🏘️")
        print("        PEACEFUL VILLAGE")
        print("🏘️ " + "="*30 + " 🏘️")
        
        self.typewriter_print("You stand in the center of a peaceful village.")
        self.typewriter_print("The villagers whisper about strange happenings in the surrounding areas.")
        
        if "Village Key" not in self.player.inventory:
            self.typewriter_print("An old man approaches you with concern in his eyes...")
            self.typewriter_print("'Adventurer! Our village is in danger!'")
            self.typewriter_print("'Take this key - it opens the ancient chest in the forest.'")
            self.player.add_item("Village Key")
        
        options = [
            "🌲 Explore the Mysterious Forest",
            "⛰️ Climb the Dangerous Mountains", 
            "🏪 Visit the Village Shop",
            "🏠 Rest at the Inn (Restore Health)",
            "📊 Check Your Stats"
        ]
        
        choice = self.get_player_choice(options)
        
        if choice == 0:  # Forest
            self.forest_scene()
        elif choice == 1:  # Mountains
            self.mountain_scene()
        elif choice == 2:  # Shop
            self.shop_scene()
        elif choice == 3:  # Inn
            self.inn_scene()
        elif choice == 4:  # Stats
            self.player.show_stats()
            input("\nPress Enter to continue...")
            self.village_scene()
            
    def forest_scene(self) -> None:
        """Forest exploration with multiple encounters."""
        print("\n🌲🌲🌲 THE MYSTERIOUS FOREST 🌲🌲🌲")
        
        self.typewriter_print("You enter a dense, dark forest.")
        self.typewriter_print("Sunlight barely penetrates the thick canopy above.")
        
        # Random encounter
        encounter = random.choice(["chest", "enemy", "merchant", "nothing"])
        
        if encounter == "chest" and "Village Key" in self.player.inventory:
            self.typewriter_print("You discover an ancient chest locked with mysterious runes!")
            self.typewriter_print("Your Village Key glows and unlocks the chest!")
            
            treasure = random.choice(["Magic Sword", "Health Potion", "Gold"])
            if treasure == "Gold":
                gold_found = random.randint(50, 150)
                self.player.gold += gold_found
                print(f"💰 You found {gold_found} gold!")
            else:
                self.player.add_item(treasure)
                
            self.player.inventory.remove("Village Key")
            
        elif encounter == "enemy":
            enemy_type = random.choice(["goblin", "bandit"])
            self.typewriter_print(f"A wild {enemy_type} jumps out from behind a tree!")
            
            if self.combat(enemy_type):
                # Chance for bonus loot
                if random.random() < 0.4:
                    self.player.add_item("Health Potion")
            else:
                if self.player.health <= 0:
                    self.game_over_scene()
                    return
                    
        elif encounter == "merchant":
            self.typewriter_print("You meet a mysterious traveling merchant!")
            self.typewriter_print("'I have rare items for sale, brave adventurer!'")
            
            options = [
                f"Buy Health Potion (30 gold) - Current gold: {self.player.gold}",
                f"Buy Magic Ring (+5 defense) (100 gold)",
                "Leave"
            ]
            
            choice = self.get_player_choice(options)
            if choice == 0 and self.player.gold >= 30:
                self.player.gold -= 30
                self.player.add_item("Health Potion")
            elif choice == 1 and self.player.gold >= 100:
                self.player.gold -= 100
                self.player.defense += 5
                print("✨ Your defense increased by 5!")
            elif choice < 2:
                print("💸 Not enough gold!")
                
        else:
            self.typewriter_print("You explore the forest but find nothing of interest.")
            self.typewriter_print("The trees seem to whisper ancient secrets...")
        
        # Continue adventure
        options = [
            "🏘️ Return to Village",
            "🌲 Explore Deeper into Forest",
            "⛰️ Head to the Mountains"
        ]
        
        choice = self.get_player_choice(options)
        if choice == 0:
            self.village_scene()
        elif choice == 1:
            if random.random() < 0.3:  # 30% chance of dragon
                self.dragon_encounter()
            else:
                self.forest_scene()
        else:
            self.mountain_scene()
            
    def mountain_scene(self) -> None:
        """Mountain climbing with challenges."""
        print("\n⛰️⛰️⛰️ THE DANGEROUS MOUNTAINS ⛰️⛰️⛰️")
        
        self.typewriter_print("You begin climbing treacherous mountain paths.")
        self.typewriter_print("The air grows thin and cold as you ascend...")
        
        # Mountain challenge
        challenge = random.choice(["avalanche", "enemy", "treasure", "village"])
        
        if challenge == "avalanche":
            self.typewriter_print("❄️ AVALANCHE! Snow cascades down the mountain!")
            
            options = [
                "🏃 Run to safety",
                "🗿 Hide behind a large rock",
                "⚡ Use magic (if you have Magic Sword)"
            ]
            
            if "Magic Sword" not in self.player.inventory:
                options.pop()
                
            choice = self.get_player_choice(options)
            
            if choice == 0:  # Run
                if random.random() < 0.6:
                    print("🎉 You successfully outrun the avalanche!")
                else:
                    damage = random.randint(15, 25)
                    self.player.health -= damage
                    print(f"💢 You got caught! Lost {damage} health.")
                    
            elif choice == 1:  # Hide
                print("🛡️ You safely hide behind the rock!")
                
            elif choice == 2:  # Magic
                print("✨ Your Magic Sword creates a protective barrier!")
                self.player.gain_experience(25)
                
        elif challenge == "enemy":
            enemy_type = random.choice(["orc", "skeleton"])
            self.typewriter_print(f"A fierce {enemy_type} blocks your path!")
            
            if not self.combat(enemy_type):
                if self.player.health <= 0:
                    self.game_over_scene()
                    return
                    
        elif challenge == "treasure":
            self.typewriter_print("You discover a hidden cave with ancient treasures!")
            treasures = ["Health Potion", "Magic Sword", "Ancient Armor"]
            found_treasure = random.choice(treasures)
            
            if found_treasure == "Ancient Armor":
                self.player.defense += 8
                print("🛡️ Your defense increased by 8!")
            else:
                self.player.add_item(found_treasure)
                
        else:  # village
            self.typewriter_print("You discover a hidden mountain village!")
            self.typewriter_print("The villagers reward you for finding them!")
            self.player.gold += 75
            self.player.gain_experience(100)
            print("💰 Received 75 gold and 100 experience!")
        
        if self.player.health <= 0:
            return
            
        # Mountain summit choice
        self.typewriter_print("You reach a crossroads near the mountain peak...")
        
        options = [
            "🏔️ Climb to the very summit",
            "🏘️ Return to village",
            "🐉 Investigate the dark cave (Dragon's Lair)"
        ]
        
        choice = self.get_player_choice(options)
        if choice == 0:
            self.summit_scene()
        elif choice == 1:
            self.village_scene()
        else:
            self.dragon_encounter()
            
    def summit_scene(self) -> None:
        """Mountain summit with final revelation."""
        print("\n🏔️✨ THE MOUNTAIN SUMMIT ✨🏔️")
        
        self.typewriter_print("You reach the highest peak in all of Aetheria!")
        self.typewriter_print("The view is breathtaking - you can see the entire kingdom below.")
        self.typewriter_print("Suddenly, a wise old sage appears before you...")
        
        self.typewriter_print("'Brave adventurer, you have proven your worth!'")
        self.typewriter_print("'Accept this blessing to aid you in your final quest!'")
        
        # Summit blessing
        blessing_choice = self.get_player_choice([
            "Blessing of Strength (+15 Attack)",
            "Blessing of Vitality (+50 Max Health)",
            "Blessing of Fortune (+200 Gold)"
        ])
        
        if blessing_choice == 0:
            self.player.attack += 15
            print("⚔️ Your attack increased by 15!")
        elif blessing_choice == 1:
            self.player.max_health += 50
            self.player.health += 50
            print("❤️ Your max health increased by 50!")
        else:
            self.player.gold += 200
            print("💰 You received 200 gold!")
            
        self.player.gain_experience(200)
        
        self.typewriter_print("'Now go, champion! Face the ancient dragon and save our kingdom!'")
        
        input("\nPress Enter to continue your destiny...")
        self.dragon_encounter()
        
    def dragon_encounter(self) -> None:
        """Final boss encounter."""
        print("\n🐉🔥 THE DRAGON'S LAIR 🔥🐉")
        
        self.typewriter_print("You enter a massive cavern filled with treasure and bones...")
        self.typewriter_print("The ground trembles as an ENORMOUS dragon awakens!")
        self.typewriter_print("'WHO DARES DISTURB MY SLUMBER?!' roars the Ancient Dragon!")
        
        # Pre-combat choice
        options = [
            "⚔️ Challenge the dragon to combat!",
            "💬 Try to negotiate with the dragon",
            "🏃 Attempt to flee (coward's path)"
        ]
        
        choice = self.get_player_choice(options)
        
        if choice == 0:  # Combat
            if self.combat("dragon"):
                self.victory_scene()
            else:
                if self.player.health <= 0:
                    self.game_over_scene()
                else:
                    self.typewriter_print("You managed to escape the dragon's lair...")
                    self.village_scene()
                    
        elif choice == 1:  # Negotiate
            if self.player.level >= 3 or "Magic Sword" in self.player.inventory:
                self.typewriter_print("The dragon senses your power and wisdom...")
                self.typewriter_print("'You are no ordinary adventurer. I will spare the kingdom.'")
                self.typewriter_print("'Take this treasure as a token of our pact.'")
                self.player.gold += 1000
                self.negotiation_victory()
            else:
                self.typewriter_print("The dragon laughs at your weakness!")
                self.typewriter_print("'FOOLISH MORTAL! PREPARE FOR BATTLE!'")
                if self.combat("dragon"):
                    self.victory_scene()
                else:
                    self.game_over_scene()
                    
        else:  # Flee
            self.typewriter_print("You flee from the dragon's lair in terror...")
            self.typewriter_print("The kingdom remains under threat...")
            self.coward_ending()
            
    def shop_scene(self) -> None:
        """Village shop for purchasing items."""
        print("\n🏪💰 VILLAGE SHOP 💰🏪")
        
        self.typewriter_print("Welcome to Gareth's General Goods!")
        self.typewriter_print("'What can I get for ye today, adventurer?'")
        
        while True:
            print(f"\n💰 Your gold: {self.player.gold}")
            options = [
                "Health Potion - 40 gold (Restores 50 health)",
                "Iron Sword - 120 gold (+8 attack)",
                "Leather Armor - 100 gold (+5 defense)",
                "Lucky Charm - 80 gold (+10% combat luck)",
                "Leave shop"
            ]
            
            choice = self.get_player_choice(options)
            
            if choice == 0 and self.player.gold >= 40:
                self.player.gold -= 40
                self.player.add_item("Health Potion")
            elif choice == 1 and self.player.gold >= 120:
                self.player.gold -= 120
                self.player.attack += 8
                print("⚔️ Your attack increased by 8!")
            elif choice == 2 and self.player.gold >= 100:
                self.player.gold -= 100
                self.player.defense += 5
                print("🛡️ Your defense increased by 5!")
            elif choice == 3 and self.player.gold >= 80:
                self.player.gold -= 80
                self.player.add_item("Lucky Charm")
            elif choice == 4:
                break
            elif choice < 4:
                print("💸 Not enough gold!")
                
        self.village_scene()
        
    def inn_scene(self) -> None:
        """Village inn for rest and healing."""
        print("\n🏠🛏️ THE COZY INN 🛏️🏠")
        
        self.typewriter_print("You enter the warm, inviting village inn.")
        self.typewriter_print("The innkeeper greets you with a friendly smile.")
        
        options = [
            f"Rest and heal (20 gold) - Current health: {self.player.health}/{self.player.max_health}",
            "Hear tavern rumors (Free)",
            "Leave inn"
        ]
        
        choice = self.get_player_choice(options)
        
        if choice == 0:
            if self.player.gold >= 20:
                self.player.gold -= 20
                self.player.health = self.player.max_health
                print("😴 You sleep peacefully and recover all health!")
            else:
                print("💸 Not enough gold for a room!")
                
        elif choice == 1:
            rumors = [
                "I heard there's a powerful sword hidden in the forest...",
                "The mountain caves hold ancient treasures, but beware the monsters!",
                "A merchant was seen near the dragon's lair - probably didn't make it out...",
                "The old sage on the mountain peak grants blessings to worthy adventurers!"
            ]
            
            self.typewriter_print(f"Rumor: {random.choice(rumors)}")
            
        input("\nPress Enter to continue...")
        self.village_scene()
        
    def victory_scene(self) -> None:
        """Victory ending after defeating the dragon."""
        print("\n🎉🏆 VICTORY! 🏆🎉")
        
        self.typewriter_print("The mighty dragon falls with a thunderous crash!")
        self.typewriter_print("The cavern shakes as the beast breathes its last...")
        self.typewriter_print("You have saved the Kingdom of Aetheria!")
        
        self.typewriter_print("The king rewards you with riches beyond imagination!")
        self.typewriter_print("Bards will sing songs of your heroic deeds for generations!")
        
        final_score = (self.player.level * 100 + self.player.gold + 
                      self.player.experience + len(self.player.inventory) * 50)
        
        print(f"\n🌟 FINAL SCORE: {final_score}")
        self.player.show_stats()
        
        print("\n🎊 Thank you for playing Fantasy Quest! 🎊")
        self.game_over = True
        
    def negotiation_victory(self) -> None:
        """Alternative victory through negotiation."""
        print("\n🕊️✨ DIPLOMATIC VICTORY! ✨🕊️")
        
        self.typewriter_print("Through wisdom and courage, you have made peace with the dragon!")
        self.typewriter_print("The kingdom is saved without bloodshed!")
        self.typewriter_print("You are hailed as the 'Peacemaker of Aetheria'!")
        
        final_score = (self.player.level * 150 + self.player.gold + 
                      self.player.experience + len(self.player.inventory) * 50)
        
        print(f"\n🌟 FINAL SCORE: {final_score} (Diplomacy Bonus!)")
        self.player.show_stats()
        
        print("\n🎊 Thank you for playing Fantasy Quest! 🎊")
        self.game_over = True
        
    def coward_ending(self) -> None:
        """Ending for fleeing from the dragon."""
        print("\n😰💔 COWARD'S ENDING 💔😰")
        
        self.typewriter_print("You fled from your destiny and the kingdom remains in peril...")
        self.typewriter_print("The people will remember you as the one who could have been a hero.")
        self.typewriter_print("Perhaps another adventurer will finish what you started...")
        
        final_score = self.player.level * 25 + self.player.gold // 2
        
        print(f"\n😔 FINAL SCORE: {final_score}")
        print("\n💭 Maybe try a different path next time...")
        self.game_over = True
        
    def game_over_scene(self) -> None:
        """Game over scene for player death."""
        print("\n💀⚰️ GAME OVER ⚰️💀")
        
        self.typewriter_print("Your adventure has come to an unfortunate end...")
        self.typewriter_print("But heroes never truly die - their legends live on!")
        
        final_score = self.player.level * 50 + self.player.gold // 2 + self.player.experience
        
        print(f"\n👻 FINAL SCORE: {final_score}")
        print(f"🏆 You reached level {self.player.level} before your demise.")
        print("\n🔄 Would you like to play again? Restart the program!")
        self.game_over = True
        
    def play(self) -> None:
        """Main game loop."""
        try:
            self.intro()
            
            while not self.game_over and self.player.health > 0:
                if self.player.location == "village":
                    self.village_scene()
                    
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for playing Fantasy Quest!")
            print("🎮 Your adventure is saved in legend!")
        
        input("\nPress Enter to exit...")


def main():
    """Main function to start the game."""
    print("🎮 Starting Fantasy Quest...")
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
