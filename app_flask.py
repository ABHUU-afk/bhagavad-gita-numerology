from flask import Flask, render_template, request, jsonify
import os
import re
import random
from bhagavad_gita_data import CHAPTER_THEMES, GITA_TOPICS, GITA_ADVICE, GITA_QUOTE_PROMPTS, GITA_KEY_TEACHINGS

app = Flask(__name__)

BHAGAVAD_GITA_FILE = os.path.join(os.path.dirname(__file__), 'bhagavad_gita.txt')
VOWELS = set('AEIOUY')
LETTER_MAP = {
    'A': 1, 'J': 1, 'S': 1,
    'B': 2, 'K': 2, 'T': 2,
    'C': 3, 'L': 3, 'U': 3,
    'D': 4, 'M': 4, 'V': 4,
    'E': 5, 'N': 5, 'W': 5,
    'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7,
    'H': 8, 'Q': 8, 'Z': 8,
    'I': 9, 'R': 9,
}

def reduce_number(value):
    while value > 9 and value not in (11, 22, 33):
        value = sum(int(digit) for digit in str(value))
    return value

def letter_value(letter):
    return LETTER_MAP.get(letter.upper(), 0)

def normalize_gender(answer):
    answer = answer.strip().lower()
    if answer in ('ladki', 'girl', 'female', 'f', 'woman'):
        return 'ladki'
    return 'ladka'

def calculate_numerology(full_name):
    letters = [ch for ch in full_name.upper() if ch.isalpha()]
    expression = sum(letter_value(ch) for ch in letters)
    soul = sum(letter_value(ch) for ch in letters if ch in VOWELS)
    personality = sum(letter_value(ch) for ch in letters if ch not in VOWELS)
    return {
        'expression': reduce_number(expression) if expression else None,
        'soul': reduce_number(soul) if soul else None,
        'personality': reduce_number(personality) if personality else None,
        'expression_raw': expression,
        'soul_raw': soul,
        'personality_raw': personality,
    }

def calculate_life_path(birthdate):
    digits = [int(ch) for ch in birthdate if ch.isdigit()]
    if len(digits) < 6:
        return None
    return reduce_number(sum(digits))

def calculate_maturity(life_path, expression):
    if life_path is None or expression is None:
        return None
    return reduce_number(life_path + expression)

def missing_karmic_numbers(full_name):
    values = {reduce_number(letter_value(ch)) for ch in full_name.upper() if ch.isalpha()}
    missing = [str(num) for num in range(1, 10) if num not in values]
    return missing

def numerology_description(number):
    descriptions = {
        1: 'Tum ek prerna dene wale neta ho. nayi shuruaat aur nirdeshan tumhari pehchan hai.',
        2: 'Tum bandhutva aur sahayog ke vyakti ho. tum samjhota aur saanjh mein vishwas karte ho.',
        3: 'Tumhara abhivyakti kaushal tej hai. rachnatmakta aur anand tumhari pehchan hai.',
        4: 'Tum sangathan aur mehnat se kaam karne wale ho. tumhari buniyad mazboot hai.',
        5: 'Tum badlav ke shaukeen ho. azaadi aur anyaay se ladne ki shakti tumhare andar hai.',
        6: 'Tum prem, seva aur zimmedari mein vishwas rakhte ho. parivar aur samaj tumhare liye mahatvapurn hai.',
        7: 'Tum gahan sochne wale ho. gyaan aur aadhyatmik khoj tumhari adhikaansh ruchi hai.',
        8: 'Tum mein udyam aur prabhavshali drishti hai. dhan aur adhikar tumhe kheenchte hain.',
        9: 'Tum ek bade uddeshya wale ho. dayalu, pehchaan yogya aur manav seva tumhara lakshya ho sakta hai.',
        11: 'Tum ek prabhaavshali aur adhyatmik soch rakhne wale ho. tum chhote se bada sapna poora kar sakte ho.',
        22: 'Tum ek brihat adyatan nirmaata ho. bade lakshyon ko vyavaharik roop dene ki kshamata tum mein hai.',
        33: 'Tum ek sachche shikshak ho. logon ko prem aur gyaan dena tumhari khasiyat hai.',
    }
    return descriptions.get(number, 'Yeh number tumhari vyaktitva yatra ko aur majboot banata hai.')

