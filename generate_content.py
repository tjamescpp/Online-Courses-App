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
        f"A person wants to learn about {topic} in {language}."
        f"Act as an instructor designing an online course, breakdown the course about {
            topic}"
        f"in {language} into a bullet pointed list of modules with a brief description for each one."
        f"Only list the modules, add bold headers and normal text description as a bullet point."
    )

    # Extract the text response
    generated_text = str(get_openai_response(prompt))
    print(generated_text)

    # Split markdown
    modules = generated_text.split("\n\n")

    return modules


def get_openai_response(prompt):
    try:
        # Send the request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 if available for better results
            messages=[
                {"role": "system", "content": "You are an college professor creating an online course."},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content
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


def generate_more_info(prompt):
    print(f"Getting more info for {prompt}: ")
    new_prompt = (
        f"Give an in-depth explanation of {
            prompt}."
        f"Only return a list, not numbered, with brief text explanations and coding examples.")
    more_info = get_openai_response(new_prompt)
    return more_info
