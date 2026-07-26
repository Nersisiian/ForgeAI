import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Typography, Box, Tabs, Tab, Paper } from '@mui/material'
import api from '../services/api'
import TaskProgress from '../components/project/TaskProgress'
import LogViewer from '../components/project/LogViewer'
import ArtifactTree from '../components/project/ArtifactTree'
import { useProjectWebSocket } from '../hooks/useWebSocket'

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [project, setProject] = useState<any>(null)
  const [tab, setTab] = useState(0)
  const messages = useProjectWebSocket(id || null)

  useEffect(() => {
    if (id) {
      api.get(`/api/v1/projects/${id}`).then(res => setProject(res.data))
    }
  }, [id])

  if (!project) return <Typography>Loading...</Typography>

  return (
    <Box>
      <Typography variant="h4">{project.name}</Typography>
      <Typography color="text.secondary" gutterBottom>{project.target_type} - {project.status}</Typography>
      <Tabs value={tab} onChange={(_, v) => setTab(v)}>
        <Tab label="Progress" />
        <Tab label="Files" />
        <Tab label="Logs" />
      </Tabs>
      <Paper sx={{ mt: 2, p: 2 }}>
        {tab === 0 && <TaskProgress projectId={id!} wsMessages={messages} />}
        {tab === 1 && <ArtifactTree projectId={id!} />}
        {tab === 2 && <LogViewer messages={messages} />}
      </Paper>
    </Box>
  )
}