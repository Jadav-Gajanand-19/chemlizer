// ChemLizer Design System - Color Palette & Theme Configuration

const theme = {
  colors: {
    // Main brand colors
    primary: '#0A4D68',      // Deep Ocean Blue - trust, precision
    secondary: '#088395',    // Vibrant Teal - innovation, energy
    accent: '#05BFDB',       // Bright Cyan - highlights, CTAs
    
    // Background colors
    background: '#F8F9FA',   // Clean White
    backgroundAlt: '#FFFFFF',
    
    // Dark mode
    darkBg: '#1A1A2E',       // Charcoal
    darkAccent: '#05BFDB',
    
    // Text colors
    text: '#2C3E50',
    textLight: '#6C757D',
    textDark: '#1A1A2E',
    
    // Status colors
    success: '#28A745',
    error: '#DC3545',
    warning: '#FFC107',
    info: '#17A2B8',
    
    // Neutral colors
    gray100: '#F8F9FA',
    gray200: '#E9ECEF',
    gray300: '#DEE2E6',
    gray400: '#CED4DA',
    gray500: '#ADB5BD',
    gray600: '#6C757D',
    gray700: '#495057',
    gray800: '#343A40',
    gray900: '#212529',
  },
  
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.15), 0 10px 10px rgba(0, 0, 0, 0.04)',
  },
  
  transitions: {
    fast: '150ms ease-in-out',
    normal: '250ms ease-in-out',
    slow: '350ms ease-in-out',
  },
  
  typography: {
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
      '4xl': '36px',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
};

export default theme;
