import { Box, Typography } from '@mui/material'

export default function Footer() {
  return (
    <Box component="footer" sx={{ py: 2, textAlign: 'center', mt: 'auto' }}>
      <Typography variant="body2" color="text.secondary">
        © {new Date().getFullYear()} Python Auto Company
      </Typography>
    </Box>
  )
}