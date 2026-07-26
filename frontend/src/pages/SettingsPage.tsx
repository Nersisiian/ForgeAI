import { useState, useEffect } from 'react'
import { Typography, TextField, Button, Box } from '@mui/material'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'

export default function SettingsPage() {
  const { user } = useAuth()
  const [name, setName] = useState(user?.full_name || '')
  const [message, setMessage] = useState('')

  const handleUpdate = async () => {
    try {
      await api.put('/api/v1/users/me', { full_name: name })
      setMessage('Profile updated')
    } catch {
      setMessage('Update failed')
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Settings</Typography>
      <TextField label="Full Name" value={name} onChange={e => setName(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" onClick={handleUpdate} sx={{ mt: 1 }}>Save</Button>
      {message && <Typography sx={{ mt: 1 }}>{message}</Typography>}
    </Box>
  )
}