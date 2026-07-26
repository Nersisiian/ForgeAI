import { Paper, Typography } from '@mui/material'

interface StatsCardProps {
  title: string
  value: number
  color?: string
}

export default function StatsCard({ title, value, color }: StatsCardProps) {
  return (
    <Paper sx={{ p: 2, textAlign: 'center', borderLeft: 4, borderColor: color || 'primary.main' }}>
      <Typography variant="h6">{title}</Typography>
      <Typography variant="h3">{value}</Typography>
    </Paper>
  )
}