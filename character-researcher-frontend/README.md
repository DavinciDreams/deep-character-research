# Character Researcher Frontend

This is a Next.js (TypeScript) frontend scaffold for the Character Researcher project, structured for Vercel deployment.

## Getting Started

### 1. Install dependencies

```bash
npm install
```

### 2. Set environment variables

Copy `.env.example` to `.env.local` and set your backend API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run locally

```bash
npm run dev
```

### 4. Deploy to Vercel

Push your repository to GitHub and import it into [Vercel](https://vercel.com/new). Vercel will detect the Next.js app and deploy automatically.

## Project Structure

- `/pages` — Main pages: research input, results, status/progress
- `/components` — UI components
- `/services` — API service layer (placeholder)

## Notes

- The API service uses `NEXT_PUBLIC_API_URL` for backend communication.
- UI and backend logic are placeholders; implement as needed.