import streamlit as st
import pickle
import time

# Set the page config as the first Streamlit command
st.set_page_config(
    page_title="Indo-Ngapak Translator",
    layout="centered"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #333333;
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 10px 24px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border-color: #ff3333;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #2D2D2D;
        margin: 10px 0;
        border: 1px solid #333333;
    }
    .info-box {
        background-color: #2D2D2D;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #333333;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the dictionary model
@st.cache_resource
def load_model():
    with open('model/word_map_model.pkl', 'rb') as file:
        word_map = pickle.load(file)
    
    # Adding new translations
    word_map.update({"aku": "nyong", "ke": "maring", "pergi": "lunga", "sama": "karo"})
    
    # Generate reverse mapping (Ngapak to Indonesia)
    reverse_word_map = {v: k for k, v in word_map.items()}
    
    return word_map, reverse_word_map

def translate_text(text, word_map):
    """Function to handle the translation process"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate translation progress
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
        status_text.text(f"Menerjemahkan... {i+1}%")
    
    # Actual translation
    words = text.lower().split()
    translated_words = [word_map.get(word, word) for word in words]
    translation = " ".join(translated_words)
    
    # Remove progress bar and status text
    progress_bar.empty()
    status_text.empty()
    
    return translation

def main():
    st.title("Indo-Ngapak Translator M-Bart")
    st.markdown("""
    <div class='info-box'>
    Pilih arah terjemahan dan masukkan teks yang ingin diterjemahkan, lalu klik tombol <b>Terjemahkan</b>.
    </div>
    """, unsafe_allow_html=True)

    # Initialize model
    word_map, reverse_word_map = load_model()

    # Dropdown to select translation direction
    translation_direction = st.selectbox("Pilih Arah Terjemahan", ["Indonesia ke Ngapak", "Ngapak ke Indonesia"])

    # Initialize session states
    if 'translation' not in st.session_state:
        st.session_state.translation = ""

    # Input text area with character counter
    source_text = st.text_area(
        "Masukkan teks", height=150, max_chars=512, help="Maksimal 512 karakter"
    )
    
    # Character counter
    remaining_chars = 512 - len(source_text)
    st.caption(f"Sisa karakter: {remaining_chars}")

    def handle_translation():
        """Callback function for the translate button"""
        if source_text.strip():
            if translation_direction == "Indonesia ke Ngapak":
                st.session_state.translation = translate_text(source_text, word_map)
            else:
                st.session_state.translation = translate_text(source_text, reverse_word_map)
        else:
            st.warning("Harap masukkan teks untuk diterjemahkan.")

    # Center the translate button with persistent text
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("Terjemahkan", on_click=handle_translation, use_container_width=True)

    # Always display translation if it exists in session state
    if st.session_state.translation:
        st.markdown("""
            <div class='success-box'>
                <h3 style='color: #ffffff;'>Hasil Terjemahan:</h3>
                <p style='font-size: 1em;'>{}</p>
            </div>
            """.format(st.session_state.translation), unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
        <p>Dikembangkan oleh Teknik Informatika PHB</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
