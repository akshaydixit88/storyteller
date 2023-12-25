from flask import Flask, render_template, jsonify, request
import re
from openai import OpenAI

app = Flask(__name__)

# Set your OpenAI GPT-3.5 Turbo API key

client = OpenAI(
  api_key='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',  # this is also the default, it can be omitted
)


def generate_story(character, situation, style,age):
    
    prompt = f"Write a 5-minute story for young children\\n Character: {character}\\n Situation: {situation}\\n Style: {style}\\n Age group: {age}\\nInstructions -\\n1. Create a story for kids in age group provided\\n2.Include supporting characters from this pool: Mom, Dad, friends,cousins, teachers or pets\\nOutput: 10 paragraphs each with 4 lines. Each line separated by line breaker\\nAdd story title on line 1"
    # Call OpenAI GPT-3.5 Turbo to generate the story
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can adjust the engine as needed
        messages=[{"role": "system","content": "You are a reputed author of young kids books"},{"role": "user","content": prompt}],
        temperature=0.8,
  max_tokens=500,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
    )

    # Extract the generated story from the OpenAI response
    generated_story = response.choices[0].message.content.strip()

    return generated_story

def generate_image(character, situation):
   
    prompt_i = f"Kids storybook cover: {character} in {situation}"

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt_i,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url


def format_story(generated_story, image_url):
    # Split the story into paragraphs
    paragraphs = generated_story.split('\n\n')  # Assuming double newline separates paragraphs

    # Extract the title from the first paragraph
    title = paragraphs[0].strip()

    # Remove the title paragraph from the content
    content = paragraphs[1:]

    # Format into the desired structure
    formatted_story = [
        {"Page": page_num + 1, "Content": paragraph.strip()}
        for page_num, paragraph in enumerate(content)
    ]

    return {"title": title, "story": formatted_story, "image_url": image_url}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_story', methods=['POST'])
def get_story():
    # Get character and situation values from the request
    character = request.form.get('character')
    situation = request.form.get('setting')  # Rename 'setting' to 'situation'
    style = request.form.get('style')
    age = request.form.get('age')
    # Generate the story based on character and situation using GPT-3.5 Turbo
    generated_story = generate_story(character, situation, style,age)
    image_url = generate_image(character, situation)
    
    # Format the generated story
    formatted_story = format_story(generated_story, image_url)
    print (formatted_story)
    return jsonify(formatted_story)

if __name__ == '__main__':
    app.run(debug=True)
