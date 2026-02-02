import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  Upload,
  Factory,
  BarChart3,
  ZoomIn,
  Info,
  Activity,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import toast from "react-hot-toast";

// ✅ Import the same animated background used in HomePage
import Background from "../components/ui/Background";

interface CalculatorPageProps {
  onNavigate: (page: "home" | "predictions" | "calculator") => void;
}

export default function CalculatorPage({ onNavigate }: CalculatorPageProps) {
  const [file, setFile] = useState<File | null>(null);
  const [plant, setPlant] = useState("");
  const [resultMsg, setResultMsg] = useState("");
  const [plotPath, setPlotPath] = useState("");
  const [zoomed, setZoomed] = useState<string | null>(null);
  const BACKEND_URL = "http://127.0.0.1:5000";

  const handleSubmit = async () => {
    if (!file || !plant) {
      toast.error("Please select both a CSV file and a plant.");
      return;
    }

    const formData = new FormData();
    formData.append("csv_file", file);
    formData.append("plant", plant);

    try {
      toast.loading("Running forecast...", { id: "load" });
      const res = await fetch(`${BACKEND_URL}/`, { method: "POST", body: formData });
      const data = await res.json();
      if (data.error) {
        toast.error(data.error, { id: "load" });
        return;
      }
      setResultMsg(data.message);
      setPlotPath(data.image);
      toast.success("Forecast generated successfully!", { id: "load" });
    } catch {
      toast.error("Error connecting to Flask.", { id: "load" });
    }
  };

  return (
    <Background> {/* ✅ Wrap entire content inside Background */}
      <div className="min-h-screen relative overflow-hidden text-foreground">
        {/* Header */}
        <div className="border-b border-border bg-card/60 backdrop-blur-md sticky top-0 z-10">
          <div className="container mx-auto px-4 py-4 flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onNavigate("home")}
              className="text-muted-foreground hover:text-foreground"
            >
              <ArrowLeft className="w-4 h-4 mr-2" /> Back
            </Button>
            <h1 className="text-2xl md:text-3xl font-serif font-bold text-foreground">
              Upload & Predict Forecasts
            </h1>
          </div>
        </div>

        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="container mx-auto px-4 py-12 max-w-3xl space-y-8"
        >
          <Card className="border-border bg-card/70 backdrop-blur-sm hover:shadow-lg transition-all">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-foreground">
                <Upload className="w-5 h-5 text-primary" /> Upload Dataset
              </CardTitle>
              <CardDescription>
                Upload your plant CSV data and select a plant to generate forecasts.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label htmlFor="csv">CSV File</Label>
                <Input id="csv" type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
              </div>
              <div>
                <Label htmlFor="plant">Select Plant</Label>
                <select
                  id="plant"
                  value={plant}
                  onChange={(e) => setPlant(e.target.value)}
                  className="w-full p-2 border border-border rounded-md bg-background text-foreground"
                >
                  <option value="">-- Choose a Plant --</option>
                  <option value="RSP">RSP</option>
                  <option value="ISP">ISP</option>
                  <option value="BSP">BSP</option>
                  <option value="DSP">DSP</option>
                  <option value="BSL">BSL</option>
                  <option value="SAIL">SAIL</option>
                  <option value="All Plants Avg">All Plants Avg</option>
                </select>
              </div>
              <Button onClick={handleSubmit} className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
                <BarChart3 className="w-4 h-4 mr-2" /> Run Forecast
              </Button>
            </CardContent>
          </Card>

          {/* Forecast Result */}
          {resultMsg && (
            <Card className="border-border bg-card/70 backdrop-blur-sm hover:shadow-lg transition-all">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-foreground">
                  <Factory className="w-5 h-5 text-accent" /> Forecast Result
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-muted-foreground" dangerouslySetInnerHTML={{ __html: resultMsg }} />
                {plotPath && (
                  <div className="relative flex justify-center">
                    <img
                      src={plotPath}
                      alt="Forecast"
                      className="rounded-md border border-border shadow-md w-3/4 max-h-[350px] object-contain cursor-pointer transition-transform hover:scale-[1.02]"
                      onClick={() => setZoomed(plotPath)}
                      title="Click to zoom"
                    />
                    <button
                      onClick={() => setZoomed(plotPath)}
                      className="absolute bottom-3 right-10 bg-primary/80 hover:bg-primary text-white p-2 rounded-full shadow-md"
                      title="Zoom in"
                    >
                      <ZoomIn className="w-4 h-4" />
                    </button>
                  </div>
                )}
                <div className="flex items-start gap-3 bg-muted/20 border border-border p-4 rounded-lg mt-6">
                  <Info className="w-5 h-5 text-accent mt-1" />
                  <div className="text-sm leading-relaxed text-muted-foreground">
                    <p>
                      The forecast above was generated using a <strong>Hybrid ARIMA + LSTM</strong> model that learns both
                      linear and non-linear energy trends.
                    </p>
                    <p className="mt-2">
                      Data was normalized using <strong>MinMaxScaler</strong>, trained for 300 epochs, and evaluated over
                      5-year sequences to predict future Gcal/tcs values.
                    </p>
                    <p className="mt-2">
                      The orange region marks the predicted period, and values are connected smoothly to represent
                      continuous plant performance.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </motion.div>

        {/* Zoom Overlay */}
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
    </Background> // ✅ End background wrapper
  );
}
