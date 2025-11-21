# AI-Stylist - Digital Closet Application

A modern full-stack web application for organizing your wardrobe digitally, with plans for AI-powered outfit recommendations and styling features.

![AI-Stylist](https://img.shields.io/badge/Next.js-16.0-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![Supabase](https://img.shields.io/badge/Supabase-Auth%20%26%20Storage-3ECF8E?style=for-the-badge&logo=supabase)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=for-the-badge&logo=typescript)

## 🌟 Features

### Current Features

- **User Authentication**: Secure signup and login with JWT tokens
- **Digital Closet**: Upload and organize clothing items with photos
- **Image Storage**: Cloud storage via Supabase
- **Metadata Tagging**: Categorize items by type, color, brand, and notes
- **Responsive Design**: Beautiful UI that works on all devices
- **Protected Routes**: Secure access to user-specific data

### Coming Soon

- 🤖 AI-powered outfit recommendations
- 🏷️ Advanced tagging and categorization
- 👔 Outfit creation and saving
- 📱 Social sharing capabilities
- 🛍️ E-commerce platform integration

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- React Hot Toast
- Axios

**Backend:**
- FastAPI (Python)
- Supabase (Auth & Storage)
- JWT Authentication
- PostgreSQL (via Supabase)

**Infrastructure:**
- Frontend: Vercel
- Backend: Render/Railway/Fly.io
- Database: Supabase
- Storage: Supabase Storage

### Project Structure

```
ai-stylist/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application file
│   ├── requirements.txt    # Python dependencies
│   ├── schema.sql          # Database schema
│   ├── .env.example        # Environment variables template
│   ├── README.md           # Backend documentation
│   ├── DEPLOYMENT.md       # Backend deployment guide
│   ├── SUPABASE_SETUP.md   # Supabase configuration guide
│   └── API_TESTING.md      # API testing guide
│
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app directory
│   │   ├── page.tsx       # Landing page
│   │   ├── login/         # Login page
│   │   ├── signup/        # Signup page
│   │   ├── closet/        # Digital closet page
│   │   └── upload/        # Upload page
│   ├── components/        # React components
│   ├── lib/              # Utilities and API client
│   ├── types/            # TypeScript type definitions
│   ├── .env.local.example # Environment variables template
│   ├── README.md         # Frontend documentation
│   └── DEPLOYMENT.md     # Frontend deployment guide
│
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ and pnpm
- **Python** 3.11+
- **Supabase** account
- **Git** for version control

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-stylist.git
cd ai-stylist
```

### 2. Set Up Supabase

Follow the detailed guide in `backend/SUPABASE_SETUP.md`:

1. Create a Supabase project
2. Get your API credentials
3. Run the database schema
4. Create storage bucket
5. Configure security policies

### 3. Set Up Backend

```bash
cd backend

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Supabase credentials
# SUPABASE_URL=your-url
# SUPABASE_KEY=your-key
# SUPABASE_SERVICE_KEY=your-service-key
# SECRET_KEY=generate-a-random-key

# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at `http://localhost:8000`

API docs available at `http://localhost:8000/docs`

### 4. Set Up Frontend

```bash
cd frontend

# Install dependencies
pnpm install

# Create .env.local file
cp .env.local.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run the development server
pnpm dev
```

Frontend will be running at `http://localhost:3000`

### 5. Test the Application

1. Open `http://localhost:3000`
2. Click **"Sign Up"** to create an account
3. Login with your credentials
4. Upload your first clothing item
5. View your digital closet!

## 📚 Documentation

### Backend Documentation

- **[Backend README](backend/README.md)**: Backend setup and API overview
- **[Supabase Setup](backend/SUPABASE_SETUP.md)**: Complete Supabase configuration guide
- **[API Testing](backend/API_TESTING.md)**: How to test API endpoints
- **[Backend Deployment](backend/DEPLOYMENT.md)**: Deploy to Render, Railway, or Fly.io

### Frontend Documentation

- **[Frontend Deployment](frontend/DEPLOYMENT.md)**: Deploy to Vercel or Netlify

## 🚢 Deployment

### Deploy Backend

Choose one of these platforms:

1. **Render** (Recommended for beginners)
   ```bash
   # See backend/DEPLOYMENT.md for detailed instructions
   ```

2. **Railway**
   ```bash
   railway init
   railway up
   ```

3. **Fly.io**
   ```bash
   fly launch
   fly deploy
   ```

See `backend/DEPLOYMENT.md` for detailed instructions.

### Deploy Frontend

**Vercel** (Recommended):

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL

# Deploy to production
vercel --prod
```

Or use the Vercel dashboard for one-click deployment.

See `frontend/DEPLOYMENT.md` for detailed instructions.

## 🔒 Security

- **JWT Authentication**: Secure token-based auth
- **Row Level Security**: Database-level access control
- **Password Hashing**: Bcrypt for password security
- **HTTPS**: Enforced in production
- **CORS**: Configured for specific origins
- **Environment Variables**: Secrets never committed to Git

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Test with curl
curl http://localhost:8000/

# Test with Python
python3 test_api.py
```

See `backend/API_TESTING.md` for comprehensive testing guide.

### Frontend Testing

```bash
cd frontend

# Build for production
pnpm build

# Run production build locally
pnpm start
```

## 📊 Database Schema

### `clothing_items` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `user_id` | UUID | Owner of the item |
| `image_url` | TEXT | Supabase storage URL |
| `category` | TEXT | Clothing category |
| `color` | TEXT | Primary color |
| `brand` | TEXT | Brand name |
| `notes` | TEXT | User notes |
| `created_at` | TIMESTAMP | Creation time |
| `updated_at` | TIMESTAMP | Last update time |

## 🔑 Environment Variables

### Backend (.env)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
SECRET_KEY=your-jwt-secret
ENVIRONMENT=development
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Endpoints

### Authentication

- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user

### Clothing Items (Protected)

- `POST /api/items/upload` - Upload clothing item
- `GET /api/items` - Get all user's items
- `DELETE /api/items/{item_id}` - Delete item

### Health Check

- `GET /` - API health check

Full API documentation available at `/docs` when running the backend.

## 🎨 UI Screenshots

### Landing Page
Beautiful gradient design with feature highlights

### Digital Closet
Grid view of all your clothing items with metadata

### Upload Page
Drag-and-drop image upload with form fields

## 🛠️ Development

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests
pytest

# Format code
black main.py

# Lint
flake8 main.py
```

### Frontend Development

```bash
# Run dev server
pnpm dev

# Type checking
pnpm type-check

# Linting
pnpm lint

# Format code
pnpm format
```

## 📈 Future Roadmap

### Phase 1: AI Integration (Q1 2025)
- [ ] AI-powered outfit recommendations
- [ ] Automatic clothing categorization
- [ ] Color palette analysis

### Phase 2: Social Features (Q2 2025)
- [ ] Share outfits with friends
- [ ] Public/private closet settings
- [ ] Follow other users

### Phase 3: E-commerce (Q3 2025)
- [ ] Integration with shopping platforms
- [ ] Price tracking for items
- [ ] Similar item suggestions

### Phase 4: Mobile App (Q4 2025)
- [ ] React Native mobile app
- [ ] Offline mode
- [ ] Camera integration

## 🐛 Known Issues

- Free tier backend (Render) may spin down after 15 minutes of inactivity
- Large images (>5MB) may take longer to upload
- Mobile responsiveness can be improved

## 💡 Tips for Learning

This project is designed to teach you:

1. **Full-stack development** with modern frameworks
2. **Authentication** and security best practices
3. **Cloud storage** integration
4. **API design** and documentation
5. **Deployment** to production platforms
6. **Database design** and Row Level Security
7. **TypeScript** for type-safe frontend
8. **React hooks** and state management

## 📞 Support

If you encounter issues:

1. Check the documentation in each directory
2. Review the troubleshooting sections in deployment guides
3. Open an issue on GitHub
4. Check Supabase dashboard for database/storage issues

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Next.js** team for the amazing framework
- **FastAPI** for the intuitive Python framework
- **Supabase** for backend-as-a-service
- **Vercel** for seamless deployment
- **Tailwind CSS** for beautiful styling

## 🔗 Links

- **Live Demo**: Coming soon
- **Documentation**: See individual README files
- **API Docs**: Available at `/docs` endpoint
- **Supabase**: https://supabase.com
- **Next.js**: https://nextjs.org
- **FastAPI**: https://fastapi.tiangolo.com

---

**Built with ❤️ for learning full-stack development**

Happy coding! 🚀
