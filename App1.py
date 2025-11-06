# import streamlit as st
# import numpy as np
# import pandas as pd
# import joblib
# import base64
# import time
# from datetime import datetime

# # ================================
# # 📄 Page config
# # ================================
# st.set_page_config(page_title="AI Career Recommender", layout="centered")

# # ================================
# # 🎯 CONFIGURATION
# # ================================
# MODEL_PATH = "Carrier_Recommendation_System.pkl"  # ensure this file is next to App.py
# FEATURE_NAMES = ["Age", "Education", "Skills", "Interests", "Recommendation_Score"]

# # ================================
# # ⚙️ UTILITIES
# # ================================
# def get_base64_image_url(uploaded_file):
#     """Converts uploaded file to base64 URL for CSS background."""
#     try:
#         bytes_data = uploaded_file.getvalue()
#         base64_encoded_data = base64.b64encode(bytes_data).decode("utf-8")
#         mime_type = uploaded_file.type or "image/png"
#         return f"data:{mime_type};base64,{base64_encoded_data}"
#     except Exception as e:
#         st.error(f"Error processing image: {e}")
#         return None


# def set_cinematic_bg(base64_urls, interval_per_image=6):
#     """Apply cinematic slideshow background using base64 URLs."""
#     num_images = len(base64_urls)
#     total_duration = max(1, num_images) * interval_per_image
#     OVERLAY_OPACITY = "rgba(0,0,0,0.6)"

#     if num_images == 0:
#         st.markdown("""
#             <style>
#             .stApp {
#                 background: linear-gradient(135deg, #1b2735, #090a0f);
#                 color: white;
#             }
#             </style>
#         """, unsafe_allow_html=True)
#         return

#     css_keyframes = []
#     for i in range(num_images):
#         start_percent = (i * 100) / num_images
#         hold_percent = start_percent + (100 / num_images)
#         css_keyframes.append(f"{start_percent:.2f}% {{ background-image: url('{base64_urls[i]}'); }}")
#         css_keyframes.append(f"{hold_percent:.2f}% {{ background-image: url('{base64_urls[i]}'); }}")
#     css_keyframes.append(f"100% {{ background-image: url('{base64_urls[0]}'); }}")

#     st.markdown(f"""
#         <style>
#         .stApp {{
#             background-size: cover;
#             background-attachment: fixed;
#             background-repeat: no-repeat;
#             background-image: url('{base64_urls[0]}');
#             animation: cinematicBg {total_duration}s infinite;
#             color: white;
#         }}
#         @keyframes cinematicBg {{
#             {"".join(css_keyframes)}
#         }}
#         .stApp::before {{
#             content: "";
#             position: fixed;
#             top: 0; left: 0;
#             width: 100%; height: 100%;
#             background: {OVERLAY_OPACITY};
#             z-index: 0;
#         }}
#         [data-testid="stSidebar"] > div:first-child {{
#             background: rgba(255, 255, 255, 0.05);
#             backdrop-filter: blur(8px);
#             border-radius: 16px;
#             padding: 20px;
#             z-index: 10;
#         }}
#         * {{ font-family: 'Poppins', sans-serif; }}
#         </style>
#     """, unsafe_allow_html=True)

# # ================================
# # 🧠 LOAD MODEL
# # ================================
# try:
#     model = joblib.load(MODEL_PATH)
#     st.info("✅ Model loaded successfully!")
# except Exception as e:
#     st.error(f"❌ Failed to load model: {e}")
#     model = None

# # ================================
# # 🧾 LOAD LABEL ENCODER FOR TARGET
# # ================================
# try:
#     label_encoders = joblib.load("label_encoders.pkl")
#     le_career = label_encoders["Recommended_Career"]
#     label_classes = list(le_career.classes_)
#     st.success(f"✅ Loaded {len(label_classes)} career categories from encoder.")
# except Exception as e:
#     st.error(f"⚠️ Failed to load label encoder: {e}")
#     label_classes = [f"Career #{i}" for i in range(32)]


