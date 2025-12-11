import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE ?? ''

axios.defaults.baseURL = API_BASE

function setAuthTokens(access, refresh) {
  if (access) {
    localStorage.setItem('access_token', access)
    axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
  }
  if (refresh) {
    localStorage.setItem('refresh_token', refresh)
  }
  // notify app that auth changed
  try {
    window.dispatchEvent(new Event('authChanged'))
  } catch (e) {
    // ignore in non-browser environments
  }
}

function clearAuth() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('username')
  delete axios.defaults.headers.common['Authorization']
  try {
    window.dispatchEvent(new Event('authChanged'))
  } catch (e) {
    // ignore
  }
}

// Initialize axios Authorization header from any existing token in storage
const _initialAccess = localStorage.getItem('access_token')
if (_initialAccess) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${_initialAccess}`
}

// Response interceptor: try refresh on 401
axios.interceptors.response.use(
  res => res,
  async err => {
    const originalRequest = err.config
    if (!originalRequest) return Promise.reject(err)

    if (err.response && err.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) {
        clearAuth()
        return Promise.reject(err)
      }
      try {
        const r = await axios.post('/api/token/refresh/', { refresh })
        const newAccess = r.data.access
        setAuthTokens(newAccess, refresh)
        originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
        return axios(originalRequest)
      } catch (refreshErr) {
        clearAuth()
        return Promise.reject(refreshErr)
      }
    }
    return Promise.reject(err)
  }
)

export default axios
export { setAuthTokens, clearAuth }


async function verifyAuth() {
  const access = localStorage.getItem('access_token')
  if (!access) return false
  try {
    // try a protected endpoint that requires authentication
    await axios.get('/api/enrollments/')
    return true
  } catch (err) {
    if (err?.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) {
        clearAuth()
        return false
      }
      try {
        const r = await axios.post('/api/token/refresh/', { refresh })
        if (r && r.data && r.data.access) {
          setAuthTokens(r.data.access, refresh)
          return true
        }
      } catch (refreshErr) {
        clearAuth()
        return false
      }
    }
    return false
  }
}

export { verifyAuth }
