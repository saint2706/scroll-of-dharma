# 🕉️ The Scroll of Dharma

Welcome, seeker of wisdom. This interactive web application unfolds ancient truths through symbolic glyphs, sacred sound, and poetic transitions. Let the lotus bloom, the wheel turn, and the trident rise as you journey through each chapter of reflection and resolve.

This project is built with Python and Streamlit, creating a serene, web-based experience.

## ✨ Features

-   **Interactive Journey**: Select from four different "scrolls," each with its own unique visuals, narrative, and audio.
-   **Animated Visuals**: Each scene features a subtly animated SVG icon that brings the experience to life.
-   **Sacred Audio**: Includes two audio tracks for each scene—an introductory chant and a looping ambient track for meditation.
-   **Responsive Design**: The application is fully responsive and provides an excellent experience on both desktop and mobile devices.
-   **Automated Setup**: A setup script handles the creation of necessary directories and the downloading and processing of all audio assets.
-   **Accessibility**: Screen-reader friendly, keyboard navigation, alt text for images, and a skip-to-content link.
-   **Contrast Mode**: Toggle high-contrast mode for improved readability.
-   **About Page**: Learn about the project, its inspiration, and features from the sidebar.

## 🛠️ Setup and Installation

To run this project locally, you will need Python 3.8+ and `pip` installed.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/scroll-of-dharma.git
    cd scroll-of-dharma
    ```

2.  **Create and Activate a Virtual Environment** (Recommended):
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    The `setup.py` script will handle this for you, but you can also install them manually from `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Setup Script**:
    This crucial step downloads the audio from YouTube and processes it into the required formats. It also creates the `config.json` file needed by the app.
    ```bash
    python setup.py
    ```
    **Note**: This step requires `ffmpeg` to be installed on your system and accessible in your PATH. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

## 📜 How to Run the App

Once the setup is complete, you can launch the Streamlit application:

```bash
streamlit run app.py
```

This will open the application in a new tab in your web browser.

## 📂 Project Structure

```
.
├── assets/              # Visual and audio assets
│   ├── audio/           # Generated audio files (ignored by git)
│   ├── svg/             # SVG icons
│   └── ...
├── app.py               # The main Streamlit application script
├── setup.py             # Setup script for asset processing
├── audio_utils.py       # Utility functions for downloading and processing audio
├── narrative.py         # Contains the narrative text for each scene
├── requirements.txt     # Project dependencies
├── .gitignore           # Specifies files for git to ignore
└── README.md            # This file
```

## 🧑‍💻 Technical Improvements

-   **Caching**: Asset loading uses Streamlit's cache for performance.
-   **Session State**: Progress tracking and contrast mode are stored in session state.
-   **Accessibility**: ARIA labels, alt text, and keyboard navigation for all major elements.
-   **Contrast Mode**: Toggle in the sidebar for high-contrast accessibility.
-   **About Page**: Sidebar page with project background, features, and credits.

## 🦾 Accessibility & Usability

-   Keyboard navigation for dropdowns and audio controls.
-   Alt text and ARIA labels for all images and SVGs.
-   Skip-to-content link for screen readers.
-   High-contrast mode for visually impaired users.

## ℹ️ About

Access the About page from the sidebar to learn more about the inspiration, features, and technical details of the Scroll of Dharma.

---

*Crafted with reverence • Powered by Streamlit*
