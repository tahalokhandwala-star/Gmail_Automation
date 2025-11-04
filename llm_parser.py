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
        - client_name (company or organization name from signature or context)
        - project_name
        - location
        - contact_person
        - mobile
        - email
        - scope (work scope or description)
        - deadline

        IMPORTANT INSTRUCTIONS:
        - Extract information that is explicitly mentioned or can be reasonably inferred from context.
        - For client_name: Look for company names in signatures, domains (e.g., azizidevelopments.com → Azizi Developments), letterhead, or any organizational mentions. This is often the sender's company.
        - For email: Check the signature, contact sections, and any email addresses mentioned.
        - For mobile: Look for phone numbers in signatures, contact info, or any phone/mobile mentions (may include country codes like +971).
        - For location: Look for addresses in signatures or project descriptions.
        - Use common sense to identify organizations from domains or context.
        - If information is not present or cannot be confidently determined, use an empty string "".
        - Pay special attention to email signatures for contact and organizational details.
        - Avoid fabricating information not supported by the email content.

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
