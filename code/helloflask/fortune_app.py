from flask import Flask, render_template, request
import random

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    name = ''
    fortune = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            if name.lower() == 'kalib':
                fortune = random.choice(KALIB_FORTUNES)
            else:
                fortune = random.choice(FORTUNES)
    return render_template('fortune.html', name=name, fortune=fortune)

if __name__ == '__main__':
    app.run(debug=True)