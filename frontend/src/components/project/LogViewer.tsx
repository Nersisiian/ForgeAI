import { Typography, Paper } from '@mui/material'

interface LogViewerProps {
  messages: any[]
}

export default function LogViewer({ messages }: LogViewerProps) {
  return (
    <Paper variant="outlined" sx={{ p: 2, maxHeight: 400, overflow: 'auto' }}>
      <Typography variant="subtitle2">Live Logs</Typography>
      {messages.map((msg, i) => (
        <Typography key={i} variant="body2" fontFamily="monospace">{JSON.stringify(msg)}</Typography>
      ))}
    </Paper>
  )
}