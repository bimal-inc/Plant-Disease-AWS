from openai import OpenAI

client = OpenAI(api_key='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')


def generate_recommendations(disease_prediction):

    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to provide plant disease management recommendations."},
            {"role": "user", "content": f"The plant has been diagnosed with {disease_prediction}. What are the recommended actions to treat or manage this disease?"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Assuming the response structure includes a 'choices' list with at least one item,
        # and each choice contains a 'message' dictionary with 'content'.
        if response.choices:
            assistant_message = response.choices[0].message.content
            return assistant_message.strip()
        else:
            return "No recommendations available."
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return "Recommendations are currently unavailable."