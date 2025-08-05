import type { AppProps } from 'next/app';
import '../styles/app.css';
import '../styles/backgroundEffects.css';
import '../styles/chatInterface.css';
import '../styles/figureCard.css';
import '../styles/historicalFigureGallery.css';
import '../styles/portalVortex.css';
import '../styles/timePortal.css';
import '../index.css';
 
function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
 
export default MyApp;