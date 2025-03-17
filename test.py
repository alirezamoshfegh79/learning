from agent import AgentFoundation
import sys
import traceback

def test_agent():
    try:
        # Initialize the agent
        print("Initializing agent...")
        agent = AgentFoundation()
        
        # Test cases
        test_cases = [
            "Review this Python function: def add(a, b): return a + b",
            "How can I make my GitHub Actions workflow faster?",
            "Check if this Docker configuration is secure: FROM python:3.9-slim",
        ]
        
        # Run tests
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print(f"Input: {test_case}")
            try:
                result = agent.analyze_request(test_case)
                print(f"Status: {result.get('status', 'N/A')}")
                print(f"Response: {result.get('response', 'N/A')}")
                
                metadata = result.get('metadata', {})
                print(f"Interaction Type: {metadata.get('interaction_type', 'N/A')}")
                print(f"Confidence: {metadata.get('confidence_score', 'N/A')}")
            except Exception as e:
                print(f"Error in test case {i}: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
            print("-" * 50)

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    test_agent()
