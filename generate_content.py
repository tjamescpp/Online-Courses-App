import openai
from openai import OpenAI
client = OpenAI()
# import os

# Load API key from environment variables
# api_key = os.getenv("OPENAI_API_KEY")


def generate_course(topic, language):
    """
    Generate a course outline based on the selected topic and programming language.

    Args:
        topic (str): The topic for the course (e.g., Data Structures).
        language (str): The programming language for the course (e.g., Python).

    Returns:
        list: A list of lessons for the course.
    """
    prompt = (
        f"A person wants to learn about {topic} using {language}."
        "Act as an instructor designing an online course, breakdown the course into a list of modules with a brief description for each one."
    )

    try:
        # Send the request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 if available for better results
            messages=[
                {"role": "system", "content": "You are creating an online college course."},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Extract the text response
        generated_text = str(response.choices[0].message.content)

        modules = generated_text.split("####")

        return modules
    except openai.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
