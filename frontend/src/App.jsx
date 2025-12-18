import { useState, useRef, useEffect } from 'react'
import AgentTracker from './components/AgentTracker'
import { Send, ShieldCheck, FileText, Download } from 'lucide-react' // Ensure you have lucide-react installed

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am the Agentic Loan Orchestrator. How can I assist you with a loan today?' }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // Agent State
  const [currentStage, setCurrentStage] = useState('sales')
  const [sanctionLetter, setSanctionLetter] = useState(null)

  // Session ID
  const sessionIdRef = useRef(`demo-${Math.floor(Math.random() * 10000)}`)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage = inputText
    setMessages(prev => [...prev, { sender: 'user', text: userMessage }])
    setInputText('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionIdRef.current,
          message: userMessage
        }),
      })

      if (!response.ok) throw new Error('Network response was not ok')
      const data = await response.json()

      // Update Chat
      setMessages(prev => [...prev, { sender: 'bot', text: data.reply }])

      // Update Stage
      if (data.stage) {
        setCurrentStage(data.stage)
      } else {
        // Fallback Logic
        const lowerReply = data.reply.toLowerCase()
        if (lowerReply.includes("sanction")) setCurrentStage('sanction')
        else if (lowerReply.includes("verify") || lowerReply.includes("pan")) setCurrentStage('verification')
        else if (lowerReply.includes("approve") || lowerReply.includes("eligib")) setCurrentStage('underwriting')
      }

      // Handle Sanction Letter
      if (data.sanction_letter) {
        setSanctionLetter(data.sanction_letter)
      } else if (data.loan_details && data.stage === 'sanction') {
        setSanctionLetter({ file: `sanction_${sessionIdRef.current}.pdf`, ...data.loan_details })
      }

    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, connection error. Is the backend running?' }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSendMessage()
  }

  return (
    <div className="flex h-screen w-full bg-slate-50 font-sans overflow-hidden">
      
      {/* --- LEFT SIDE: CHAT INTERFACE (65%) --- */}
      <div className="flex-1 flex flex-col h-full bg-white relative">
        
        {/* Header */}
        <header className="px-6 py-4 bg-white border-b border-slate-100 flex items-center justify-between shadow-sm z-10">
            <div className="flex items-center gap-3">
                <div className="bg-blue-600 p-2 rounded-lg text-white">
                    <ShieldCheck size={24} />
                </div>
                <div>
                    <h1 className="font-bold text-slate-800 text-lg leading-tight">LoanOps AI</h1>
                    <p className="text-xs text-slate-500 flex items-center gap-1">
                        <span className="w-2 h-2 rounded-full bg-green-500"></span> Online • Secure
                    </p>
                </div>
            </div>
            <div className="text-right">
                <span className="text-[10px] text-slate-400 font-mono block">SESSION ID</span>
                <span className="text-xs font-mono text-slate-600">{sessionIdRef.current}</span>
            </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/50">
            {messages.map((msg, index) => (
                <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`flex flex-col max-w-[80%] ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                        {/* Bubble */}
                        <div className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
                            msg.sender === 'user' 
                                ? 'bg-blue-600 text-white rounded-br-none' 
                                : 'bg-white border border-slate-200 text-slate-700 rounded-bl-none'
                        }`}>
                            <div style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</div>
                        </div>
                        <span className="text-[10px] text-slate-400 mt-1 px-1">
                            {msg.sender === 'user' ? 'You' : 'LoanOps Agent'}
                        </span>
                    </div>
                </div>
            ))}

            {/* Loading Animation */}
            {isLoading && (
                <div className="flex justify-start">
                    <div className="bg-white border border-slate-200 px-4 py-3 rounded-2xl rounded-bl-none shadow-sm flex items-center gap-2">
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-.3s]" />
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-.5s]" />
                    </div>
                </div>
            )}
            
            {/* Sanction Letter Card */}
            {sanctionLetter && (
                <div className="flex justify-start animate-fade-in-up">
                    <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-4 shadow-sm w-full max-w-sm">
                        <div className="flex items-center gap-4 mb-3">
                            <div className="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600">
                                <FileText size={20} />
                            </div>
                            <div>
                                <h3 className="text-sm font-bold text-emerald-900">Loan Sanctioned</h3>
                                <p className="text-xs text-emerald-700">Ready for download</p>
                            </div>
                        </div>
                        <button 
                            onClick={() => alert(`Downloading ${sanctionLetter.file}...`)}
                            className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg flex items-center justify-center gap-2 transition-colors"
                        >
                            <Download size={14} /> Download PDF
                        </button>
                    </div>
                </div>
            )}
            
            <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-slate-200">
            <div className="flex gap-2 max-w-3xl mx-auto">
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message..."
                    className="flex-1 bg-slate-100 text-slate-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/20 border border-transparent focus:border-blue-500 transition-all text-sm"
                    disabled={isLoading}
                />
                <button 
                    onClick={handleSendMessage}
                    disabled={isLoading || !inputText.trim()}
                    className="bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 text-white p-3 rounded-xl transition-colors"
                >
                    <Send size={20} />
                </button>
            </div>
        </div>
      </div>

      {/* --- RIGHT SIDE: AGENT TRACKER (35%) --- */}
      <div className="w-[35%] hidden md:block h-full shadow-2xl z-20">
        <AgentTracker currentStage={currentStage} />
      </div>

    </div>
  )
}

export default App