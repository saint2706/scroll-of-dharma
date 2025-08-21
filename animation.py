import streamlit as st

def inject_glyph_animations():
    st.markdown("""
    <style>
    /* Mobile scaling */
    @media screen and (max-width: 768px) {
      svg { max-width: 80px !important; }
    }

    /* Lotus bloom */
    svg.lotus {
      animation: bloom 4s ease-in-out infinite;
      max-width: 100px;
      display: block;
      margin: auto;
    }
    @keyframes bloom {
      0% { transform: scale(1); opacity: 0.8; }
      50% { transform: scale(1.05); opacity: 1; }
      100% { transform: scale(1); opacity: 0.8; }
    }

    /* Dharma wheel rotation */
    svg.wheel {
      animation: spin 6s linear infinite;
      max-width: 80px;
      display: block;
      margin: auto;
    }
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }

    /* Trident rise */
    svg.trident {
      animation: rise 3s ease-in-out infinite;
      max-width: 100px;
      display: block;
      margin: auto;
    }
    @keyframes rise {
      0% { transform: translateY(0); opacity: 0.8; }
      50% { transform: translateY(-4px); opacity: 1; }
      100% { transform: translateY(0); opacity: 0.8; }
    }
    </style>
    """, unsafe_allow_html=True)
