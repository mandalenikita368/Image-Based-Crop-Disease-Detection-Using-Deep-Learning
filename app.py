import streamlit as st
from PIL import Image
import numpy as np
import json
from datetime import datetime
from model import PlantDiseaseModel
from disease_info import get_disease_info, parse_disease_name
from database import SessionLocal, init_db
from auth import create_user, authenticate_user, get_user_by_id
from detection_utils import save_detection, get_user_detections, get_user_stats

st.set_page_config(
    page_title="AI Plant Disease Detector",
    page_icon="🌱",
    layout="wide"
)

init_db()

@st.cache_resource
def load_model():
    """Load and cache the model"""
    plant_model = PlantDiseaseModel()
    plant_model.initialize_model()
    return plant_model

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'page' not in st.session_state:
        st.session_state['page'] = 'detect'

def login_page():
    """Login page UI"""
    st.title("🌱 AI Plant Disease Detector")
    st.markdown("### Login to Your Account")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    db = SessionLocal()
                    try:
                        user, error = authenticate_user(db, username, password)
                        if user:
                            st.session_state['logged_in'] = True
                            st.session_state['user_id'] = user.id
                            st.session_state['username'] = user.username
                            st.session_state['full_name'] = user.full_name
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(error)
                    finally:
                        db.close()
                else:
                    st.error("Please enter both username and password")
        
        st.markdown("---")
        st.markdown("Don't have an account?")
        if st.button("Register Here", use_container_width=True):
            st.session_state['show_register'] = True
            st.rerun()

def register_page():
    """Registration page UI"""
    st.title("🌱 AI Plant Disease Detector")
    st.markdown("### Create New Account")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            full_name = st.text_input("Full Name")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            password_confirm = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register", use_container_width=True)
            
            if submit:
                if not all([username, email, password, password_confirm]):
                    st.error("Please fill in all fields")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    db = SessionLocal()
                    try:
                        user, error = create_user(db, username, email, password, full_name)
                        if user:
                            st.success("Registration successful! Please login.")
                            st.session_state['show_register'] = False
                            st.rerun()
                        else:
                            st.error(error)
                    finally:
                        db.close()
        
        st.markdown("---")
        if st.button("Back to Login", use_container_width=True):
            st.session_state['show_register'] = False
            st.rerun()

def detection_page():
    """Main detection page"""
    st.title("🌱 AI Plant Disease Detector")
    
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.markdown(f"**Welcome, {st.session_state.get('username', 'User')}!**")
    with col_logout:
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    st.markdown("""
    ### Upload images of your crops to detect diseases
    **Supported Crops:** Tomato, Corn (Maize), Potato
    """)
    
    with st.container():
        st.info("ℹ️ **Demo Mode:** This model uses synthetic training data for demonstration. For production use, train with the actual PlantVillage dataset (~54K images). See README.md for instructions.")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📤 Single Image Analysis", "📦 Batch Processing"])
    
    with tab1:
        single_image_detection()
    
    with tab2:
        batch_image_detection()

