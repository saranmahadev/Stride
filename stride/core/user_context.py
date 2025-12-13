"""
User context helper module for personalized CLI experience.
Provides utilities for getting user information, greetings, and motivational messages.
"""

import random
import datetime
from typing import Optional, Dict


def get_current_user() -> Optional[Dict[str, str]]:
    """
    Get currently authenticated user information.
    
    Returns:
        Dict with 'email', 'username', 'token' if authenticated, None otherwise
    """
    try:
        from .auth import SupabaseAuth
        auth = SupabaseAuth()
        return auth.get_current_user()
    except Exception:
        return None


def get_username_display() -> str:
    """
    Get username for display purposes.
    
    Returns:
        Username if authenticated, "Developer" as fallback
    """
    user = get_current_user()
    if user and user.get("username"):
        return user["username"]
    return "Developer"


def get_time_based_greeting() -> str:
    """
    Return greeting based on current time of day.
    
    Returns:
        Time-appropriate greeting string
    """
    hour = datetime.datetime.now().hour
    
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Hey"


def get_user_greeting(include_username: bool = True, time_based: bool = True) -> str:
    """
    Get personalized greeting with optional time and username.
    
    Args:
        include_username: Whether to include username in greeting
        time_based: Whether to use time-based greeting
        
    Returns:
        Personalized greeting string
    """
    if time_based:
        greeting = get_time_based_greeting()
    else:
        greeting = "Hey"
    
    if include_username:
        username = get_username_display()
        return f"{greeting}, {username}"
    
    return greeting


def get_welcome_message(is_returning: bool = True) -> str:
    """
    Get welcome message for init command.
    
    Args:
        is_returning: Whether user is returning (has existing sprints)
        
    Returns:
        Welcome message string
    """
    username = get_username_display()
    
    if is_returning:
        messages = [
            f"Welcome back, {username}!",
            f"Great to see you again, {username}!",
            f"Ready to sprint, {username}?",
        ]
    else:
        messages = [
            f"Welcome to Stride, {username}!",
            f"Let's get started, {username}!",
            f"Ready to build something amazing, {username}?",
        ]
    
    return random.choice(messages)


def get_motivational_message(context: str = "general") -> str:
    """
    Return context-aware motivational message.
    
    Args:
        context: Context for the message (init, status, complete, validate, etc.)
        
    Returns:
        Motivational message string
    """
    messages = {
        "init": [
            "Let's build something amazing!",
            "Time to create magic!",
            "Your next great sprint awaits!",
        ],
        "status": [
            "You're doing great!",
            "Keep up the momentum!",
            "You're making excellent progress!",
        ],
        "progress_high": [
            "You're crushing it!",
            "Almost there!",
            "Great progress!",
        ],
        "progress_low": [
            "Every step counts!",
            "Keep going!",
            "You've got this!",
        ],
        "complete": [
            "Excellent work!",
            "You're crushing it!",
            "Outstanding achievement!",
        ],
        "validate_success": [
            "Perfect work!",
            "Looking great!",
            "Everything checks out!",
        ],
        "validate_error": [
            "No worries, here's what needs fixing:",
            "Small tweaks needed:",
            "Let's get these sorted:",
        ],
        "metrics": [
            "Keep up the momentum!",
            "You're on fire!",
            "Impressive stats!",
        ],
    }
    
    return random.choice(messages.get(context, ["Keep going!"]))


def get_progress_encouragement(completed: int, total: int) -> str:
    """
    Get encouraging message based on progress percentage.
    
    Args:
        completed: Number of completed items
        total: Total number of items
        
    Returns:
        Encouragement message
    """
    if total == 0:
        return "Ready to get started!"
    
    percentage = (completed / total) * 100
    username = get_username_display()
    
    if percentage >= 90:
        return f"Almost done, {username}! 🎉"
    elif percentage >= 75:
        return f"Great progress, {username}! Keep it up! 💪"
    elif percentage >= 50:
        return f"You're halfway there, {username}! 🚀"
    elif percentage >= 25:
        return f"Good start, {username}! Keep going! ⭐"
    else:
        return f"Let's do this, {username}! 💪"


def is_authenticated() -> bool:
    """
    Check if user is currently authenticated.
    
    Returns:
        True if authenticated, False otherwise
    """
    return get_current_user() is not None


def get_personal_stats_message(sprint_count: int) -> str:
    """
    Get personalized message about user's sprint statistics.
    
    Args:
        sprint_count: Number of sprints user has
        
    Returns:
        Personalized statistics message
    """
    username = get_username_display()
    
    if sprint_count == 0:
        return f"This is your first sprint, {username}! Let's make it count! 🎯"
    elif sprint_count == 1:
        return f"You've created 1 sprint so far. Let's build another! 🚀"
    elif sprint_count < 5:
        return f"You've created {sprint_count} sprints so far. You're building momentum! 💪"
    elif sprint_count < 10:
        return f"You've created {sprint_count} sprints! You're getting good at this! ⭐"
    elif sprint_count < 20:
        return f"Impressive! {sprint_count} sprints and counting! You're a pro! 🏆"
    else:
        return f"Wow! {sprint_count} sprints! You're a Stride master! 👑"