# # ================================
# # 🧾 LOAD LABEL ENCODER OR CREATE MAPPING
# # ================================
# try:
#     # Try to load LabelEncoder used in training (if you saved it)
#     le = joblib.load("label_encoder.pkl")
#     st.success("✅ Label Encoder loaded successfully.")
#     label_classes = list(le.classes_)
# except Exception:
#     # Otherwise, rebuild mapping directly from dataset
#     dataset = pd.read_csv("AI-based Career Recommendation System (1).csv")
#     label_classes = dataset.sort_values("Recommended_Career")["Recommended_Career"].unique().tolist()
#     st.warning("⚠️ Using dataset to rebuild label mapping (not exact order).")

# def get_career_name(pred_value):
#     """Convert model's numeric output to real career name."""
#     if 0 <= int(pred_value) < len(label_classes):
#         return label_classes[int(pred_value)]
#     return f"Career #{int(pred_value)}"

# # ================================
# # 🧾 LOAD DATASET FOR CAREER NAMES
# # ================================
# try:
#     dataset = pd.read_csv("AI-based Career Recommendation System (1).csv")
#     # Create mapping dynamically
#     unique_careers = dataset[['Recommended_Career']].drop_duplicates().reset_index(drop=True)
#     career_map = {i: name for i, name in enumerate(unique_careers['Recommended_Career'])}
#     st.success(f"✅ Loaded {len(career_map)} career categories from dataset.")
# except Exception as e:
#     st.error(f"⚠️ Failed to load dataset for career names: {e}")
#     career_map = {i: f"Career #{i}" for i in range(32)}  # fallback

# # ================================
# # 📂 SIDEBAR
# # ================================
# base64_image_urls = []
# with st.sidebar:
#     st.title("⚙️ App Configuration")
#     uploaded_files = st.file_uploader(
#         "🖼️ Upload background images (slideshow):",
#         type=["jpg", "jpeg", "png"],
#         accept_multiple_files=True,
#         help="Upload 3+ background images for cinematic transitions.",
#     )
#     if uploaded_files:
#         with st.spinner("Processing images..."):
#             for file in uploaded_files:
#                 url = get_base64_image_url(file)
#                 if url:
#                     base64_image_urls.append(url)
#             time.sleep(0.5)
#         st.success("✅ Background images ready!")

#     st.markdown("---")
#     st.subheader("📘 About the Model")
#     st.info("This ML model predicts the most suitable career path based on your profile and interests.")
#     st.markdown(f"📅 Last Updated: **{datetime.now().strftime('%b %d, %Y')}**")
#     st.markdown("👨‍💻 Developed by **Umar Imam**", unsafe_allow_html=True)

# set_cinematic_bg(base64_image_urls)

# # ================================
# # 🎓 HEADER
# # ================================
# st.markdown("""
# <h1 style='text-align:center; color:#ff9900; text-shadow: 2px 2px 6px #000;'>🎓 AI-Based Career Recommendation System</h1>
# <p style='text-align:center; font-size:18px; color:#fff;'>Find the ideal career path based on your academic background, skills, and interests.</p>
# """, unsafe_allow_html=True)

# # ================================
# # 📊 TABS
# # ================================
# tab1, tab2, tab3 = st.tabs(["💡 Career Prediction", "📈 Model Analytics", "📘 Info"])

# # ================================
# # 💡 TAB 1 — CAREER PREDICTION
# # ================================
# with tab1:
#     st.header("Enter Your Details")
#     col1, col2 = st.columns(2)

#     with col1:
#         age = st.number_input("🎂 Age", min_value=15, max_value=60, step=1, value=None, placeholder="Enter your age")
#         education = st.selectbox(
#             "🎓 Education Level",
#             ["Select Education Level", "High School", "Bachelor's", "Master's", "PhD"],
#             index=0
#         )
#         skills = st.text_input("🧠 Skills (e.g., Python, Data Analysis, Java)", value="")

