import { useEffect, useState } from "react";
import { ArrowLeft, BarChart3, Info, Factory, Activity, ZoomIn } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { motion, AnimatePresence } from "framer-motion";

interface Forecast {
  title: string;
  src: string;
}

interface PredictionsPageProps {
  onNavigate: (page: "home" | "predictions" | "calculator") => void;
}

export default function PredictionsPage({ onNavigate }: PredictionsPageProps) {
  const [forecasts, setForecasts] = useState<Forecast[]>([]);
  const [loading, setLoading] = useState(true);
  const [zoomed, setZoomed] = useState<string | null>(null);
  const BACKEND_URL = "http://127.0.0.1:5000";

  useEffect(() => {
    const fetchForecasts = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/forecasts`);
        const data = await res.json();
        setForecasts(data);
      } catch (err) {
        console.error("Error fetching forecasts:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchForecasts();
  }, []);

  const getDescription = (title: string) => {
    if (title.includes("Cluster 0"))
      return `Cluster 0 (RSP + ISP) shows strong downward energy consumption trends.
      The forecast indicates consistent efficiency gains driven by modernization, slag reuse,
      and process automation.`;
    if (title.includes("Cluster 1"))
      return `Cluster 1 (BSP + DSP + BSL + SAIL) exhibits steady improvements with moderate slope reduction.
      The model predicts further gains as renewable projects and AI-driven monitoring expand.`;
    if (title.includes("All Plants"))
      return `This aggregate forecast represents the national steel energy consumption trend.
      It combines data across all SAIL plants using hybrid ARIMA + LSTM, revealing an overall efficiency improvement of 10–15% over 5 years.`;
    if (title.includes("Comparison"))
      return `Cluster 0 outperforms Cluster 1 in energy efficiency improvement rate.
      The gap highlights modernization benefits and targeted sustainability strategies for older plants.`;
    if (title.includes("RSP"))
      return `Rourkela Steel Plant (RSP) has achieved significant reductions due to process optimization,
      digital twins, and waste-heat recovery projects.`;
    if (title.includes("ISP"))
      return `IISCO Steel Plant (ISP) maintains one of the lowest energy intensities, 
      backed by 100% slag reuse and high-capacity furnaces.`;
    if (title.includes("BSP"))
      return `Bhilai Steel Plant (BSP) shows gradual improvements, reflecting the effect of floating solar plants and green fuel adoption.`;
    if (title.includes("DSP"))
      return `Durgapur Steel Plant (DSP) demonstrates moderate progress — recent investments in LED lighting and wastewater systems have measurable energy benefits.`;
    if (title.includes("BSL"))
      return `Bokaro Steel Plant (BSL) continues to enhance its flat-product line energy profile through internal recycling and steam recovery units.`;
    if (title.includes("SAIL"))
      return `SAIL Average forecast shows a macro-level decline in energy use, 
      suggesting successful group-wide sustainability measures across all integrated plants.`;
    return `This forecast reflects modeled energy efficiency using ARIMA + LSTM hybrid learning.`;
  };

  // 🔹 NEW: plant-specific optimization recommendations
  const getRecommendations = (title: string) => {
    if (title.includes("Cluster 0"))
      return [
        "Scale up real-time process monitoring and anomaly detection for blast furnaces and BOFs.",
        "Deepen digitization (digital twins, predictive maintenance) to lock in current efficiency gains.",
        "Expand slag granulation and waste-heat recovery to secondary units and auxiliaries.",
      ];
    if (title.includes("Cluster 1"))
      return [
        "Prioritize capex for retrofitting older furnaces with modern control systems and better refractories.",
        "Accelerate renewable integration (solar, green power PPAs) for auxiliary loads.",
        "Introduce AI-based maintenance scheduling to reduce unplanned outages and energy spikes.",
      ];
    if (title.includes("All Plants"))
      return [
        "Standardize an enterprise-wide energy KPI dashboard across all plants for comparability and benchmarking.",
        "Roll out unified best-practice playbooks on air leakage control, combustion tuning, and waste-heat reuse.",
        "Tie part of management KPIs to specific Gcal/tcs reduction targets over the next 3–5 years.",
      ];
    if (title.includes("Comparison"))
      return [
        "Use Cluster 0 as a benchmark lab to pilot advanced optimization (digital twins, process AI) before scaling to Cluster 1.",
        "Identify specific process gaps where Cluster 1 deviates most from Cluster 0 and prioritize focused improvement sprints.",
        "Design targeted training programs so operating teams can adopt Cluster 0’s best practices faster.",
      ];
    if (title.includes("RSP"))
      return [
        "Further optimize coke rate and hot blast temperature using tighter furnace control loops.",
        "Extend digital twin coverage to secondary steel-making and rolling mills for end-to-end optimization.",
        "Integrate more granular energy metering at shop-level to isolate and fix micro-inefficiencies.",
      ];
    if (title.includes("ISP"))
      return [
        "Leverage already low energy intensity by piloting near-real-time optimization (MPC / RL-based controllers).",
        "Push slag reuse to value-added products (cement-grade, road material) to offset energy costs.",
        "Benchmark ISP’s operating windows and share as best practices across all SAIL plants.",
      ];
    if (title.includes("BSP"))
      return [
        "Optimize the interface between solar generation and plant loads to minimize curtailment and grid draw.",
        "Retrofit older mills with variable frequency drives (VFDs) and high-efficiency motors.",
        "Focus on reducing rework and rejects, which indirectly increase specific energy consumption.",
      ];
    if (title.includes("DSP"))
      return [
        "Complement lighting and utilities upgrades with process-level optimization in reheating furnaces.",
        "Introduce heat recovery from flue gases for preheating combustion air and charge materials.",
        "Implement strict leak-detection and repair (steam, compressed air, water) campaigns.",
      ];
    if (title.includes("BSL"))
      return [
        "Strengthen closed-loop control around flat-product rolling schedules to reduce idle and transition losses.",
        "Scale internal recycling of process gases to displace fresh fuel consumption.",
        "Integrate steam recovery with a centralized monitoring dashboard to catch underperforming units.",
      ];
    if (title.includes("SAIL"))
      return [
        "Create a central energy excellence cell to coordinate projects, funding, and technology transfer across plants.",
        "Adopt uniform measurement & verification (M&V) protocols so savings from each project are trackable and auditable.",
        "Plan long-term fuel mix transitions (natural gas, hydrogen-readiness) aligned with national decarbonization goals.",
      ];

    // Generic default
    return [
      "Install or upgrade high-resolution energy metering at critical process stages.",
      "Use the ARIMA + LSTM forecasts as baselines to quantify the impact of upcoming energy projects.",
      "Continuously retrain the model with fresh data to detect drifts in process behavior and emerging inefficiencies.",
    ];
  };

  const getTechnicalInfo = (title: string) => {
    return (
      <>
        <p className="text-xs text-muted-foreground">
          <strong>📊 Model Used:</strong> Hybrid ARIMA + LSTM — combining statistical linearity with non-linear temporal memory.  
        </p>
        <p className="text-xs text-muted-foreground">
          <strong>📅 Forecast Horizon:</strong> Next 5 years (2025–2030)
        </p>
        <p className="text-xs text-muted-foreground">
          <strong>⚙️ Data:</strong> Annual Energy Consumption (Gcal/tcs) aggregated by plant
        </p>
        <p className="text-xs text-muted-foreground">
          <strong>🔍 Key Insight:</strong> {getDescription(title)}
        </p>
      </>
    );
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <div className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onNavigate("home")}
              className="text-muted-foreground hover:text-foreground"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-2xl md:text-3xl font-serif font-bold text-foreground">
                Static Forecasts
              </h1>
              <p className="text-sm text-muted-foreground">
                Forecasts derived from ARIMA + LSTM hybrid models across Indian steel plants
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-sm text-muted-foreground">
              Connected to Flask
            </span>
          </div>
        </div>
      </div>

      {/* Forecasts */}
      <div className="container mx-auto px-4 py-10 space-y-10">
        {loading ? (
          <p className="text-center text-muted-foreground animate-pulse">
            Loading forecasts...
          </p>
        ) : (
          forecasts.map((forecast, idx) => (
            <Card
              key={idx}
              className="border-border bg-card/60 backdrop-blur-sm hover:shadow-md transition-all"
            >
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-primary" />
                  {forecast.title}
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Smaller Graph with Zoom Button */}
                <div className="relative flex justify-center">
                  <img
                    src={forecast.src}
                    alt={forecast.title}
                    className="rounded-md border border-border shadow-sm w-3/4 max-h-[300px] object-contain cursor-pointer transition-transform hover:scale-[1.02]"
                    onClick={() => setZoomed(forecast.src)}
                    title="Click to zoom"
                  />
                  <button
                    onClick={() => setZoomed(forecast.src)}
                    className="absolute bottom-3 right-8 bg-primary/80 hover:bg-primary text-white p-2 rounded-full shadow-md"
                    title="Zoom in"
                  >
                    <ZoomIn className="w-4 h-4" />
                  </button>
                </div>

                {/* Info Box */}
                <div className="flex items-start gap-3 bg-muted/20 border border-border p-4 rounded-lg">
                  <Info className="w-5 h-5 text-accent mt-1" />
                  <div className="text-sm leading-relaxed text-muted-foreground">
                    {getDescription(forecast.title)}
                  </div>
                </div>

                {/* Technical Info + Recommendations */}
                <div className="bg-muted/10 border border-border p-4 rounded-lg space-y-3">
                  {getTechnicalInfo(forecast.title)}
                  <div className="flex items-center gap-2 text-xs text-muted-foreground mt-2">
                    <Activity className="w-4 h-4 text-chart-3" />
                    <span>
                      Data preprocessed using MinMaxScaler and trained over
                      300 epochs with LSTM (sequence length = 5)
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Factory className="w-4 h-4 text-chart-4" />
                    <span>
                      Forecast validated against real energy efficiency trends
                      from SAIL’s 5 integrated steel plants
                    </span>
                  </div>

                  {/* 🔹 NEW: Plant-specific optimization recommendations */}
                  <div className="mt-3 border-t border-border/60 pt-3">
                    <p className="text-xs font-semibold text-foreground mb-1">
                      🎯 Plant-Specific Optimization Recommendations
                    </p>
                    <ul className="list-disc list-inside space-y-1 text-xs text-muted-foreground">
                      {getRecommendations(forecast.title).map((rec, i) => (
                        <li key={i}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Fullscreen Zoom Overlay */}
      <AnimatePresence>
        {zoomed && (
          <motion.div
            className="fixed inset-0 bg-black/85 flex items-center justify-center z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setZoomed(null)}
          >
            <motion.img
              src={zoomed}
              alt="Zoomed Forecast"
              className="max-h-[90vh] max-w-[90vw] rounded-lg shadow-2xl border border-border"
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
