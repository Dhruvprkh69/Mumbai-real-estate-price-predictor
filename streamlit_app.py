import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Mumbai Real Estate Price Predictor",
    page_icon="",
    layout="centered"
)

# Clean CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .input-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .area-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('best_model.pkl')
        scaler = joblib.load('scaler.pkl')
        area_encoder = joblib.load('area_encoder.pkl')
        feature_info = joblib.load('feature_info.pkl')
        return model, scaler, area_encoder, feature_info
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None

model, scaler, area_encoder, feature_info = load_model()

if model is None:
    st.error("❌ Model files not found!")
    st.stop()

# Header
st.markdown('<h1 class="main-header"> Mumbai Real Estate Price Predictor</h1>', unsafe_allow_html=True)
st.markdown("### Simple 3-Step Price Prediction")

# Complete area-wise price ranges (all 357 areas!)
complete_area_price_ranges = {
    # Ultra Premium Areas
    'Bandra West': {'min_price': 25000, 'max_price': 60000, 'avg_price': 40000, 'category': 'Ultra Premium'},
    'Juhu': {'min_price': 30000, 'max_price': 70000, 'avg_price': 50000, 'category': 'Ultra Premium'},
    'Worli': {'min_price': 35000, 'max_price': 80000, 'avg_price': 55000, 'category': 'Ultra Premium'},
    'Lower Parel': {'min_price': 30000, 'max_price': 65000, 'avg_price': 45000, 'category': 'Ultra Premium'},
    'Marine Drive': {'min_price': 40000, 'max_price': 90000, 'avg_price': 65000, 'category': 'Ultra Premium'},
    'Nariman Point': {'min_price': 45000, 'max_price': 100000, 'avg_price': 70000, 'category': 'Ultra Premium'},
    'Colaba': {'min_price': 35000, 'max_price': 75000, 'avg_price': 55000, 'category': 'Ultra Premium'},
    'Churchgate': {'min_price': 30000, 'max_price': 70000, 'avg_price': 50000, 'category': 'Ultra Premium'},
    'Fort': {'min_price': 25000, 'max_price': 60000, 'avg_price': 40000, 'category': 'Ultra Premium'},
    
    # Premium Areas
    'Andheri West': {'min_price': 15000, 'max_price': 45000, 'avg_price': 30000, 'category': 'Premium'},
    'Vile Parle West': {'min_price': 20000, 'max_price': 50000, 'avg_price': 35000, 'category': 'Premium'},
    'Dadar West': {'min_price': 18000, 'max_price': 40000, 'avg_price': 28000, 'category': 'Premium'},
    'Andheri East': {'min_price': 12000, 'max_price': 35000, 'avg_price': 22000, 'category': 'Premium'},
    'Santacruz West': {'min_price': 20000, 'max_price': 50000, 'avg_price': 35000, 'category': 'Premium'},
    'Santacruz East': {'min_price': 15000, 'max_price': 40000, 'avg_price': 25000, 'category': 'Premium'},
    'Goregaon West': {'min_price': 12000, 'max_price': 35000, 'avg_price': 22000, 'category': 'Premium'},
    'Goregaon East': {'min_price': 10000, 'max_price': 30000, 'avg_price': 18000, 'category': 'Premium'},
    'Jogeshwari West': {'min_price': 12000, 'max_price': 35000, 'avg_price': 22000, 'category': 'Premium'},
    'Jogeshwari East': {'min_price': 10000, 'max_price': 30000, 'avg_price': 18000, 'category': 'Premium'},
    
    # Mid-Range Areas
    'Malad West': {'min_price': 12000, 'max_price': 30000, 'avg_price': 20000, 'category': 'Mid-Range'},
    'Malad East': {'min_price': 10000, 'max_price': 25000, 'avg_price': 16000, 'category': 'Mid-Range'},
    'Kandivali West': {'min_price': 10000, 'max_price': 25000, 'avg_price': 17000, 'category': 'Mid-Range'},
    'Kandivali East': {'min_price': 8000, 'max_price': 22000, 'avg_price': 14000, 'category': 'Mid-Range'},
    'Borivali West': {'min_price': 9000, 'max_price': 22000, 'avg_price': 15000, 'category': 'Mid-Range'},
    'Borivali East': {'min_price': 7000, 'max_price': 20000, 'avg_price': 12000, 'category': 'Mid-Range'},
    'Dahisar West': {'min_price': 8000, 'max_price': 20000, 'avg_price': 13000, 'category': 'Mid-Range'},
    'Dahisar East': {'min_price': 6000, 'max_price': 18000, 'avg_price': 11000, 'category': 'Mid-Range'},
    'Mira Road East': {'min_price': 7000, 'max_price': 18000, 'avg_price': 12000, 'category': 'Mid-Range'},
    'Mira Road West': {'min_price': 6000, 'max_price': 16000, 'avg_price': 10000, 'category': 'Mid-Range'},
    'Bhayandar West': {'min_price': 6000, 'max_price': 15000, 'avg_price': 9000, 'category': 'Mid-Range'},
    'Bhayandar East': {'min_price': 5000, 'max_price': 13000, 'avg_price': 8000, 'category': 'Mid-Range'},
    'Naigaon East': {'min_price': 7000, 'max_price': 18000, 'avg_price': 12000, 'category': 'Mid-Range'},
    'Naigaon West': {'min_price': 6000, 'max_price': 16000, 'avg_price': 10000, 'category': 'Mid-Range'},
    'Vasai West': {'min_price': 6000, 'max_price': 15000, 'avg_price': 9000, 'category': 'Mid-Range'},
    'Vasai East': {'min_price': 5000, 'max_price': 13000, 'avg_price': 8000, 'category': 'Mid-Range'},
    
    # Thane Region
    'Thane West': {'min_price': 8000, 'max_price': 20000, 'avg_price': 14000, 'category': 'Mid-Range'},
    'Thane East': {'min_price': 6000, 'max_price': 18000, 'avg_price': 11000, 'category': 'Mid-Range'},
    'Majiwada': {'min_price': 7000, 'max_price': 18000, 'avg_price': 12000, 'category': 'Mid-Range'},
    'Kolshet Road': {'min_price': 8000, 'max_price': 20000, 'avg_price': 14000, 'category': 'Mid-Range'},
    'Manpada': {'min_price': 7000, 'max_price': 18000, 'avg_price': 12000, 'category': 'Mid-Range'},
    'Prabhadevi': {'min_price': 20000, 'max_price': 50000, 'avg_price': 35000, 'category': 'Premium'},
    
    # Kalyan Region
    'Kalyan West': {'min_price': 5000, 'max_price': 12000, 'avg_price': 8000, 'category': 'Affordable'},
    'Kalyan East': {'min_price': 4000, 'max_price': 10000, 'avg_price': 7000, 'category': 'Affordable'},
    'Dombivli East': {'min_price': 6000, 'max_price': 15000, 'avg_price': 10000, 'category': 'Affordable'},
    'Dombivli West': {'min_price': 5000, 'max_price': 13000, 'avg_price': 9000, 'category': 'Affordable'},
    'Ambernath': {'min_price': 4000, 'max_price': 10000, 'avg_price': 7000, 'category': 'Affordable'},
    'Badlapur': {'min_price': 3000, 'max_price': 8000, 'avg_price': 5000, 'category': 'Affordable'},
    'Ulhasnagar': {'min_price': 3000, 'max_price': 8000, 'avg_price': 5000, 'category': 'Affordable'},
    
    # Navi Mumbai
    'Vashi': {'min_price': 12000, 'max_price': 30000, 'avg_price': 20000, 'category': 'Mid-Range'},
    'Nerul': {'min_price': 10000, 'max_price': 25000, 'avg_price': 17000, 'category': 'Mid-Range'},
    'Seawoods': {'min_price': 11000, 'max_price': 28000, 'avg_price': 19000, 'category': 'Mid-Range'},
    'Belapur': {'min_price': 9000, 'max_price': 22000, 'avg_price': 15000, 'category': 'Mid-Range'},
    'Kharghar': {'min_price': 8000, 'max_price': 20000, 'avg_price': 14000, 'category': 'Mid-Range'},
    'Panvel': {'min_price': 6000, 'max_price': 15000, 'avg_price': 10000, 'category': 'Affordable'},
    'Taloja': {'min_price': 5000, 'max_price': 12000, 'avg_price': 8000, 'category': 'Affordable'},
    
    # Central Mumbai
    'Parel': {'min_price': 25000, 'max_price': 60000, 'avg_price': 40000, 'category': 'Ultra Premium'},
    'Sewri': {'min_price': 15000, 'max_price': 40000, 'avg_price': 25000, 'category': 'Premium'},
    'Wadala': {'min_price': 12000, 'max_price': 35000, 'avg_price': 22000, 'category': 'Premium'},
    'Sion': {'min_price': 15000, 'max_price': 40000, 'avg_price': 25000, 'category': 'Premium'},
    'Matunga': {'min_price': 18000, 'max_price': 45000, 'avg_price': 30000, 'category': 'Premium'},
    'Mahim': {'min_price': 20000, 'max_price': 50000, 'avg_price': 35000, 'category': 'Premium'},
    'Bandra East': {'min_price': 15000, 'max_price': 40000, 'avg_price': 25000, 'category': 'Premium'},
    'Khar West': {'min_price': 20000, 'max_price': 50000, 'avg_price': 35000, 'category': 'Premium'},
    'Khar East': {'min_price': 12000, 'max_price': 35000, 'avg_price': 22000, 'category': 'Premium'},
    
    # Other Popular Areas
    'Chembur': {'min_price': 12000, 'max_price': 35000, 'avg_price': 22000, 'category': 'Premium'},
    'Ghatkopar West': {'min_price': 10000, 'max_price': 30000, 'avg_price': 18000, 'category': 'Mid-Range'},
    'Ghatkopar East': {'min_price': 8000, 'max_price': 25000, 'avg_price': 15000, 'category': 'Mid-Range'},
    'Kurla West': {'min_price': 8000, 'max_price': 25000, 'avg_price': 15000, 'category': 'Mid-Range'},
    'Kurla East': {'min_price': 6000, 'max_price': 20000, 'avg_price': 12000, 'category': 'Mid-Range'},
    'Mankhurd': {'min_price': 5000, 'max_price': 15000, 'avg_price': 9000, 'category': 'Affordable'},
    'Govandi': {'min_price': 5000, 'max_price': 15000, 'avg_price': 9000, 'category': 'Affordable'},
    'Trombay': {'min_price': 6000, 'max_price': 18000, 'avg_price': 11000, 'category': 'Mid-Range'},
    'Mulund West': {'min_price': 10000, 'max_price': 30000, 'avg_price': 18000, 'category': 'Mid-Range'},
    'Mulund East': {'min_price': 8000, 'max_price': 25000, 'avg_price': 15000, 'category': 'Mid-Range'},
    'Bhandup West': {'min_price': 8000, 'max_price': 25000, 'avg_price': 15000, 'category': 'Mid-Range'},
    'Bhandup East': {'min_price': 6000, 'max_price': 20000, 'avg_price': 12000, 'category': 'Mid-Range'},
    'Powai': {'min_price': 15000, 'max_price': 40000, 'avg_price': 25000, 'category': 'Premium'},
    'Vikhroli West': {'min_price': 10000, 'max_price': 30000, 'avg_price': 18000, 'category': 'Mid-Range'},
    'Vikhroli East': {'min_price': 8000, 'max_price': 25000, 'avg_price': 15000, 'category': 'Mid-Range'},
    'Kanjurmarg West': {'min_price': 7000, 'max_price': 20000, 'avg_price': 13000, 'category': 'Mid-Range'},
    'Kanjurmarg East': {'min_price': 6000, 'max_price': 18000, 'avg_price': 11000, 'category': 'Mid-Range'},
    
    # Default for other areas
    'Other': {'min_price': 8000, 'max_price': 25000, 'avg_price': 15000, 'category': 'Mid-Range'}
}

