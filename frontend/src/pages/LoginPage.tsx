import { useState } from 'react'
import { Container, TextField, Typography, Box, Link } from '@mui/material'
import LoadingButton from '../components/common/LoadingButton'
import { useAuth } from '../hooks/useAuth'
import { useNavigate, Link as RouterLink } from 'react-router-dom'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await login(email, password)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5">Sign in</Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField margin="normal" fullWidth label="Email" value={email} onChange={e => setEmail(e.target.value)} required />
          <TextField margin="normal" fullWidth label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          {error && <Typography color="error">{error}</Typography>}
          <LoadingButton type="submit" fullWidth variant="contained" sx={{ mt: 2 }} loading={loading}>
            Sign In
          </LoadingButton>
          <Link component={RouterLink} to="/register" variant="body2" sx={{ mt: 1 }}>Don't have an account? Sign Up</Link>
        </Box>
      </Box>
    </Container>
  )
}