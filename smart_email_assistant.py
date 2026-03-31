"""
Smart Email Reply Assistant with Agentic Tone Selection
Classifies email intent and generates professional replies with contextual tone
"""

import json
import re
from enum import Enum
from typing import Tuple, Dict, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Try to import ML libraries, fallback to pattern-based approach
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class EmailIntent(Enum):
    """Email intent classification"""
    QUERY = "query"
    COMPLAINT = "complaint"
    REQUEST = "request"
    SCHEDULING = "scheduling"
    FOLLOW_UP = "follow_up"
    APPLICATION = "application"
    FEEDBACK = "feedback"
    UNKNOWN = "unknown"


class Tone(Enum):
    """Response tone options"""
    FORMAL = "formal"
    FRIENDLY = "friendly"
    ASSERTIVE = "assertive"


@dataclass
class Email:
    """Email data structure"""
    subject: str
    body: str
    sender_context: str = "unknown"  # Context: professor, HR, recruiter, peer, etc.


class IntentClassifier:
    """Classifies the intent of incoming emails"""

    def __init__(self):
        self.patterns = {
            EmailIntent.SCHEDULING: [
                r'meet\b', r'avail', r'time', r'slot', r'calendar', r'schedule',
                r'when.*can', r'free.*', r'upcoming'
            ],
            EmailIntent.QUERY: [
                r'what\b', r'how\b', r'why\b', r'when\b', r'where\b', r'can\s+you',
                r'could\s+you', r'would\s+you', r'question', r'clarify', r'doubt'
            ],
            EmailIntent.COMPLAINT: [
                r'issue', r'problem', r'broken', r'doesn\'t work', r'complained',
                r'disappointed', r'unsatisfied', r'poor', r'bad', r'concern'
            ],
            EmailIntent.REQUEST: [
                r'request', r'need', r'require', r'please.*send', r'could\s+you\s+provide',
                r'would\s+you\s+mind', r'favor', r'help.*with'
            ],
            EmailIntent.FOLLOW_UP: [
                r'follow.*up', r'status', r'update', r'regarding.*previous', r'as\s+discussed',
                r'earlier.*mentioned', r'circle\s+back'
            ],
            EmailIntent.APPLICATION: [
                r'apply', r'application', r'position', r'role', r'opportunity',
                r'interested.*in', r'vacancy', r'internship', r'job', r'recruiting'
            ],
            EmailIntent.FEEDBACK: [
                r'feedback', r'suggestion', r'comment', r'opinion', r'thought',
                r'improvement', r'review', r'suggestion'
            ]
        }

    def classify(self, email: Email) -> Tuple[EmailIntent, float]:
        """Classify email intent with confidence score"""
        combined_text = f"{email.subject} {email.body}".lower()

        scores = {}
        for intent, patterns in self.patterns.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, combined_text))
            scores[intent] = matches / len(patterns) if patterns else 0

        if max(scores.values()) == 0:
            return EmailIntent.UNKNOWN, 0.0

        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        return best_intent, min(confidence, 1.0)


class ToneSelector:
    """Agentic component that selects appropriate tone based on context"""

    @staticmethod
    def select_tone(
        intent: EmailIntent,
        sender_context: str,
        email_sentiment: str,
        urgency_level: int
    ) -> Tone:
        """
        Agentic logic to select tone based on multiple context factors
        
        Args:
            intent: Classified email intent
            sender_context: Context of sender (professor, HR, recruiter, peer, customer)
            email_sentiment: Detected sentiment (positive, negative, neutral)
            urgency_level: Urgency level (1-5)
        
        Returns:
            Selected tone (formal, friendly, assertive)
        """
        # Rule-based agentic decision making
        
        # Complaints get assertive tone for urgent matters
        if intent == EmailIntent.COMPLAINT and urgency_level >= 3:
            return Tone.ASSERTIVE
        
        # Applications and queries to authority figures - formal
        if sender_context.lower() in ['professor', 'hr', 'recruiter', 'manager', 'director']:
            if intent in [EmailIntent.APPLICATION, EmailIntent.QUERY, EmailIntent.REQUEST]:
                return Tone.FORMAL
        
        # Scheduling and follow-ups with peers - friendly
        if sender_context.lower() in ['peer', 'colleague', 'team']:
            if intent in [EmailIntent.SCHEDULING, EmailIntent.FOLLOW_UP]:
                return Tone.FRIENDLY
        
        # Negative sentiment - assertive but professional
        if email_sentiment == 'negative':
            return Tone.ASSERTIVE if urgency_level >= 3 else Tone.FORMAL
        
        # Positive sentiment with peers - friendly
        if email_sentiment == 'positive' and sender_context.lower() == 'peer':
            return Tone.FRIENDLY
        
        # Default: formal for professional context, friendly for casual
        unknown_context_types = ['unknown', 'external']
        if sender_context.lower() in unknown_context_types:
            return Tone.FRIENDLY
        
        return Tone.FORMAL

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = {'thank', 'great', 'excellent', 'happy', 'good', 'appreciated', 'wonderful'}
        negative_words = {'issue', 'problem', 'concern', 'disappointed', 'bad', 'wrong', 'complaint'}
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if neg_count > pos_count:
            return 'negative'
        elif pos_count > neg_count:
            return 'positive'
        return 'neutral'

    @staticmethod
    def calculate_urgency(text: str) -> int:
        """Estimate urgency level 1-5"""
        urgent_indicators = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'today']
        count = sum(1 for indicator in urgent_indicators if indicator in text.lower())
        return min(5, 1 + count)


