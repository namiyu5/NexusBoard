import axios from 'axios'; 

const API_URL = 'http://127.0.0.1:8000/api/'; 

export default { login(credentials) {
     return axios.post(API_URL + 'token/', credentials);
     }, 
     refreshToken(refreshToken) { 
        return axios.post(API_URL + 'token/refresh/', { refresh: refreshToken }); },
 logout() { 
    localStorage.removeItem('access_token'); 
    localStorage.removeItem('refresh_token'); 
} 
}