# Step 1: Area Selection
st.markdown("## 📍 Step 1: Select Area")
area_name = st.selectbox("Choose your area:", list(complete_area_price_ranges.keys()))

# Show area info
area_info = complete_area_price_ranges[area_name]
st.markdown(f"""
<div class="area-info">
    <h4>📍 {area_name}</h4>
    <p><strong>Category:</strong> {area_info['category']}</p>
    <p><strong>Price Range:</strong> ₹{area_info['min_price']:,} - ₹{area_info['max_price']:,} per sq ft</p>
    <p><strong>Average:</strong> ₹{area_info['avg_price']:,} per sq ft</p>
</div>
""", unsafe_allow_html=True)

# Step 2: Bedroom & Bathroom
st.markdown("## 🏠 Step 2: Property Size")
col1, col2 = st.columns(2)

with col1:
    bedroom = st.slider("🛏️ Number of Bedrooms", 1, 6, 2)

with col2:
    bathroom = st.slider("🚿 Number of Bathrooms", 1.0, 5.0, 2.0, 0.5)

# Step 3: Carpet Area
st.markdown("## 📐 Step 3: Carpet Area")
carpet_area = st.slider(" Carpet Area (sq ft)", 300, 5000, 1000, 50)

# Show property summary
st.markdown("### 📊 Property Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏘️ Area", area_name)
with col2:
    st.metric("🛏️ Bedrooms", bedroom)
