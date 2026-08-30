# Multi-Algorithmic Predictive Maintenance Engine with IBM Cloud Deployment

An end-to-end data science and machine learning solution designed to monitor mechanical stress, analyze sensory logs, and predict component failure types before equipment breakdowns occur. This system leverages an optimized Random Forest classifier deployed on enterprise infrastructure.

---

## 🚀 Live Production Links & References

* **Live Streamlit Web Application:** [Click Here to View Live Dashboard](https://predictive-maintenance-ml-hminumxwwprhfguue9vdyd.streamlit.app/)
* **Cloud Hosted API Endpoint:** Deployed via IBM Watson Machine Learning (endpoint available on request / stored in `.env`)

> **🔒 Security Note:** In alignment with cloud security best practices, sensitive authentication vectors (such as individual IBM Cloud master API Keys) are explicitly omitted from this documentation and isolated via environment variables. The asset identifiers listed above serve purely as structural routing references.

---

## 🛠️ System Architecture & Workflow

1. **Exploratory Data Analysis & Outlier Rectification:** Cleaned manufacturing data points using median mathematical distribution to secure stable modeling boundaries.
2. **Feature Engineering:** Engineered specialized metrics (`Total_Work_Stress`) mapping physical torque parameters alongside real tool wear timelines.
3. **Algorithmic Training Benchmark:** Evaluated 5 diverse classification frameworks locally via Scikit-Learn to track F1-Score metrics and identify our champion algorithm.
4. **Cloud Integration Pipeline:** Hand-selected and exported the champion **Random Forest model** to an enterprise environment running Python 3.12 (`runtime-25.1`) and `scikit-learn_1.6`.
5. **Production Deployment:** Provisioned a cloud deployment factory engine (`Predictive_Maintenance_Space`) to compile an active, production-ready online REST API scoring route.

---

## 🖥️ Local Execution Guide

Follow these steps to stand up the interactive machine learning web dashboard locally.

### 1. Environment Installation
Ensure you have the required dependencies installed on your system terminal:
```bash
pip install streamlit requests python-dotenv
