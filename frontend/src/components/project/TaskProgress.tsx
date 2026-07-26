import { useEffect, useState } from 'react'
import { List, ListItem, ListItemText, LinearProgress, Typography } from '@mui/material'
import api from '../../services/api'

interface TaskProgressProps {
  projectId: string
  wsMessages: any[]
}

export default function TaskProgress({ projectId, wsMessages }: TaskProgressProps) {
  const [tasks, setTasks] = useState<any[]>([])

  useEffect(() => {
    api.get(`/api/v1/tasks/project/${projectId}`).then(res => setTasks(res.data))
  }, [projectId])

  useEffect(() => {
    // update tasks from ws messages (status changes)
    wsMessages.forEach(msg => {
      setTasks(prev => prev.map(t => t.id === msg.task_id ? { ...t, status: msg.status } : t))
    })
  }, [wsMessages])

  const completed = tasks.filter(t => t.status === 'success').length
  const progress = tasks.length ? (completed / tasks.length) * 100 : 0

  return (
    <div>
      <Typography variant="h6">Agent Progress</Typography>
      <LinearProgress variant="determinate" value={progress} sx={{ mb: 2 }} />
      <List>
        {tasks.map(task => (
          <ListItem key={task.id}>
            <ListItemText primary={task.agent_type} secondary={task.status} />
          </ListItem>
        ))}
      </List>
    </div>
  )
}