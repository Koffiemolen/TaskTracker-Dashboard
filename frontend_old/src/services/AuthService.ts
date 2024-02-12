// src/services/AuthService.ts
import axios from 'axios';

class AuthService {
    login(user: { username: string; password: string }) {
        return axios
            .post('http://127.0.0.1:8000/users/login', user, {
                headers: {
                    accept: 'application/json',
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.data.accessToken) {
                    // Store the token in localStorage or another secure place
                    localStorage.setItem('user', JSON.stringify(response.data));
                }
                return response.data;
            });
    }

    logout() {
        localStorage.removeItem('user');
    }

    getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
}

export default new AuthService();
