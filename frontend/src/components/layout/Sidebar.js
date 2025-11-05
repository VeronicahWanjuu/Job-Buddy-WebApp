/**
 * Sidebar Component
 * 
 * This component renders the left sidebar with navigation links to different
 * sections of the application.
 */

import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Assignment as ApplicationsIcon,
  Business as CompaniesIcon,
  People as ContactsIcon,
  Phone as OutreachIcon,
  Description as CVIcon,
  Flag as GoalsIcon,
  School as ResourcesIcon,
  Person as CoachesIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ open = true }) => {
  const navigate = useNavigate();

  const menuItems = [
    { label: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { label: 'Applications', icon: <ApplicationsIcon />, path: '/applications' },
    { label: 'Companies', icon: <CompaniesIcon />, path: '/companies' },
    { label: 'Contacts', icon: <ContactsIcon />, path: '/contacts' },
    { label: 'Outreach', icon: <OutreachIcon />, path: '/outreach' },
    { label: 'CV Matcher', icon: <CVIcon />, path: '/cv-matcher' },
    { label: 'Goals', icon: <GoalsIcon />, path: '/goals' },
    { label: 'Resources', icon: <ResourcesIcon />, path: '/resources' },
    { label: 'Coaches', icon: <CoachesIcon />, path: '/coaches' },
  ];

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: open ? 280 : 80,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: open ? 280 : 80,
          boxSizing: 'border-box',
          background: 'linear-gradient(180deg, #2d3748 0%, #1a202c 100%)',
          color: '#fff',
          transition: 'width 0.3s ease',
        },
      }}
    >
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
          {open ? '🚀 Menu' : '📋'}
        </Typography>
      </Box>
      <Divider sx={{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }} />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.path}
            onClick={() => navigate(item.path)}
            sx={{
              '&:hover': {
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
              },
            }}
          >
            <ListItemIcon sx={{ color: '#667eea', minWidth: open ? 40 : 0 }}>
              {item.icon}
            </ListItemIcon>
            {open && <ListItemText primary={item.label} />}
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

// Import Typography from MUI
import { Typography } from '@mui/material';

export default Sidebar;
