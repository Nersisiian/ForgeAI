import { Drawer, List, ListItemButton, ListItemIcon, ListItemText } from '@mui/material'
import { Dashboard, Add, History, Settings, Queue } from '@mui/icons-material'
import { useNavigate, useLocation } from 'react-router-dom'

const navItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/' },
  { text: 'New Project', icon: <Add />, path: '/new' },
  { text: 'Task Queue', icon: <Queue />, path: '/queue' },
  { text: 'History', icon: <History />, path: '/history' },
  { text: 'Settings', icon: <Settings />, path: '/settings' },
]

export default function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <Drawer variant="permanent" sx={{ width: 240, flexShrink: 0, '& .MuiDrawer-paper': { width: 240, boxSizing: 'border-box', mt: 8 } }}>
      <List>
        {navItems.map((item) => (
          <ListItemButton key={item.path} selected={location.pathname === item.path} onClick={() => navigate(item.path)}>
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  )
}