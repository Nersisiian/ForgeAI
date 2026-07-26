import { useState } from 'react'
import { Container, TextField, Typography, Box, Link } from '@mui/material'
import LoadingButton from '../components/common/LoadingButton'
import { useAuth } from '../hooks/useAuth'
import { useNavigate, Link as RouterLink } from 'react-router-dom'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await register(email, password, name)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5">Sign up</Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField margin="normal" fullWidth label="Full Name" value={name} onChange={e => setName(e.target.value)} />
          <TextField margin="normal" fullWidth label="Email" value={email} onChange={e => setEmail(e.target.value)} required />
          <TextField margin="normal" fullWidth label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          {error && <Typography color="error">{error}</Typography>}
          <LoadingButton type="submit" fullWidth variant="contained" sx={{ mt: 2 }} loading={loading}>
            Sign Up
          </LoadingButton>
          <Link component={RouterLink} to="/login" variant="body2" sx={{ mt: 1 }}>Already have an account? Sign in</Link>
        </Box>
      </Box>
    </Container>
  )
}