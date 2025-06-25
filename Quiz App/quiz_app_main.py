#!/usr/bin/env python3
"""
Interactive Quiz Application
A command-line quiz app with multiple categories, scoring, and progress tracking.
"""

import json
import random
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class QuizQuestion:
    """Represents a single quiz question with multiple choice answers."""
    
    def __init__(self, question: str, options: List[str], correct_answer: int, explanation: str = ""):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer  # Index of correct option (0-based)
        self.explanation = explanation
    
    def is_correct(self, answer_index: int) -> bool:
        """Check if the given answer index is correct."""
        return answer_index == self.correct_answer
    
    def get_correct_answer_text(self) -> str:
        """Get the text of the correct answer."""
        return self.options[self.correct_answer]


class QuizCategory:
    """Represents a category of quiz questions."""
    
    def __init__(self, name: str, questions: List[QuizQuestion]):
        self.name = name
        self.questions = questions
    
    def get_random_questions(self, count: int) -> List[QuizQuestion]:
        """Get a random sample of questions from this category."""
        return random.sample(self.questions, min(count, len(self.questions)))


class QuizSession:
    """Manages a single quiz session with scoring and progress tracking."""
    
    def __init__(self, category: QuizCategory, num_questions: int):
        self.category = category
        self.questions = category.get_random_questions(num_questions)
        self.current_question = 0
        self.score = 0
        self.answers = []  # Store user answers for review
        self.start_time = datetime.now()
    
    def get_current_question(self) -> Optional[QuizQuestion]:
        """Get the current question or None if quiz is complete."""
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None
    
    def submit_answer(self, answer_index: int) -> bool:
        """Submit an answer and return whether it was correct."""
        question = self.get_current_question()
        if question is None:
            return False
        
        is_correct = question.is_correct(answer_index)
        if is_correct:
            self.score += 1
        
        # Store the answer for review
        self.answers.append({
            'question': question.question,
            'user_answer': question.options[answer_index],
            'correct_answer': question.get_correct_answer_text(),
            'is_correct': is_correct,
            'explanation': question.explanation
        })
        
        self.current_question += 1
        return is_correct
    
    def is_complete(self) -> bool:
        """Check if the quiz session is complete."""
        return self.current_question >= len(self.questions)
    
    def get_progress(self) -> Tuple[int, int]:
        """Get current progress as (current_question, total_questions)."""
        return (self.current_question, len(self.questions))
    
    def get_score_percentage(self) -> float:
        """Get the score as a percentage."""
        if len(self.questions) == 0:
            return 0.0
        return (self.score / len(self.questions)) * 100
    
    def get_duration(self) -> str:
        """Get the duration of the quiz session."""
        duration = datetime.now() - self.start_time
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        return f"{minutes}m {seconds}s"


