import { useState, useEffect } from 'react'
import mermaid from 'mermaid'

// Initialize mermaid
mermaid.initialize({ startOnLoad: true })

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am the Agentic Loan Orchestrator. How can I assist you?' }
  ])

  const [graphDefinition, setGraphDefinition] = useState(`
    graph TD
    A[Start] --> B(Sales Agent)
    B --> C{Verified?}
    C -->|Yes| D[Underwriting]
    C -->|No| E[Reject]
    D --> F[Sanction Letter]
  `)

  useEffect(() => {
    mermaid.contentLoaded()
  }, [])

  return (
    <div className="flex h-screen w-screen bg-gray-100 overflow-hidden">
      {/* Left Panel: Chat */}
      <div className="w-1/2 flex flex-col border-r border-gray-300 bg-white">
        <header className="p-4 bg-blue-600 text-white font-bold text-lg shadow-md">
          Loan Assistant
        </header>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs p-3 rounded-lg shadow ${msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
                {msg.text}
              </div>
            </div>
          ))}
          {/* TODO: Connect to backend */}
        </div>

        <div className="p-4 border-t border-gray-200 bg-gray-50">
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="Type your message..." 
              className="flex-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled
            />
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-medium" disabled>
              Send
            </button>
          </div>
        </div>
      </div>

      {/* Right Panel: Workflow Visualization */}
      <div className="w-1/2 flex flex-col bg-slate-50">
        <header className="p-4 bg-slate-800 text-white font-bold text-lg shadow-md">
          Live Workflow State (Mermaid.js)
        </header>
        <div className="flex-1 flex items-center justify-center p-4 overflow-auto">
          <div className="mermaid">
            {graphDefinition}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
