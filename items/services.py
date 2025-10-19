from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import requests
from django.core.files.base import ContentFile
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Load environment variables from openai.env file
load_dotenv('openai.env')

# Get API key from environment variable using the correct name
api_key = os.getenv('openai_apikey')
if not api_key:
    raise ValueError("No OpenAI API key found. Please check openai.env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": f"Generate a detailed description for a clothing item based on the following prompt: {prompt}. Keep it under 200 words and focus on style, materials, and unique features."}]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        raise

def get_item_details(prompt):
    try:
        # Get description and price estimate
        messages = [
            {"role": "system", "content": "You are a fashion expert and pricing specialist."},
            {"role": "user", "content": f"""Based on this clothing description: '{prompt}',
             provide the following in JSON format:
             1. A detailed description (under 200 words)
             2. An estimated price in USD (just the number)
             Format: {{"description": "text", "price": number}}"""}
        ]
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        response = eval(completion.choices[0].message.content.strip())
        
        # Generate image
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Professional product photo of: {prompt}. Fashion photography style, white background.",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Download the generated image
        image_url = image_response.data[0].url
        image_content = requests.get(image_url).content
        
        return {
            'description': response['description'],
            'price': Decimal(str(response['price'])),
            'image_content': image_content
        }
        
    except OpenAIError as e:
        logger.error(f"OpenAI API Error: {str(e)}")
        if os.getenv('DEBUG', 'False').lower() == 'true':
            raise OpenAIError(f"OpenAI API Error: {str(e)}")
        else:
            raise OpenAIError("The AI service is currently unavailable. Please try again later.")