import { useEffect, useState } from 'react'
import { Grid, Typography, Box } from '@mui/material'
import api from '../services/api'
import StatsCard from '../components/dashboard/StatsCard'
import RecentProjects from '../components/dashboard/RecentProjects'

export default function DashboardPage() {
  const [projects, setProjects] = useState<any[]>([])
  const [stats, setStats] = useState({ total: 0, generating: 0, completed: 0 })

  useEffect(() => {
    api.get('/api/v1/projects/').then(res => {
      setProjects(res.data.items || [])
      const generating = res.data.items.filter((p: any) => p.status === 'generating').length
      const completed = res.data.items.filter((p: any) => p.status === 'completed').length
      setStats({ total: res.data.total, generating, completed })
    })
  }, [])

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={4}><StatsCard title="Total Projects" value={stats.total} /></Grid>
        <Grid item xs={12} md={4}><StatsCard title="In Progress" value={stats.generating} color="warning" /></Grid>
        <Grid item xs={12} md={4}><StatsCard title="Completed" value={stats.completed} color="success" /></Grid>
      </Grid>
      <RecentProjects projects={projects.slice(0, 5)} />
    </Box>
  )
}
