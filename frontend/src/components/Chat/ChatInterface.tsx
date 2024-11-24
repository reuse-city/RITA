import React, { useState } from 'react'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([])
  const [input, setInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    setMessages(prev => [...prev, { text: input, isUser: true }])
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      })
      
      const data = await response.json()
      
      // Add assistant message
      setMessages(prev => [...prev, { text: data.response, isUser: false }])
    } catch (error) {
      setMessages(prev => [...prev, { 
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false 
      }])
    }

    setInput('')
  }

  return (
    <div className="h-screen flex flex-col">
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-4 ${msg.isUser ? 'text-right' : 'text-left'}`}
          >
            <div
              className={`inline-block p-2 rounded-lg ${
                msg.isUser ? 'bg-blue-500 text-white' : 'bg-gray-200'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 p-2 border rounded-l"
            placeholder="Type your message..."
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-r"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  )
}
