import { Box } from '@mui/material'
import { Outlet } from 'react-router-dom'
import { useState } from 'react'
import AppBar from '../common/AppBar'
import Sidebar from './Sidebar'
import Footer from '../common/Footer'

export default function MainLayout() {
  const [darkMode, setDarkMode] = useState(true)
  const toggleDarkMode = () => setDarkMode(!darkMode)

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      <Box sx={{ display: 'flex', flex: 1 }}>
        <Sidebar />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Outlet />
        </Box>
      </Box>
      <Footer />
    </Box>
  )
}