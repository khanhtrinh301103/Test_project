# test_project

cd /d D:\Test_project
conda activate env_data_analysis
cd Test_project
python app.py

Update:
Trong index.html 
thêm  class="rainprobability" vào div dưới này
<div>Rain probability: {{ weather['precipitation_probability'] }}%</div>

Trong app.py:
pip install flask-cors
from flask_cors import CORS


để CORS(server) ở dưới server.secrectkey

http://127.0.0.1:5000/
