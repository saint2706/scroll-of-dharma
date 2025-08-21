# 🌸 The Dharma Scroll 🔄  
_An Interactive Journey Through Arjuna’s Awakening_

> “Slay with equanimity. Grieve not. Act with clarity.”  
> — Krishna, Bhagavad Gita

---

## 🧙‍♂️ What Is This?

**The Dharma Scroll** is a mythic web app that transforms the Bhagavad Gita’s emotional arc into an interactive experience.  
Built with **Streamlit**, it blends:

- 🌀 **Symbolic animations** inspired by ancient Indian motifs  
- 📖 **Narrative chapters** drawn from Arjuna’s spiritual crisis  
- 🎼 **Chants and ambient loops** that deepen emotional resonance  
- 📜 **Parchment textures and lotus glyphs** for manuscript-style storytelling

---

## 🔍 Chapters

| Chapter | Symbol | Theme |
|--------|--------|-------|
| 🌸 Arjuna’s Doubt | Lotus | Compassion vs Duty  
| 🔄 Krishna’s Counsel | Chakra | Clarity through Wisdom  
| 🌀 Vision of Dharma | Spiral | Surrender to Eternity  
| ⚔️ Call to Action | Sword | Action without Attachment  

Each chapter unfolds with narration, animation, and sound.

---

## 🚀 Launch It

### ▶️ Streamlit Cloud  
You can run the app instantly via [Streamlit Community Cloud](https://streamlit.io/cloud).  
Just clone this repo and deploy:

```bash
git clone https://github.com/your-username/dharma-scroll.git
cd dharma-scroll
streamlit run app.py
```

---

## 📦 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Setup Script
```bash
python setup.py
```
This will:
- Download chants from YouTube
- Generate fade-in and ambient audio
- Organize assets and create `config.json`

---

## 📁 Project Structure

```
dharma_scroll/
├── app.py
├── animation.py
├── narrative.py
├── audio.py
├── audio_utils.py
├── setup.py
├── config.json
├── assets/
│   ├── audio/{raw,fadein,ambient}
│   ├── textures/parchment_bg.png
│   ├── fonts/UncialAntiqua.ttf
│   └── svg/lotus.svg
```

---

## 📱 Mobile Responsiveness

The app is optimized for mobile with:
- Responsive layout using `use_container_width=True`
- Scalable fonts and banner
- Touch-friendly chapter selector

---

## 🧾 Credits

- Narration & Design: **Saint**  
- Built with: [Streamlit](https://streamlit.io), [Plotly](https://plotly.com), [yt-dlp](https://github.com/yt-dlp/yt-dlp), [pydub](https://github.com/jiaaro/pydub)  
- Fonts: [Uncial Antiqua](https://fonts.google.com/specimen/Uncial+Antiqua)  
- Textures: Custom parchment with lotus watermark

---

## ⚖️ License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🌺 Final Blessing

> _May your actions be rooted in clarity, your vision in truth, and your path in dharma._
