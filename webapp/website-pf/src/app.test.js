import React from 'react';
import renderer from 'react-test-renderer';
import { BrowserRouter } from "react-router-dom";
import App from './js/app.js';
import 'bootstrap/dist/css/bootstrap.min.css';


it('renders the web application', () => {
    renderer.act(() => {
        <BrowserRouter>
        <App />
      </BrowserRouter>
    });
  });