def single_image_detection():
    """Single image detection UI"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image of your crop leaf",
            type=['jpg', 'jpeg', 'png'],
            key="single_upload",
            help="Upload a clear image of the crop leaf for accurate disease detection"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            notes = st.text_area("Add notes (optional)", key="single_notes", help="Add any observations or context")
            
            if st.button("🔍 Analyze Image", type="primary", use_container_width=True, key="single_analyze"):
                with st.spinner("Analyzing image... This may take a moment on first run."):
                    try:
                        model = load_model()
                        result = model.predict(image)
                        
                        db = SessionLocal()
                        try:
                            save_detection(
                                db=db,
                                user_id=st.session_state['user_id'],
                                image_name=uploaded_file.name,
                                predicted_class=result['predicted_class'],
                                confidence=result['confidence'],
                                top_3_predictions=result['top_3_predictions'],
                                notes=notes if notes else None
                            )
                        finally:
                            db.close()
                        
                        st.session_state['prediction_result'] = result
                        st.session_state['analyzed'] = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error analyzing image: {str(e)}")
                        st.error("Please try uploading a different image.")
        else:
            st.info("👆 Please upload an image to get started")
            st.markdown("""
            **Tips for best results:**
            - Use clear, well-lit images
            - Focus on the affected leaf area
            - Ensure the leaf fills most of the frame
            - Avoid blurry or dark images
            """)
    
    with col2:
        st.subheader("📊 Analysis Results")
        
        if 'analyzed' in st.session_state and st.session_state['analyzed']:
            result = st.session_state['prediction_result']
            predicted_class = result['predicted_class']
            confidence = result['confidence']
            
            crop, disease = parse_disease_name(predicted_class)
            
            st.success(f"**Analysis Complete!**")
            
            if confidence < 0.3:
                st.warning("⚠️ Low confidence detection. The image may not be clear or the disease may not be in our database. Please consult an expert.")
            
            st.metric(
                label="Detected Condition",
                value=disease,
                delta=f"{confidence*100:.1f}% confidence"
            )
            
            st.metric(label="Crop Type", value=crop)
            
            st.markdown("#### Top 3 Predictions:")
            for i, pred in enumerate(result['top_3_predictions'], 1):
                pred_crop, pred_disease = parse_disease_name(pred['class'])
                confidence_pct = pred['confidence'] * 100
                st.progress(pred['confidence'], text=f"{i}. {pred_disease} - {confidence_pct:.1f}%")
            
        else:
            st.info("Upload an image and click 'Analyze Image' to see results")
    
    if 'analyzed' in st.session_state and st.session_state['analyzed']:
        display_disease_information(st.session_state['prediction_result']['predicted_class'])

def batch_image_detection():
    """Batch image detection UI"""
    st.subheader("📦 Upload Multiple Images")
    st.markdown("Upload multiple crop images for batch analysis")
    
    uploaded_files = st.file_uploader(
        "Choose multiple images",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        key="batch_upload"
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} images uploaded")
        
        if st.button("🔍 Analyze All Images", type="primary", use_container_width=True, key="batch_analyze"):
            model = load_model()
            db = SessionLocal()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            try:
                for idx, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"Processing {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")
                    
                    try:
                        image = Image.open(uploaded_file)
                        result = model.predict(image)
                        
                        save_detection(
                            db=db,
                            user_id=st.session_state['user_id'],
                            image_name=uploaded_file.name,
                            predicted_class=result['predicted_class'],
                            confidence=result['confidence'],
                            top_3_predictions=result['top_3_predictions']
                        )
                        
                        results.append({
                            'filename': uploaded_file.name,
                            'result': result,
                            'success': True
                        })
                    except Exception as e:
                        results.append({
                            'filename': uploaded_file.name,
                            'error': str(e),
                            'success': False
                        })
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                status_text.text("✅ Batch processing complete!")
                
                st.markdown("### Batch Results")
                
                for idx, res in enumerate(results, 1):
                    with st.expander(f"{idx}. {res['filename']}", expanded=False):
                        if res['success']:
                            result = res['result']
                            crop, disease = parse_disease_name(result['predicted_class'])
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Crop", crop)
                            with col2:
                                st.metric("Disease", disease)
                            with col3:
                                st.metric("Confidence", f"{result['confidence']*100:.1f}%")
                            
                            st.markdown("**Top 3 Predictions:**")
                            for i, pred in enumerate(result['top_3_predictions'], 1):
                                _, pred_disease = parse_disease_name(pred['class'])
                                st.write(f"{i}. {pred_disease} ({pred['confidence']*100:.1f}%)")
                        else:
                            st.error(f"Error: {res['error']}")
                
            finally:
                db.close()

def display_disease_information(predicted_class):
    """Display detailed disease information"""
    st.markdown("---")
    
    disease_info = get_disease_info(predicted_class)
    
    st.subheader(f"📋 Disease Information: {disease_info['name']}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔬 Overview", "🩺 Symptoms", "💊 Treatment", "🛡️ Prevention"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Crop:**")
            st.write(disease_info['crop'])
            
        with col_b:
            st.markdown("**Pathogen:**")
            st.write(disease_info['pathogen'])
    
    with tab2:
        st.markdown("**Common Symptoms:**")
        for symptom in disease_info['symptoms']:
            st.markdown(f"- {symptom}")
    
    with tab3:
        st.markdown("**Recommended Treatment:**")
        for treatment in disease_info['treatment']:
            st.markdown(f"- {treatment}")
        
        if 'healthy' not in predicted_class.lower():
            st.warning("⚠️ **Important:** Always consult with a local agricultural expert for severe infections or if you're unsure about treatment options.")
    
    with tab4:
        st.markdown("**Prevention Measures:**")
        for prevention in disease_info['prevention']:
            st.markdown(f"- {prevention}")
        
        st.info("💡 **Tip:** Prevention is always better than cure. Regular monitoring and good agricultural practices can prevent most diseases.")

def dashboard_page():
    """User dashboard showing detection history and statistics"""
    st.title("📊 My Dashboard")
    
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.markdown(f"**Welcome, {st.session_state.get('username', 'User')}!**")
    with col_logout:
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    db = SessionLocal()
    try:
        stats = get_user_stats(db, st.session_state['user_id'])
        detections = get_user_detections(db, st.session_state['user_id'], limit=50)
        
        st.markdown("### 📈 Your Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Scans", stats['total_scans'])
        with col2:
            st.metric("Healthy Plants", stats['healthy_count'])
        with col3:
            st.metric("Diseased Plants", stats['diseased_count'])
        with col4:
            health_rate = (stats['healthy_count'] / stats['total_scans'] * 100) if stats['total_scans'] > 0 else 0
            st.metric("Health Rate", f"{health_rate:.1f}%")
        
        st.markdown("---")
        
        if stats['crops_analyzed']:
            st.markdown("### 🌾 Crops Analyzed")
            col1, col2 = st.columns(2)
            
            with col1:
                for crop, count in stats['crops_analyzed'].items():
                    st.metric(crop, count)
        
        if stats['diseases_detected']:
            st.markdown("### 🦠 Diseases Detected")
            for disease, count in sorted(stats['diseases_detected'].items(), key=lambda x: x[1], reverse=True)[:5]:
                st.write(f"- **{disease}**: {count} occurrence(s)")
        
        st.markdown("---")
        st.markdown("### 📜 Detection History")
        
        if detections:
            for detection in detections:
                with st.expander(f"🔍 {detection.disease_name} - {detection.detection_date.strftime('%Y-%m-%d %H:%M')}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Crop:** {detection.crop_type}")
                        st.write(f"**Confidence:** {detection.confidence*100:.1f}%")
                    
                    with col2:
                        st.write(f"**Image:** {detection.image_name}")
                        st.write(f"**Date:** {detection.detection_date.strftime('%Y-%m-%d %H:%M')}")
                    
                    with col3:
                        if detection.notes:
                            st.write(f"**Notes:** {detection.notes}")
                    
                    if detection.top_3_predictions:
                        st.markdown("**Top 3 Predictions:**")
                        try:
                            top_3 = json.loads(detection.top_3_predictions)
                            for i, pred in enumerate(top_3, 1):
                                _, disease = parse_disease_name(pred['class'])
                                st.write(f"{i}. {disease} ({pred['confidence']*100:.1f}%)")
                        except:
                            pass
        else:
            st.info("No detection history yet. Start analyzing images to build your history!")
    
    finally:
        db.close()

def main():
    """Main application logic"""
    init_session_state()
    
    if not st.session_state['logged_in']:
        if 'show_register' in st.session_state and st.session_state['show_register']:
            register_page()
        else:
            login_page()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["🔍 Detect Disease", "📊 Dashboard"], label_visibility="collapsed")
        
        st.sidebar.markdown("---")
        
        with st.sidebar.expander("ℹ️ About This App"):
            st.markdown("""
            **AI Plant Disease Detector** uses deep learning to identify diseases in crop leaves.
            
            **Features:**
            - Single & batch image analysis
            - Detection history tracking
            - Crop health statistics
            - Detailed disease information
            
            **Supported Crops:**
            - 🍅 Tomato (10 classes)
            - 🌽 Corn/Maize (4 classes)
            - 🥔 Potato (3 classes)
            """)
        
        if page == "🔍 Detect Disease":
            detection_page()
        else:
            dashboard_page()

if __name__ == "__main__":
    main()