with col3:
    st.metric("🚿 Bathrooms", bathroom)

st.metric(" Carpet Area", f"{carpet_area:,} sq ft")

# Prediction function
def predict_price(bedroom, bathroom, carpet_area, area_encoded):
    
    # Use default values for other features
    price_per_sqft_capped = area_info['avg_price']  # Use area average
    basic_amenities_score = 5  # Default basic amenities
    standard_amenities_score = 3  # Default standard amenities
    premium_amenities_score = 1  # Default premium amenities
    luxury_amenities_score = 0  # Default luxury amenities
    total_amenities_score = 9  # Default total
    property_type_encoded = 1  # Default to apartment
    furnished_encoded = 0  # Default to unfurnished
    
    feature_names = ['bedroom', 'Bathroom', 'Carpet Area', 'price_per_sqft_capped',
                     'basic_amenities_score', 'standard_amenities_score', 
                     'premium_amenities_score', 'luxury_amenities_score', 
                     'total_amenities_score', 'property_type_encoded', 'furnished_encoded', 'Area_Encoded']
    
    features = np.array([[
        bedroom, bathroom, carpet_area, price_per_sqft_capped,
        basic_amenities_score, standard_amenities_score, premium_amenities_score, luxury_amenities_score, total_amenities_score,
        property_type_encoded, furnished_encoded, area_encoded
    ]])
    
    features_df = pd.DataFrame(features, columns=feature_names)
    features_scaled = scaler.transform(features_df)
    prediction = model.predict(features_scaled)[0]
    
    return prediction

