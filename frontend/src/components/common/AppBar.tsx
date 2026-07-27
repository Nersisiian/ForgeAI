import { AppBar as MuiAppBar, Toolbar, Typography, IconButton } from '@mui/material'
import { Brightness4, Brightness7, Logout } from '@mui/icons-material'
import { useAuth } from '../../hooks/useAuth'

interface AppBarProps {
  darkMode: boolean
  toggleDarkMode: () => void
}

export default function AppBar({ darkMode, toggleDarkMode }: AppBarProps) {
  const { logout, user } = useAuth()
  return (
    <MuiAppBar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Python Auto Company
        </Typography>
        <Typography variant="body2" sx={{ mr: 2 }}>{user?.email}</Typography>
        <IconButton color="inherit" onClick={toggleDarkMode}>
          {darkMode ? <Brightness7 /> : <Brightness4 />}
        </IconButton>
        <IconButton color="inherit" onClick={logout}>
          <Logout />
        </IconButton>
      </Toolbar>
    </MuiAppBar>
  )
}