def get_gita_advice(challenge, ambition):
    text = (challenge + ' ' + ambition).lower()
    if any(keyword in text for keyword in ('dar', 'doubt', 'kise', 'asha')):
        return GITA_ADVICE['fear']
    if any(keyword in text for keyword in ('career', 'job', 'kaam', 'paisa', 'business')):
        return GITA_ADVICE['career']
    if any(keyword in text for keyword in ('pyaar', 'prema', 'love')):
        return GITA_ADVICE['love']
    if any(keyword in text for keyword in ('tanaav', 'stress', 'pressure', 'chinta')):
        return GITA_ADVICE['stress']
    if any(keyword in text for keyword in ('swasthya', 'health', 'sharir', 'bimari')):
        return GITA_ADVICE['health']
    if any(keyword in text for keyword in ('rishta', 'relationship', 'parivar', 'dosti')):
        return GITA_ADVICE['relationships']
    if any(keyword in text for keyword in ('aadhyatmik', 'spirituality', 'gyaan', 'bhakti', 'ishwar')):
        return GITA_ADVICE['spirituality']
    if any(keyword in text for keyword in ('safalta', 'success', 'jay', 'vijay')):
        return GITA_ADVICE['success']
    if any(keyword in text for keyword in ('asafalta', 'failure', 'haar', 'nakaam')):
        return GITA_ADVICE['failure']
    if any(keyword in text for keyword in ('krodh', 'anger', 'gussa')):
        return GITA_ADVICE['anger']
    if any(keyword in text for keyword in ('lobh', 'greed', 'lalach')):
        return GITA_ADVICE['greed']
    if any(keyword in text for keyword in ('irsha', 'jealousy', 'jaln')):
        return GITA_ADVICE['jealousy']
    if any(keyword in text for keyword in ('kshama', 'forgiveness', 'maaf')):
        return GITA_ADVICE['forgiveness']
    if any(keyword in text for keyword in ('dhairya', 'patience', 'sabar')):
        return GITA_ADVICE['patience']
    if any(keyword in text for keyword in ('netritva', 'leadership', 'leader')):
        return GITA_ADVICE['leadership']
    if any(keyword in text for keyword in ('dhan', 'wealth', 'paise', 'rich')):
        return GITA_ADVICE['wealth']
    if any(keyword in text for keyword in ('padhai', 'education', 'study', 'gyaan')):
        return GITA_ADVICE['education']
    if any(keyword in text for keyword in ('parivar', 'family', 'ghar')):
        return GITA_ADVICE['family']
    if any(keyword in text for keyword in ('dosti', 'friendship', 'mitra')):
        return GITA_ADVICE['friendship']
    if any(keyword in text for keyword in ('akela', 'loneliness', 'alone')):
        return GITA_ADVICE['loneliness']
    if any(keyword in text for keyword in ('kartavya', 'duty', 'farz')):
        return GITA_ADVICE['duty']
    if any(keyword in text for keyword in ('anasakta', 'detachment', 'phaltwag')):
        return GITA_ADVICE['detachment']
    if any(keyword in text for keyword in ('dhyana', 'meditation', 'sadhana')):
        return GITA_ADVICE['meditation']
    if any(keyword in text for keyword in ('gyaan', 'knowledge', 'jaan')):
        return GITA_ADVICE['knowledge']
    if any(keyword in text for keyword in ('bhakti', 'devotion', 'pooja')):
        return GITA_ADVICE['devotion']
    if any(keyword in text for keyword in ('samaanta', 'equanimity', 'barabar')):
        return GITA_ADVICE['equanimity']
    if any(keyword in text for keyword in ('yajna', 'sacrifice', 'bali')):
        return GITA_ADVICE['sacrifice']
    if any(keyword in text for keyword in ('niyantran', 'self-control', 'vash')):
        return GITA_ADVICE['self-control']
    if any(keyword in text for keyword in ('daya', 'compassion', 'rahm')):
        return GITA_ADVICE['compassion']
    if any(keyword in text for keyword in ('satya', 'truth', 'sach')):
        return GITA_ADVICE['truth']
    if any(keyword in text for keyword in ('ahimsa', 'non-violence', 'shanti')):
        return GITA_ADVICE['non-violence']
    if any(keyword in text for keyword in ('santushti', 'contentment', 'khushi')):
        return GITA_ADVICE['contentment']
    if any(keyword in text for keyword in ('sanyas', 'renunciation', 'tyag')):
        return GITA_ADVICE['renunciation']
    if any(keyword in text for keyword in ('mukti', 'liberation', 'azadi')):
        return GITA_ADVICE['liberation']
    return 'Gita ka mool tatva: apne kartavya ko nishkaam bhav se karo aur man ko shaant rakho.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/profile', methods=['POST'])
def get_profile():
    data = request.json
    full_name = data.get('full_name', 'Mitra Sharma')
    age = data.get('age', 20)
    gender = data.get('gender', 'ladka')
    city = data.get('city', 'apna sheher')
    ambition = data.get('ambition', 'safalta paana')
    favorite_color = data.get('favorite_color', 'neela')
    challenge = data.get('challenge', 'naya mauka dhundhna')
    career_goal = data.get('career_goal', 'apna vyavasaay')
    birthdate = data.get('birthdate', '')

    gender_label = normalize_gender(gender)
    numbers = calculate_numerology(full_name)
    life_path = calculate_life_path(birthdate) if birthdate else None
    maturity = calculate_maturity(life_path, numbers['expression']) if life_path else None
    missing = missing_karmic_numbers(full_name)

    result = {
        'profile': f"Namaste {full_name}! Tum ek {gender_label} ho jo {city} mein rehta hai.\nTumhari umar {age} saal hai, aur tumhara sapna hai: {ambition}.",
        'numerology': {
            'expression': numbers['expression'],
            'soul': numbers['soul'],
            'personality': numbers['personality'],
            'life_path': life_path,
            'maturity': maturity,
            'missing': missing,
        },
        'gita_advice': get_gita_advice(challenge, ambition),
        'quote': random.choice(GITA_QUOTE_PROMPTS),
        'chapter_themes': CHAPTER_THEMES,
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
