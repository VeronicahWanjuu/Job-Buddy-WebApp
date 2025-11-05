/**
 * Entry point for the React application.
 * 
 * This file initializes the React app and renders the root App component
 * into the DOM.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
