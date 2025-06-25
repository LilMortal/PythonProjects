#!/usr/bin/env python3
"""
Plagiarism Checker Tool
A comprehensive text similarity detection tool that uses multiple algorithms
to identify potential plagiarism between documents.

Author: Assistant
Version: 1.0
Python Version: 3.8+
"""

import re
import os
import sys
import json
import argparse
from collections import Counter
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Set
import hashlib
import math


class PlagiarismChecker:
    """
    A comprehensive plagiarism detection tool that uses multiple similarity algorithms.
    """
    
    def __init__(self, min_similarity_threshold: float = 0.3):
        """
        Initialize the plagiarism checker.
        
        Args:
            min_similarity_threshold (float): Minimum similarity score to flag as potential plagiarism
        """
        self.min_similarity_threshold = min_similarity_threshold
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and normalize text for comparison.
        
        Args:
            text (str): Raw text input
            
        Returns:
            str: Cleaned and normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        
        return text
    
    def tokenize(self, text: str, remove_stopwords: bool = True) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text (str): Input text
            remove_stopwords (bool): Whether to remove common stopwords
            
        Returns:
            List[str]: List of tokens
        """
        # Basic word tokenization
        words = re.findall(r'\b\w+\b', text.lower())
        
        if remove_stopwords:
            words = [word for word in words if word not in self.stopwords]
        
        return words
    
    def get_ngrams(self, tokens: List[str], n: int = 3) -> Set[str]:
        """
        Generate n-grams from tokens.
        
        Args:
            tokens (List[str]): List of tokens
            n (int): Size of n-grams
            
        Returns:
            Set[str]: Set of n-grams
        """
        if len(tokens) < n:
            return set()
        
        ngrams = set()
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i + n])
            ngrams.add(ngram)
        
        return ngrams
    
    def jaccard_similarity(self, set1: Set, set2: Set) -> float:
        """
        Calculate Jaccard similarity between two sets.
        
        Args:
            set1, set2: Sets to compare
            
        Returns:
            float: Jaccard similarity score (0-1)
        """
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def cosine_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """
        Calculate cosine similarity between two token lists.
        
        Args:
            tokens1, tokens2: Lists of tokens
            
        Returns:
            float: Cosine similarity score (0-1)
        """
        # Create word frequency vectors
        counter1 = Counter(tokens1)
        counter2 = Counter(tokens2)
        
        # Get all unique words
        all_words = set(counter1.keys()).union(set(counter2.keys()))
        
        if not all_words:
            return 1.0
        
        # Create vectors
        vector1 = [counter1[word] for word in all_words]
        vector2 = [counter2[word] for word in all_words]
        
        # Calculate dot product and magnitudes
        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        magnitude1 = math.sqrt(sum(a * a for a in vector1))
        magnitude2 = math.sqrt(sum(a * a for a in vector2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def sequence_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate sequence similarity using difflib.
        
        Args:
            text1, text2: Texts to compare
            
        Returns:
            float: Sequence similarity score (0-1)
        """
        return SequenceMatcher(None, text1, text2).ratio()
    
    def longest_common_subsequence_ratio(self, text1: str, text2: str) -> float:
        """
        Calculate LCS ratio between two texts.
        
        Args:
            text1, text2: Texts to compare
            
        Returns:
            float: LCS ratio (0-1)
        """
        def lcs_length(s1: str, s2: str) -> int:
            m, n = len(s1), len(s2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if s1[i-1] == s2[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            
            return dp[m][n]
        
        if not text1 or not text2:
            return 0.0
        
        lcs_len = lcs_length(text1, text2)
        max_len = max(len(text1), len(text2))
        
        return lcs_len / max_len if max_len > 0 else 0.0
    
    def calculate_comprehensive_similarity(self, text1: str, text2: str) -> Dict[str, float]:
        """
        Calculate multiple similarity metrics between two texts.
        
        Args:
            text1, text2: Texts to compare
            
        Returns:
            Dict[str, float]: Dictionary of similarity scores
        """
        # Preprocess texts
        clean_text1 = self.preprocess_text(text1)
        clean_text2 = self.preprocess_text(text2)
        
        # Tokenize
        tokens1 = self.tokenize(clean_text1)
        tokens2 = self.tokenize(clean_text2)
        
        # Generate n-grams
        trigrams1 = self.get_ngrams(tokens1, 3)
        trigrams2 = self.get_ngrams(tokens2, 3)
        
        bigrams1 = self.get_ngrams(tokens1, 2)
        bigrams2 = self.get_ngrams(tokens2, 2)
        
        # Calculate similarities
        similarities = {
            'sequence_similarity': self.sequence_similarity(clean_text1, clean_text2),
            'cosine_similarity': self.cosine_similarity(tokens1, tokens2),
            'jaccard_word_similarity': self.jaccard_similarity(set(tokens1), set(tokens2)),
            'jaccard_trigram_similarity': self.jaccard_similarity(trigrams1, trigrams2),
            'jaccard_bigram_similarity': self.jaccard_similarity(bigrams1, bigrams2),
            'lcs_ratio': self.longest_common_subsequence_ratio(clean_text1, clean_text2)
        }
        
        # Calculate weighted average
        weights = {
            'sequence_similarity': 0.2,
            'cosine_similarity': 0.25,
            'jaccard_word_similarity': 0.15,
            'jaccard_trigram_similarity': 0.25,
            'jaccard_bigram_similarity': 0.1,
            'lcs_ratio': 0.05
        }
        
        weighted_score = sum(similarities[metric] * weight 
                           for metric, weight in weights.items())
        similarities['weighted_average'] = weighted_score
        
        return similarities
    
    def is_plagiarism(self, similarity_scores: Dict[str, float]) -> bool:
        """
        Determine if the similarity scores indicate potential plagiarism.
        
        Args:
            similarity_scores: Dictionary of similarity metrics
            
        Returns:
            bool: True if potential plagiarism detected
        """
        return similarity_scores['weighted_average'] >= self.min_similarity_threshold
    
    def check_file_against_file(self, file1_path: str, file2_path: str) -> Dict:
        """
        Compare two files for plagiarism.
        
        Args:
            file1_path, file2_path: Paths to files to compare
            
        Returns:
            Dict: Comparison results
        """
        try:
            with open(file1_path, 'r', encoding='utf-8') as f1:
                text1 = f1.read()
            
            with open(file2_path, 'r', encoding='utf-8') as f2:
                text2 = f2.read()
            
            similarities = self.calculate_comprehensive_similarity(text1, text2)
            
            return {
                'file1': file1_path,
                'file2': file2_path,
                'similarities': similarities,
                'is_plagiarism': self.is_plagiarism(similarities),
                'status': 'success'
            }
            
        except FileNotFoundError as e:
            return {
                'error': f"File not found: {e}",
                'status': 'error'
            }
        except Exception as e:
            return {
                'error': f"Error processing files: {e}",
                'status': 'error'
            }
    
    def check_directory(self, directory_path: str, file_extension: str = '.txt') -> List[Dict]:
        """
        Check all files in a directory against each other for plagiarism.
        
        Args:
            directory_path: Path to directory containing files
            file_extension: File extension to check
            
        Returns:
            List[Dict]: List of comparison results
        """
        if not os.path.exists(directory_path):
            return [{'error': f"Directory not found: {directory_path}", 'status': 'error'}]
        
        # Get all files with specified extension
        files = [f for f in os.listdir(directory_path) 
                if f.endswith(file_extension)]
        
        if len(files) < 2:
            return [{'error': f"Need at least 2 {file_extension} files to compare", 'status': 'error'}]
        
        results = []
        
        # Compare each file with every other file
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file1_path = os.path.join(directory_path, files[i])
                file2_path = os.path.join(directory_path, files[j])
                
                result = self.check_file_against_file(file1_path, file2_path)
                results.append(result)
        
        return results


def format_results(results: List[Dict]) -> str:
    """
    Format results for display.
    
    Args:
        results: List of comparison results
        
    Returns:
        str: Formatted results string
    """
    output = []
    output.append("=" * 60)
    output.append("PLAGIARISM CHECK RESULTS")
    output.append("=" * 60)
    
    if isinstance(results, dict):
        results = [results]
    
    for i, result in enumerate(results, 1):
        if result.get('status') == 'error':
            output.append(f"\nResult {i}: ERROR")
            output.append(f"Error: {result['error']}")
            continue
        
        output.append(f"\nResult {i}:")
        output.append(f"File 1: {result['file1']}")
        output.append(f"File 2: {result['file2']}")
        output.append(f"Plagiarism Detected: {'YES' if result['is_plagiarism'] else 'NO'}")
        
        output.append("\nSimilarity Scores:")
        similarities = result['similarities']
        
        for metric, score in similarities.items():
            metric_name = metric.replace('_', ' ').title()
            output.append(f"  {metric_name}: {score:.3f}")
        
        # Add interpretation
        weighted_score = similarities['weighted_average']
        if weighted_score >= 0.8:
            interpretation = "Very High Similarity - Likely Plagiarism"
        elif weighted_score >= 0.6:
            interpretation = "High Similarity - Possible Plagiarism"
        elif weighted_score >= 0.3:
            interpretation = "Moderate Similarity - Review Recommended"
        else:
            interpretation = "Low Similarity - Unlikely Plagiarism"
        
        output.append(f"\nInterpretation: {interpretation}")
        output.append("-" * 40)
    
    return "\n".join(output)


def main():
    """Main function to run the plagiarism checker."""
    parser = argparse.ArgumentParser(
        description="Plagiarism Checker - Detect similarity between text documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py file1.txt file2.txt
  python main.py --directory ./documents --extension .txt
  python main.py --threshold 0.5 file1.txt file2.txt
        """
    )
    
    parser.add_argument('files', nargs='*', help='Files to compare (2 files required)')
    parser.add_argument('--directory', '-d', help='Directory containing files to compare')
    parser.add_argument('--extension', '-e', default='.txt', 
                       help='File extension to check in directory mode (default: .txt)')
    parser.add_argument('--threshold', '-t', type=float, default=0.3,
                       help='Similarity threshold for plagiarism detection (default: 0.3)')
    parser.add_argument('--output', '-o', help='Output file for results (optional)')
    parser.add_argument('--json', action='store_true', 
                       help='Output results in JSON format')
    
    args = parser.parse_args()
    
    # Initialize plagiarism checker
    checker = PlagiarismChecker(min_similarity_threshold=args.threshold)
    
    results = []
    
    # Directory mode
    if args.directory:
        print(f"Checking files in directory: {args.directory}")
        print(f"File extension: {args.extension}")
        print(f"Similarity threshold: {args.threshold}")
        print("Processing...")
        
        results = checker.check_directory(args.directory, args.extension)
    
    # File comparison mode
    elif len(args.files) == 2:
        print(f"Comparing files: {args.files[0]} vs {args.files[1]}")
        print(f"Similarity threshold: {args.threshold}")
        print("Processing...")
        
        result = checker.check_file_against_file(args.files[0], args.files[1])
        results = [result]
    
    else:
        print("Error: Please provide either 2 files to compare or use --directory option")
        parser.print_help()
        sys.exit(1)
    
    # Format and display results
    if args.json:
        output_text = json.dumps(results, indent=2)
    else:
        output_text = format_results(results)
    
    print(output_text)
    
    # Save to file if specified
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"\nResults saved to: {args.output}")
        except Exception as e:
            print(f"Error saving results: {e}")


# Simple unit tests (can be run separately)
def run_tests():
    """Run basic unit tests for the plagiarism checker."""
    print("Running unit tests...")
    
    checker = PlagiarismChecker()
    
    # Test 1: Identical texts
    text1 = "This is a sample text for testing."
    text2 = "This is a sample text for testing."
    similarities = checker.calculate_comprehensive_similarity(text1, text2)
    assert similarities['weighted_average'] > 0.9, "Identical texts should have high similarity"
    print("✓ Test 1 passed: Identical texts")
    
    # Test 2: Completely different texts
    text1 = "This is about machine learning and artificial intelligence."
    text2 = "The weather today is sunny with clear blue skies."
    similarities = checker.calculate_comprehensive_similarity(text1, text2)
    assert similarities['weighted_average'] < 0.3, "Different texts should have low similarity"
    print("✓ Test 2 passed: Different texts")
    
    # Test 3: Paraphrased texts
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "A fast brown fox leaps over a sleepy dog."
    similarities = checker.calculate_comprehensive_similarity(text1, text2)
    assert 0.2 < similarities['weighted_average'] < 0.8, "Paraphrased texts should have moderate similarity"
    print("✓ Test 3 passed: Paraphrased texts")
    
    # Test 4: Empty texts
    similarities = checker.calculate_comprehensive_similarity("", "")
    assert similarities['weighted_average'] >= 0, "Empty texts should not cause errors"
    print("✓ Test 4 passed: Empty texts")
    
    print("All tests passed!")


if __name__ == "__main__":
    # Uncomment the line below to run tests
    # run_tests()
    
    main()
