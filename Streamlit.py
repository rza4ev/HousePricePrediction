import streamlit as st
import joblib
import pandas as pd

# Yer adları ve konum grupları eşleştirmesi
location_groups = {
    0.5: ['Şah İsmayıl Xətai m.', 'Ağ şəhər q.', 'Bayıl q.', 'İçəri Şəhər m.', 'Sahil m.'],
    1.0: ['Nardaran q.', 'Nizami m.', 'Nəsimi r.', '28 May m.', 'Kubinka q.'],
    1.5: ['8 Noyabr m.', 'Səbail r.', 'Gənclik m.', 'Nəriman Nərimanov m.', 'Yasamal q.'],
    2.0: ['Elmlər Akademiyası m.', 'Nərimanov r.', '8-ci mikrorayon q.', 'Koroğlu m.', '1-ci mikrorayon q.'],
    2.5: ['Həzi Aslanov q.', 'Xutor q.', 'Xətai r.', 'Şıxov q.', 'Böyükşor q.'],
    3.0: ['Qara Qarayev m.', 'İnşaatçılar m.', 'Badamdar q.', 'Dərnəgül m.', 'Xəzər r.'],
    3.5: ['Binəqədi r.', '20 Yanvar m.', 'Azadlıq Prospekti m.', 'Yasamal r.', '20-ci sahə q.'],
    4.0: ['Həzi Aslanov m.', 'Nizami r.', 'Neftçilər m.', '7-ci mikrorayon q.', 'Nəsimi m.'],
    4.5: ['Memar Əcəmi m.', '9-cu mikrorayon q.', 'Xalqlar Dostluğu m.', 'Yeni Yasamal q.', '8-ci kilometr q.'],
    5.0: ['Əhmədli m.', 'Binəqədi q.', 'Bakıxanov q.', 'Əhmədli q.', 'Əmircan q.'],
    5.5: ['Bakmil m.', 'Köhnə Günəşli q.', 'Avtovağzal m.', 'Sabunçu r.', '6-cı mikrorayon q.'],
    6.0: ['Qaraçuxur q.', '4-cü mikrorayon q.', 'Biləcəri q.', 'Massiv D q.', 'Gəncə'],
    6.5: ['Yeni Günəşli q.', 'Abşeron r.', 'Lökbatan q.', 'Zabrat q.', 'Qaradağ r.'],
    7.0: ['Sumqayıt', 'Hövsan q.', 'Məmmədli q.', 'Suraxanı r.', 'Massiv A q.'],
    7.5: ['Zığ q.', 'Xırdalan', 'Masazır q.', 'Lənkəran', 'Saray q.', 'Hökməli q.', 'Şirvan', 'Massiv V q.', 'Binə q.', 'Mehdiabad q.', 'Kürdəxanı q.', 'Günəşli q.', 'Şimal DRES q.', 'Sahil q.', 'Yeni Suraxanı q.']
}

# Tüm yer adlarını bir listeye al
all_locations = [location for sublist in location_groups.values() for location in sublist]

# Load the trained model
filename = 'RandomForest2.sav'
model = joblib.load(filename)

# Streamlit application layout
st.title('House Price Prediction App')
st.write('Welcome to the house price prediction app.')

# Sidebar for user inputs
st.sidebar.header('Input Parameters')
num_rooms = st.sidebar.number_input('Number of Rooms', min_value=1, max_value=10, value=3)
area = st.sidebar.number_input('Area (sqm)', min_value=20, max_value=500, value=100)
floor = st.sidebar.number_input('Floor Number', min_value=1, max_value=30, value=5)
total_floors = st.sidebar.number_input('Total Floors', min_value=1, max_value=50, value=10)

# Location selection
location = st.sidebar.selectbox('Location', all_locations)

# Location group determination
location_group = None
for group, locations in location_groups.items():
    if location in locations:
        location_group = group
        break

if location_group is None:
    st.sidebar.error('Invalid location selected.')
else:
    st.sidebar.write(f'Selected Location Group: {location_group}')

# Calculate derived feature
area_per_room = area / num_rooms if num_rooms > 0 else 0

# Predict function
def predict_price(num_rooms, area, floor, total_floors, location_group, area_per_room):
    input_data = pd.DataFrame({
        'Number of Rooms': [num_rooms],
        'Area': [area],
        'Floor': [floor],
        'Total Floors': [total_floors],
        'Location_Group': [location_group],
        'Area_for_Room': [area_per_room]
    })
    prediction = model.predict(input_data)
    return prediction[0]

# Prediction
if location_group is not None:
    predicted_price = predict_price(num_rooms, area, floor, total_floors, location_group, area_per_room)

    # Display prediction result
    st.subheader('Predicted House Price')
    st.write(f'Estimated house price: {predicted_price:.2f}')
