import { motion } from "framer-motion";

export default function Background({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-[#0b0b0b] via-[#1a1a1a] to-[#2a2a2a]">
      <motion.div
        className="absolute inset-0 bg-[url('/steel-texture.jpg')] bg-cover bg-center opacity-20"
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.2 }}
        transition={{ duration: 2 }}
      />
      <div className="relative z-10">{children}</div>
    </div>
  );
}
