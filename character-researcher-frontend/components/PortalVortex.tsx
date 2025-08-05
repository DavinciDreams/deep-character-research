import React, { useRef, useEffect } from 'react';

interface PortalVortexProps {
  active: boolean;
  isSearching?: boolean;
}

const PortalVortex: React.FC<PortalVortexProps> = ({ active, isSearching }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const requestIdRef = useRef<number | null>(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const setCanvasDimensions = () => {
      const parent = canvas.parentElement;
      if (parent) {
        const size = Math.min(parent.offsetWidth, parent.offsetHeight) * 0.9;
        canvas.width = size;
        canvas.height = size;
      }
    };
    
    setCanvasDimensions();
    window.addEventListener('resize', setCanvasDimensions);
    
    class Particle {
      x: number;
      y: number;
      radius: number;
      color: string;
      angle: number;
      velocity: number;
      distance: number;
      
      constructor(canvas: HTMLCanvasElement) {
        this.x = canvas.width / 2;
        this.y = canvas.height / 2;
        this.radius = Math.random() * 2 + 1;
        
        const hue = Math.random() * 60 + 180;
        this.color = `hsl(${hue}, 100%, ${Math.random() * 20 + 60}%)`;
        
        this.angle = Math.random() * Math.PI * 2;
        this.velocity = (Math.random() * 2 + 0.5) * (active ? 1 : 0.2) * (isSearching ? 2 : 1);
        this.distance = Math.random() * (canvas.width / 4) + 5;
      }
      
      update(ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) {
        this.angle += this.velocity / 20;
        this.distance += this.velocity / 5;
        
        if (this.distance > canvas.width / 2) {
          this.x = canvas.width / 2;
          this.y = canvas.height / 2;
          this.distance = 0;
          this.angle = Math.random() * Math.PI * 2;
        } else {
          this.x = canvas.width / 2 + Math.cos(this.angle) * this.distance;
          this.y = canvas.height / 2 + Math.sin(this.angle) * this.distance;
        }
        
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        const trailLength = active ? (isSearching ? 30 : 20) : 5;
        ctx.lineTo(
          this.x - Math.cos(this.angle) * trailLength,
          this.y - Math.sin(this.angle) * trailLength
        );
        ctx.strokeStyle = this.color;
        ctx.globalAlpha = 0.3;
        ctx.lineWidth = this.radius / 2;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }
    }
    
    const particles: Particle[] = [];
    const particleCount = active ? (isSearching ? 300 : 200) : 50;
    
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle(canvas));
    }
    
    const animate = () => {
      if (!ctx || !canvas) return;
      
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach(particle => particle.update(ctx, canvas));
      
      const gradient = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 2, 0,
        canvas.width / 2, canvas.height / 2, canvas.width / 2
      );
      
      gradient.addColorStop(0, 'rgba(74, 238, 234, 0.3)');
      gradient.addColorStop(0.5, 'rgba(74, 238, 234, 0.1)');
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      requestIdRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (requestIdRef.current) {
        cancelAnimationFrame(requestIdRef.current);
      }
      window.removeEventListener('resize', setCanvasDimensions);
    };
  }, [active, isSearching]);
  
  return (
    <div className={`portal-vortex ${active ? 'active' : ''} ${isSearching ? 'searching' : ''}`}>
      <canvas ref={canvasRef} className="vortex-canvas"></canvas>
    </div>
  );
};

export default PortalVortex;