class ResponseGenerator:
    """Generates professional email responses"""

    TEMPLATES = {
        EmailIntent.QUERY: {
            Tone.FORMAL: {
                'opening': 'Thank you for your inquiry.',
                'answer_prefix': 'To address your question:',
                'closing': 'Please feel free to reach out if you have further questions.'
            },
            Tone.FRIENDLY: {
                'opening': 'Hi! Thanks for asking!',
                'answer_prefix': 'Here\'s what you wanted to know:',
                'closing': 'Let me know if you need anything else!'
            },
            Tone.ASSERTIVE: {
                'opening': 'I\'ve received your inquiry.',
                'answer_prefix': 'The answer is straightforward:',
                'closing': 'This should clarify the matter.'
            }
        },
        EmailIntent.SCHEDULING: {
            Tone.FORMAL: {
                'opening': 'I appreciate you reaching out to schedule a meeting.',
                'answer_prefix': 'My availability is as follows:',
                'closing': 'Please let me know what time works best for you.'
            },
            Tone.FRIENDLY: {
                'opening': 'Sounds great! Let\'s set up a time.',
                'answer_prefix': 'I\'m available:',
                'closing': 'Let me know what works for you!'
            },
            Tone.ASSERTIVE: {
                'opening': 'Regarding your meeting request.',
                'answer_prefix': 'I can meet at these times:',
                'closing': 'Please confirm your preference.'
            }
        },
        EmailIntent.REQUEST: {
            Tone.FORMAL: {
                'opening': 'Thank you for your request.',
                'answer_prefix': 'I will be happy to assist:',
                'closing': 'I hope this meets your needs.'
            },
            Tone.FRIENDLY: {
                'opening': 'Of course! Happy to help.',
                'answer_prefix': 'Here\'s what you need:',
                'closing': 'Let me know if you need anything else!'
            },
            Tone.ASSERTIVE: {
                'opening': 'Your request has been noted.',
                'answer_prefix': 'I can provide:',
                'closing': 'Please confirm receipt.'
            }
        },
        EmailIntent.APPLICATION: {
            Tone.FORMAL: {
                'opening': 'Thank you for considering my application.',
                'answer_prefix': 'I am particularly interested in this opportunity because:',
                'closing': 'I look forward to hearing from you.'
            },
            Tone.FRIENDLY: {
                'opening': 'Thanks so much for the opportunity!',
                'answer_prefix': 'I\'m excited about this role because:',
                'closing': 'Can\'t wait to discuss further!'
            },
            Tone.ASSERTIVE: {
                'opening': 'Regarding the position you advertised.',
                'answer_prefix': 'My qualifications include:',
                'closing': 'I am confident I can contribute significantly.'
            }
        },
        EmailIntent.COMPLAINT: {
            Tone.FORMAL: {
                'opening': 'I am writing to bring to your attention an issue I have encountered.',
                'answer_prefix': 'The details are as follows:',
                'closing': 'I would appreciate your prompt attention to this matter.'
            },
            Tone.FRIENDLY: {
                'opening': 'Hi, I wanted to flag something:',
                'answer_prefix': 'Here\'s what happened:',
                'closing': 'Could we work on fixing this together?'
            },
            Tone.ASSERTIVE: {
                'opening': 'This is to formally lodge a complaint.',
                'answer_prefix': 'The issue is:',
                'closing': 'I expect this to be resolved immediately.'
            }
        },
        EmailIntent.FOLLOW_UP: {
            Tone.FORMAL: {
                'opening': 'I am following up on my previous message.',
                'answer_prefix': 'To recap:',
                'closing': 'I would appreciate your response at your earliest convenience.'
            },
            Tone.FRIENDLY: {
                'opening': 'Just checking in!',
                'answer_prefix': 'Quick update:',
                'closing': 'Let me know your thoughts!'
            },
            Tone.ASSERTIVE: {
                'opening': 'This is a follow-up to my previous communication.',
                'answer_prefix': 'Status update:',
                'closing': 'I require a response by [specific date].'
            }
        },
        EmailIntent.UNKNOWN: {
            Tone.FORMAL: {
                'opening': 'Thank you for your email.',
                'answer_prefix': 'Regarding your message:',
                'closing': 'Please let me know if you need further assistance.'
            },
            Tone.FRIENDLY: {
                'opening': 'Thanks for reaching out!',
                'answer_prefix': 'Here\'s my take:',
                'closing': 'Feel free to get back to me anytime!'
            },
            Tone.ASSERTIVE: {
                'opening': 'I have reviewed your message.',
                'answer_prefix': 'My response is:',
                'closing': 'I trust this addresses your concern.'
            }
        }
    }

    @staticmethod
    def generate(
        intent: EmailIntent,
        tone: Tone,
        subject: str,
        sender_name: str = "Colleague"
    ) -> str:
        """Generate response email"""
        template = ResponseGenerator.TEMPLATES.get(
            intent,
            ResponseGenerator.TEMPLATES[EmailIntent.UNKNOWN]
        ).get(tone, ResponseGenerator.TEMPLATES[EmailIntent.UNKNOWN][Tone.FORMAL])

        response = f"Subject: Re: {subject}\n\n"
        response += f"Hi {sender_name},\n\n"
        response += f"{template['opening']}\n\n"
        response += f"{template['answer_prefix']}\n"
        response += "- [Your specific response content here]\n"
        response += f"- [Additional details as relevant]\n\n"
        response += f"{template['closing']}\n\n"
        response += "Best regards,\n[Your Name]"

        return response