class QuizApp:
    """Main application class that manages the quiz experience."""
    
    def __init__(self):
        self.categories = self._load_quiz_data()
        self.high_scores = self._load_high_scores()
    
    def _load_quiz_data(self) -> Dict[str, QuizCategory]:
        """Load quiz questions and categories."""
        # Sample quiz data - in a real app, this might come from a file or database
        quiz_data = {
            "General Knowledge": [
                QuizQuestion(
                    "What is the capital of France?",
                    ["London", "Berlin", "Paris", "Madrid"],
                    2,
                    "Paris has been the capital of France since 508 AD."
                ),
                QuizQuestion(
                    "Which planet is known as the Red Planet?",
                    ["Venus", "Mars", "Jupiter", "Saturn"],
                    1,
                    "Mars appears red due to iron oxide (rust) on its surface."
                ),
                QuizQuestion(
                    "What is the largest ocean on Earth?",
                    ["Atlantic", "Indian", "Arctic", "Pacific"],
                    3,
                    "The Pacific Ocean covers about 63 million square miles."
                ),
                QuizQuestion(
                    "Who painted the Mona Lisa?",
                    ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
                    2,
                    "Leonardo da Vinci painted the Mona Lisa between 1503-1519."
                ),
                QuizQuestion(
                    "What is the smallest country in the world?",
                    ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
                    1,
                    "Vatican City is only 0.17 square miles (0.44 square kilometers)."
                )
            ],
            "Science": [
                QuizQuestion(
                    "What is the chemical symbol for gold?",
                    ["Go", "Gd", "Au", "Ag"],
                    2,
                    "Au comes from the Latin word 'aurum' meaning gold."
                ),
                QuizQuestion(
                    "How many bones are in an adult human body?",
                    ["196", "206", "216", "226"],
                    1,
                    "Adults have 206 bones, while babies are born with about 270."
                ),
                QuizQuestion(
                    "What is the speed of light in vacuum?",
                    ["299,792,458 m/s", "300,000,000 m/s", "186,000 mph", "Both A and B"],
                    0,
                    "The exact speed of light is 299,792,458 meters per second."
                ),
                QuizQuestion(
                    "Which gas makes up about 78% of Earth's atmosphere?",
                    ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"],
                    2,
                    "Nitrogen makes up about 78% of our atmosphere, oxygen about 21%."
                ),
                QuizQuestion(
                    "What is the hardest natural substance on Earth?",
                    ["Quartz", "Diamond", "Graphite", "Titanium"],
                    1,
                    "Diamond rates 10 on the Mohs hardness scale."
                )
            ],
            "History": [
                QuizQuestion(
                    "In which year did World War II end?",
                    ["1944", "1945", "1946", "1947"],
                    1,
                    "World War II ended in 1945 with Japan's surrender in September."
                ),
                QuizQuestion(
                    "Who was the first person to walk on the moon?",
                    ["Buzz Aldrin", "Neil Armstrong", "John Glenn", "Alan Shepard"],
                    1,
                    "Neil Armstrong stepped onto the moon on July 20, 1969."
                ),
                QuizQuestion(
                    "Which ancient wonder of the world was located in Alexandria?",
                    ["Hanging Gardens", "Colossus of Rhodes", "Lighthouse", "Statue of Zeus"],
                    2,
                    "The Lighthouse of Alexandria was one of the Seven Wonders of the Ancient World."
                ),
                QuizQuestion(
                    "The Berlin Wall fell in which year?",
                    ["1987", "1988", "1989", "1990"],
                    2,
                    "The Berlin Wall fell on November 9, 1989."
                ),
                QuizQuestion(
                    "Which empire was ruled by Julius Caesar?",
                    ["Greek Empire", "Roman Empire", "Byzantine Empire", "Persian Empire"],
                    1,
                    "Julius Caesar was a Roman general and dictator of the Roman Empire."
                )
            ]
        }
        
        categories = {}
        for category_name, questions_data in quiz_data.items():
            categories[category_name] = QuizCategory(category_name, questions_data)
        
        return categories
    
    def _load_high_scores(self) -> Dict[str, List[Dict]]:
        """Load high scores from file if it exists."""
        try:
            if os.path.exists('quiz_scores.json'):
                with open('quiz_scores.json', 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load high scores: {e}")
        
        return {category: [] for category in self.categories.keys()}
    
    def _save_high_scores(self):
        """Save high scores to file."""
        try:
            with open('quiz_scores.json', 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save high scores: {e}")
    
    def _add_high_score(self, category: str, score: int, total: int, duration: str):
        """Add a new high score."""
        if category not in self.high_scores:
            self.high_scores[category] = []
        
        score_entry = {
            'score': score,
            'total': total,
            'percentage': (score / total) * 100,
            'duration': duration,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.high_scores[category].append(score_entry)
        # Keep only top 5 scores per category
        self.high_scores[category].sort(key=lambda x: x['percentage'], reverse=True)
        self.high_scores[category] = self.high_scores[category][:5]
        
        self._save_high_scores()
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("=" * 60)
        print("🧠 WELCOME TO THE INTERACTIVE QUIZ APP! 🧠")
        print("=" * 60)
        print("Test your knowledge across different categories!")
        print("Answer multiple choice questions and track your progress.")
        print()
    
    def display_categories(self):
        """Display available quiz categories."""
        print("📚 Available Categories:")
        print("-" * 30)
        for i, (category_name, category) in enumerate(self.categories.items(), 1):
            print(f"{i}. {category_name} ({len(category.questions)} questions)")
        print()
    
    def get_user_choice(self, prompt: str, min_val: int, max_val: int) -> int:
        """Get a valid integer choice from user within specified range."""
        while True:
            try:
                choice = int(input(prompt))
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f"Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_category(self) -> QuizCategory:
        """Let user select a quiz category."""
        self.display_categories()
        
        choice = self.get_user_choice(
            "Select a category (enter number): ",
            1,
            len(self.categories)
        )
        
        category_name = list(self.categories.keys())[choice - 1]
        return self.categories[category_name]
    
    def select_num_questions(self, max_questions: int) -> int:
        """Let user select number of questions for the quiz."""
        print(f"\n📝 This category has {max_questions} questions available.")
        
        choice = self.get_user_choice(
            f"How many questions would you like? (1-{max_questions}): ",
            1,
            max_questions
        )
        
        return choice
    
    def display_question(self, question: QuizQuestion, question_num: int, total_questions: int):
        """Display a quiz question with options."""
        print("\n" + "=" * 60)
        print(f"Question {question_num}/{total_questions}")
        print("=" * 60)
        print(f"❓ {question.question}")
        print()
        
        for i, option in enumerate(question.options, 1):
            print(f"{i}. {option}")
        print()
    
    def get_answer(self, num_options: int) -> int:
        """Get user's answer choice."""
        return self.get_user_choice(
            "Your answer (enter number): ",
            1,
            num_options
        ) - 1  # Convert to 0-based index
    
    def display_answer_feedback(self, is_correct: bool, question: QuizQuestion, user_answer_index: int):
        """Display feedback for the user's answer."""
        if is_correct:
            print("✅ Correct! Well done!")
        else:
            print("❌ Incorrect!")
            print(f"Your answer: {question.options[user_answer_index]}")
            print(f"Correct answer: {question.get_correct_answer_text()}")
        
        if question.explanation:
            print(f"📖 Explanation: {question.explanation}")
        
        input("\nPress Enter to continue...")
    
    def display_final_results(self, session: QuizSession):
        """Display final quiz results and statistics."""
        print("\n" + "🎉" * 20)
        print("QUIZ COMPLETED!")
        print("🎉" * 20)
        
        percentage = session.get_score_percentage()
        print(f"\n📊 Your Results:")
        print(f"   Score: {session.score}/{len(session.questions)}")
        print(f"   Percentage: {percentage:.1f}%")
        print(f"   Duration: {session.get_duration()}")
        print(f"   Category: {session.category.name}")
        
        # Performance feedback
        if percentage >= 90:
            print("\n🏆 Outstanding! You're a quiz master!")
        elif percentage >= 80:
            print("\n🥇 Excellent work! Great knowledge!")
        elif percentage >= 70:
            print("\n🥈 Good job! Keep it up!")
        elif percentage >= 60:
            print("\n🥉 Not bad! Room for improvement!")
        else:
            print("\n📚 Keep studying! You'll do better next time!")
        
        # Add to high scores
        self._add_high_score(
            session.category.name,
            session.score,
            len(session.questions),
            session.get_duration()
        )
    
    def display_answer_review(self, session: QuizSession):
        """Display detailed review of all answers."""
        print("\n" + "=" * 60)
        print("📋 ANSWER REVIEW")
        print("=" * 60)
        
        for i, answer_data in enumerate(session.answers, 1):
            print(f"\n{i}. {answer_data['question']}")
            print(f"   Your answer: {answer_data['user_answer']}")
            print(f"   Correct answer: {answer_data['correct_answer']}")
            print(f"   Result: {'✅ Correct' if answer_data['is_correct'] else '❌ Incorrect'}")
            
            if answer_data['explanation']:
                print(f"   Explanation: {answer_data['explanation']}")
    
    def display_high_scores(self):
        """Display high scores for all categories."""
        print("\n" + "🏆" * 20)
        print("HIGH SCORES")
        print("🏆" * 20)
        
        for category, scores in self.high_scores.items():
            print(f"\n📚 {category}:")
            if not scores:
                print("   No scores yet!")
            else:
                for i, score in enumerate(scores, 1):
                    print(f"   {i}. {score['percentage']:.1f}% "
                          f"({score['score']}/{score['total']}) - "
                          f"{score['duration']} - {score['date']}")
    
    def run_quiz(self, category: QuizCategory, num_questions: int):
        """Run a complete quiz session."""
        session = QuizSession(category, num_questions)
        
        print(f"\n🚀 Starting {category.name} Quiz!")
        print(f"You'll be asked {len(session.questions)} questions.")
        input("Press Enter to begin...")
        
        # Main quiz loop
        while not session.is_complete():
            question = session.get_current_question()
            if question is None:
                break
            
            current, total = session.get_progress()
            self.display_question(question, current + 1, total)
            
            answer_index = self.get_answer(len(question.options))
            is_correct = session.submit_answer(answer_index)
            
            self.display_answer_feedback(is_correct, question, answer_index)
        
        # Display results
        self.display_final_results(session)
        
        # Ask if user wants to review answers
        print("\n" + "-" * 40)
        review = input("Would you like to review your answers? (y/n): ").lower().strip()
        if review.startswith('y'):
            self.display_answer_review(session)
    
    def main_menu(self):
        """Display and handle the main menu."""
        while True:
            print("\n" + "=" * 40)
            print("📋 MAIN MENU")
            print("=" * 40)
            print("1. Start New Quiz")
            print("2. View High Scores")
            print("3. Exit")
            print()
            
            choice = self.get_user_choice("Select an option: ", 1, 3)
            
            if choice == 1:
                category = self.select_category()
                num_questions = self.select_num_questions(len(category.questions))
                self.run_quiz(category, num_questions)
            
            elif choice == 2:
                self.display_high_scores()
            
            elif choice == 3:
                print("\n👋 Thanks for playing! Goodbye!")
                break
    
    def run(self):
        """Start the quiz application."""
        self.display_welcome()
        self.main_menu()


def main():
    """Main entry point of the application."""
    try:
        app = QuizApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Quiz interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try running the quiz again.")


# Simple unit tests (can be run by uncommenting the code below)
def run_tests():
    """Run basic unit tests for the quiz app."""
    print("Running tests...")
    
    # Test QuizQuestion
    question = QuizQuestion("Test question?", ["A", "B", "C", "D"], 1, "Test explanation")
    assert question.is_correct(1) == True
    assert question.is_correct(0) == False
    assert question.get_correct_answer_text() == "B"
    
    # Test QuizCategory
    questions = [
        QuizQuestion("Q1", ["A", "B"], 0),
        QuizQuestion("Q2", ["A", "B"], 1),
        QuizQuestion("Q3", ["A", "B"], 0)
    ]
    category = QuizCategory("Test", questions)
    random_questions = category.get_random_questions(2)
    assert len(random_questions) == 2
    
    # Test QuizSession
    session = QuizSession(category, 2)
    assert session.get_progress() == (0, 2)
    assert session.is_complete() == False
    
    print("✅ All tests passed!")


if __name__ == "__main__":
    # Uncomment the line below to run tests
    # run_tests()
    
    # Run the main application
    main()
