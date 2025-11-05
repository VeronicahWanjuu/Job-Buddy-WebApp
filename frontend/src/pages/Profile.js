/**
 * Profile Page
 * 
 * This page allows users to view and update their profile information,
 * change password, and delete their account.
 */

import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Divider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { profileAPI } from '../services/api';

const Profile = () => {
  const navigate = useNavigate();
  const { user, updateUser, logout } = useAuth();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    dream_milestone: '',
  });
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await profileAPI.getProfile();
        setProfileData({
          name: response.data.user.name,
          dream_milestone: response.data.user.dream_milestone || '',
        });
      } catch (err) {
        setError('Failed to load profile');
      }
    };

    fetchProfile();
  }, []);

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await profileAPI.updateProfile(profileData);
      updateUser(response.data.user);
      setSuccess('Profile updated successfully!');
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    if (passwordData.new_password !== passwordData.confirm_password) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      await profileAPI.changePassword(
        passwordData.current_password,
        passwordData.new_password
      );
      setSuccess('Password changed successfully!');
      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: '',
      });
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    setLoading(true);
    try {
      await profileAPI.deleteAccount();
      logout();
      navigate('/login');
    } catch (err) {
      setError('Failed to delete account');
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 4, fontWeight: 'bold' }}>
        👤 Profile Settings
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      {/* Profile Information */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
          Profile Information
        </Typography>

        <form onSubmit={handleUpdateProfile}>
          <TextField
            fullWidth
            label="Full Name"
            value={profileData.name}
            onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            label="Dream Milestone"
            value={profileData.dream_milestone}
            onChange={(e) => setProfileData({ ...profileData, dream_milestone: e.target.value })}
            margin="normal"
            multiline
            rows={3}
            placeholder="What's your ultimate career goal?"
          />

          <Button
            variant="contained"
            type="submit"
            sx={{ mt: 2, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Update Profile'}
          </Button>
        </form>
      </Paper>

      <Divider sx={{ my: 3 }} />

      {/* Change Password */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
          Change Password
        </Typography>

        <form onSubmit={handleChangePassword}>
          <TextField
            fullWidth
            label="Current Password"
            type="password"
            value={passwordData.current_password}
            onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            label="New Password"
            type="password"
            value={passwordData.new_password}
            onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
            margin="normal"
            required
            helperText="Min 8 chars, 1 uppercase, 1 lowercase, 1 number"
          />

          <TextField
            fullWidth
            label="Confirm New Password"
            type="password"
            value={passwordData.confirm_password}
            onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
            margin="normal"
            required
          />

          <Button
            variant="contained"
            type="submit"
            sx={{ mt: 2, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Change Password'}
          </Button>
        </form>
      </Paper>

      <Divider sx={{ my: 3 }} />

      {/* Danger Zone */}
      <Paper sx={{ p: 3, backgroundColor: '#fff3cd', borderLeft: '4px solid #ff6b6b' }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', color: '#d63447' }}>
          ⚠️ Danger Zone
        </Typography>

        <Typography variant="body2" sx={{ mb: 2 }}>
          Deleting your account will permanently remove all your data including applications,
          companies, contacts, and all other information. This action cannot be undone.
        </Typography>

        <Button
          variant="contained"
          color="error"
          onClick={() => setOpenDeleteDialog(true)}
        >
          Delete Account
        </Button>
      </Paper>

      {/* Delete Account Confirmation Dialog */}
      <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
        <DialogTitle>Delete Account</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete your account? This action cannot be undone.
            All your data will be permanently deleted.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)}>Cancel</Button>
          <Button
            onClick={handleDeleteAccount}
            color="error"
            variant="contained"
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Profile;
