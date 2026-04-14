import os
import urllib.request

URL = 'https://www.gutenberg.org/cache/epub/2388/pg2388.txt'
TARGET = os.path.join(os.path.dirname(__file__), 'bhagavad_gita.txt')


def download_bhagavad_gita():
    print('Downloading Bhagavad Gita text from Project Gutenberg...')
    with urllib.request.urlopen(URL, timeout=30) as response:
        text = response.read().decode('utf-8')
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Saved:', TARGET)
    print('Size:', len(text), 'characters')


if __name__ == '__main__':
    download_bhagavad_gita()
