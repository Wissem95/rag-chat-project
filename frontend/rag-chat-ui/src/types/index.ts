export interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
}

export interface Conversation {
    id: string;
    messages: Message[];
}

export interface ChatResponse {
    response: string;
    conversation_id: string;
}

export interface LLMSettings {
    temperature: number;
    maxTokens: number;
    topP: number;
    frequencyPenalty: number;
    presencePenalty: number;
}
