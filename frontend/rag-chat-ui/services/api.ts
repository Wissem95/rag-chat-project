import axios from 'axios';
import { ChatResponse } from '../src/types';

const API_URL = 'http://localhost:8000/api';

export const chatService = {
    sendMessage: async (message: string, conversationId?: string): Promise<ChatResponse> => {
        const response = await axios.post(`${API_URL}/chat`, {
            message,
            conversation_id: conversationId
        });
        return response.data;
    },

    getConversations: async () => {
        const response = await axios.get(`${API_URL}/conversations`);
        return response.data.conversations;
    },

    getConversation: async (id: string) => {
        const response = await axios.get(`${API_URL}/conversations/${id}`);
        return response.data;
    }
};
