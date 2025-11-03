import openai
from config import OPENAI_API_KEY, OPENAI_MODEL

class LLMParser:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def parse_email_body(self, email_body):
        """
        Send email body to OpenAI and extract structured data.
        Returns dict with: client_name, project_name, location, contact_person, mobile, email, scope, deadline
        """
        prompt = f"""
        Extract the following information from the email body below. Respond only with a JSON object containing these fields:
        - client_name
        - project_name
        - location
        - contact_person
        - mobile
        - email
        - scope (work scope or description)
        - deadline

        If a field is not mentioned, use an empty string "". Try to infer if possible.

        Email Body:
        {email_body}
        """

        try:
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at extracting structured information from emails. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0
            )

            result_text = response.choices[0].message.content.strip()
            # Assuming it returns JSON, parse it
            import json
            parsed = json.loads(result_text)
            return parsed
        except Exception as e:
            print(f"Error parsing with LLM: {e}")
            # Return fallback empty dict or handle error
            return {
                'client_name': '',
                'project_name': '',
                'location': '',
                'contact_person': '',
                'mobile': '',
                'email': '',
                'scope': '',
                'deadline': ''
            }
