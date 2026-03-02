import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://dziennik.polandcentral.cloudapp.azure.com',
        changeOrigin: true,
        secure: false,      
      }
    }
  }
})
