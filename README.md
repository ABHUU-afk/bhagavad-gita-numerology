# Bhagavad Gita Project

Is folder mein Bhagavad Gita ki public-domain text (`bhagavad_gita.txt`) rakhi gayi hai.

## Files

- `bhagavad_gita.txt`: Bhagavad Gita ka public-domain anuvad.
- `bhagavad_gita_data.py`: Bhagavad Gita ke chapter themes, topics aur advice data.
- `fetch_bhagavad_gita.py`: Agar tumhe text dobara download karna ho to is script ko chalayo.
- `interactive_profile.py`: Ye script tumse zyada sawaal poochega, poore numerology profile ke saath tumhe Bhagavad Gita insights dega.
- `app.py`: Web app version using Streamlit.
- `requirements.txt`: Dependencies for the app.
- `run_project.bat`: Windows par double-click karne se script turant chal jayega.

## Features

- Poora naam aur janam tithi lekar numerology calculate karta hai:
  - Expression/Destiny number
  - Soul urge number
  - Personality number
  - Life path number
  - Maturity number
  - Missing karmic lesson numbers
- Bhagavad Gita ke mukhya topics aur chapter themes dikhata hai.
- Gita ke aadhar par aapki chunautiyon aur ambitions ke liye advice deta hai.
- Bhagavad Gita file se chapter preview bhi nikalta hai.

## Kaise chalaye

### Command Line Version
Windows mein terminal khol kar:

```bash
cd "c:\Users\abhin\OneDrive\Documents\BHAGWAD GITA PROJECT\New folder"
python interactive_profile.py
```

Ya seedha `run_project.bat` pe double-click karke bhi chala sakte ho.

### Web App Version
Streamlit app ko chalane ke liye:

1. Dependencies install karo:
```bash
pip install -r requirements.txt
```

2. App chalao:
```bash
python -m streamlit run app.py
```

Ya Windows par directly run karne ke liye `run_web_app.bat` double-click karo.

Ye browser mein app khol dega.

### Online Deployment
App ko online deploy karne ke liye:
- GitHub pe repository banao aur files upload karo.
- Streamlit Cloud pe jaao (share.streamlit.io) aur repository connect karo.
- Ye ek public link dega jahan se app access kar sakte ho.

### GitHub push commands
Agar tumne GitHub repo create kiya hai aur local folder ko repo banana hai, to terminal mein yeh chalayo:

```bash
cd "c:\Users\abhin\OneDrive\Documents\BHAGWAD GITA PROJECT\New folder"
git init
git add .
git commit -m "Add Bhagavad Gita Streamlit app"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

अगर GitHub repo पहले से connected है, तो बस:

```bash
git add .
git commit -m "Update Bhagavad Gita app"
git push
```

अगर Git आपके system में नहीं है, तो पहले इसे install करो:
- https://git-scm.com/download/win

### Streamlit Cloud deploy steps
1. `share.streamlit.io` पर जाओ और GitHub login करो.
2. `New app` चुनो.
3. GitHub repo select करो.
4. Branch चुनो: `main`.
5. Main file path डालो: `app.py`.
6. Deploy करो.

Deploy के बाद link copy कर लो, और वही public link सबको दे सकते हो.

Agar `bhagavad_gita.txt` nahi milta, to:

```bash
python fetch_bhagavad_gita.py
```

Fir dubara `python interactive_profile.py` ya `streamlit run app.py` chalaye.
