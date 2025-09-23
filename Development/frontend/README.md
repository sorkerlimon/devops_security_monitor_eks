# Security Monitor Frontend

A modern, cyberpunk-themed React dashboard for real-time security monitoring including network, malware, and web activity monitoring.

## 🎨 Design Features

- **Cyberpunk Theme**: Dark background with neon accents and glowing effects
- **Security-Focused UI**: Professional security monitoring interface
- **Real-time Updates**: Live data refresh and notifications
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Animated Elements**: Scan lines, pulsing indicators, and smooth transitions

## 🚀 Tech Stack

- **React 19** - Latest React with modern features
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client for API communication
- **React Router** - Client-side routing

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🎯 Features

### Authentication
- **Login Page** - Cyberpunk-themed login with security aesthetics
- **Register Page** - User registration with validation
- **Protected Routes** - Authentication required for all pages

### Dashboard
- **Real-time Stats** - Network, malware, web monitoring statistics
- **Quick Actions** - Direct links to monitoring pages
- **Recent Activity** - Live feed of all activities
- **System Status** - Online/offline indicators

### Network Monitor
- **Port Scanning** - Real-time port status monitoring
- **Host Analysis** - Network host scanning
- **Filtering** - Filter by host, port, status
- **Export Data** - CSV export functionality

### Malware Detector
- **File Analysis** - Suspicious file detection
- **Threat Levels** - High/Medium/Low/Safe indicators
- **File Management** - Delete reports, filter by score
- **Threat Indicators** - Detailed threat analysis

### Web Monitor
- **Domain Tracking** - Web activity monitoring
- **Site Management** - Blocked/allowed site lists
- **Add/Remove Sites** - Dynamic site management
- **Activity Filtering** - Filter by domain, score

## 🎨 Design System

### Colors
- **Primary**: Blue tones for main actions
- **Success**: Green tones for safe/positive states
- **Danger**: Red tones for alerts and threats
- **Warning**: Yellow tones for warnings
- **Dark**: Dark theme with gray tones

### Typography
- **Inter**: Main font for UI elements
- **JetBrains Mono**: Monospace font for code/data

### Animations
- **Scan Lines**: Moving scan effects
- **Pulse Effects**: Status indicators
- **Glow Effects**: Button and card highlights
- **Smooth Transitions**: Hover and state changes

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### API Integration
The frontend connects to the backend API at `http://localhost:8000/api/v1` by default.

## 📱 Responsive Design

- **Desktop**: Full sidebar navigation
- **Tablet**: Collapsible sidebar
- **Mobile**: Hamburger menu navigation

## 🚀 Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🎯 Key Components

- **Layout**: Main layout with sidebar navigation
- **AuthContext**: Authentication state management
- **API Service**: Backend communication
- **Pages**: Login, Register, Dashboard, Monitors
- **Components**: Reusable UI components

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Protected Routes**: Authentication required
- **API Integration**: Secure backend communication
- **Error Handling**: Graceful error management

## 📊 Monitoring Features

- **Real-time Data**: Live updates every 30 seconds
- **Filtering**: Advanced filtering options
- **Export**: CSV data export
- **Status Indicators**: Visual status representation
- **Threat Analysis**: Detailed threat scoring

The frontend provides a beautiful, modern interface for monitoring network security, detecting malware, and tracking web activity with a professional cyberpunk aesthetic! 🛡️✨