from openai import OpenAI
from cfg import CONFIG

client = OpenAI(api_key=CONFIG.get("OpenAI_API"))

def description_by_image(image_url, description_type: str = "for buyer"):
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "you're an expert at detecting interior designs from photos and writing descriptions for them.\n"
                "If image isn't iterior design (photo of flat or house), write about it and don't write any descriptions.\n"
                "Input: the type of description and an image of the design.\n"
                "Output: a detailed text description of the design in Russian.\n"
                
            },
            {
                "role": "user",
                "content": f"Type: {description_type}, Image URL: {image_url}"
            },
        ],
    )
    return completion.choices[0].message.content