#     with col2:
#         interests = st.text_input("💡 Interests (e.g., AI, Web Dev, Finance)", value="")
#         rec_score = st.number_input(
#             "📊 Recommendation Score",
#             min_value=0.0, max_value=100.0, step=0.5,
#             value=None, placeholder="Enter recommendation score"
#         )

# if st.button("🚀 Predict Career", use_container_width=True):
#     if education == "Select Education Level" or not age or not skills or not interests or rec_score is None:
#         st.warning("⚠️ Please fill out all fields before predicting.")
#     elif model is None:
#         st.error("⚠️ Model not loaded. Please check the file path.")
#     else:
#         try:
#             # ============================
#             # 🎓 Use the same encoders as training
#             # ============================
#             edu_encoder = label_encoders["Education"]
#             skill_encoder = label_encoders["Skills"]
#             interest_encoder = label_encoders["Interests"]

#             # Encode user input using the same label encoders
#             try:
#                 edu_val = edu_encoder.transform([education])[0]
#             except:
#                 edu_val = 0

#             try:
#                 skill_val = skill_encoder.transform([skills])[0]
#             except:
#                 skill_val = 0

#             try:
#                 interest_val = interest_encoder.transform([interests])[0]
#             except:
#                 interest_val = 0

#             # ============================
#             # 🧠 Make prediction
#             # ============================
#             input_data = np.array([[age, edu_val, skill_val, interest_val, rec_score]])
#             pred = model.predict(input_data)[0]

#             # Decode numeric prediction into career name
#             if 0 <= int(pred) < len(label_classes):
#                 career_name = label_classes[int(pred)]
#             else:
#                 career_name = f"Career #{int(pred)}"

#             # ============================
#             # 🎯 Display result (only once)
#             # ============================
#             st.success(f"🎯 Predicted Career: {career_name}")
#             st.markdown(f"""
#             <div style="background-color:rgba(255,153,0,0.2); padding:20px; border-radius:15px; text-align:center;">
#                 <h3 style="color:white;">Your Recommended Career Path:</h3>
#                 <h2 style="color:#ff9900;">{career_name}</h2>
#                 <p>Explore opportunities aligned with your skills and interests.</p>
#             </div>
#             """, unsafe_allow_html=True)

#         except Exception as e:
#             st.error(f"Prediction failed: {e}")




# # Encode inputs using same LabelEncoder used during training
# try:
#     edu_val = edu_encoder.transform([education])[0]
# except:
#     edu_val = 0  # fallback if unseen

# try:
#     skill_val = skill_encoder.transform([skills])[0]
# except:
#     skill_val = 0

# try:
#     interest_val = interest_encoder.transform([interests])[0]
# except:
#     interest_val = 0

#     input_data = np.array([[age, edu_val, skill_val, interest_val, rec_score]])
#     pred = model.predict(input_data)[0]
#     if 0 <= int(pred) < len(label_classes):
#         career_name = label_classes[int(pred)]
#     else:
#         career_name = f"Career #{int(pred)}"
#                 # career_map = {
#                 #     0: "Software Engineer", 1: "Data Scientist", 2: "Web Developer", 3: "AI Researcher",
#                 #     4: "Cloud Engineer", 5: "Business Analyst", 6: "Cybersecurity Expert", 7: "UI/UX Designer",
#                 #     8: "Database Administrator", 9: "Network Engineer", 10: "Game Developer", 11: "Machine Learning Engineer"
#                 # }
#         career_map = {
#                                     0: "Career #0", 1: "Career #1", 2: "Career #2", 3: "Career #3",
#                                      4: "Career #4", 5: "Career #5", 6: "Career #6", 7: "Career #7",
#                                     8: "Career #8", 9: "Career #9", 10: "Career #10", 11: "Career #11",
#                                     12: "Career #12", 13: "Career #13", 14: "Career #14", 15: "Career #15",
#                                     16: "Career #16", 17: "Career #17", 18: "Career #18", 19: "Career #19",
#                                     20: "Career #20", 21: "Career #21", 22: "Career #22", 23: "Career #23",
#                                     24: "Career #24", 25: "Career #25", 26: "Career #26", 27: "Career #27",
#                                     28: "Career #28", 29: "Career #29", 30: "Career #30", 31: "Career #31"
#                     }
# try:
#     # Your prediction logic before this
#     pred = model.predict(input_data)[0]

