// src/services/DataService.ts
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/';

class DataService {
    getProtectedData() {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return axios.get(API_URL + 'some-protected-endpoint', {
            headers: {
                Authorization: `Bearer ${user.accessToken}`,
            },
        });
    }
}

export default new DataService();
