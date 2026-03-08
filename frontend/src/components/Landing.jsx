import { motion } from "framer-motion"
import LandingScene from "./LandingScene"
import RepoInput from "./RepoInput"

export default function Landing({ onAnalyze, disabled }) {
  return (
    <>
      <LandingScene />
      <div className="relative z-10 flex flex-col items-center justify-center min-h-[72vh] px-4">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="text-center max-w-2xl"
        >
          <motion.h1
            className="text-5xl md:text-7xl font-bold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-indigo-400 drop-shadow-[0_0_40px_rgba(99,102,241,0.15)]"
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.15, duration: 0.6 }}
          >
            CodePulse
          </motion.h1>
          <motion.p
            className="text-lg md:text-xl text-slate-300 mb-2 font-medium"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.35 }}
          >
            AI-powered repository insights
          </motion.p>
          <motion.p
            className="text-sm text-slate-500 mb-12 max-w-md mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            Health score · Commit heatmap · Dependency graph · Architecture review
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="w-full max-w-xl mx-auto"
          >
            <RepoInput onAnalyze={onAnalyze} disabled={disabled} />
          </motion.div>
        </motion.div>
      </div>
    </>
  )
}
