# 🏔️ Nepal Trek Connect

![Nepal Trek Connect Banner](https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=2074&auto=format&fit=crop)

**Nepal Trek Connect** is a full-stack web application designed to help adventurers discover, plan, and book their trekking journeys across the beautiful landscapes of Nepal. Whether you're planning to conquer the Everest Base Camp or explore the Annapurna Circuit, Nepal Trek Connect provides a seamless booking experience.

---

## 🚀 Features

- **Trek Discovery**: Browse and search through a comprehensive list of treks in Nepal.
- **Interactive Maps**: View trek routes and destinations using integrated interactive maps (Leaflet).
- **Secure Booking & Payments**: Book your trek and pay securely. Integrated with international (Stripe) and local Nepali payment gateways (eSewa, Khalti).
- **User Accounts**: Create an account, manage your profile, and keep track of your bookings.
- **Reviews & Ratings**: Share your trekking experiences and read reviews from other adventurers.
- **WhatsApp Integration**: Quickly connect with support or guides via WhatsApp.
- **SEO Optimized**: Built with SEO best practices for better discoverability.

## 🛠️ Tech Stack

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) (App Router)
- **UI Library**: [React](https://reactjs.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Maps**: [React Leaflet](https://react-leaflet.js.org/)
- **Payments**: Stripe React
- **Other Tools**: Axios, Date-fns, Swiper

### Backend
- **Framework**: [Django](https://www.djangoproject.com/)
- **API**: [Django REST Framework](https://www.django-rest-framework.org/) (DRF)
- **Database**: PostgreSQL / SQLite (Development)
- **Authentication**: JWT (JSON Web Tokens)
- **Storage**: AWS S3 (Optional for media storage)
- **Payments**: Stripe, eSewa, Khalti integration

---

## 💻 Getting Started

Follow these instructions to set up the project locally for development and testing.

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python](https://www.python.org/) (3.10 or higher)
- [Git](https://git-scm.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Nepal-Trek-Connect.git
cd Nepal-Trek-Connect
```

### 2. Backend Setup
Navigate to the backend directory and set up the Python virtual environment:
```bash
cd backend
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (Create a .env file based on .env.example)
cp .env.example .env

# Run database migrations
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```
The backend server will be running at `http://127.0.0.1:8000/`.

### 3. Frontend Setup
Open a new terminal window, navigate to the frontend directory, and install dependencies:
```bash
cd frontend

# Install packages
npm install
# or yarn install

# Set up environment variables (Create a .env.local file based on your needs)
# Add your API URLs and Stripe keys here

# Start the Next.js development server
npm run dev
# or yarn dev
```
The frontend application will be running at `http://localhost:3000/`.

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)
Ensure you configure the following variables in your backend environment:
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- Database Credentials
- `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- `KHALTI_PUBLIC_KEY`, `KHALTI_SECRET_KEY`
- `ESEWA_MERCHANT_CODE`
- `WHATSAPP_NUMBER`

### Frontend (`frontend/.env.local`)
Configure the necessary variables for the frontend:
- `NEXT_PUBLIC_API_URL` (e.g., `http://127.0.0.1:8000/api`)
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve Nepal Trek Connect, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
*Built with ❤️ for adventurers around the world.*
