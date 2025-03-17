from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from typing import Dict, Any

class AgentFoundation:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key and verify it exists
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("No API key found! Make sure OPENAI_API_KEY is set in your .env file")
        
        # Print first few characters of API key to verify it's loaded (for testing)
        print(f"API Key loaded successfully! Key starts with: {self.api_key[:5]}...")
        
        self.agent_identity = """
        You are a specialized CI/CD AI Agent with expertise in:
        1. Code Analysis & Review
        2. Pipeline Optimization
        3. Security Assessment
        4. Development Workflow Enhancement
        
        Your primary goal is to assist with software development processes,
        providing accurate analysis and actionable recommendations.
        """
        
        try:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",  # Changed from gpt-4 for wider compatibility
                temperature=0.7,
                api_key=self.api_key
            )
            print("LLM initialized successfully!")
        except Exception as e:
            print(f"Detailed error during LLM initialization: {str(e)}")
            raise Exception(f"Error initializing LLM: {str(e)}")
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Initialize conversation chain with custom prompt
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template="""
            {agent_identity}

            Previous conversation context:
            {chat_history}

            Human: {input}
            AI Assistant: Let me help you with that.
            """.format(agent_identity=self.agent_identity, chat_history="{chat_history}", input="{input}")
        )

        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )

    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """
        Analyzes the user's request and provides appropriate response
        """
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
        
        if any(word in input_lower for word in ["analyze", "review", "check"]):
            return "code_analysis"
        elif any(word in input_lower for word in ["pipeline", "workflow", "ci", "cd"]):
            return "pipeline_optimization"
        elif any(word in input_lower for word in ["secure", "vulnerability", "risk"]):
            return "security_assessment"
        else:
            return "general_inquiry"

    def _calculate_confidence_score(self, response: str) -> float:
        """
        Calculates a confidence score for the response
        """
        score = 0.7  # Base confidence score
        
        if len(response) > 200:
            score += 0.1
        if "however" in response.lower() or "alternatively" in response.lower():
            score += 0.1
            
        return min(score, 1.0)

    def verify_api_key(self) -> bool:
       
        try:
                # Make a simple test call
            test_response = self.llm.invoke("Test message")
            return True
        except Exception as e:
            print(f"API Key verification failed: {str(e)}")
            return False


