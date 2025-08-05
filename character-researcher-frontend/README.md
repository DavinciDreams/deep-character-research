# Character Researcher Frontend

This is a Next.js (TypeScript) frontend for the Character Researcher project, structured for Vercel deployment.

## Features

- **Historical Figure Gallery:** Browse, search, and filter a gallery of historical figures. Each card displays a portrait, era, years, and a short description.
- **Chat Interface:** Open a time portal to chat with a selected historical figure. Simulated responses and sound effects enhance the experience.
- **Research Integration:** Submit research queries about a figure and track progress/results (requires backend).
- **Accessible UI:** Keyboard navigation, ARIA labels, and responsive design.
- **API Integration:** Communicates with a backend via REST API (`NEXT_PUBLIC_API_URL`).

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

## Usage

1. **Browse Figures:** On the home page, view the gallery. Use the search bar and filters to find figures by name, era, or description.
2. **Connect & Chat:** Click "Connect" on a figure card to open a chat. Type questions and receive simulated responses.
3. **Research (if backend enabled):** Use research input forms to submit queries and view results.
4. **Sound Effects:** Enable or disable sound for chat interactions.

## Project Structure

- `/pages` — Main pages: gallery, chat, research input, results, status/progress
- `/components` — UI components (cards, chat, gallery, etc.)
- `/context` — React context for chat state
- `/services` — API service functions
- `/types` — Shared TypeScript types
- `/styles` — CSS modules and global styles

## Development Notes

- The frontend is fully migrated to Next.js. All legacy SPA files and components have been removed from `/src` except for shared types, context, and styles still referenced by the Next.js app.
- The API service uses `NEXT_PUBLIC_API_URL` for backend communication.
- UI and backend logic are extensible; replace simulated chat with real backend responses as needed.
- For local development, ensure your backend is running and accessible at the URL specified in `.env.local`.

## License

MIT License