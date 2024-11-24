// frontend/src/pages/admin/sources.tsx
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

interface Source {
  id?: number;
  name: string;
  url: string;
  description: string;
  type: string;
  license_type: string;
}

export default function SourceManagement() {
  const [sources, setSources] = useState<Source[]>([]);
  const [newSource, setNewSource] = useState<Source>({
    name: '',
    url: '',
    description: '',
    type: '',
    license_type: ''
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSources();
  }, []);

  const fetchSources = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/knowledge/sources');
      if (!response.ok) throw new Error('Failed to fetch sources');
      const data = await response.json();
      setSources(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch sources');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/v1/knowledge/sources', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSource),
      });

      if (!response.ok) throw new Error('Failed to add source');
      
      // Reset form and refresh list
      setNewSource({
        name: '',
        url: '',
        description: '',
        type: '',
        license_type: ''
      });
      fetchSources();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add source');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Manage Repair Knowledge Sources</h1>
      
      {/* Add new source form */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Add New Source</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              type="text"
              value={newSource.name}
              onChange={(e) => setNewSource({...newSource, name: e.target.value})}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">URL</label>
            <input
              type="url"
              value={newSource.url}
              onChange={(e) => setNewSource({...newSource, url: e.target.value})}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea
              value={newSource.description}
              onChange={(e) => setNewSource({...newSource, description: e.target.value})}
              className="w-full p-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Type</label>
            <select
              value={newSource.type}
              onChange={(e) => setNewSource({...newSource, type: e.target.value})}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Select type...</option>
              <option value="wiki">Wiki</option>
              <option value="guide">Guide</option>
              <option value="video">Video</option>
              <option value="community">Community</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">License</label>
            <select
              value={newSource.license_type}
              onChange={(e) => setNewSource({...newSource, license_type: e.target.value})}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Select license...</option>
              <option value="CC-BY">CC-BY</option>
              <option value="CC-BY-SA">CC-BY-SA</option>
              <option value="MIT">MIT</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Add Source
          </button>
        </form>
      </div>

      {/* Source list */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Current Sources</h2>
        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
          </div>
        )}
        <div className="space-y-4">
          {sources.map((source) => (
            <div key={source.id} className="border p-4 rounded">
              <h3 className="font-semibold">{source.name}</h3>
              <p className="text-sm text-gray-600">{source.description}</p>
              <div className="flex justify-between mt-2 text-sm">
                <span className="text-blue-600">{source.type}</span>
                <span className="text-gray-500">{source.license_type}</span>
              </div>
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline text-sm"
              >
                Visit Source
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
