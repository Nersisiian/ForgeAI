import { useState } from 'react';
import { Box, TextField, MenuItem, Typography, Alert } from '@mui/material';
import LoadingButton from '../common/LoadingButton';
import api from '../../services/api';

const TARGET_TYPES = [
  { value: 'fastapi', label: 'FastAPI' },
  { value: 'django', label: 'Django' },
  { value: 'telegram_bot', label: 'Telegram Bot' },
  { value: 'discord_bot', label: 'Discord Bot' },
  { value: 'cli', label: 'CLI Tool' },
  { value: 'desktop', label: 'Desktop Application' },
  { value: 'rest_api', label: 'REST API' },
  { value: 'microservice', label: 'Microservice' },
];

interface ProjectFormProps {
  onSuccess?: (projectId: string) => void;
  initialValues?: {
    name: string;
    description: string;
    natural_language_query: string;
    target_type: string;
  };
  isEdit?: boolean;
  projectId?: string;
}

export default function ProjectForm({ onSuccess, initialValues, isEdit = false, projectId }: ProjectFormProps) {
  const [name, setName] = useState(initialValues?.name || '');
  const [description, setDescription] = useState(initialValues?.description || '');
  const [query, setQuery] = useState(initialValues?.natural_language_query || '');
  const [target, setTarget] = useState(initialValues?.target_type || 'fastapi');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !query.trim()) {
      setError('Name and query are required.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const payload = {
        name: name.trim(),
        description: description.trim() || undefined,
        natural_language_query: query.trim(),
        target_type: target,
      };
      if (isEdit && projectId) {
        await api.put(`/api/v1/projects/${projectId}`, payload);
        onSuccess?.(projectId);
      } else {
        const response = await api.post('/api/v1/projects/', payload);
        onSuccess?.(response.data.id);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Operation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <TextField
        fullWidth
        label="Project Name"
        value={name}
        onChange={e => setName(e.target.value)}
        required
        margin="normal"
        inputProps={{ maxLength: 255 }}
      />
      <TextField
        fullWidth
        label="Description (optional)"
        value={description}
        onChange={e => setDescription(e.target.value)}
        margin="normal"
        multiline
        rows={2}
      />
      <TextField
        fullWidth
        label="Natural Language Query"
        value={query}
        onChange={e => setQuery(e.target.value)}
        required
        multiline
        rows={4}
        margin="normal"
        helperText="Describe the software you want to generate in plain English."
      />
      <TextField
        select
        fullWidth
        label="Target Type"
        value={target}
        onChange={e => setTarget(e.target.value)}
        margin="normal"
      >
        {TARGET_TYPES.map(t => (
          <MenuItem key={t.value} value={t.value}>{t.label}</MenuItem>
        ))}
      </TextField>
      <LoadingButton
        type="submit"
        variant="contained"
        fullWidth
        sx={{ mt: 3 }}
        loading={loading}
        disabled={loading}
      >
        {isEdit ? 'Update Project' : 'Generate Project'}
      </LoadingButton>
    </Box>
  );
}