import axios from 'axios';

export function sendMessage(text: string) {
  return axios.post('/api/message', { text });
}

export function getMessage() {
  return axios.get('/api/message');
} 