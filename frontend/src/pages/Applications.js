/**
 * Applications Page - Kanban Board
 * 
 * This page displays job applications in a Kanban board with 5 status columns:
 * Planned, Applied, Interview, Offer, Rejected
 * Users can drag and drop applications between columns to update status.
 */

import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Paper,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { applicationsAPI, companiesAPI } from '../services/api';

const Applications = () => {
  const [applications, setApplications] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    company_id: '',
    job_title: '',
    job_url: '',
    status: 'Planned',
    notes: '',
  });
  const [error, setError] = useState('');

  const statuses = ['Planned', 'Applied', 'Interview', 'Offer', 'Rejected'];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [appsRes, companiesRes] = await Promise.all([
          applicationsAPI.listApplications({ per_page: 100 }),
          companiesAPI.listCompanies({ per_page: 100 }),
        ]);
        setApplications(appsRes.data.applications);
        setCompanies(companiesRes.data.companies);
      } catch (err) {
        setError('Failed to load applications');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAddApplication = async () => {
    if (!formData.company_id || !formData.job_title) {
      setError('Company and job title are required');
      return;
    }

    try {
      const response = await applicationsAPI.createApplication(formData);
      setApplications([...applications, response.data.application]);
      setOpenDialog(false);
      setFormData({
        company_id: '',
        job_title: '',
        job_url: '',
        status: 'Planned',
        notes: '',
      });
      setError('');
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to create application');
    }
  };

  const handleDeleteApplication = async (id) => {
    try {
      await applicationsAPI.deleteApplication(id);
      setApplications(applications.filter((app) => app.id !== id));
    } catch (err) {
      setError('Failed to delete application');
    }
  };

  const handleStatusChange = async (id, newStatus) => {
    try {
      const response = await applicationsAPI.updateApplication(id, { status: newStatus });
      setApplications(
        applications.map((app) => (app.id === id ? response.data.application : app))
      );
    } catch (err) {
      setError('Failed to update application');
    }
  };

  const getApplicationsByStatus = (status) => {
    return applications.filter((app) => app.status === status);
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
          📋 Application Tracker
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
          sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
        >
          Add Application
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {/* Kanban Board */}
      <Grid container spacing={2}>
        {statuses.map((status) => (
          <Grid item xs={12} sm={6} md={2.4} key={status}>
            <Paper
              sx={{
                p: 2,
                minHeight: '500px',
                backgroundColor: '#f5f5f5',
                borderRadius: 2,
              }}
            >
              <Typography
                variant="h6"
                sx={{
                  mb: 2,
                  fontWeight: 'bold',
                  textAlign: 'center',
                  color: '#667eea',
                }}
              >
                {status}
              </Typography>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                {getApplicationsByStatus(status).map((app) => (
                  <Card
                    key={app.id}
                    sx={{
                      cursor: 'pointer',
                      '&:hover': {
                        boxShadow: 3,
                        transform: 'translateY(-2px)',
                      },
                      transition: 'all 0.2s ease',
                    }}
                  >
                    <CardContent sx={{ p: 1.5 }}>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                        {app.job_title}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {app.company?.name}
                      </Typography>
                      <Box sx={{ mt: 1, display: 'flex', justifyContent: 'space-between' }}>
                        <select
                          value={app.status}
                          onChange={(e) => handleStatusChange(app.id, e.target.value)}
                          style={{
                            padding: '4px 8px',
                            borderRadius: '4px',
                            border: '1px solid #ddd',
                            fontSize: '12px',
                          }}
                        >
                          {statuses.map((s) => (
                            <option key={s} value={s}>
                              {s}
                            </option>
                          ))}
                        </select>
                        <DeleteIcon
                          sx={{
                            fontSize: 16,
                            cursor: 'pointer',
                            color: '#f5576c',
                            '&:hover': { color: '#d63447' },
                          }}
                          onClick={() => handleDeleteApplication(app.id)}
                        />
                      </Box>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Add Application Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add New Application</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <TextField
            select
            fullWidth
            label="Company"
            value={formData.company_id}
            onChange={(e) => setFormData({ ...formData, company_id: e.target.value })}
            margin="normal"
            required
          >
            {companies.map((company) => (
              <option key={company.id} value={company.id}>
                {company.name}
              </option>
            ))}
          </TextField>

          <TextField
            fullWidth
            label="Job Title"
            value={formData.job_title}
            onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            label="Job URL"
            value={formData.job_url}
            onChange={(e) => setFormData({ ...formData, job_url: e.target.value })}
            margin="normal"
          />

          <TextField
            select
            fullWidth
            label="Status"
            value={formData.status}
            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
            margin="normal"
          >
            {statuses.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </TextField>

          <TextField
            fullWidth
            label="Notes"
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            margin="normal"
            multiline
            rows={3}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button
            onClick={handleAddApplication}
            variant="contained"
            sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
          >
            Add
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Applications;
