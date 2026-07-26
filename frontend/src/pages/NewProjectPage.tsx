import { useState } from 'react'
import { Container, TextField, Typography, MenuItem, Box } from '@mui/material'
import LoadingButton from '../components/common/LoadingButton'
import api from '../services/api'
import { useNavigate } from 'react-router-dom'

const targetTypes = ['fastapi', 'django', 'telegram_bot', 'discord_bot', 'cli', 'desktop', 'rest_api', 'microservice']

export default function NewProjectPage() {
  const [name, setName] = useState('')
  const [query, setQuery] = useState('')
  const [target, setTarget] = useState('fastapi')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await api.post('/api/v1/projects/', {
        name,
        natural_language_query: query,
        target_type: target,
      })
      navigate(`/projects/${res.data.id}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create project')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>New Project</Typography>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField fullWidth label="Project Name" value={name} onChange={e => setName(e.target.value)} required margin="normal" />
        <TextField fullWidth label="Natural Language Description" value={query} onChange={e => setQuery(e.target.value)} required multiline rows={4} margin="normal"
          helperText="e.g., Create CRM for a dental clinic with appointment scheduling" />
        <TextField select fullWidth label="Target Type" value={target} onChange={e => setTarget(e.target.value)} margin="normal">
          {targetTypes.map(t => <MenuItem key={t} value={t}>{t.replace('_', ' ')}</MenuItem>)}
        </TextField>
        {error && <Typography color="error">{error}</Typography>}
        <LoadingButton type="submit" variant="contained" sx={{ mt: 2 }} loading={loading}>Generate Project</LoadingButton>
      </Box>
    </Container>
  )
}