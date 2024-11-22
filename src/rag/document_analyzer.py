from typing import Dict, List, Set
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

class DocumentAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('french'))

    def analyze_document(self, text: str) -> Dict:
        """Analyse un document et retourne ses métadonnées"""
        # Statistiques de base
        stats = self._get_basic_stats(text)
        
        # Extraction de tags
        tags = self._extract_tags(text)
        
        # Analyse de complexité
        complexity = self._analyze_complexity(text)
        
        return {
            "stats": stats,
            "tags": list(tags),
            "complexity": complexity
        }

    def _get_basic_stats(self, text: str) -> Dict:
        """Calcule les statistiques de base du texte"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum()]  # Garder seulement les mots alphanumériques
        
        return {
            "char_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0
        }

    def _extract_tags(self, text: str) -> Set[str]:
        """Extrait des tags pertinents du texte"""
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        
        # Compter les occurrences des mots
        word_freq = Counter(words)
        
        # Prendre les N mots les plus fréquents comme tags
        top_words = word_freq.most_common(5)
        return {word for word, _ in top_words}

    def _analyze_complexity(self, text: str) -> Dict:
        """Analyse la complexité du texte"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        
        # Calculer la diversité du vocabulaire
        unique_words = set(words)
        
        return {
            "vocabulary_diversity": len(unique_words) / len(words) if words else 0,
            "avg_sentence_complexity": sum(len(word_tokenize(s)) for s in sentences) / len(sentences) if sentences else 0
        }