class SmartEmailAssistant:
    """Main assistant that orchestrates classification, tone selection, and generation"""

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.tone_selector = ToneSelector()
        self.response_generator = ResponseGenerator()

    def process_email(
        self,
        email: Email,
        urgency_override: int = None
    ) -> Dict:
        """
        Process incoming email and generate professional reply
        
        Args:
            email: Email object with subject and body
            urgency_override: Optional override for urgency level
        
        Returns:
            Dictionary containing analysis and response
        """
        # Classify intent
        intent, confidence = self.intent_classifier.classify(email)

        # Analyze sentiment and urgency
        sentiment = self.tone_selector.analyze_sentiment(email.body)
        urgency = urgency_override or self.tone_selector.calculate_urgency(email.body)

        # Select appropriate tone
        tone = self.tone_selector.select_tone(intent, email.sender_context, sentiment, urgency)

        # Generate response
        response = self.response_generator.generate(
            intent, tone, email.subject, "there"
        )

        return {
            'intent': intent.value,
            'intent_confidence': round(confidence, 2),
            'tone': tone.value,
            'sentiment': sentiment,
            'urgency_level': urgency,
            'sender_context': email.sender_context,
            'suggested_response': response,
            'analysis': {
                'messages': [
                    f"Detected intent: {intent.value} (confidence: {confidence:.0%})",
                    f"Sentiment: {sentiment}",
                    f"Urgency level: {urgency}/5",
                    f"Selected tone: {tone.value}"
                ]
            }
        }


# Example usage
if __name__ == "__main__":
    assistant = SmartEmailAssistant()

    # Test email 1: Query from professor
    email1 = Email(
        subject="Question about Assignment Deadline",
        body="Hi, I have a quick question about the assignment deadline. Can we extend it by a few days?",
        sender_context="professor"
    )

    # Test email 2: Scheduling request from colleague
    email2 = Email(
        subject="Let's get together to discuss the project",
        body="Hey! When are you free next week? I'd love to meet and chat about our project.",
        sender_context="peer"
    )

    # Test email 3: Complaint
    email3 = Email(
        subject="Issue with recent service",
        body="I'm very disappointed with the service I received. The issue is unacceptable and needs immediate attention!",
        sender_context="customer"
    )

    print("=" * 80)
    print("SMART EMAIL REPLY ASSISTANT - TEST RESULTS")
    print("=" * 80)

    for i, email in enumerate([email1, email2, email3], 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {email.subject}")
        print(f"{'='*80}")
        result = assistant.process_email(email)

        print(f"\n📊 ANALYSIS:")
        for msg in result['analysis']['messages']:
            print(f"  • {msg}")

        print(f"\n💬 SUGGESTED RESPONSE:")
        print("-" * 80)
        print(result['suggested_response'])
        print("-" * 80)
