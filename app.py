import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load key variables securely from local .env environment
load_dotenv()

API_KEY = os.getenv("IBM_CLOUD_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")

# The exact verified active URL path from your IBM console
DEPLOYMENT_URL = os.getenv("IBM_DEPLOYMENT_URL")

if not API_KEY:
    st.error("⚠️ IBM_CLOUD_API_KEY missing! Check your local .env file setup.")
    st.stop()

def get_iam_token(api_key):
    """Generates bearer token access directly from IBM Identity Access Management."""
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token") if response.status_code == 200 else None

# ==========================================
# STREAMLIT INTERFACE UI
# ==========================================
st.set_page_config(page_title="Predictive Maintenance Portal", page_icon="⚙️", layout="centered")
st.title("⚙️ Smart Industrial Predictive Maintenance Portal")
st.write("Input sensory telemetry metrics below to compute operational health statuses.")

st.markdown("---")
st.subheader("Machine Sensor Inputs")

col1, col2 = st.columns(2)

with col1:
    type_display = st.selectbox("Machine Type", options=["Low (L)", "Medium (M)", "High (H)"])
    air_temp = st.number_input("Air Temperature [K]", value=300.0, step=0.1)
    process_temp = st.number_input("Process Temperature [K]", value=310.0, step=0.1)
    rotational_speed = st.number_input("Rotational Speed [rpm]", value=1500, step=1)

with col2:
    torque = st.number_input("Torque [Nm]", value=40.0, step=0.1)
    tool_wear = st.number_input("Tool Wear [min]", value=0, step=1)
    total_work_stress = st.number_input("Total Work Stress Feature", value=1200.0, step=0.1)

st.markdown("---")

if st.button("Analyze Equipment Health Status", type="primary"):
    with st.spinner("Streaming data to IBM Cloud Pak endpoint..."):
        token = get_iam_token(API_KEY)
        
        if token:
            # Map type to the numerical encoding found in your dataset (Low=1, Medium=2, High=0)
            if "Low (L)" in type_display:
                type_numeric = 1.0
            elif "Medium (M)" in type_display:
                type_numeric = 2.0
            else:
                type_numeric = 0.0

            # Compute the exact engineered features found in your CSV template schema
            temp_difference = float(process_temp - air_temp)
            power_index = float(rotational_speed * torque)
            thermal_strain_accumulation = float(temp_difference * tool_wear)
            
            # THE HOLY GRAIL PAYLOAD - MATCHING YOUR 10-COLUMN CSV TEMPLATE EXACTLY
            payload = {
                "input_data": [{
                    "fields": [
                        "Type", 
                        "Air temperature [K]", 
                        "Process temperature [K]", 
                        "Rotational speed [rpm]", 
                        "Torque [Nm]", 
                        "Tool wear [min]", 
                        "Temperature_Difference", 
                        "Power_Index", 
                        "Thermal_Strain_Accumulation", 
                        "Total_Work_Stress"
                    ],
                    "values": [[
                        float(type_numeric), 
                        float(air_temp), 
                        float(process_temp), 
                        float(rotational_speed), 
                        float(torque), 
                        float(tool_wear), 
                        float(temp_difference), 
                        float(power_index), 
                        float(thermal_strain_accumulation), 
                        float(total_work_stress)
                    ]]
                }]
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            try:
                response = requests.post(DEPLOYMENT_URL, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    prediction_class = result["predictions"][0]["values"][0][0]
                    
                    if prediction_class == 0:
                        st.success("✅ **Machine Status: Normal Operational Parameters**")
                    else:
                        st.error(f"🚨 **Warning: Machine Failure Signature Detected (Category Code: {prediction_class})**")
                else:
                    st.error(f"❌ **API Scoring Error: Server returned status code {response.status_code}**")
                    with st.expander("View Server Error Response Details"):
                        st.text(response.text)
                        
            except Exception as e:
                st.error(f"Network Connection Error: {str(e)}")