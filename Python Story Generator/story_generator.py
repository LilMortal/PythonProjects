#!/usr/bin/env python3
"""
Interactive Story Generator
A CLI tool that creates personalized stories based on user input.
Compatible with Python 3.10+
"""

import random
import re
from typing import Dict, List, Tuple
from datetime import datetime


class StoryGenerator:
    """Main class for generating interactive stories."""
    
    def __init__(self):
        """Initialize the story generator with templates and word lists."""
        self.story_templates = {
            "adventure": [
                "Once upon a time, {character_name} was a brave {profession} living in {location}. "
                "One {adjective_1} morning, they discovered a {adjective_2} {object} that could {magical_power}. "
                "Without hesitation, {character_name} decided to {action_verb} to the {destination} to find the legendary {treasure}. "
                "Along the way, they met a {adjective_3} {creature} who {helped_or_hindered} them. "
                "After a {adjective_4} battle, {character_name} finally {victory_action} and became the most {final_adjective} {profession} in all of {location}!",
                
                "In the mystical land of {location}, {character_name} worked as a {profession}. "
                "Every day was {adjective_1} until they found a {adjective_2} {object} hidden in their {hiding_place}. "
                "The {object} whispered secrets about a {treasure} located in the dangerous {destination}. "
                "Gathering their {adjective_3} courage, {character_name} began their quest, riding a {creature} across {adjective_4} landscapes. "
                "When they finally {victory_action}, the whole kingdom celebrated their {final_adjective} achievement!"
            ],
            
            "mystery": [
                "Detective {character_name} was known throughout {location} as the most {adjective_1} investigator. "
                "One stormy night, a {adjective_2} {object} appeared at their doorstep with a cryptic message about {treasure}. "
                "The only clue was a {adjective_3} {creature} seen near the {destination}. "
                "Using their {magical_power} skills, {character_name} began to {action_verb} through the evidence. "
                "After a {adjective_4} investigation, they {victory_action} and solved the most {final_adjective} case of their career!",
                
                "The {adjective_1} town of {location} was peaceful until {character_name}, a local {profession}, noticed something strange. "
                "A {adjective_2} {object} kept appearing in different places, always accompanied by the sound of {creature} footsteps. "
                "Determined to {action_verb} the mystery, {character_name} followed the clues to {destination}. "
                "There, they discovered the {treasure} and realized their {magical_power} was the key to everything. "
                "With a {adjective_4} revelation, they {victory_action} and became {final_adjective} throughout {location}!"
            ],
            
            "comedy": [
                "Meet {character_name}, the most {adjective_1} {profession} in {location}. "
                "Their life changed forever when they accidentally {action_verb} into a {adjective_2} {object}. "
                "Suddenly, they gained the {magical_power} to communicate with every {creature} in town! "
                "This led to {adjective_3} situations, especially when they had to {victory_action} at the {destination}. "
                "In the end, {character_name} learned that being {final_adjective} was more valuable than finding any {treasure}!",
                
                "In the {adjective_1} city of {location}, {character_name} worked as a {profession} with a very {adjective_2} problem. "
                "Every time they touched a {object}, something {adjective_3} would happen! "
                "One day, while trying to {action_verb} to {destination}, they met a wise {creature}. "
                "The {creature} taught them to use their {magical_power} properly, and soon {character_name} could {victory_action}. "
                "Now they're the most {final_adjective} person in {location}, and everyone wants their {treasure}!"
            ]
        }
        
        # Default word suggestions for each category
        self.word_suggestions = {
            "character_name": ["Alex", "Morgan", "Riley", "Casey", "Jordan", "Taylor"],
            "profession": ["knight", "wizard", "explorer", "detective", "inventor", "chef"],
            "location": ["Mystic Valley", "Crystal City", "Dragon Mountain", "Moonlight Forest", "Golden Harbor"],
            "adjective_1": ["mysterious", "exciting", "peaceful", "chaotic", "magical"],
            "adjective_2": ["ancient", "glowing", "cursed", "enchanted", "mysterious"],
            "adjective_3": ["friendly", "suspicious", "helpful", "grumpy", "wise"],
            "adjective_4": ["epic", "dangerous", "thrilling", "challenging", "incredible"],
            "final_adjective": ["famous", "respected", "legendary", "beloved", "powerful"],
            "object": ["crystal", "map", "book", "sword", "key", "scroll"],
            "creature": ["dragon", "unicorn", "phoenix", "wolf", "owl", "cat"],
            "destination": ["Dark Cave", "Sky Castle", "Hidden Temple", "Secret Garden", "Lost City"],
            "treasure": ["Golden Crown", "Magic Scroll", "Crystal Heart", "Ancient Wisdom", "True Love"],
            "magical_power": ["ability", "power", "gift", "talent", "skill"],
            "action_verb": ["journey", "travel", "venture", "rush", "sneak"],
            "victory_action": ["succeeded", "triumphed", "won", "conquered", "achieved victory"],
            "helped_or_hindered": ["helped", "guided", "challenged", "tested", "befriended"],
            "hiding_place": ["attic", "basement", "garden", "closet", "trunk"]
        }

    def display_welcome(self) -> None:
        """Display welcome message and instructions."""
        print("=" * 60)
        print("🎭 WELCOME TO THE INTERACTIVE STORY GENERATOR! 🎭")
        print("=" * 60)
        print("Create your own personalized adventure, mystery, or comedy story!")
        print("You'll be prompted to enter words that will be woven into your tale.")
        print("Press Enter without typing anything to get a random suggestion.")
        print("-" * 60)

    def get_story_genre(self) -> str:
        """Get the story genre from user input."""
        genres = list(self.story_templates.keys())
        print(f"\nAvailable story genres: {', '.join(genres)}")
        
        while True:
            genre = input("Choose a story genre (or press Enter for random): ").lower().strip()
            
            if not genre:  # Random selection
                genre = random.choice(genres)
                print(f"✨ Randomly selected: {genre.title()}")
                return genre
            
            if genre in genres:
                return genre
            
            print(f"Invalid genre. Please choose from: {', '.join(genres)}")

    def get_user_input(self, prompt: str, category: str) -> str:
        """Get user input with suggestions and validation."""
        suggestions = self.word_suggestions.get(category, [])
        
        if suggestions:
            suggestion_text = f" (suggestions: {', '.join(suggestions[:3])}...)"
        else:
            suggestion_text = ""
            
        while True:
            user_input = input(f"{prompt}{suggestion_text}: ").strip()
            
            if not user_input:  # Use random suggestion
                if suggestions:
                    user_input = random.choice(suggestions)
                    print(f"✨ Using: {user_input}")
                else:
                    user_input = "mysterious thing"
                    print(f"✨ Using: {user_input}")
            
            # Basic validation - no numbers, reasonable length
            if self.validate_input(user_input):
                return user_input
            else:
                print("Please enter a valid word (letters only, 1-30 characters)")

    def validate_input(self, text: str) -> bool:
        """Validate user input."""
        if not text or len(text) > 30:
            return False
        
        # Allow letters, spaces, and basic punctuation
        if not re.match(r"^[a-zA-Z\s'-]+$", text):
            return False
            
        return True

    def collect_story_words(self) -> Dict[str, str]:
        """Collect all words needed for the story."""
        words = {}
        
        print("\n📝 Let's gather the words for your story!")
        print("(Press Enter for random suggestions)")
        print("-" * 40)
        
        # Define the order and prompts for word collection
        word_prompts = [
            ("character_name", "Enter the main character's name"),
            ("profession", "Enter a profession/job"),
            ("location", "Enter a place/location"),
            ("adjective_1", "Enter a descriptive word (adjective)"),
            ("adjective_2", "Enter another descriptive word"),
            ("adjective_3", "Enter a third descriptive word"),
            ("adjective_4", "Enter a fourth descriptive word"),
            ("final_adjective", "Enter a final descriptive word"),
            ("object", "Enter an object/item"),
            ("creature", "Enter a creature/animal"),
            ("destination", "Enter a destination/place"),
            ("treasure", "Enter something valuable"),
            ("magical_power", "Enter a special ability"),
            ("action_verb", "Enter an action word"),
            ("victory_action", "Enter a victory action"),
        ]
        
        for key, prompt in word_prompts:
            words[key] = self.get_user_input(prompt, key)
        
        # Add some additional words that might be needed
        additional_words = ["helped_or_hindered", "hiding_place"]
        for key in additional_words:
            if key not in words:
                words[key] = random.choice(self.word_suggestions.get(key, ["something"]))
        
        return words

    def generate_story(self, genre: str, words: Dict[str, str]) -> str:
        """Generate a story using the template and user words."""
        template = random.choice(self.story_templates[genre])
        
        try:
            story = template.format(**words)
            return story
        except KeyError as e:
            # Handle missing keys gracefully
            print(f"Warning: Missing word for {e}, using default...")
            words[str(e).strip("'")] = "mysterious thing"
            story = template.format(**words)
            return story

    def display_story(self, story: str, genre: str) -> None:
        """Display the generated story with formatting."""
        print("\n" + "=" * 80)
        print(f"🎉 YOUR {genre.upper()} STORY IS READY! 🎉")
        print("=" * 80)
        print()
        
        # Word wrap for better readability
        words = story.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 70:
                lines.append(' '.join(current_line))
                current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines:
            print(line)
        
        print("\n" + "=" * 80)

    def save_story(self, story: str, genre: str) -> None:
        """Save the story to a file."""
        save = input("\n💾 Would you like to save your story to a file? (y/n): ").lower().strip()
        
        if save.startswith('y'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"story_{genre}_{timestamp}.txt"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Generated Story - {genre.title()}\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(story)
                    f.write(f"\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                print(f"✅ Story saved as: {filename}")
            except Exception as e:
                print(f"❌ Error saving file: {e}")

    def play_again(self) -> bool:
        """Ask if user wants to generate another story."""
        while True:
            again = input("\n🔄 Would you like to create another story? (y/n): ").lower().strip()
            if again.startswith('y'):
                return True
            elif again.startswith('n'):
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def run(self) -> None:
        """Main game loop."""
        self.display_welcome()
        
        while True:
            try:
                # Get story preferences
                genre = self.get_story_genre()
                
                # Collect words from user
                words = self.collect_story_words()
                
                # Generate and display story
                story = self.generate_story(genre, words)
                self.display_story(story, genre)
                
                # Offer to save
                self.save_story(story, genre)
                
                # Check if user wants to play again
                if not self.play_again():
                    break
                    
                print("\n" + "🌟" * 20)  # Separator for next story
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using Story Generator! Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("Let's try again!")
                continue
        
        print("\n🎭 Thanks for creating stories with us! Happy writing! 🎭")


def main():
    """Main function to run the story generator."""
    generator = StoryGenerator()
    generator.run()


if __name__ == "__main__":
    main()
