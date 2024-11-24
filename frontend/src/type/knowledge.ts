// frontend/src/types/knowledge.ts
export interface Source {
  id: number;
  name: string;
  url: string;
  description?: string;
  type: string;
  license_type: string;
  created_at: string;
}

export interface Guide {
  id: number;
  title: string;
  description?: string;
  device_type: string;
  difficulty_level?: string;
  time_estimate?: string;
  source_id: number;
  author: string;
  license: string;
  created_at: string;
  updated_at: string;
}
