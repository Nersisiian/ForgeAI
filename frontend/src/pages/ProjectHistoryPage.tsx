import { useEffect, useState, useCallback } from 'react';
import {
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  TablePagination,
  TextField,
  MenuItem,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Visibility, Refresh } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Project {
  id: string;
  name: string;
  target_type: string;
  status: string;
  created_at: string;
  updated_at: string | null;
}

const STATUS_OPTIONS = ['all', 'pending', 'generating', 'completed', 'failed'];

export default function ProjectHistoryPage() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [statusFilter, setStatusFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    try {
      const params: any = { page: page + 1, page_size: rowsPerPage };
      if (statusFilter !== 'all') params.status = statusFilter;
      if (search) params.search = search;
      const response = await api.get('/api/v1/projects/', { params });
      setProjects(response.data.items || []);
      setTotal(response.data.total || 0);
    } catch (error) {
      console.error('Failed to fetch projects', error);
    } finally {
      setLoading(false);
    }
  }, [page, rowsPerPage, statusFilter, search]);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleChangePage = (_: unknown, newPage: number) => setPage(newPage);
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'generating': return 'info';
      case 'failed': return 'error';
      case 'pending': return 'default';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4">Project History</Typography>
        <Tooltip title="Refresh">
          <IconButton onClick={fetchProjects} disabled={loading}><Refresh /></IconButton>
        </Tooltip>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          label="Search"
          variant="outlined"
          size="small"
          value={search}
          onChange={e => { setSearch(e.target.value); setPage(0); }}
          sx={{ width: 250 }}
        />
        <TextField
          select
          label="Status"
          value={statusFilter}
          onChange={e => { setStatusFilter(e.target.value); setPage(0); }}
          size="small"
          sx={{ width: 150 }}
        >
          {STATUS_OPTIONS.map(opt => (
            <MenuItem key={opt} value={opt}>{opt.charAt(0).toUpperCase() + opt.slice(1)}</MenuItem>
          ))}
        </TextField>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {projects.map(project => (
              <TableRow key={project.id} hover>
                <TableCell>{project.name}</TableCell>
                <TableCell>{project.target_type}</TableCell>
                <TableCell>
                  <Chip label={project.status} color={getStatusColor(project.status)} size="small" />
                </TableCell>
                <TableCell>{new Date(project.created_at).toLocaleDateString()}</TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => navigate(`/projects/${project.id}`)} size="small">
                    <Visibility />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
            {projects.length === 0 && !loading && (
              <TableRow>
                <TableCell colSpan={5} align="center">No projects found</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={total}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          rowsPerPageOptions={[5, 10, 25]}
        />
      </TableContainer>
    </Box>
  );
}
