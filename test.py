from agent import AgentFoundation

def test_agent():
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
        print(f"
Test Case {i}:")
        print(f"Input: {test_case}")
        result = agent.analyze_request(test_case)
        print(f"Status: {result['status']}")
        print(f"Response: {result['response']}")
        print(f"Interaction Type: {result['metadata']['interaction_type']}")
        print(f"Confidence: {result['metadata']['confidence_score']}")
        print("-" * 50)

if __name__ == "__main__":
    test_agent()
