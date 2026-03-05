# IoT Monitoring Dashboard

A **full-stack IoT monitoring dashboard** built with **React, Django REST Framework, and PostgreSQL**.
The application allows users to monitor IoT devices, visualize sensor data, and manage devices through a modern dashboard interface.

---

## Features

 **Device Monitoring** – View all connected IoT devices
 **Add Devices** – Register new sensor devices
 **Delete Devices** – Remove devices from the system
 **Analytics Dashboard** – Temperature & humidity charts
 **Online / Offline Status** – Monitor device connectivity
 **Last Updated Timestamp** – Track latest sensor readings
 **Dark Mode UI** – Modern dashboard styling
 **Auto Refresh** – Polling updates every 5 seconds
 **Responsive Design** – Works on desktop and mobile

---

## Tech Stack

### Frontend

* React
* TailwindCSS
* Chart.js
* Axios

### Backend

* Django
* Django REST Framework
* PostgreSQL

### Tools

* Git & GitHub
* Vercel (Frontend deployment)
* Render (Backend deployment)

---

## Project Structure

```
iot-monitoring-dashboard
│
├── backend
│   ├── api
│   ├── config
│   ├── manage.py
│
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── DeviceCard.js
│   │   │   ├── DeviceForm.js
│   │   │   ├── DeviceChart.js
│   │   │
│   │   ├── App.js
│   │   ├── index.js
│   │
│   ├── package.json
│
└── README.md
```

---

## Installation

### Clone the repository

```
git clone https://github.com/Jeynthagj/iot-monitoring-dashboard.git
cd iot-monitoring-dashboard
```

---

### Backend Setup (Django)

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Start backend server:

```
python manage.py runserver
```

Backend will run at:

```
http://127.0.0.1:8000
```

---

### Frontend Setup (React)

```
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## Environment Variables

Create `.env` inside the **frontend folder**:

```
REACT_APP_API_URL=http://127.0.0.1:8000
```

---

## Dashboard Preview

Example features shown in the dashboard:

* Device cards
* Temperature & humidity chart
* Device status indicators
* Dark mode interface

*(You can add screenshots here later)*

---

## Future Improvements

* Device editing support
* Historical sensor data tracking
* Device search & filtering
* Authentication system
* Real-time WebSocket updates
* Docker deployment

---

## Author

**Jeynth A**

GitHub:
https://github.com/Jeynthagj

---

## License

This project is licensed under the **MIT License**.
