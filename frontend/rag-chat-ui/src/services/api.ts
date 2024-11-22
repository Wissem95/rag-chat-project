import axios from 'axios';
import { ChatResponse, LLMSettings } from '../types';

const API_URL = 'http://localhost:8000/api';

export const chatService = {
    sendMessage: async (message: string, conversationId?: string, settings?: LLMSettings): Promise<ChatResponse> => {
        const response = await axios.post(`${API_URL}/chat`, {
            message,
            conversation_id: conversationId,
            settings
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
    },

    deleteConversation: async (id: string) => {
        const response = await axios.delete(`${API_URL}/conversations/${id}`);
        return response.data;
    }
};
