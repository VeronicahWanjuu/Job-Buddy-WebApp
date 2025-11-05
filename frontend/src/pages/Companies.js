/**
 * Companies Page
 * 
 * This page allows users to view, add, edit, and delete companies.
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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  IconButton,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import { companiesAPI } from '../services/api';

const Companies = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    website: '',
    location: '',
    industry: '',
    notes: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await companiesAPI.listCompanies({ per_page: 100 });
        setCompanies(response.data.companies);
      } catch (err) {
        setError('Failed to load companies');
      } finally {
        setLoading(false);
      }
    };

    fetchCompanies();
  }, []);

  const handleAddCompany = async () => {
    if (!formData.name) {
      setError('Company name is required');
      return;
    }

    try {
      if (editingId) {
        const response = await companiesAPI.updateCompany(editingId, formData);
        setCompanies(
          companies.map((c) => (c.id === editingId ? response.data.company : c))
        );
      } else {
        const response = await companiesAPI.createCompany(formData);
        setCompanies([...companies, response.data.company]);
      }
      setOpenDialog(false);
      setEditingId(null);
      setFormData({
        name: '',
        website: '',
        location: '',
        industry: '',
        notes: '',
      });
      setError('');
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to save company');
    }
  };

  const handleEditCompany = (company) => {
    setFormData(company);
    setEditingId(company.id);
    setOpenDialog(true);
  };

  const handleDeleteCompany = async (id) => {
    if (window.confirm('Are you sure you want to delete this company?')) {
      try {
        await companiesAPI.deleteCompany(id);
        setCompanies(companies.filter((c) => c.id !== id));
      } catch (err) {
        setError('Failed to delete company');
      }
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
          🏢 Companies
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditingId(null);
            setFormData({ name: '', website: '', location: '', industry: '', notes: '' });
            setOpenDialog(true);
          }}
          sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
        >
          Add Company
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TableContainer component={Paper}>
        <Table>
          <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold' }}>Company Name</TableCell>
              <TableCell>Website</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Industry</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {companies.map((company) => (
              <TableRow key={company.id} hover>
                <TableCell sx={{ fontWeight: '500' }}>{company.name}</TableCell>
                <TableCell>
                  {company.website ? (
                    <a href={company.website} target="_blank" rel="noopener noreferrer">
                      {company.website}
                    </a>
                  ) : (
                    '-'
                  )}
                </TableCell>
                <TableCell>{company.location || '-'}</TableCell>
                <TableCell>{company.industry || '-'}</TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleEditCompany(company)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDeleteCompany(company.id)}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {companies.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography color="textSecondary">No companies yet. Add one to get started!</Typography>
        </Box>
      )}

      {/* Add/Edit Company Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? 'Edit Company' : 'Add New Company'}</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <TextField
            fullWidth
            label="Company Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            label="Website"
            value={formData.website}
            onChange={(e) => setFormData({ ...formData, website: e.target.value })}
            margin="normal"
          />

          <TextField
            fullWidth
            label="Location"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            margin="normal"
          />

          <TextField
            fullWidth
            label="Industry"
            value={formData.industry}
            onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
            margin="normal"
          />

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
            onClick={handleAddCompany}
            variant="contained"
            sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
          >
            {editingId ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Companies;