#     if 0 <= int(pred) < len(label_classes):
#         career_name = label_classes[int(pred)]
#     else:
#         career_name = f"Career #{int(pred)}"

#     # Display the result nicely
#     st.success(f"🎯 Predicted Career: {career_name}")

# except Exception as e:
#     st.error(f"Prediction failed: {e}")


# # ================================
# # 📈 TAB 2 — MODEL ANALYTICS
# # ================================
# with tab2:
#     st.header("Model Insights and Performance")
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Training Accuracy", "94%")
#     col2.metric("Testing Accuracy", "91%")
#     col3.metric("Model Type", "LightGBM Classifier")

#     st.markdown("---")
#     st.write("### 🔍 Feature Importance Visualization")

#     uploaded_analytics_img = st.file_uploader(
#         "📊 Upload Feature Importance Image (optional)",
#         type=["png", "jpg", "jpeg"],
#         help="Upload an image showing model insights or feature importance."
#     )

#     if uploaded_analytics_img is not None:
#         st.image(uploaded_analytics_img, caption="Feature Impact Overview", use_container_width=True)
#     else:
#         st.info("Upload a feature importance image to display here.")

# # # ================================
# # # 📘 TAB 3 — INFO
# # # ================================
# # with tab3:
# #     st.header("About This Project")
# #     st.markdown("""
# #     This system uses a **Machine Learning model** trained on academic and personal data to recommend the best career options.

# #     **Features:**
# #     - 🌟 Predicts career based on 5 features: Age, Education, Skills, Interests, Recommendation Score.
# #     - 🎨 Cinematic background UI with interactive inputs.
# #     - 📈 Model analytics section with metrics & dynamic feature image upload.

# #     **Tech Stack:**  
# #     - Python, Streamlit, LightGBM, Pandas, Joblib.
# #     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     pass

# ================================this is my code ================
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
MODEL_PATH = "Carrier_Recommendation_System.pkl"
FEATURE_NAMES = ["Age", "Education", "Skills", "Interests", "Recommendation_Score"]

