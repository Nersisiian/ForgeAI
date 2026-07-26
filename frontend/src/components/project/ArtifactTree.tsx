import { useEffect, useState } from 'react'
import { List, ListItemButton, ListItemText, Dialog, DialogTitle, DialogContent, Typography } from '@mui/material'
import api from '../../services/api'

interface ArtifactTreeProps {
  projectId: string
}

export default function ArtifactTree({ projectId }: ArtifactTreeProps) {
  const [artifacts, setArtifacts] = useState<any[]>([])
  const [selected, setSelected] = useState<any>(null)

  useEffect(() => {
    api.get(`/api/v1/artifacts/project/${projectId}`).then(res => setArtifacts(res.data))
  }, [projectId])

  return (
    <>
      <List>
        {artifacts.map(a => (
          <ListItemButton key={a.id} onClick={() => setSelected(a)}>
            <ListItemText primary={a.file_path} secondary={a.status} />
          </ListItemButton>
        ))}
      </List>
      <Dialog open={!!selected} onClose={() => setSelected(null)} maxWidth="md" fullWidth>
        <DialogTitle>{selected?.file_path}</DialogTitle>
        <DialogContent>
          <pre style={{ whiteSpace: 'pre-wrap' }}><code>{selected?.content}</code></pre>
        </DialogContent>
      </Dialog>
    </>
  )
}