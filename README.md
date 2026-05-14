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

## � Deployment Guide

This project can be deployed for free using the following services:

### Prerequisites
- GitHub account
- Stripe account (for payments)
- Optional: Khalti and eSewa merchant accounts

### Step 1: Prepare Your Code
1. **Generate a Django secret key:**
   ```bash
   python generate_secret.py
   ```
   Copy the generated SECRET_KEY.

2. **Create environment files:**
   - Copy `backend/.env.example` to `backend/.env`
   - Fill in your actual values

3. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/nepal-trek-connect.git
   git push -u origin main
   ```

### Step 2: Deploy Frontend (Vercel - Free)
1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`
5. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend URL (will add after backend deployment)
   - `NEXT_PUBLIC_STRIPE_PUBLIC_KEY`: Your Stripe publishable key
   - `NEXT_PUBLIC_KHALTI_PUBLIC_KEY`: Your Khalti public key
   - `NEXT_PUBLIC_WHATSAPP_NUMBER`: `9779846958184`
6. Click "Deploy"

### Step 3: Deploy Database (Supabase - Free)
1. Go to [supabase.com](https://supabase.com) and sign up
2. Create a new project
3. Go to Settings → Database → Connection string
4. Copy the PostgreSQL connection string (URI format)

### Step 4: Deploy Backend (Render - Free)
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure service:
   - **Name:** nepal-trek-backend
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`
5. Add environment variables:
   - `SECRET_KEY`: Your generated secret key
   - `DEBUG`: `false`
   - `DATABASE_URL`: Your Supabase connection string
   - `ALLOWED_HOSTS`: Your Render backend URL
   - `CORS_ALLOWED_ORIGINS`: Your Vercel frontend URL
   - `STRIPE_PUBLIC_KEY`: Your Stripe keys
   - `STRIPE_SECRET_KEY`: Your Stripe keys
   - `KHALTI_PUBLIC_KEY`: Your Khalti keys
   - `KHALTI_SECRET_KEY`: Your Khalti keys
   - `ESEWA_MERCHANT_CODE`: `EPAYTEST` (sandbox)
   - `WHATSAPP_NUMBER`: `9779846958184`
6. Click "Create Web Service"

### Step 5: Update Frontend Environment
1. Go back to Vercel dashboard
2. Update `NEXT_PUBLIC_API_URL` with your Render backend URL
3. Redeploy the frontend

### Step 6: Test Your Deployment
1. Visit your Vercel frontend URL
2. Try registering a user
3. Browse treks
4. Test the booking flow (with Stripe test cards)

### Alternative Free Hosting Options

#### Backend Alternatives:
- **Fly.io**: `fly.io` (free tier available)
- **Railway**: `railway.app` (free tier available)

#### Database Alternatives:
- **Neon**: `neon.tech` (free tier)
- **ElephantSQL**: `elephantsql.com` (free tier)

### ⚠️ Important Notes
- **Free tiers have limitations**: Database size, bandwidth, etc.
- **Media uploads**: Free backends may lose uploaded files. Consider using Cloudinary free tier for images.
- **Payments**: Stripe test mode works for demo. Live payments require merchant accounts.
- **Domain**: Free hosting provides subdomains. Custom domains cost extra.

### 🔧 Troubleshooting
- **CORS errors**: Double-check `CORS_ALLOWED_ORIGINS` in backend
- **Database connection**: Ensure `DATABASE_URL` is correct
- **Static files**: WhiteNoise handles static files automatically
- **Media files**: Consider external storage for production

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
