import streamlit as st
import numpy as np
import pandas as pd
import joblib
import base64
import time
from datetime import datetime

# ================================
# 🎯 CONFIGURATION
# ================================
MODEL_PATH = "Carrier_Recommendation_System.pkl"  # ✅ Update to your actual model name
FEATURE_NAMES = ["Age", "Education", "Skills", "Interests", "Recommendation_Score"]

# ================================
# ⚙️ UTILITIES
# ================================
def get_base64_image_url(uploaded_file):
    """Converts uploaded image to Base64 URL."""
    try:
        bytes_data = uploaded_file.getvalue()
        base64_encoded_data = base64.b64encode(bytes_data).decode("utf-8")
        mime_type = uploaded_file.type or "image/png"
        return f"data:{mime_type};base64,{base64_encoded_data}"
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None


def set_cinematic_bg(base64_urls, interval_per_image=6):
    """Applies cinematic slideshow background."""
    num_images = len(base64_urls)
    total_duration = num_images * interval_per_image
    OVERLAY_OPACITY = "rgba(0,0,0,0.6)"

    FROSTED_GLASS_SELECTORS = """
        [data-testid="stSidebar"] > div:first-child,
        [data-testid="stTabs"] > div:nth-child(2)
    """

    if num_images == 0:
        st.info("No images uploaded. Using default gradient background.")
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #1b2735, #090a0f);
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)
        return

    css_keyframes = []
    for i in range(num_images):
        start_percent = (i * 100) / num_images
        hold_percent = start_percent + (100 / num_images)
        css_keyframes.append(f"{start_percent:.2f}% {{ background-image: url('{base64_urls[i]}'); }}")
        css_keyframes.append(f"{hold_percent:.2f}% {{ background-image: url('{base64_urls[i]}'); }}")
    css_keyframes.append(f"100% {{ background-image: url('{base64_urls[0]}'); }}")

    st.markdown(f"""
        <style>
        .stApp {{
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-image: url('{base64_urls[0]}');
            animation: cinematicBg {total_duration}s infinite;
            color: white;
        }}
        @keyframes cinematicBg {{
            {"".join(css_keyframes)}
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: {OVERLAY_OPACITY};
            z-index: 0;
        }}
        {FROSTED_GLASS_SELECTORS} {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(8px);
            border-radius: 16px;
            padding: 20px;
            z-index: 10;
        }}
        * {{ font-family: 'Poppins', sans-serif; }}
        [data-testid="stHeader"], [data-testid="stToolbar"] {{ background: transparent !important; }}
        </style>
    """, unsafe_allow_html=True)


