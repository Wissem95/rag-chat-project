import axios from 'axios';
import { ChatResponse } from '../types';

const API_URL = 'http://localhost:8000/api';

interface ChatParams {
    message: string;
    conversation_id?: string;
    temperature: number;
    use_rag: boolean;
    documents: string[];
}

export const chatService = {
    sendMessage: async (params: ChatParams): Promise<ChatResponse> => {
        const response = await axios.post(`${API_URL}/chat`, params);
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
