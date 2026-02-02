import { useEffect, useState } from 'react';
import { ArrowRight, Factory, TrendingUp } from 'lucide-react';
import { Card } from '@/components/ui/card';

interface HomePageProps {
  onNavigate: (page: 'home' | 'predictions' | 'calculator') => void;
}

// Curated images of Indian steel plants and industrial scenes (Unsplash)
const steelImages = [
  // Tata Steel, Jamshedpur (India)
  'https://images.unsplash.com/photo-1571652639465-858b519a2542?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1920',
  // Indian city with factory skyline
  'https://images.unsplash.com/photo-1711553460847-172fea01f6e2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1920',
  // Factory beyond fields in India
  'https://images.unsplash.com/photo-1662958656945-746c5758f62d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1920',
  // Busy steelworks scene
  'https://images.unsplash.com/photo-1474674556023-efef886fa147?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1920',
  // Industrial steel production interior
  'https://images.unsplash.com/photo-1697281679290-ad7be1b10682?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1920',
];

export default function HomePage({ onNavigate }: HomePageProps) {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCurrent((i) => (i + 1) % steelImages.length);
    }, 6000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background slideshow */}
      <div className="absolute inset-0">
        {steelImages.map((src, i) => (
          <div
            key={i}
            className={`absolute inset-0 bg-center bg-cover transition-opacity duration-1000 ease-in-out ${i === current ? 'opacity-100' : 'opacity-0'}`}
            style={{ backgroundImage: `url(${src})` }}
          />
        ))}
        {/* Dark gradient and industrial pattern overlays for readability */}
        <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-background/70 to-background/80" />
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23DC4405' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
          }}
        />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16 animate-fade-in">
          <div className="flex items-center justify-center mb-6">
            <Factory className="w-16 h-16 text-primary" strokeWidth={1.5} />
          </div>
          <h1 className="text-6xl md:text-7xl font-serif font-bold text-foreground mb-4 tracking-tight">
            Steel Industry
            <span className="block text-primary mt-2">Insights India</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Comprehensive analytics and prediction tools for India's steel manufacturing sector
          </p>
        </div>

        {/* Navigation Cards */}
        <div className="grid md:grid-cols-2 gap-6 max-w-5xl w-full animate-slide-up">
          {/* Real Predictions Card */}
          <Card
            className="group relative overflow-hidden border-border hover:border-primary/50 transition-all duration-300 cursor-pointer bg-card/60 backdrop-blur-sm"
            onClick={() => onNavigate('predictions')}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            <div className="relative p-8">
              <div className="flex items-start justify-between mb-6">
                <div className="p-3 rounded-lg bg-primary/10 text-primary">
                  <TrendingUp className="w-8 h-8" />
                </div>
                <ArrowRight className="w-6 h-6 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all duration-300" />
              </div>

              <h2 className="text-3xl font-serif font-bold text-foreground mb-3">Real Predictions</h2>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Explore real-time data analytics and forecasting models based on historical steel industry performance across India
              </p>

              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium">Historical Data</span>
                <span className="px-3 py-1 rounded-full bg-accent/10 text-accent text-sm font-medium">Analytics</span>
                <span className="px-3 py-1 rounded-full bg-chart-3/10 text-chart-3 text-sm font-medium">Forecasts</span>
              </div>
            </div>
          </Card>

          {/* Predict Your Values Card */}
          <Card
            className="group relative overflow-hidden border-border hover:border-accent/50 transition-all duration-300 cursor-pointer bg-card/60 backdrop-blur-sm"
            onClick={() => onNavigate('calculator')}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-accent/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            <div className="relative p-8">
              <div className="flex items-start justify-between mb-6">
                <div className="p-3 rounded-lg bg-accent/10 text-accent">
                  <Factory className="w-8 h-8" />
                </div>
                <ArrowRight className="w-6 h-6 text-muted-foreground group-hover:text-accent group-hover:translate-x-1 transition-all duration-300" />
              </div>

              <h2 className="text-3xl font-serif font-bold text-foreground mb-3">Predict Your Values</h2>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Interactive prediction tool to calculate custom forecasts based on your specific steel production parameters
              </p>

              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 rounded-full bg-accent/10 text-accent text-sm font-medium">Interactive</span>
                <span className="px-3 py-1 rounded-full bg-chart-4/10 text-chart-4 text-sm font-medium">Prediction</span>
                <span className="px-3 py-1 rounded-full bg-chart-5/10 text-chart-5 text-sm font-medium">Fast</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Footer Info */}
        <div className="mt-16 text-center text-muted-foreground text-sm">
          <p>Powered by advanced analytics • Real-time industry data • Predictive modeling</p>
        </div>
      </div>
    </div>
  );
}
