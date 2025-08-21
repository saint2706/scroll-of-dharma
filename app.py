import streamlit as st
from animation import get_dharma_animation
from narrative import chapters
from audio import chant_links

# Page setup
st.set_page_config(page_title="The Dharma Scroll", layout="wide")

# Responsive banner styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Uncial+Antiqua&display=swap');

.banner {
  font-family: 'Uncial Antiqua', serif;
  background: linear-gradient(135deg, #fdf6e3 0%, #f5e6b3 100%);
  background-image: url('assets/textures/parchment_bg.png');
  background-repeat: repeat;
  background-size: 400px;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  color: #3e2f1c;
  box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 0, 0, 0.4);
  border: 10px solid transparent;
  border-image: url('https://i.imgur.com/6YVZzGk.png') 30 round;
}

.banner h1 {
  font-size: 3em;
  margin-bottom: 10px;
  color: #5c3d1b;
  text-shadow: 1px 1px 2px #d8caa8;
}

.banner p {
  font-size: 1.2em;
  margin-top: 5px;
  color: #4a3b2c;
}

@media screen and (max-width: 600px) {
  .banner h1 { font-size: 2em !important; }
  .banner p { font-size: 1em !important; }
}
</style>

<div class="banner">
  <h1>🌸 The Dharma Scroll 🔄</h1>
  <p>An Interactive Journey Through Arjuna’s Awakening</p>
  <p>Unfold the Mahabharata’s wisdom through animated symbolism, mythic narration, and immersive storytelling.</p>
  <p><em>🕉️ Built with Streamlit | Designed by Rishabh</em></p>
</div>
""", unsafe_allow_html=True)

# Chapter selector
selected_chapter = st.radio("📜 Choose a Chapter", list(chapters.keys()), horizontal=True)
chapter = chapters[selected_chapter]
audio = chant_links[selected_chapter]

# Layout: narration and animation side by side
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"## {chapter['title']}")
    st.markdown(chapter["text"])
with col2:
    fig = get_dharma_animation(chapter["tooltip"])
    st.plotly_chart(fig, use_container_width=True)

# Symbolic insight
with st.expander("🔍 Symbolic Insight"):
    st.markdown(f"**Tooltip Meaning:** {chapter['tooltip']}")

# Sound of Dharma
st.markdown("### 🎼 Sound of Dharma")
mute = st.checkbox("🔇 Mute ambient loop")

st.markdown(f"""
<audio autoplay controls title="{audio['tooltip']}">
  <source src="{audio['url']}" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

if not mute:
    st.markdown(f"""
    <audio autoplay loop hidden>
      <source src="{audio['ambient']}" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🪷 _May your actions be rooted in clarity, your vision in truth, and your path in dharma._")