import { Typography, Button, Container } from '@mui/material'
import { useNavigate } from 'react-router-dom'

export default function NotFoundPage() {
  const navigate = useNavigate()
  return (
    <Container sx={{ textAlign: 'center', mt: 8 }}>
      <Typography variant="h2">404</Typography>
      <Typography variant="h5" gutterBottom>Page not found</Typography>
      <Button variant="contained" onClick={() => navigate('/')}>Go to Dashboard</Button>
    </Container>
  )
}