# ================================
# ⚙️ UTILITIES
# ================================
def get_base64_image_url(uploaded_file):
    try:
        bytes_data = uploaded_file.getvalue()
        base64_encoded_data = base64.b64encode(bytes_data).decode("utf-8")
        mime_type = uploaded_file.type or "image/png"
        return f"data:{mime_type};base64,{base64_encoded_data}"
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def set_cinematic_bg(base64_urls, interval_per_image=6):
    num_images = len(base64_urls)
    total_duration = num_images * interval_per_image
    OVERLAY_OPACITY = "rgba(0,0,0,0.6)"
    if num_images == 0:
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
        [data-testid="stSidebar"] > div:first-child {{
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
# 🧠 LOAD MODEL & ENCODERS
# ================================
try:
    model = joblib.load(MODEL_PATH)
    label_encoders = joblib.load("label_encoders.pkl")
    le_career = label_encoders["Recommended_Career"]
    label_classes = list(le_career.classes_)
    st.info("✅ Model and encoders loaded successfully!")
except Exception as e:
    st.error(f"⚠️ Error loading model/encoders: {e}")
    model, label_encoders, label_classes = None, None, []

# ================================
# 📂 SIDEBAR
# ================================
base64_image_urls = []
with st.sidebar:
    st.title("⚙️ App Configuration")
    uploaded_files = st.file_uploader(
        "🖼️ Upload background images:",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        for file in uploaded_files:
            url = get_base64_image_url(file)
            if url:
                base64_image_urls.append(url)
        st.success("✅ Background ready!")

    st.markdown("---")
    st.subheader("📘 About the Model")
    st.info("This ML model predicts your ideal career based on education, skills, and interests.")
    st.markdown(f"📅 Updated: **{datetime.now().strftime('%b %d, %Y')}**")
    st.markdown("Made with ❤️ ", unsafe_allow_html=True) 
    st.markdown("✨ Developed by **Umar Imam**", unsafe_allow_html=True)

set_cinematic_bg(base64_image_urls)

# ================================
# 🎓 HEADER
# ================================
st.markdown("""
<h1 style='text-align:center; color:#ff9900; text-shadow: 2px 2px 6px #000;'>🎓 AI-Based Career Recommendation System</h1>
<p style='text-align:center; font-size:18px; color:#fff;'>Find the perfect career path that fits your profile.</p>
""", unsafe_allow_html=True)

# ================================
# 📊 TABS
# ================================
tab1, tab2 = st.tabs(["💡 Career Prediction", "ℹ️ Model Info"])

# ================================
# 💡 TAB 1 — CAREER PREDICTION
# ================================
with tab1:
    st.header("Enter Your Details")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("🎂 Age", min_value=15, max_value=60, step=1)
        education = st.selectbox(
            "🎓 Education Level",
            ["Select Education Level", "High School", "Bachelor's", "Master's", "PhD"],
            index=0 )
        skills = st.text_input("🧠 Skills (e.g., Python, Java, Data Analysis)")

    with col2:
        interests = st.text_input("💡 Interests (e.g., AI, Web Dev, Finance)")
        rec_score = st.number_input("📊 Recommendation Score", min_value=0.0, max_value=100.0, step=0.5)

    if st.button("🚀 Predict Career", use_container_width=True):
        if not all([education, skills, interests, rec_score]):
            st.warning("⚠️ Please fill all the details.")
        elif model is None:
            st.error("⚠️ Model not loaded.")
        else:
            try:
                edu_encoder = label_encoders["Education"]
                skill_encoder = label_encoders["Skills"]
                interest_encoder = label_encoders["Interests"]

                edu_val = edu_encoder.transform([education])[0] if education in edu_encoder.classes_ else 0
                skill_val = skill_encoder.transform([skills])[0] if skills in skill_encoder.classes_ else 0
                interest_val = interest_encoder.transform([interests])[0] if interests in interest_encoder.classes_ else 0

                input_data = np.array([[age, edu_val, skill_val, interest_val, rec_score]])
                pred = model.predict(input_data)[0]
                career_name = label_classes[int(pred)] if 0 <= int(pred) < len(label_classes) else f"Career #{pred}"

                st.balloons()
                st.markdown(f"""
                    <div style="background-color:rgba(255,153,0,0.2);
                                padding:25px; border-radius:15px;
                                text-align:center; box-shadow:0 0 20px #ff9900;">
                        <h2 style="color:white;">Predicted Career</h2>
                        <h1 style="color:#ff9900; font-size:3.2em;">{career_name}</h1>
                    </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction failed: {e}")

# ================================
# 📘 TAB 2 — MODEL INFO
# ================================
with tab2:
    st.header("Model Overview")
    st.info("This AI model uses **LightGBM Classifier** trained on a dataset of academic, skill, and interest features to predict the best career path.")
    col1, col2 = st.columns(2)
    col1.metric("Training Accuracy", "94%")
    col2.metric("Testing Accuracy", "91%")
    st.markdown("""
    **Features Used:**
    - Age  
    - Education  
    - Skills  
    - Interests  
    - Recommendation Score  
    """)

if __name__ == "__main__":
    pass
