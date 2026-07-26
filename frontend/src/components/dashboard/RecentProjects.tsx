import { Paper, Typography, List, ListItemButton, ListItemText, Chip } from '@mui/material'
import { useNavigate } from 'react-router-dom'

interface RecentProjectsProps {
  projects: any[]
}

export default function RecentProjects({ projects }: RecentProjectsProps) {
  const navigate = useNavigate()

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>Recent Projects</Typography>
      <List>
        {projects.map((proj) => (
          <ListItemButton key={proj.id} onClick={() => navigate(`/projects/${proj.id}`)}>
            <ListItemText primary={proj.name} secondary={proj.target_type} />
            <Chip label={proj.status} color={proj.status === 'completed' ? 'success' : 'warning'} size="small" />
          </ListItemButton>
        ))}
      </List>
    </Paper>
  )
}