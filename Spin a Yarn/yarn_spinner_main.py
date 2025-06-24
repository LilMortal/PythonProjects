#!/usr/bin/env python3
"""
Spin a Yarn - Interactive Story Generator
A command-line application that creates personalized stories based on user input.
"""

import random
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple


class StoryGenerator:
    """Main class for generating interactive stories."""
    
    def __init__(self):
        """Initialize the story generator with story templates and components."""
        self.story_templates = {
            "adventure": {
                "opening": [
                    "In the mystical land of {setting}, a brave {character} named {name} discovered a mysterious {object}.",
                    "Deep in the heart of {setting}, {name} the {character} stumbled upon an ancient {object}.",
                    "When the sun rose over {setting}, {name} knew today would be different. The {character} had found a magical {object}."
                ],
                "middle": [
                    "Suddenly, the {object} began to glow with {color} light, revealing a hidden path through the {obstacle}.",
                    "As {name} touched the {object}, a {creature} appeared, speaking in riddles about the {obstacle} ahead.",
                    "The {object} whispered secrets of power, but warned {name} about the dangerous {obstacle} that guards the treasure."
                ],
                "ending": [
                    "After overcoming the {obstacle}, {name} realized the true treasure was the {lesson} learned along the way.",
                    "With courage and {virtue}, {name} defeated the {obstacle} and became the legendary {title} of {setting}.",
                    "The {object} granted {name} the power of {virtue}, forever changing the fate of {setting}."
                ]
            },
            "mystery": {
                "opening": [
                    "Detective {name} arrived at the scene in {setting}, where a valuable {object} had mysteriously vanished.",
                    "In the quiet town of {setting}, {name} the {character} noticed something strange about the missing {object}.",
                    "The case of the missing {object} brought {name} to the peculiar {setting}, where nothing was as it seemed."
                ],
                "middle": [
                    "Following a trail of {color} clues, {name} discovered that the {creature} was somehow involved.",
                    "The {object} held the key to solving the mystery, but first {name} had to overcome the {obstacle}.",
                    "As {name} investigated deeper, the {creature} revealed crucial information about the hidden {obstacle}."
                ],
                "ending": [
                    "In a brilliant deduction, {name} solved the mystery and recovered the {object}, learning about {lesson}.",
                    "The truth about the {object} was revealed, and {name} was praised for their {virtue} and detective skills.",
                    "Justice was served when {name} exposed the real culprit, proving that {lesson} always prevails."
                ]
            },
            "romance": {
                "opening": [
                    "In the enchanting {setting}, {name} the {character} met someone special while searching for a rare {object}.",
                    "During the {color} sunset in {setting}, {name} accidentally bumped into destiny while carrying a precious {object}.",
                    "The annual festival in {setting} brought {name} face-to-face with love, all because of a simple {object}."
                ],
                "middle": [
                    "Despite the challenges posed by {obstacle}, their love grew stronger, symbolized by the {object} they shared.",
                    "The {creature} tested their relationship, but the {object} reminded them of their deep connection.",
                    "When {obstacle} threatened to separate them, the magical {object} revealed the power of true love."
                ],
                "ending": [
                    "Hand in hand, they overcame every {obstacle}, and the {object} became a symbol of their eternal {virtue}.",
                    "Their love story became legend in {setting}, inspiring others to believe in {lesson}.",
                    "The {object} blessed their union, and they lived happily ever after, embodying {virtue} and {lesson}."
                ]
            }
        }
        
        # Story components for filling templates
        self.story_components = {
            "settings": ["Elderwood Forest", "Crystal Mountains", "Moonlit Harbor", "Golden Desert", "Whispering Valley", 
                        "Starfall City", "Misty Highlands", "Coral Reef Kingdom", "Cloudtop Village", "Shadowmere Lake"],
            "characters": ["warrior", "wizard", "merchant", "artist", "scholar", "healer", "explorer", "inventor", 
                          "musician", "chef", "librarian", "captain", "detective", "farmer", "blacksmith"],
            "objects": ["crystal orb", "ancient scroll", "silver locket", "magic compass", "golden key", "ruby ring", 
                       "enchanted mirror", "moonstone pendant", "leather journal", "carved flute", "treasure map"],
            "creatures": ["wise owl", "mischievous fairy", "ancient dragon", "talking cat", "forest spirit", 
                         "phoenix", "unicorn", "friendly ghost", "magical fox", "crystal butterfly"],
            "obstacles": ["raging storm", "deep chasm", "enchanted maze", "riddle of the sphinx", "cursed forest", 
                         "treacherous mountain", "underground labyrinth", "time paradox", "memory spell", "mirror dimension"],
            "colors": ["golden", "silver", "emerald", "crimson", "azure", "violet", "amber", "pearl", "obsidian", "coral"],
            "virtues": ["wisdom", "courage", "kindness", "patience", "honesty", "loyalty", "compassion", "determination", 
                       "creativity", "humility", "justice", "forgiveness"],
            "lessons": ["friendship conquers all", "true strength comes from within", "love finds a way", 
                       "wisdom is the greatest treasure", "courage grows with each challenge", "kindness creates magic",
                       "patience reveals hidden truths", "honesty lights the darkest path"],
            "titles": ["Guardian", "Champion", "Protector", "Master", "Keeper", "Sage", "Hero", "Legend", "Savior", "Oracle"]
        }
        
        # File to store user stories
        self.stories_file = "saved_stories.json"
    
    def get_user_input(self) -> Dict[str, str]:
        """Collect user preferences for story generation."""
        print("🎭 Welcome to Spin a Yarn! Let's create your personalized story.\n")
        
        # Get basic story parameters
        user_input = {}
        
        # Character name
        while True:
            name = input("What's your character's name? ").strip()
            if name and name.replace(" ", "").isalpha():
                user_input["name"] = name.title()
                break
            print("Please enter a valid name (letters only).")
        
        # Story genre
        print("\nChoose your story genre:")
        genres = list(self.story_templates.keys())
        for i, genre in enumerate(genres, 1):
            print(f"{i}. {genre.title()}")
        
        while True:
            try:
                choice = int(input("\nEnter genre number: "))
                if 1 <= choice <= len(genres):
                    user_input["genre"] = genres[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(genres)}")
            except ValueError:
                print("Please enter a valid number.")
        
        # Optional: Let user choose specific elements or use random
        use_random = input("\nWould you like to customize story elements? (y/n): ").lower().startswith('y')
        
        if use_random:
            user_input.update(self._get_custom_elements())
        else:
            user_input.update(self._get_random_elements())
        
        return user_input
    
    def _get_custom_elements(self) -> Dict[str, str]:
        """Allow user to customize story elements."""
        elements = {}
        
        print("\nCustomize your story elements (press Enter for random):")
        
        # Setting
        print(f"\nAvailable settings: {', '.join(self.story_components['settings'])}")
        setting = input("Choose a setting: ").strip()
        elements["setting"] = setting.title() if setting else random.choice(self.story_components["settings"])
        
        # Character type
        print(f"\nAvailable character types: {', '.join(self.story_components['characters'])}")
        character = input("Choose character type: ").strip()
        elements["character"] = character.lower() if character else random.choice(self.story_components["characters"])
        
        # Fill remaining elements randomly
        for key in ["object", "creature", "obstacle", "color", "virtue", "lesson", "title"]:
            elements[key] = random.choice(self.story_components[key + "s"])
        
        return elements
    
    def _get_random_elements(self) -> Dict[str, str]:
        """Generate random story elements."""
        return {
            "setting": random.choice(self.story_components["settings"]),
            "character": random.choice(self.story_components["characters"]),
            "object": random.choice(self.story_components["objects"]),
            "creature": random.choice(self.story_components["creatures"]),
            "obstacle": random.choice(self.story_components["obstacles"]),
            "color": random.choice(self.story_components["colors"]),
            "virtue": random.choice(self.story_components["virtues"]),
            "lesson": random.choice(self.story_components["lessons"]),
            "title": random.choice(self.story_components["titles"])
        }
    
    def generate_story(self, user_input: Dict[str, str]) -> str:
        """Generate a complete story based on user input."""
        genre = user_input["genre"]
        template = self.story_templates[genre]
        
        # Select random templates for each story part
        opening = random.choice(template["opening"])
        middle = random.choice(template["middle"])
        ending = random.choice(template["ending"])
        
        # Format the story with user input
        story_parts = []
        for part in [opening, middle, ending]:
            try:
                formatted_part = part.format(**user_input)
                story_parts.append(formatted_part)
            except KeyError as e:
                print(f"Warning: Missing story element {e}")
                story_parts.append(part)
        
        # Combine story parts
        story = "\n\n".join(story_parts)
        
        return story
    
    def save_story(self, story: str, user_input: Dict[str, str]) -> None:
        """Save the generated story to a file."""
        story_data = {
            "timestamp": datetime.now().isoformat(),
            "character_name": user_input.get("name", "Unknown"),
            "genre": user_input.get("genre", "Unknown"),
            "story": story,
            "elements": {k: v for k, v in user_input.items() if k not in ["name", "genre"]}
        }
        
        # Load existing stories or create new list
        stories = []
        if os.path.exists(self.stories_file):
            try:
                with open(self.stories_file, 'r', encoding='utf-8') as f:
                    stories = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                stories = []
        
        stories.append(story_data)
        
        # Save updated stories
        try:
            with open(self.stories_file, 'w', encoding='utf-8') as f:
                json.dump(stories, f, indent=2, ensure_ascii=False)
            print(f"\n📖 Story saved to {self.stories_file}")
        except IOError as e:
            print(f"Warning: Could not save story - {e}")
    
    def display_story(self, story: str, user_input: Dict[str, str]) -> None:
        """Display the generated story with formatting."""
        print("\n" + "="*60)
        print(f"🌟 {user_input['name']}'s {user_input['genre'].title()} Story 🌟")
        print("="*60)
        print()
        
        # Display story with paragraph breaks
        paragraphs = story.split('\n\n')
        for i, paragraph in enumerate(paragraphs, 1):
            print(f"Chapter {i}:")
            print(paragraph)
            print()
        
        print("="*60)
        print("✨ The End ✨")
        print("="*60)
    
    def view_saved_stories(self) -> None:
        """Display previously saved stories."""
        if not os.path.exists(self.stories_file):
            print("No saved stories found.")
            return
        
        try:
            with open(self.stories_file, 'r', encoding='utf-8') as f:
                stories = json.load(f)
            
            if not stories:
                print("No saved stories found.")
                return
            
            print(f"\n📚 You have {len(stories)} saved stories:")
            for i, story_data in enumerate(stories, 1):
                timestamp = datetime.fromisoformat(story_data["timestamp"])
                print(f"{i}. {story_data['character_name']} ({story_data['genre']}) - {timestamp.strftime('%Y-%m-%d %H:%M')}")
            
            # Let user select a story to view
            while True:
                try:
                    choice = input(f"\nEnter story number to view (1-{len(stories)}) or 'q' to quit: ")
                    if choice.lower() == 'q':
                        break
                    
                    story_num = int(choice) - 1
                    if 0 <= story_num < len(stories):
                        selected_story = stories[story_num]
                        print("\n" + "="*60)
                        print(f"📖 {selected_story['character_name']}'s {selected_story['genre'].title()} Story")
                        print(f"Created: {datetime.fromisoformat(selected_story['timestamp']).strftime('%Y-%m-%d %H:%M')}")
                        print("="*60)
                        print(selected_story['story'])
                        print("="*60)
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(stories)}")
                except ValueError:
                    print("Please enter a valid number or 'q' to quit.")
        
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading saved stories: {e}")
    
    def run(self) -> None:
        """Main application loop."""
        while True:
            print("\n🎭 Spin a Yarn - Story Generator")
            print("1. Create a new story")
            print("2. View saved stories")
            print("3. Exit")
            
            choice = input("\nChoose an option (1-3): ").strip()
            
            if choice == "1":
                try:
                    user_input = self.get_user_input()
                    story = self.generate_story(user_input)
                    self.display_story(story, user_input)
                    
                    # Ask if user wants to save the story
                    save_choice = input("\nWould you like to save this story? (y/n): ")
                    if save_choice.lower().startswith('y'):
                        self.save_story(story, user_input)
                
                except KeyboardInterrupt:
                    print("\n\nStory creation cancelled.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            
            elif choice == "2":
                self.view_saved_stories()
            
            elif choice == "3":
                print("\n👋 Thank you for using Spin a Yarn! Keep storytelling!")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")


def run_tests():
    """Simple unit tests for the StoryGenerator class."""
    print("Running tests...")
    
    # Test story generator initialization
    generator = StoryGenerator()
    assert len(generator.story_templates) == 3, "Should have 3 story templates"
    assert "adventure" in generator.story_templates, "Should have adventure template"
    
    # Test random elements generation
    elements = generator._get_random_elements()
    required_keys = ["setting", "character", "object", "creature", "obstacle", "color", "virtue", "lesson", "title"]
    for key in required_keys:
        assert key in elements, f"Missing required element: {key}"
    
    # Test story generation
    test_input = {
        "name": "TestHero",
        "genre": "adventure",
        **elements
    }
    
    story = generator.generate_story(test_input)
    assert len(story) > 0, "Story should not be empty"
    assert "TestHero" in story, "Story should contain character name"
    
    print("✅ All tests passed!")


if __name__ == "__main__":
    # Uncomment the line below to run tests
    # run_tests()
    
    # Run the main application
    try:
        app = StoryGenerator()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using Spin a Yarn!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please report this issue if it persists.")