import React from 'react';
import { User, FileSearch, Calculator, FileCheck, Loader2, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

const steps = [
  { id: 'sales', label: 'Sales Agent', sub: 'Negotiating Terms', icon: User },
  { id: 'verification', label: 'Verification Agent', sub: 'KYC & Identity Check', icon: FileSearch },
  { id: 'underwriting', label: 'Underwriting Agent', sub: 'Risk Analysis & Scoring', icon: Calculator },
  { id: 'sanction', label: 'Sanction Generator', sub: 'Finalizing PDF', icon: FileCheck },
];

const AgentTracker = ({ currentStage }) => {
  // Helper to determine step status
  const getStatus = (stepId) => {
    // Normalize stage names to match IDs
    const current = (currentStage || 'sales').toLowerCase();
    const stepIds = steps.map(s => s.id);
    
    // Handle 'rejected' or final 'sanction' states
    if (current === 'rejected') {
        if (stepId === 'underwriting') return 'rejected';
        // If rejected at underwriting, previous steps are done
        const rejectIndex = stepIds.indexOf('underwriting');
        const stepIndex = stepIds.indexOf(stepId);
        return stepIndex < rejectIndex ? 'completed' : 'pending';
    }

    const currentIndex = stepIds.indexOf(current);
    const stepIndex = stepIds.indexOf(stepId);

    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'active';
    return 'pending';
  };

  return (
    <div className="h-full bg-slate-900 text-white p-6 border-l border-slate-800 flex flex-col font-sans shadow-2xl">
      {/* Header */}
      <div className="mb-8 flex items-center gap-3 border-b border-slate-700 pb-4">
        <div className="relative">
            <div className="absolute inset-0 bg-green-500 blur-sm opacity-50 animate-pulse"></div>
            <ActivityIcon className="relative z-10 text-green-400" size={24} />
        </div>
        <div>
            <h2 className="text-lg font-bold tracking-wider text-slate-100">ORCHESTRATOR</h2>
            <p className="text-xs text-slate-400 font-mono">LIVE AGENT SWARM</p>
        </div>
      </div>

      {/* Vertical Steps */}
      <div className="flex-1 space-y-8 relative pl-2">
        {/* Connector Line */}
        <div className="absolute left-6 top-4 bottom-20 w-0.5 bg-slate-800 z-0" />

        {steps.map((step) => {
          const status = getStatus(step.id);
          const Icon = step.icon;
          
          return (
            <motion.div 
                key={step.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
                className={`relative z-10 flex items-center gap-4 p-3 rounded-xl transition-all duration-300
                    ${status === 'active' ? 'bg-slate-800 border border-green-500/30 shadow-[0_0_15px_rgba(34,197,94,0.1)]' : 'border border-transparent'}
                    ${status === 'rejected' ? 'bg-red-900/20 border border-red-500/50' : ''}
                `}
            >
              {/* Icon Circle */}
              <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors duration-300
                ${status === 'active' ? 'bg-green-900/20 border-green-500 text-green-400' : ''}
                ${status === 'completed' ? 'bg-slate-800 border-slate-600 text-slate-500' : ''}
                ${status === 'pending' ? 'bg-slate-900 border-slate-700 text-slate-700' : ''}
                ${status === 'rejected' ? 'bg-red-900/20 border-red-500 text-red-500' : ''}
              `}>
                {status === 'active' ? <Loader2 className="animate-spin" size={18} /> : 
                 status === 'completed' ? <CheckCircle2 size={18} /> : 
                 status === 'rejected' ? <span>✕</span> :
                 <Icon size={18} />}
              </div>

              {/* Text Info */}
              <div>
                <h3 className={`font-bold text-sm ${status === 'active' ? 'text-green-400' : status === 'rejected' ? 'text-red-400' : 'text-slate-300'}`}>
                    {step.label}
                </h3>
                <p className="text-xs text-slate-500 font-mono">{step.sub}</p>
              </div>

              {/* Active Pulse */}
              {status === 'active' && (
                <span className="absolute right-3 top-3 flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Mock Terminal Output */}
      {/* FIXED: Replaced '>' with '&gt;' to fix JSX error */}
      <div className="mt-auto bg-black rounded-lg p-3 font-mono text-[10px] text-green-500/80 border border-slate-800 h-32 overflow-hidden shadow-inner">
        <p>&gt; System initialized...</p>
        <p>&gt; Session ID: {Math.random().toString(36).substr(2, 9)}</p>
        <p className="animate-pulse">&gt; Active Agent: {currentStage.toUpperCase()}_WORKER</p>
      </div>
    </div>
  );
};

const ActivityIcon = ({ className, size }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
);

export default AgentTracker;