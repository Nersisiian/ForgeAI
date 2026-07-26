import { useEffect, useState, useCallback } from 'react';
import {
  List,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  Chip,
  Typography,
  Box,
  Skeleton,
} from '@mui/material';
import { FolderOpen, ErrorOutline } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface Project {
  id: string;
  name: string;
  target_type: string;
  status: string;
  created_at: string;
}

interface ProjectListProps {
  limit?: number;
  statusFilter?: string;
  showAll?: boolean;
}

export default function ProjectList({ limit = 5, statusFilter, showAll = false }: ProjectListProps) {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: any = { page_size: limit };
      if (statusFilter && statusFilter !== 'all') params.status = statusFilter;
      const response = await api.get('/api/v1/projects/', { params });
      setProjects(response.data.items || []);
    } catch (err) {
      setError('Failed to load projects.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [limit, statusFilter]);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const getStatusChip = (status: string) => {
    let color: 'success' | 'info' | 'error' | 'default' | 'warning' = 'default';
    if (status === 'completed') color = 'success';
    else if (status === 'generating') color = 'info';
    else if (status === 'failed') color = 'error';
    else if (status === 'pending') color = 'warning';
    return <Chip label={status} color={color} size="small" />;
  };

  if (loading) {
    return (
      <Box>
        {[...Array(3)].map((_, i) => (
          <Skeleton key={i} variant="rectangular" height={60} sx={{ mb: 1 }} />
        ))}
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, p: 2 }}>
        <ErrorOutline color="error" />
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (projects.length === 0) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">No projects found.</Typography>
      </Box>
    );
  }

  return (
    <List disablePadding>
      {projects.map(project => (
        <ListItemButton key={project.id} onClick={() => navigate(`/projects/${project.id}`)} divider>
          <ListItemIcon>
            <FolderOpen />
          </ListItemIcon>
          <ListItemText
            primary={project.name}
            secondary={`${project.target_type} · ${new Date(project.created_at).toLocaleDateString()}`}
          />
          {getStatusChip(project.status)}
        </ListItemButton>
      ))}
      {showAll && limit && projects.length === limit && (
        <ListItemButton onClick={() => navigate('/history')}>
          <ListItemText primary="View all projects" sx={{ textAlign: 'center', color: 'primary.main' }} />
        </ListItemButton>
      )}
    </List>
  );
}