# ================================
# 🧠 LOAD MODEL
# ================================
try:
    model = joblib.load(MODEL_PATH)
    st.info("✅ Model loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    model = None

# ================================
# 📂 SIDEBAR
# ================================
base64_image_urls = []
with st.sidebar:
    st.title("⚙️ App Configuration")

    uploaded_files = st.file_uploader(
        "🖼️ Upload background images (slideshow):",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload 3+ background images for cinematic transitions."
    )

    if uploaded_files:
        with st.spinner("Processing images..."):
            for file in uploaded_files:
                url = get_base64_image_url(file)
                if url:
                    base64_image_urls.append(url)
            time.sleep(0.5)
        st.success("✅ Background images ready!")

    st.markdown("---")
    st.subheader("📘 About the Model")
    st.info("This ML model predicts the most suitable career path based on your profile and interests.")
    st.markdown(f"📅 Last Updated: **{datetime.now().strftime('%b %d, %Y')}**")
    st.markdown("👨‍💻 Developed by **Umar Imam**", unsafe_allow_html=True)

set_cinematic_bg(base64_image_urls)

# ================================
# 🎓 HEADER
# ================================
st.set_page_config(layout="centered")
st.markdown("""
<h1 style='text-align:center; color:#ff9900; text-shadow: 2px 2px 6px #000;'>🎓 AI-Based Career Recommendation System</h1>
<p style='text-align:center; font-size:18px; color:#fff;'>Find the ideal career path based on your academic background, skills, and interests.</p>
""", unsafe_allow_html=True)

# ================================
# 📊 TABS
# ================================
tab1, tab2, tab3 = st.tabs(["💡 Career Prediction", "📈 Model Analytics", "📘 Info"])

# ================================
# 💡 TAB 1 — CAREER PREDICTION
# ================================
# ================================
# 💡 TAB 1 — CAREER PREDICTION
# ================================
with tab1:
    st.header("Enter Your Details")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("🎂 Age", min_value=15, max_value=60, step=1)
        education = st.selectbox("🎓 Education Level", ["High School", "Bachelor's", "Master's", "PhD"])
        skills = st.text_input("🧠 Skills (e.g., Python, Data Analysis, Java)")
    with col2:
        interests = st.text_input("💡 Interests (e.g., AI, Web Dev, Finance)")
        rec_score = st.number_input("📊 Recommendation Score", min_value=0.0, max_value=100.0, step=0.5)

    if st.button("🚀 Predict Career", use_container_width=True):
        if not model:
            st.error("⚠️ Model not loaded. Please check the file path.")
        else:
            try:
                # --- Encoding categorical fields ---
                education_map = {
                    "High School": 0,
                    "Bachelor's": 1,
                    "Master's": 2,
                    "PhD": 3
                }

                skills_map = {
                    "Python": 0, "Java": 1, "C++": 2, "Data Analysis": 3,
                    "Machine Learning": 4, "Web Development": 5, "AI": 6
                }

                interests_map = {
                    "AI": 0, "Web Dev": 1, "Finance": 2, "Data Science": 3, "Cloud": 4
                }

                edu_val = education_map.get(education, 0)
                skill_val = next((v for k, v in skills_map.items() if k.lower() in skills.lower()), 0)
                interest_val = next((v for k, v in interests_map.items() if k.lower() in interests.lower()), 0)

                # --- Make prediction ---
                input_data = np.array([[age, edu_val, skill_val, interest_val, rec_score]])
                pred = model.predict(input_data)[0]

                # --- Career label mapping ---
                career_map = {
                    0: "Software Engineer",
                    1: "Data Scientist",
                    2: "Web Developer",
                    3: "AI Researcher",
                    4: "Cloud Engineer",
                    5: "Business Analyst",
                    6: "Cybersecurity Expert",
                    7: "UI/UX Designer",
                    8: "Database Administrator",
                    9: "Network Engineer",
                    10: "Game Developer",
                    11: "Machine Learning Engineer"
                }

                career_name = career_map.get(int(pred), "Unknown Career")

                # --- Display prediction ---
                st.success(f"🎯 Predicted Career: {career_name}")
                st.markdown(f"""
                <div style="background-color:rgba(255, 153, 0, 0.2); padding:20px; border-radius:15px; text-align:center;">
                    <h3 style="color:white;">Your Recommended Career Path:</h3>
                    <h2 style="color:#ff9900;">{career_name}</h2>
                    <p>Explore opportunities aligned with your skills and interests.</p>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction failed: {e}")



# ✅ Display results
st.success(f"🎯 Predicted Career: {career_name}")

st.markdown(f"""
<div style="background-color:rgba(255, 153, 0, 0.2); padding:20px; border-radius:15px; text-align:center;">
    <h3 style="color:white;">Your Recommended Career Path:</h3>
    <h2 style="color:#ff9900;">{career_name}</h2>
    <p>Explore opportunities aligned with your skills and interests.</p>
</div>
""", unsafe_allow_html=True)
# ================================
# 📈 TAB 2 — MODEL ANALYTICS (Dynamic Image Upload)
# ================================
with tab2:
    st.header("Model Insights and Performance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Training Accuracy", "94%")
    col2.metric("Testing Accuracy", "91%")
    col3.metric("Model Type", "LightGBM Classifier")

    st.markdown("---")
    st.write("### 🔍 Feature Importance Visualization")

    # ✅ Dynamic image uploader instead of static path
    uploaded_analytics_img = st.file_uploader(
        "📊 Upload Feature Importance Image (optional)",
        type=["png", "jpg", "jpeg"],
        help="Upload an image showing model insights or feature importance."
    )

    if uploaded_analytics_img is not None:
        st.image(uploaded_analytics_img, caption="Feature Impact Overview", use_container_width=True)
    else:
        st.info("Upload a feature importance image to display here.")

    st.write("""
    - **Age** and **Recommendation_Score** have the highest impact.
    - **Skills** and **Interests** are key factors through encoded patterns.
    """)

# ================================
# 📘 TAB 3 — INFO
# ================================
with tab3:
    st.header("About This Project")
    st.markdown("""
    This system uses a **Machine Learning model** trained on academic and personal data to recommend the best career options.

    **Features:**
    - 🌟 Predicts career based on 5 features: Age, Education, Skills, Interests, Recommendation Score.
    - 🎨 Cinematic background UI with interactive inputs.
    - 📈 Model analytics section with metrics & dynamic feature image upload.

    **Tech Stack:**  
    - Python, Streamlit, LightGBM, Pandas, Joblib.
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    pass
