import pandas as pd

def load_properties():
    # Mock data - replace with actual data loading
    data = {
        'project_name': ['Apex Greens', 'Elite Heights', 'Urban Nest'],
        'locality': ['Sector 74', 'Sector 137', 'Sector 150'],
        'price': [21000000, 24000000, 20000000],
        'status': ['Ready to Move', 'Under Construction', 'Ready to Move'],
        'amenities': [['Pool', 'Gym'], ['Park', 'Club'], ['Gym', 'Pool']],
        'metro_nearby': [True, False, True],
        'distance_office': [5, 8, 3],
        'distance_school': [2, 4, 1]
    }
    return pd.DataFrame(data)

def filter_properties(df, preferences):
    # Simple filtering - implement your actual logic
    filtered = df.copy()
    if preferences['status'] != 'Any':
        filtered = filtered[filtered['status'] == preferences['status']]
    if preferences['metro']:
        filtered = filtered[filtered['metro_nearby'] == True]
    filtered = filtered[filtered['price'] <= preferences['budget']]
    filtered = filtered[filtered['distance_office'] <= preferences['office_distance']]
    filtered = filtered[filtered['distance_school'] <= preferences['school_distance']]
    return filtered

def recommend_localities(df):
    return df['locality'].unique()[:3]

def translate_text(text):
    # Simple translation placeholder
    return text