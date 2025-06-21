#!/usr/bin/env python3
"""
Mad Libs Generator - A fun interactive story creation game
Author: Claude AI Assistant
Python Version: 3.10+
"""

import random
import sys
from typing import Dict, List, Tuple


class MadLibsGenerator:
    """A class to handle Mad Libs story generation with multiple templates."""
    
    def __init__(self):
        """Initialize the Mad Libs Generator with story templates."""
        self.templates = [
            {
                "title": "The Crazy Adventure",
                "prompts": [
                    ("adjective", "Adjective (describing word)"),
                    ("noun", "Noun (person, place, or thing)"),
                    ("verb", "Verb (action word)"),
                    ("place", "Place"),
                    ("animal", "Animal"),
                    ("color", "Color"),
                    ("number", "Number"),
                    ("food", "Food")
                ],
                "story": """Once upon a time, there was a {adjective} {noun} who loved to {verb}. 
Every day, they would travel to {place} to find a {color} {animal}. 
One day, they discovered {number} pieces of {food} hidden behind a tree. 
"This is the best day ever!" shouted the {adjective} {noun} as they began to {verb} 
around {place} with joy. The {animal} watched in amazement and decided to join the fun!"""
            },
            {
                "title": "The Mysterious School Day",
                "prompts": [
                    ("adjective1", "Adjective"),
                    ("noun1", "Noun"),
                    ("verb1", "Verb"),
                    ("adjective2", "Another adjective"),
                    ("noun2", "Another noun"),
                    ("verb2", "Another verb"),
                    ("place", "Place"),
                    ("emotion", "Emotion")
                ],
                "story": """It was a {adjective1} morning when I walked into school with my {noun1}. 
I decided to {verb1} down the hallway when I saw something {adjective2}. 
There was a giant {noun2} in the middle of {place}! 
All the students began to {verb2} in {emotion}. 
The teacher said, "Don't worry, this {adjective2} {noun2} is just here to help us {verb1} better!" 
What a {adjective1} day at school!"""
            },
            {
                "title": "The Superhero Origin Story",
                "prompts": [
                    ("name", "Your superhero name"),
                    ("adjective", "Adjective"),
                    ("power", "Superpower"),
                    ("villain", "Villain name"),
                    ("place", "City/place"),
                    ("verb", "Verb"),
                    ("object", "Object"),
                    ("number", "Number")
                ],
                "story": """Meet {name}, the most {adjective} superhero in all of {place}! 
With the incredible power of {power}, {name} can {verb} faster than anyone else. 
One day, the evil {villain} threatened to destroy {place} using a giant {object}. 
"Not so fast!" shouted {name}, using {power} to stop the {villain}. 
After {number} minutes of epic battle, {name} saved the day! 
The people of {place} cheered as their {adjective} hero flew away into the sunset."""
            },
            {
                "title": "The Cooking Disaster",
                "prompts": [
                    ("adjective", "Adjective"),
                    ("food1", "Food item"),
                    ("verb", "Cooking verb (like 'bake', 'fry', etc.)"),
                    ("ingredient", "Weird ingredient"),
                    ("number", "Number"),
                    ("food2", "Another food item"),
                    ("adjective2", "Another adjective"),
                    ("reaction", "Reaction word (like 'yum' or 'yuck')")
                ],
                "story": """Today I decided to make a {adjective} {food1} for dinner. 
I started to {verb} it in the kitchen, but then I accidentally added {ingredient}! 
The recipe called for {number} cups of {food2}, but I used {number} pounds instead. 
When I tasted it, the {food1} was incredibly {adjective2}. 
"{reaction}!" I said, as smoke filled the kitchen. 
I guess I'll order pizza tonight instead of eating my {adjective} {food1}!"""
            }
        ]
    
    def get_valid_input(self, prompt: str) -> str:
        """Get valid input from user with validation."""
        while True:
            user_input = input(f"Enter a {prompt}: ").strip()
            if user_input:
                return user_input
            print("⚠️  Please enter a valid response (cannot be empty).")
    
    def collect_inputs(self, prompts: List[Tuple[str, str]]) -> Dict[str, str]:
        """Collect all required inputs from the user."""
        inputs = {}
        print("\n" + "="*50)
        print("🎯 TIME TO FILL IN THE BLANKS!")
        print("="*50)
        
        for key, prompt in prompts:
            inputs[key] = self.get_valid_input(prompt)
        
        return inputs
    
    def generate_story(self, template: Dict, inputs: Dict[str, str]) -> str:
        """Generate the completed story using the template and inputs."""
        return template["story"].format(**inputs)
    
    def display_story(self, title: str, story: str) -> None:
        """Display the completed story in a formatted way."""
        print("\n" + "="*60)
        print(f"📖 YOUR MAD LIBS STORY: {title.upper()}")
        print("="*60)
        print()
        
        # Split story into paragraphs and display with proper formatting
        paragraphs = story.split('\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                print(paragraph.strip())
                print()
        
        print("="*60)
    
    def play_game(self) -> None:
        """Main game loop."""
        print("🎉 WELCOME TO THE MAD LIBS GENERATOR! 🎉")
        print("Create hilarious stories by filling in the blanks!")
        
        while True:
            # Select random template
            template = random.choice(self.templates)
            
            print(f"\n🎲 Random story selected: '{template['title']}'")
            print(f"📝 You'll need to provide {len(template['prompts'])} words/phrases.")
            
            # Get user inputs
            inputs = self.collect_inputs(template["prompts"])
            
            # Generate and display story
            story = self.generate_story(template, inputs)
            self.display_story(template["title"], story)
            
            # Ask if user wants to play again
            while True:
                play_again = input("\n🔄 Would you like to create another story? (y/n): ").lower().strip()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("\n🎭 Thanks for playing Mad Libs! Keep being creative!")
                    return
                else:
                    print("⚠️  Please enter 'y' for yes or 'n' for no.")
    
    def show_available_templates(self) -> None:
        """Display all available story templates."""
        print("\n📚 AVAILABLE STORY TEMPLATES:")
        print("-" * 30)
        for i, template in enumerate(self.templates, 1):
            print(f"{i}. {template['title']}")
        print()


def main():
    """Main function to run the Mad Libs Generator."""
    try:
        generator = MadLibsGenerator()
        
        # Check if user wants to see available templates
        if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
            print("Mad Libs Generator Help")
            print("Usage: python mad_libs.py")
            print("\nOptional arguments:")
            print("  --help, -h     Show this help message")
            print("  --templates    Show available story templates")
            return
        
        if len(sys.argv) > 1 and sys.argv[1] == '--templates':
            generator.show_available_templates()
            return
        
        # Start the game
        generator.play_game()
        
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing! Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try running the program again.")


if __name__ == "__main__":
    main()