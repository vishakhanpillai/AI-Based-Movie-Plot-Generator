import streamlit as st
from groq import Groq
from pdf_generator import generate_pdf_bytes
from image_gen import generate_stability_image

client = Groq(api_key="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")

# Page config
st.set_page_config(
    page_title="🎬 AI Movie Plot Generator",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pro styling
st.markdown("""
    <style>
    html, body {
        background-color: #f9fafb;
        font-family: 'Segoe UI', sans-serif;
    }

    .block-container {
        padding: 3rem 5rem !important;
    }

    .stTextInput > div > input,
    .stTextArea textarea {
        font-size: 16px;
        border-radius: 8px;
    }

    .stButton button {
        background: linear-gradient(90deg, #ff4b4b, #f97316);
        color: white;
        font-weight: 600;
        font-size: 18px;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2rem;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #e43f3f, #ea580c);
    }

    .script-box {
        background-color: #1e293b;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        overflow-x: auto;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .title-text {
        font-size: 2.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .subtitle-text {
        font-size: 1.2rem;
        color: #ffffff;
        margin-bottom: 2rem;
    }

    .section-header {
        margin-top: 2rem;
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title & subtitle
st.markdown('<div class="title-text">🎬 AI Movie Plot & Scene Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Unleash your creativity. Generate compelling movie plots and visualize dramatic scenes using AI.</div>', unsafe_allow_html=True)

# Sidebar inputs
with st.sidebar:
    st.markdown("### 📝 Story Settings")
    genre = st.text_input("🎭 Genre", "Sci-Fi")
    theme = st.text_input("💡 Theme", "Survival in space")
    characters = st.text_area("👥 Main Characters", "Nova, Zeke, Captain Orlan")

    st.markdown("---")
    model_choice = st.selectbox("🧠 Model", ["meta-llama/llama-4-scout-17b-16e-instruct", "llama3-70b-8192", "llama3-8b-8192"])
    temperature = st.slider("🎲 Creativity (Temperature)", 0.0, 1.0, 0.7)

# Main generate button
if st.button("🎬 Generate Movie Plot and Scene"):
    prompt = f"""
    Write a short movie plot for a {genre} film with the theme '{theme}'. 
    Include the main characters: {characters}.

    Then write a screenplay-style scene based on this plot. 
    The scene should be dramatic or visually impressive.

    Separate the plot and the script clearly using the following format:

    PLOT:  
    <write the plot here>

    SCENE:  
    <write the screenplay scene here>
    """

    with st.spinner("🎥 Generating plot and key scene using Groq..."):
        try:
            response = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1200
            )

            output_text = response.choices[0].message.content

            plot_text = ""
            scene_text = ""

            if "SCENE:" in output_text:
                parts = output_text.split("SCENE:")
                plot_text = parts[0].replace("PLOT:", "").strip()
                scene_text = parts[1].strip()
            else:
                plot_text = output_text.strip()

            st.success("✅ Generation complete!")

            # Show plot in its own section
            st.markdown('<div class="section-header">🎥 Movie Plot Summary</div>', unsafe_allow_html=True)
            st.markdown(plot_text)

            # Show script in styled box
            st.markdown('<div class="section-header">🎬 Key Scene (Script Format)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="script-box">{scene_text}</div>', unsafe_allow_html=True)

            pdf_buffer = generate_pdf_bytes(plot_text, scene_text)
            # Generate image from scene using Stability AI
            if scene_text:
                with st.spinner("🎨 Generating scene image with Stability AI..."):
                    try:
                        img = generate_stability_image(scene_text)
                        st.image(img, caption="🎬 Scene Visualization", use_container_width=True)

                        # Prepare image bytes for download
                        from io import BytesIO

                        buf = BytesIO()
                        img.save(buf, format="JPEG")
                        byte_im = buf.getvalue()

                        st.download_button(
                            label="📥 Download Scene Image",
                            data=byte_im,
                            file_name="scene.jpeg",
                            mime="image/jpeg"
                        )
                    except Exception as e:
                        st.error(f"❌ Image generation failed: {e}")

            st.download_button(
                label="📥 Download Plot & Script as PDF",
                data=pdf_buffer,
                file_name="movie_plot_and_script.pdf",
                mime="application/pdf"
            )


        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
