
## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dhruvprkh69/Mumbai-real-estate-price-predictor.git
   
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the entire ipynb file**

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open in browser**
   - Local URL: http://localhost:8501
   - Network URL: http://your-ip:8501

## 📊 Dataset Information

### Dataset Statistics
- **Total Properties**: 12,685
- **Features**: 145
- **Unique Areas**: 357
- **Price Range**: ₹1 Lakh - ₹37 Crore
- **Property Types**: Apartment, Villa, Penthouse, Residential House, Builder Floor

### Key Features Used
- **Basic**: Bedroom, Bathroom, Carpet Area
- **Location**: Area Name (357 unique areas)
- **Amenities**: 91 amenities categorized into 4 levels
- **Property Type**: 5 different types
- **Furnishing**: 3 categories

## 🔧 Model Development

### Data Preprocessing
- **Missing Value Handling**: Imputation for <50% missing, drop for >50%
- **Outlier Management**: 99th percentile capping for apartments, keep luxury properties
- **Feature Engineering**: Bedroom-bathroom ratio, amenities scoring, area encoding

### Feature Engineering
- **Amenities Categorization**:
  - Basic: Lift, Security, Parking (5-9 amenities)
  - Standard: Gym, Swimming Pool, Club House (3-5 amenities)
  - Premium: Private Garage, Marble flooring (1-3 amenities)
  - Luxury: Sea facing, Helipad, Wine Cellar (0-2 amenities)

### Model Selection
- **Algorithms Tested**: Linear Regression, Ridge, Lasso, Random Forest, XGBoost
- **Best Model**: Random Forest (96.73% accuracy)
- **Feature Importance**: Carpet Area (65%), Price per sq ft (22%), Bedroom (6%)

## ��️ Area Categories

### Ultra Premium Areas
- **Price Range**: ₹25,000 - ₹100,000 per sq ft
- **Areas**: Bandra West, Juhu, Worli, Marine Drive, Nariman Point, Colaba
- **Features**: Luxury amenities, prime locations, high-end properties

### Premium Areas
- **Price Range**: ₹15,000 - ₹50,000 per sq ft
- **Areas**: Andheri West, Vile Parle West, Dadar West, Santacruz West
- **Features**: Good connectivity, modern amenities, established markets

### Mid-Range Areas
- **Price Range**: ₹6,000 - ₹30,000 per sq ft
- **Areas**: Malad West, Kandivali West, Borivali West, Thane West
- **Features**: Affordable luxury, growing infrastructure, family-friendly

### Affordable Areas
- **Price Range**: ₹3,000 - ₹15,000 per sq ft
- **Areas**: Dombivli East, Kalyan West, Ambernath, Badlapur
- **Features**: Budget-friendly, developing infrastructure, good connectivity

## 🎨 Application Features

### User Interface
- **3-Step Process**: Simple and intuitive
- **Real-time Updates**: Instant price calculations
- **Visual Feedback**: Area information and property summary
- **Responsive Design**: Works on all devices

### Price Breakdown
- **Base Price**: Area × Price per sq ft
- **Location Premium**: Market positioning and area value
- **Features Premium**: Amenities and property characteristics
- **Final Price per sq ft**: Total price divided by area

## 📱 Usage Guide

### Step 1: Select Area
- Choose from 100+ Mumbai areas
- View area category and price range
- Understand market positioning

### Step 2: Property Size
- Set number of bedrooms (1-6)
- Set number of bathrooms (1-5)
- View property summary

### Step 3: Carpet Area
- Select carpet area (300-5000 sq ft)
- Get instant price prediction
- View detailed price breakdown

## �� Model Validation

### Overfitting Analysis
- **Train-Test Gap**: 1.44% (minimal)
- **Cross-validation**: Consistent performance across folds
- **Error Patterns**: Similar between train and test sets
- **Model Complexity**: Reasonable parameters

### Validation Metrics
- **R² Consistency**: Standard deviation < 5%
- **Error Distribution**: Normal distribution
- **Prediction Accuracy**: 83% within 10% error
- **Model Robustness**: Stable across different data splits

## 🚀 Deployment

### Local Deployment
```bash
streamlit run streamlit_app.py
```

### Market Insights
- **Price Trends**: Area-wise market analysis
- **Investment Opportunities**: Emerging areas identification
- **Market Segmentation**: Category-based pricing strategy
- **Demand Patterns**: Property type preferences

---

## �� Project Statistics

- **Development Time**: 1-3 weeks
- **Lines of Code**: 500+
- **Model Accuracy**: 96.73%
- **Areas Covered**: 100+
- **Properties Analyzed**: 12,685

---

**⭐ Star this repository if you find it helpful!**

**🏠 Happy Property Hunting!**