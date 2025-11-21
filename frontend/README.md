# AI-Stylist Frontend

Next.js 16 frontend for the AI-Stylist digital closet application with TypeScript and Tailwind CSS.

## Features

- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Type-Safe**: Full TypeScript support
- **Authentication**: Secure login/signup with JWT
- **Protected Routes**: Client-side route protection
- **Image Upload**: Drag-and-drop file upload with preview
- **Real-time Feedback**: Toast notifications for user actions
- **Optimized**: Next.js App Router for best performance

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5.9
- **Styling**: Tailwind CSS 4.1
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast
- **Package Manager**: pnpm

## Prerequisites

- Node.js 20 or higher
- pnpm (recommended) or npm
- Backend API running (see `../backend/README.md`)

## Installation

```bash
# Install pnpm globally if you haven't
npm install -g pnpm

# Install dependencies
pnpm install
```

## Environment Setup

```bash
# Copy environment template
cp .env.local.example .env.local

# Edit .env.local and set your backend URL
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

```bash
# Run development server
pnpm dev

# Open http://localhost:3000
```

The app will automatically reload when you make changes.

## Building for Production

```bash
# Create production build
pnpm build

# Start production server
pnpm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Landing page
│   ├── login/             # Login page
│   ├── signup/            # Signup page
│   ├── closet/            # Digital closet (protected)
│   └── upload/            # Upload page (protected)
│
├── components/            # React components
│   ├── Navbar.tsx        # Navigation bar
│   └── ProtectedRoute.tsx # Route protection HOC
│
├── lib/                   # Utilities
│   ├── api.ts            # API client and endpoints
│   └── auth-context.tsx  # Authentication context
│
├── types/                 # TypeScript types
│   └── index.ts          # Type definitions
│
└── .env.local.example    # Environment template
```

## Pages

### Public Pages

- **`/`** - Landing page with features
- **`/login`** - User login
- **`/signup`** - User registration

### Protected Pages

- **`/closet`** - View all clothing items
- **`/upload`** - Upload new items

## API Integration

### Authentication

```typescript
import { authApi } from '@/lib/api';

// Signup
await authApi.signup({
  email: 'user@example.com',
  password: 'password123',
  full_name: 'John Doe'
});

// Login
await authApi.login({
  email: 'user@example.com',
  password: 'password123'
});
```

### Clothing Items

```typescript
import { itemsApi } from '@/lib/api';

// Upload item
await itemsApi.upload(file, {
  category: 'shirt',
  color: 'blue',
  brand: 'Nike',
  notes: 'Favorite shirt'
});

// Get all items
const { items } = await itemsApi.getAll();

// Delete item
await itemsApi.delete(itemId);
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions to Vercel, Netlify, or AWS Amplify.

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
