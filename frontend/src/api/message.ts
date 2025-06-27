import axios from 'axios';

export interface MessageHistory {
  text: string;
  timestamp: string;
}

export function sendMessage(text: string) {
  return axios.post('/api/message/', { text });
}

export function getMessage() {
  return axios.get<{text: string}>('/api/message/');
}

export function getMessageHistory() {
  return axios.get<{history: MessageHistory[]}>('/api/message/history');
} 