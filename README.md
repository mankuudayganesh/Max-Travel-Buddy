🌍 AI Travel Planner – India

An AI-powered travel planning web application that generates a day-by-day travel itinerary based on destination, number of days, and budget.

This project combines Frontend UI, Interactive Maps, and AI backend to create a smart travel planning experience.

🚀 Features
🧠 AI Trip Planning

Automatically generates day-by-day itinerary

Suggests places to visit

Suggests nearby hotels

Suggests nearby attractions

Generates description for each place

📍 Smart Destination Search

Autocomplete suggestions for:

States

Districts

Tourist places

Uses India tourism dataset

🗺 Interactive Map

Built using Leaflet.js

Shows:

Start location

Destination

Travel route

Distance calculation

Travel time estimation

📄 PDF Travel Plan

Users can download the generated itinerary as a PDF travel guide.

Includes:

Day-wise travel plan

Hotel recommendations

Nearby attractions

Budget details

🔐 Login System

Simple authentication system using LocalStorage

Users can:

Create account

Login

Access travel planner

🧱 Tech Stack
Frontend

HTML5

CSS3

JavaScript

Leaflet.js (Maps)

HTML2PDF.js

Backend

Python

FastAPI

Groq AI API

Llama 3.1 model

AI Model

Groq Llama 3.1 8B Instant

Used for:

Travel description generation

Smart itinerary creation

AI-Travel-Planner
│
├── backend
│   │
│   ├── main.py
│   ├── travel_ai.py
│   ├── .env
│
├── frontend
│   │
│   ├── index.html
│   ├── login.html
│   ├── plan.html
│   │
│   ├── css
│   │   └── style.css
│   │
│   ├── js
│   │   └── script.js
│   │
│   └── data
│       └── india_places.json
│
└── README.md
⚙️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/yourusername/ai-travel-planner.git
2️⃣ Install Backend Dependencies
pip install fastapi uvicorn python-dotenv groq
3️⃣ Setup Environment Variables

Create .env

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
4️⃣ Start Backend Server
python main.py

Server runs on:

http://127.0.0.1:8001
5️⃣ Run Frontend

Open:

index.html

in browser.

🧠 How the AI Works

1️⃣ User enters:

From location

Destination

Number of days

Budget

2️⃣ Frontend sends request to backend:

POST /generate-trip

3️⃣ Backend:

Searches tourism dataset

Selects best places

Generates itinerary

Suggests hotels

Returns travel plan

4️⃣ Frontend displays:

Day-wise travel plan

Map route

Cost estimation

PDF download option

📊 Example Output
Day 1
Visit: Charminar
Hotel: Hyderabad Grand Hotel (4.5★)
Nearby: Golconda Fort

Day 2
Visit: Ramoji Film City
Hotel: Royal Stay Hyderabad
Nearby: Hussain Sagar Lake
🗺 Dataset

Contains tourism data for:

All Indian states

Districts

Tourist places

Temples

Natural attractions

Beaches

Historical monuments

💡 Future Improvements

Google Maps API integration

Real hotel APIs (Booking / Agoda)

Flight suggestions

Multi-country travel

AI chatbot travel assistant

React frontend version

👨‍💻 Author

Uday S

Computer Science Engineering Student

Projects:

AI Travel Planner

SkillFault Learning Platform (in development)

⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork it
📢 Share with others