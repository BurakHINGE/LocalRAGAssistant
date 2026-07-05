from foundry_local_sdk import Configuration, FoundryLocalManager

def main():
    print("Foundry Local is starting...")
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    chat_model_name = "phi-3.5-mini" 
    model = manager.catalog.get_model(chat_model_name)
    
    print(f"Loading '{chat_model_name}' chat model...")
    # Zaten indirdiğimiz için sadece load() yapmamız yeterli
    model.load()
    
    client = model.get_chat_client()
    
    # RAG Scenario Simulation (English Context)
    retrieved_context = "Marmara University Cyber Security Society organized 5 major CTF competitions in the spring semester of 2026. The club's events are generally held in the engineering faculty laboratories."
    
    # PROMPT ENGINEERING: Precise English rules
    system_prompt = f"""You are a precise AI assistant. 
    Use ONLY the information provided in the 'Context' below to answer questions. 
    If the answer is not contained in the context, do not guess, do not explain why, and do not hallucinate. Simply say: 'I do not have this information.'
    
    Context: {retrieved_context}
    """
    
    # Test 1: Answer IS in the context
    question_1 = "How many competitions did the club organize in the spring of 2026?"
    
    # Test 2: Answer IS NOT in the context (Hallucination trigger)
    question_2 = "Who is the current president of the club, and how can I join?"

    print("\n--- Test 1: In-Context Question ---")
    print(f"User: {question_1}")
    response_1 = client.complete_chat(messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question_1}
    ])
    print(f"AI: {response_1.choices[0].message.content}")

    print("\n--- Test 2: Out-of-Context Question (Hallucination Test) ---")
    print(f"User: {question_2}")
    response_2 = client.complete_chat(messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question_2}
    ])
    print(f"AI: {response_2.choices[0].message.content}")

if __name__ == "__main__":
    main()