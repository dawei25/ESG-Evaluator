import pandas as pd
import numpy as np

def calculate_esg_score(company_data, weights):
    environmental_score = np.dot(company_data['environmental_metrics'], weights['environmental'])
    social_score = np.dot(company_data['social_metrics'], weights['social'])
    governance_score = np.dot(company_data['governance_metrics'], weights['governance'])
    
    total_score = (environmental_score + social_score + governance_score) / 3
    return {
        'environmental': environmental_score,
        'social': social_score,
        'governance': governance_score,
        'total': total_score
    }

# Example company data (simplified)
company_data = {
    'environmental_metrics': np.array([0.7, 0.8, 0.6]),  # e.g., [carbon_emissions, water_usage, waste_management]
    'social_metrics': np.array([0.9, 0.7, 0.8]),  # e.g., [employee_satisfaction, diversity_score, community_impact]
    'governance_metrics': np.array([0.8, 0.9, 0.7])  # e.g., [board_independence, executive_compensation, transparency]
}

# Example weights (can be adjusted based on industry or other factors)
weights = {
    'environmental': np.array([0.4, 0.3, 0.3]),
    'social': np.array([0.3, 0.4, 0.3]),
    'governance': np.array([0.3, 0.3, 0.4])
}

esg_scores = calculate_esg_score(company_data, weights)
print("ESG Scores:", esg_scores)