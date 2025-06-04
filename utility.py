import pandas as pd

def load_properties():
    
    data = [
    {
        "project_name": "Green Homes",
        "locality": "Sector 62",
        "price": 3250000,
        "bhk": 2,
        "status": "Ready to Move",
        "metro_nearby": False,
        "distance_office": 8,
        "distance_school": 4,
        "amenities": "Clubhouse, Gym, Swimming Pool"
    },
    {
        "project_name": "Skyline Residency",
        "locality": "Sector 63",
        "price": 3500000,
        "bhk": 2,
        "status": "Ready to Move",
        "metro_nearby": False,
        "distance_office": 6,
        "distance_school": 3,
        "amenities": "Park, Jogging Track, 24/7 Security"
    },
    {
        "project_name": "Sunshine Apartments",
        "locality": "Sector 74",
        "price": 3300000,
        "bhk": 2,
        "status": "Under Construction",
        "metro_nearby": False,
        "distance_office": 9,
        "distance_school": 2,
        "amenities": "Clubhouse, Gym, Children's Play Area"
    },
    {
        "project_name": "Luxury Heights",
        "locality": "Sector 50",
        "price": 5000000,
        "bhk": 3,
        "status": "Ready to Move",
        "metro_nearby": True,
        "distance_office": 4,
        "distance_school": 1,
        "amenities": "Pool, Gym, Garden"
    }
]
    return pd.DataFrame(data)

def filter_properties(df, preferences):
    
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
    
    return text