from llm_app.llm_utils import get_ambiguity_detection_response, get_tool_use, search_pinecone, check_response_appropriateness, generate_response, get_pension_numbers


def runner(query, previous_queries=None):
    if previous_queries is None:
        previous_queries = []

    guardrail = get_ambiguity_detection_response(query)
    if guardrail.get('question_irrelevant') == "yes":
        return "Нерелевантен въпрос", None
    elif guardrail.get('clarification_needed') == "yes":
        clarification_message = guardrail.get('clarification')
        return clarification_message, None
    else:
        tools = get_tool_use(query)
        if tools.get("needs_pension_guidance") == "yes":
            queries_summary = ""
            max_attempts = 3
            for attempt in range(max_attempts):
                # Perform Pinecone search with rephrased query
                search_results, rephrased_query = search_pinecone(query, context=queries_summary)
                generated_response = generate_response(query, search_results)
                
                # Track original query, rephrased query, and the truncated response
                previous_queries.append({
                    "original_query": query,
                    "rephrased_query": rephrased_query,
                    "response": generated_response[:500]
                })

                # Update queries summary to include original and rephrased queries
                queries_summary = "\n".join(
                    [f"Query {i + 1}: {item['original_query']}\nRephrased: {item['rephrased_query']}\nResponse: {item['response']}" 
                    for i, item in enumerate(previous_queries)]
                )

                response = f"Response: {generated_response}, Pinecone History: {queries_summary}"
                
                result, feedback = check_response_appropriateness(generated_response, responses=response)
                if result == "yes":
                    return generated_response, queries_summary
                else:
                    queries_summary = "\n".join(f"Feedback: {feedback}")
            
            return "Неуспешно генериране на отговор", queries_summary
        elif tools.get('needs_pension_calculation') == 'yes':
            result = get_pension_numbers(query=query)
            return result, None
        else:
            return "Няма наличен отговор", None 

def main():
    """
    Main function to execute the runner logic with a user-provided prompt.
    """
    #user_prompt = "How to get old age pension in Bulgaria for war veterans?"
    user_prompt = "I am a 60 year old Bulgarian grandma, who earned 20,000 euros a few years ago. Calculate my private pension."
    try:
        response, additional_info = runner(user_prompt)
        print("Response:", response)
        if additional_info:
            print("Additional Info:", additional_info)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
