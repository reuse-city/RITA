// frontend/src/components/Chat/ChatInterface.tsx
import React, { useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface ChatResponse {
  response: string;
  error: string | null;
}

export default function ChatInterface() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: message,
          role: 'user'
        }),
      });

      const data: ChatResponse = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResponse(data.response);
        setMessage(''); // Clear input after successful send
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      
      {response && (
        <div className="mb-4 p-4 bg-gray-100 rounded-lg">
          <p>{response}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full p-2 border rounded-md"
            placeholder="Type your message..."
            rows={4}
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded-md disabled:opacity-50"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}
