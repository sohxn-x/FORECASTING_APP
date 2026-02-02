# Steel Industry Insights India — Energy Forecasting Platform

A full-stack web application for forecasting energy consumption trends (Gcal/tcs) for Indian steel plants using an LSTM time-series model.  
Frontend: **React + Vite + TypeScript + Tailwind + Shadcn UI**  
Backend: **Flask + Pandas + TensorFlow/Keras + Matplotlib**

---

## 1) File Structure

### Root (Project)
energy_app/
│
├─ app.py
├─ static/
│ └─ uploads/ # Generated forecast plots are saved here
│
├─ forecast/ # (Optional) your static forecast generation scripts (if any)
├─ comparison/ # (Optional) comparison scripts (if any)
│
└─ frontend/ # React + Vite Frontend
├─ index.html
├─ package.json
├─ vite.config.ts
├─ tailwind.config.cjs
├─ postcss.config.cjs
├─ tsconfig.json
├─ tsconfig.app.json
├─ tsconfig.node.json
├─ src/
│ ├─ main.tsx
│ ├─ App.tsx
│ ├─ index.css
│ ├─ pages/
│ │ ├─ HomePage.tsx
│ │ ├─ PredictionsPage.tsx
│ │ └─ CalculatorPage.tsx
│ ├─ components/
│ │ └─ ui/
│ │ └─ Background.tsx
│ └─ lib/ (optional)
│
└─ public/
├─ favicon.svg
└─ backgrounds/ # Background slideshow images (add your images here)


---

## 2) Required Modules / Dependencies

### Backend (Python)
Install these inside your Python virtual environment:

- Flask
- flask-cors
- pandas
- numpy
- matplotlib
- scikit-learn
- tensorflow

### Frontend (Node.js)
Installed via `package.json`:
- React + Vite + TypeScript
- TailwindCSS
- Shadcn UI
- framer-motion
- react-hot-toast
- lucide-react

---

## 3) Setup & Installation

### 3.1 Backend Setup (Flask)
#### Step 1: Create & activate venv
**Windows (PowerShell)**
```powershell
cd energy_app
python -m venv .venv
.\.venv\Scripts\activate
Mac/Linux

cd energy_app
python3 -m venv .venv
source .venv/bin/activate
Step 2: Install backend dependencies
pip install flask flask-cors pandas numpy matplotlib scikit-learn tensorflow
Step 3: Run backend
python app.py
Backend runs at:

http://127.0.0.1:5000

3.2 Frontend Setup (React)
Step 1: Go to frontend folder
cd energy_app/frontend
Step 2: Install node modules
npm install
Step 3: Start frontend dev server
npm run dev
Frontend runs at:

http://localhost:5173

##4) Commands Needed (Quick List)
Backend
python app.py
Frontend
npm install
npm run dev
(Optional linting)

npm run lint
##5) Step-by-Step Execution (Recommended Order)
Step 1 — Start Flask Backend
Open terminal in energy_app/

Activate venv

Run:

python app.py
Confirm backend is running:

Open http://127.0.0.1:5000/api/forecasts in browser
(Should return a JSON list)

Step 2 — Start React Frontend
Open another terminal in energy_app/frontend/

Run:

npm install
npm run dev
Open:

http://localhost:5173

Step 3 — Upload & Predict (Calculator Page)
Go to Upload & Predict Forecasts

Upload a CSV file with columns:

Plant

Date

Energy_Gcal_tcs

Select a plant (RSP/ISP/BSP/DSP/BSL/SAIL/All Plants Avg)

Click Run Forecast

Output:

Forecast message

Forecast plot shown on the page

Plot is also saved in:

energy_app/static/uploads/

Step 4 — View Static Forecasts (Predictions Page)
Navigate to Predictions Page

React calls:

GET http://127.0.0.1:5000/api/forecasts

Static forecast images appear (one per row)

Click on any image to zoom fullscreen

##6) Notes / Troubleshooting
If you get ModuleNotFoundError: flask_cors
Run:

pip install flask-cors
If images are not loading in frontend
Ensure Flask is running on port 5000

Ensure image URLs returned are like:

http://127.0.0.1:5000/static/uploads/<filename>.png

Ensure the folder exists:

energy_app/static/uploads/

Background images not visible
Add images in:

frontend/public/backgrounds/

Ensure Background.tsx uses correct paths like:

/backgrounds/img1.jpg

##7) CSV Format Example
Date,Plant,Energy_Gcal_tcs
2015-01-01,RSP,7.8
2016-01-01,RSP,7.6
2017-01-01,RSP,7.5
...
##8) Output
Forecast plots are generated dynamically and stored in:

energy_app/static/uploads/

Frontend loads them via Flask static route.
