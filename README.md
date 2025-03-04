# Airbnb Rental Price Prediction in Sydney  

## Project Overview  
This project applies machine learning techniques to predict Airbnb rental prices in Sydney.  
By analyzing key factors such as property attributes, host details, location trends, and seasonal demand, it provides data-driven insights to optimize pricing strategies for Airbnb hosts and real estate investors.  

This project was developed as part of QBUS6810 - Statistical Learning and Data Mining at the University of Sydney and was a collaborative effort by a team of students working together to apply data analytics and machine learning concepts in a real-world scenario.  



## Objective  
- Develop predictive models to estimate nightly rental prices.  
- Identify key factors influencing pricing strategies.  
- Provide data-driven insights for maximizing revenue and occupancy rates.  


## Dataset  
The dataset includes Airbnb listing details, covering:  

| Category          | Description |
|------------------|------------|
| Property Features | Bedrooms, bathrooms, amenities, guest capacity |
| Host Information | Superhost status, listing duration, pricing history |
| Location Data | Proximity to city center, landmarks, and public transport |
| Market Trends | Seasonal fluctuations, competitor pricing analysis |
| Guest Experience | Ratings, reviews, and customer engagement metrics |


## Methodology  
1. **Data Collection & Preprocessing** – Handling missing values, outliers, and feature engineering.  
2. **Exploratory Data Analysis (EDA)** – Identifying trends and correlations.  
3. **Model Selection & Training** – Implementing and comparing:  
   - Ridge Regression  
   - k-Nearest Neighbors (kNN)  
   - Decision Trees & Random Forests  
   - Gradient Boosting (XGBoost, Stacking Models)  
4. **Model Evaluation** – Using Mean Squared Error (MSE) and R² Score to assess performance.  
5. **Insights & Recommendations** – Generating data-driven pricing strategies for Airbnb hosts.  


## Key Findings  
- Listings with higher guest capacity command premium pricing.  
- Proximity to major landmarks and public transport significantly influences rental price.  
- Seasonal trends drive price fluctuations, with peak seasons offering higher revenue opportunities.  
- Highly-rated hosts and well-reviewed properties attract more bookings and higher pricing.  
- Dynamic pricing strategies help optimize occupancy rates and maximize revenue.  


## Technologies Used  
- **Programming Language**: Python  
- **Libraries**: Pandas, NumPy, Scikit-learn, XGBoost, Matplotlib, Seaborn  
- **Machine Learning Models**: Regression-based and tree-based ensemble models  
- **Data Visualization**: Price distribution plots, correlation heatmaps, and trend analysis  
