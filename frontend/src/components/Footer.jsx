import { motion } from "framer-motion"

const LINKEDIN = "https://www.linkedin.com/in/aryan-sadvelkar-510555311/"
const EMAIL = "aryan.sadvelkar@gmail.com"

export default function Footer() {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.5 }}
      className="relative z-10 mt-auto border-t border-slate-700/60 bg-gradient-to-b from-transparent to-slate-900/60 backdrop-blur-sm"
    >
      <div className="max-w-5xl mx-auto px-6 py-10">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-8">
          <div className="text-center sm:text-left">
            <p className="text-base font-semibold text-white">
              Created by{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-violet-400">
                Aryan Sadvelkar
              </span>
            </p>
            <p className="text-xs text-slate-500 mt-1">CodePulse · AI-powered repository insights</p>
          </div>
          <div className="flex items-center gap-8">
            <a
              href={LINKEDIN}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2.5 px-4 py-2.5 rounded-lg text-slate-400 hover:text-[#0a66c2] hover:bg-slate-800/60 transition-all"
            >
              <svg className="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
              </svg>
              <span className="text-sm font-medium">LinkedIn</span>
            </a>
            <a
              href={`mailto:${EMAIL}`}
              className="flex items-center gap-2.5 px-4 py-2.5 rounded-lg text-slate-400 hover:text-indigo-400 hover:bg-slate-800/60 transition-all"
            >
              <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span className="text-sm font-medium hidden sm:inline">{EMAIL}</span>
            </a>
          </div>
        </div>
      </div>
    </motion.footer>
  )
}
