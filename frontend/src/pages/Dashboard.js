/**
 * Dashboard Page
 * 
 * This is the main dashboard page that displays the user's job search progress,
 * weekly goals, streaks, and quick action buttons.
 */

import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  LinearProgress,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  TrendingUp as TrendingUpIcon,
  EmojiEvents as TrophyIcon,
  Assignment as ApplicationsIcon,
  Phone as OutreachIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { goalsAPI } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [goal, setGoal] = useState(null);
  const [streak, setStreak] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [goalRes, streakRes] = await Promise.all([
          goalsAPI.getCurrentGoal(),
          goalsAPI.getStreak(),
        ]);
        setGoal(goalRes.data.goal);
        setStreak(streakRes.data.streak);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 4, fontWeight: 'bold' }}>
        📊 Welcome to Your Job Search Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Weekly Goals Widget */}
        <Grid item xs={12} md={6}>
          <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: '#fff' }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                📋 Weekly Goals
              </Typography>
              {goal && (
                <>
                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Applications</Typography>
                      <Typography variant="body2">
                        {goal.applications_current} / {goal.applications_goal}
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={goal.applications_progress}
                      sx={{ backgroundColor: 'rgba(255, 255, 255, 0.3)' }}
                    />
                  </Box>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Outreach</Typography>
                      <Typography variant="body2">
                        {goal.outreach_current} / {goal.outreach_goal}
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={goal.outreach_progress}
                      sx={{ backgroundColor: 'rgba(255, 255, 255, 0.3)' }}
                    />
                  </Box>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Streak Widget */}
        <Grid item xs={12} md={6}>
          <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: '#fff' }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                🔥 Your Streak
              </Typography>
              {streak && (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-around', mb: 2 }}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                        {streak.current_streak}
                      </Typography>
                      <Typography variant="body2">Current Streak</Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                        {streak.longest_streak}
                      </Typography>
                      <Typography variant="body2">Longest Streak</Typography>
                    </Box>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <TrophyIcon sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="body2">
                      {streak.total_points} Points
                    </Typography>
                  </Box>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              ⚡ Quick Actions
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => navigate('/applications')}
                  sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
                >
                  Add Application
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => navigate('/outreach')}
                  sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}
                >
                  Log Outreach
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => navigate('/cv-matcher')}
                  sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}
                >
                  Analyze CV
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<TrendingUpIcon />}
                  onClick={() => navigate('/goals')}
                  sx={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}
                >
                  Set Goals
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Stats Overview */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              📈 Your Statistics
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f0f0f0', borderRadius: 1 }}>
                  <ApplicationsIcon sx={{ fontSize: 32, color: '#667eea', mb: 1 }} />
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>0</Typography>
                  <Typography variant="body2" color="textSecondary">Total Applications</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f0f0f0', borderRadius: 1 }}>
                  <OutreachIcon sx={{ fontSize: 32, color: '#f5576c', mb: 1 }} />
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>0</Typography>
                  <Typography variant="body2" color="textSecondary">Outreach Activities</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f0f0f0', borderRadius: 1 }}>
                  <TrendingUpIcon sx={{ fontSize: 32, color: '#43e97b', mb: 1 }} />
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>0</Typography>
                  <Typography variant="body2" color="textSecondary">CV Analyses</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f0f0f0', borderRadius: 1 }}>
                  <TrophyIcon sx={{ fontSize: 32, color: '#ffa500', mb: 1 }} />
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>0</Typography>
                  <Typography variant="body2" color="textSecondary">Companies Tracked</Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
