import streamlit as st
from PIL import Image
import numpy as np
from model import PlantDiseaseModel
from disease_info import get_disease_info, parse_disease_name

st.set_page_config(
    page_title="AI Plant Disease Detector",
    page_icon="🌱",
    layout="wide"
)

@st.cache_resource
def load_model():
    """Load and cache the model"""
    plant_model = PlantDiseaseModel()
    plant_model.initialize_weights()
    return plant_model

def main():
    st.title("🌱 AI Plant Disease Detector")
    st.markdown("""
    ### Upload an image of your crop to detect diseases
    **Supported Crops:** Tomato, Corn (Maize), Potato
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image of your crop leaf",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of the crop leaf for accurate disease detection"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
                with st.spinner("Analyzing image..."):
                    model = load_model()
                    
                    result = model.predict(image)
                    
                    st.session_state['prediction_result'] = result
                    st.session_state['analyzed'] = True
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
        st.markdown("---")
        
        result = st.session_state['prediction_result']
        predicted_class = result['predicted_class']
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
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>AI Plant Disease Detector</strong> | Powered by Deep Learning CNN Model</p>
        <p>Trained on PlantVillage Dataset | Supporting Tomato, Corn, and Potato Crops</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