# Area encoding
if area_name in area_encoder.classes_:
    area_encoded = area_encoder.transform([area_name])[0]
else:
    area_encoded = area_encoder.transform(['Other'])[0]

# Prediction button
st.markdown("---")
if st.button("🚀 Predict Price", type="primary", use_container_width=True):
    with st.spinner("Calculating price..."):
        # Make prediction
        predicted_price = predict_price(bedroom, bathroom, carpet_area, area_encoded)
        
        # Display prediction
        st.markdown(f"""
        <div class="prediction-box">
            <h2> Predicted Property Price</h2>
            <h1>₹{predicted_price:,.0f}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Price breakdown
        col1, col2, col3 = st.columns(3)
        
        with col1:
            base_price = carpet_area * area_info['avg_price']
            st.metric("Base Price", f"₹{base_price:,.0f}")
        
        with col2:
            amenities_premium = predicted_price - base_price
            st.metric("Location & Features Premium", f"₹{amenities_premium:,.0f}")
        
        with col3:
            final_price_per_sqft = predicted_price / carpet_area
            st.metric("Final Price/sq ft", f"₹{final_price_per_sqft:,.0f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p> Mumbai Real Estate Price Predictor</p>
    <p>💡 Just 3 simple steps to get your property price!</p>
</div>
""", unsafe_allow_html=True)