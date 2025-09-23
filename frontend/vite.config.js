import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    allowedHosts: ['security-monitor.local', 'localhost','security-monitor.dreamhrai.com']
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    allowedHosts: ['security-monitor.local', 'localhost','security-monitor.dreamhrai.com']
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})