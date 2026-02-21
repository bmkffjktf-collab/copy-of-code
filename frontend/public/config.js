// Runtime configuration file
// With nginx reverse proxy, we use relative paths for API calls
window.API_CONFIG = {
  apiUrl: '' // Use relative paths - nginx will proxy /api requests to backend
};

console.log('✅ API Config Loaded:', window.API_CONFIG);

