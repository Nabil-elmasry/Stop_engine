import pickle
import requests

# رابط الملف على GitHub (raw link)
url = "https://raw.githubusercontent.com/YOUR_USERNAME/stop_engine/main/modules/trained_model.pkl"

response = requests.get(url)

if response.status_code == 200:
    model = pickle.loads(response.content)
    st.success("تم تحميل النموذج بنجاح من GitHub ✅")
else:
    st.error("فشل تحميل النموذج من GitHub ❌")