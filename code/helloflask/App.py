from flask import Flask, render_template, request
import openai
import os
import random

app = Flask(__name__)

# Load local .env file if present, then read OPENAI_API_KEY from environment
def load_local_dotenv(path):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value

load_local_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=openai_api_key)

FORTUNES = [
    "Today you will find a small surprise that makes you smile.",
    "A friend will offer you unexpected help.",
    "New ideas are coming; write them down as they arrive.",
    "A quiet moment will bring you a useful answer.",
    "You will make progress on something you have been putting off.",
    "A pleasant change is on the way.",
    "Your energy is strong today; use it to finish one good task.",
    "A simple kindness will come back to you in an unexpected way.",
    "Today is a good day to try something you have never done before.",
    "A fresh perspective will help you solve a small problem."
]

KALIB_FORTUNES = [
    "A flock of seagulls will mistake you for a beach picnic and carry you off.",
    "You will be chased by a swarm of confused garden gnomes until you hide in a trash can.",
    "A giant inflatable duck will deflate beneath you just as you step onto it.",
    "You accidentally glue your shoes to a moving sidewalk and become a local legend.",
    "A bus full of clowns will stop and insist you join their caravan.",
    "You will trip into a vat of glitter and be mistaken for a disco ghost.",
    "A squirrel will steal your hat and demand a ransom in acorns.",
    "You will discover your reflection has run away to start a circus.",
    "A sudden rain of rubber chickens will force you to dance in the street.",
    "You will be recruited by a secret society of overly dramatic pigeons."
]

@app.route('/fortune', methods=['GET', 'POST'])
def fortune():
    name = ''
    fortune_text = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            if name.lower() == 'kalib':
                fortune_text = random.choice(KALIB_FORTUNES)
            else:
                fortune_text = random.choice(FORTUNES)
    return render_template('fortune.html', name=name, fortune=fortune_text)

@app.route('/', methods=['GET', 'POST'])
def index():
    story = None
    kalib_list = None
    if request.method == 'POST':
        if 'action' in request.form and request.form['action'] == 'kalib':
            prompt = "Generate a long, detailed list of creative and fun things someone could do to or with Kalib. Include a variety of activities, pranks, adventures, and interactions."
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a creative and friendly assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.8,
                )
                kalib_list = response.choices[0].message["content"].strip()
            except Exception as e:
                kalib_list = f"Error: {str(e)}"
        elif 'prompt' in request.form:
            prompt = request.form.get('prompt')
            if prompt:
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a creative storyteller."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500,
                        temperature=0.8,
                    )
                    story = response.choices[0].message["content"].strip()
                except Exception as e:
                    story = f"Error: {str(e)}"
    return render_template('index.html', story=story, kalib_list=kalib_list)

if __name__ == '__main__':
    app.run(debug=True)
    