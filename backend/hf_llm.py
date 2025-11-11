import random

FALLBACK_RESPONSES = [
    "That's very interesting. Tell me more about that.",
    "I see. What else would you like to share?",
    "Thank you for explaining that. Please continue.",
    "That sounds important. Can you elaborate?",
    "I understand. What are your thoughts on this?"
]

async def ask_hf(prompt: str) -> str:
    """
    Returns a random fallback response.
    """
    return random.choice(FALLBACK_RESPONSES)