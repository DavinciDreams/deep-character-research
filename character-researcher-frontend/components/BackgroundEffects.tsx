import React, { useEffect, useRef } from 'react';

const BackgroundEffects: React.FC = () => {
  const starsCanvasRef = useRef<HTMLCanvasElement>(null);
  const requestIdRef = useRef<number | null>(null);

  useEffect(() => {
    const canvas = starsCanvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const setCanvasDimensions = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    setCanvasDimensions();
    window.addEventListener('resize', setCanvasDimensions);

    class Star {
      x: number;
      y: number;
      size: number;
      speed: number;
      brightness: number;
      opacity: number;
      twinkleSpeed: number;

      constructor(canvas: HTMLCanvasElement) {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 1.5 + 0.5;
        this.speed = Math.random() * 0.05 + 0.01;
        this.brightness = Math.random() * 50 + 50;
        this.opacity = Math.random() * 0.5 + 0.5;
        this.twinkleSpeed = Math.random() * 0.01 + 0.005;
      }

      update(ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) {
        this.y += this.speed;
        if (this.y > canvas.height) {
          this.y = 0;
          this.x = Math.random() * canvas.width;
        }
        this.opacity = Math.sin(Date.now() * this.twinkleSpeed) * 0.2 + 0.8;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
        ctx.fill();
      }
    }

    const stars: Star[] = [];
    const starCount = Math.min(window.innerWidth, window.innerHeight) / 3;

    for (let i = 0; i < starCount; i++) {
      stars.push(new Star(canvas));
    }

    const animate = () => {
      if (!ctx || !canvas) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach(star => star.update(ctx, canvas));
      requestIdRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (requestIdRef.current) {
        cancelAnimationFrame(requestIdRef.current);
      }
      window.removeEventListener('resize', setCanvasDimensions);
    };
  }, []);

  return (
    <div className="background-effects">
      <canvas ref={starsCanvasRef} className="stars-canvas"></canvas>
      <div className="vignette-overlay"></div>
      <div className="noise-overlay"></div>
    </div>
  );
};

export default BackgroundEffects;