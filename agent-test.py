from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from typing import Dict, Any, Optional

class AgentFoundation:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key and verify it exists
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("No API key found! Make sure OPENAI_API_KEY is set in your .env file")
        
        # Log API key presence without exposing any characters
        print("API Key loaded successfully!")
        
        self.agent_identity = """
        You are a specialized CI/CD AI Agent with expertise in:
        1. Code Analysis & Review
        2. Pipeline Optimization
        3. Security Assessment
        4. Development Workflow Enhancement
        
        Your primary goal is to assist with software development processes,
        providing accurate analysis and actionable recommendations.
        """
        
        self._initialize_llm()
        self._initialize_conversation_chain()

    def _initialize_llm(self) -> None:
        """Initialize the language model with error handling"""
        try:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.7,
                api_key=self.api_key
            )
            print("LLM initialized successfully!")
        except Exception as e:
            error_msg = f"Error initializing LLM: {str(e)}"
            print(f"Detailed error during LLM initialization: {error_msg}")
            raise RuntimeError(error_msg)

    def _initialize_conversation_chain(self) -> None:
        """Initialize the conversation chain with memory and prompt"""
        try:
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

            self.prompt = PromptTemplate(
                input_variables=["chat_history", "input"],
                template=f"{self.agent_identity}\n\n"
                        "Previous conversation context:\n"
                        "{chat_history}\n\n"
                        "Human: {input}\n"
                        "AI Assistant: Let me help you with that."
            )

            self.conversation = ConversationChain(
                llm=self.llm,
                memory=self.memory,
                prompt=self.prompt,
                verbose=True
            )
            print("Conversation chain initialized successfully!")
        except Exception as e:
            error_msg = f"Error initializing conversation chain: {str(e)}"
            print(f"Detailed error: {error_msg}")
            raise RuntimeError(error_msg)

    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """
        Analyzes the user's request and provides appropriate response
        """
        if not user_input or not user_input.strip():
            return {
                "status": "error",
                "error": "Empty input provided",
                "metadata": {
                    "error_type": "ValueError"
                }
            }

        try:
            response = self.conversation.predict(input=user_input)
            
            return {
                "status": "success",
                "response": response,
                "metadata": {
                    "interaction_type": self._determine_interaction_type(user_input),
                    "confidence_score": self._calculate_confidence_score(response)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "metadata": {
                    "error_type": type(e).__name__
                }
            }

    def _determine_interaction_type(self, user_input: str) -> str:
        """
        Determines the type of interaction based on user input
        """
        input_lower = user_input.lower()
        
        keywords = {
            "code_analysis": ["analyze", "review", "check", "function", "code"],
            "pipeline_optimization": ["pipeline", "workflow", "ci", "cd", "actions"],
            "security_assessment": ["secure", "vulnerability", "risk", "safety"]
        }
        
        for interaction_type, words in keywords.items():
            if any(word in input_lower for word in words):
                return interaction_type
        
        return "general_inquiry"

    def _calculate_confidence_score(self, response: str) -> float:
        """
        Calculates a confidence score for the response
        """
        score = 0.7  # Base confidence score
        
        # Analyze response complexity
        if len(response) > 200:
            score += 0.1
        if len(response) > 500:
            score += 0.05
            
        # Check for analytical indicators
        indicators = ["however", "alternatively", "consider", "recommend", "analysis"]
        score += 0.02 * sum(1 for indicator in indicators if indicator in response.lower())
            
        return min(score, 1.0)

    def verify_api_key(self) -> bool:
        """
        Verifies if the API key is valid by making a test call
        """
        try:
            # Make a minimal test call
            self.llm.invoke("Test")
            return True
        except Exception as e:
            print(f"API Key verification failed: {str(e)}")
            return False
