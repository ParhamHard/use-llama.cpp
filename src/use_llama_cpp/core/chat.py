"""
Chat functionality for AI Room application.
"""

import logging
from typing import List, Dict, Any, Optional
from llama_cpp import Llama

logger = logging.getLogger(__name__)


class AIChat:
    """Handles chat interactions with the loaded language model."""
    
    def __init__(self, model: Llama, system_prompt: str = None):
        """
        Initialize the chat interface.
        
        Args:
            model: Loaded Llama model instance
            system_prompt: System prompt for the AI assistant
        """
        self.model = model
        self.system_prompt = system_prompt or "You are a helpful AI assistant. Keep your responses concise and relevant."
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]
        
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_response(self, 
                    user_message: str, 
                    max_tokens: int = 100,
                    temperature: float = 0.3,
                    top_p: float = 0.9,
                    top_k: int = 40,
                    repeat_penalty: float = 1.1) -> Optional[str]:
        """
        Get a response from the AI model.
        
        Args:
            user_message: User's input message
            max_tokens: Maximum tokens in response
            temperature: Response randomness (0.0 = deterministic, 1.0 = random)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            repeat_penalty: Penalty for repetition
            
        Returns:
            AI response text or None if error
        """
        # Add user message to conversation
        self.add_message("user", user_message)
        
        try:
            response = self.model.create_chat_completion(
                messages=self.conversation_history,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repeat_penalty=repeat_penalty,
                stop=["\nHuman:", "Human:", "Assistant:"]
            )
            
            response_text = response['choices'][0]['message']['content'].strip()
            
            if response_text:
                # Add AI response to conversation history
                self.add_message("assistant", response_text)
                return response_text
            else:
                logger.warning("Empty response from model")
                return None
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        logger.info("Conversation history reset")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
    
    def set_system_prompt(self, new_prompt: str):
        """Update the system prompt."""
        self.system_prompt = new_prompt
        # Update the first message in conversation history
        if self.conversation_history and self.conversation_history[0]["role"] == "system":
            self.conversation_history[0]["content"] = new_prompt
        else:
            self.conversation_history.insert(0, {"role": "system", "content": new_prompt})
        logger.info("System prompt updated")
