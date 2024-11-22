import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, TextField, Button, Paper, Typography, CircularProgress, IconButton, FormControlLabel, Switch, Drawer, List, ListItem, ListItemText, Snackbar, Alert, Slider, Checkbox, Chip } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import CloseIcon from '@mui/icons-material/Close';
import { Message, LLMSettings as LLMSettingsType } from '../../types';
import { chatService } from '../../services/api';
import { LLMSettings } from '../Settings/LLMSettings';

export const ChatWindow: React.FC = () => {
    const { conversationId } = useParams<{ conversationId?: string }>();
    const navigate = useNavigate();
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<null | HTMLDivElement>(null);
    const [loading, setLoading] = useState(false);
    const [useRag, setUseRag] = useState(false);
    const [llmSettings, setLLMSettings] = useState<LLMSettingsType>({
        temperature: 0.7,
        maxTokens: 2000,
        topP: 0.9,
        frequencyPenalty: 0,
        presencePenalty: 0
    });
    const [isDocumentDrawerOpen, setIsDocumentDrawerOpen] = useState(false);
    const [documents, setDocuments] = useState<Array<{ name: string; size: number }>>([]);
    const [uploading, setUploading] = useState(false);
    const [uploadError, setUploadError] = useState<string | null>(null);
    const [temperature, setTemperature] = useState(0.7);
    const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        if (conversationId) {
            setDocuments([]);
            setUseRag(false);
            setMessages([]);
            chatService.getConversation(conversationId)
                .then(data => {
                    if (Array.isArray(data)) {
                        setMessages(data);
                    }
                })
                .catch(console.error)
                .finally(() => setLoading(false));
        }
    }, [conversationId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSettingsChange = (newSettings: any) => {
        setLLMSettings(newSettings);
    };

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        try {
            setLoading(true);
            
            if (useRag && selectedDocuments.length === 0) {
                setUploadError("Veuillez sélectionner au moins un document quand RAG est activé");
                return;
            }

            const userMessage: Message = {
                role: 'user',
                content: input,
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, userMessage]);
            setInput('');

            const response = await chatService.sendMessage({
                message: input,
                conversation_id: conversationId,
                temperature: temperature,
                use_rag: useRag,
                documents: useRag ? selectedDocuments : []
            });
            
            const assistantMessage: Message = {
                role: 'assistant',
                content: response.response,
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        if (!event.target.files?.length) return;

        try {
            setUploading(true);
            const formData = new FormData();
            
            for (let i = 0; i < event.target.files.length; i++) {
                const file = event.target.files[i];
                if (!file.name.match(/\.(pdf|txt|doc|docx)$/i)) {
                    setUploadError("Type de fichier non supporté. Types acceptés: PDF, TXT, DOC, DOCX");
                    continue;
                }
                formData.append('files', file);
            }

            const response = await fetch('http://localhost:8000/api/documents/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            await loadDocuments();
            
            setIsDocumentDrawerOpen(true);
        } catch (error: any) {
            console.error('Upload error:', error);
            setUploadError(error.message || 'Failed to upload document');
        } finally {
            setUploading(false);
            if (event.target) {
                event.target.value = '';
            }
        }
    };

    const loadDocuments = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/documents/list');
            if (!response.ok) throw new Error('Failed to fetch documents');
            const data = await response.json();
            setDocuments(data.documents || []);
        } catch (error) {
            console.error('Error loading documents:', error);
        }
    };

    return (
        <Box sx={{ height: 'calc(100vh - 140px)', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                mb: 2,
                gap: 2
            }}>
                <IconButton 
                    onClick={() => navigate('/')}
                    sx={{ 
                        color: 'white',
                        '&:hover': {
                            backgroundColor: 'rgba(255, 255, 255, 0.1)'
                        }
                    }}
                >
                    <ArrowBackIcon />
                </IconButton>
                <Typography variant="h6" sx={{ color: 'white' }}>
                    {conversationId ? 'Conversation' : 'Nouvelle conversation'}
                </Typography>
            </Box>
            <Paper elevation={3} sx={{ 
                flex: 1, 
                overflow: 'auto', 
                p: 2, 
                mb: 2,
                backgroundColor: 'background.paper',
                position: 'relative'
            }}>
                {loading && (
                    <Box sx={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)'
                    }}>
                        <CircularProgress />
                    </Box>
                )}
                {Array.isArray(messages) && messages.map((msg, idx) => (
                    <Box
                        key={idx}
                        sx={{
                            display: 'flex',
                            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                            mb: 2
                        }}
                    >
                        <Paper
                            sx={{
                                p: 2,
                                maxWidth: '70%',
                                backgroundColor: msg.role === 'user' 
                                    ? 'primary.dark'  // Couleur pour les messages utilisateur
                                    : '#2D2D2D',     // Couleur pour les messages assistant
                                color: '#fff',       // Texte en blanc
                                '& .MuiTypography-root': {
                                    color: '#fff'    // S'assurer que la typographie est aussi en blanc
                                }
                            }}
                        >
                            <Typography>{msg.content}</Typography>
                            <Typography 
                                variant="caption" 
                                sx={{ 
                                    display: 'block',
                                    mt: 1,
                                    color: 'rgba(255, 255, 255, 0.7)'  // Timestamp légèrement transparent
                                }}
                            >
                                {new Date(msg.timestamp).toLocaleTimeString()}
                            </Typography>
                        </Paper>
                    </Box>
                ))}
                <div ref={messagesEndRef} />
            </Paper>
            
            <Box sx={{ display: 'flex', gap: 1 }}>
                <input
                    type="file"
                    id="document-upload"
                    multiple
                    style={{ display: 'none' }}
                    onChange={handleFileUpload}
                    accept=".txt,.pdf,.doc,.docx"
                />
                <label htmlFor="document-upload">
                    <IconButton 
                        component="span"
                        onClick={() => setIsDocumentDrawerOpen(true)}
                    >
                        <AttachFileIcon />
                    </IconButton>
                </label>
                <TextField
                    fullWidth
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !loading && handleSend()}
                    placeholder="Tapez votre message..."
                    variant="outlined"
                    disabled={loading}
                    sx={{
                        '& .MuiOutlinedInput-root': {
                            backgroundColor: 'background.paper',
                            '& fieldset': {
                                borderColor: 'rgba(255, 255, 255, 0.23)'
                            },
                            '&:hover fieldset': {
                                borderColor: 'rgba(255, 255, 255, 0.4)'
                            },
                            '&.Mui-focused fieldset': {
                                borderColor: 'primary.main'
                            }
                        },
                        '& .MuiInputBase-input': {
                            color: '#fff'
                        }
                    }}
                />
                <Button
                    variant="contained"
                    onClick={handleSend}
                    endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                    disabled={loading}
                >
                    Envoyer
                </Button>
            </Box>
            <LLMSettings 
                settings={llmSettings}
                onSettingsChange={handleSettingsChange}
            />
            <Drawer
                anchor="right"
                open={isDocumentDrawerOpen}
                onClose={() => setIsDocumentDrawerOpen(false)}
            >
                <Box sx={{ width: 300, p: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                        <Typography variant="h6">Documents</Typography>
                        <IconButton onClick={() => setIsDocumentDrawerOpen(false)}>
                            <CloseIcon />
                        </IconButton>
                    </Box>

                    <label htmlFor="document-upload">
                        <Button
                            variant="contained"
                            component="span"
                            fullWidth
                            disabled={uploading}
                            sx={{ mb: 2 }}
                        >
                            {uploading ? 'Uploading...' : 'Upload Document'}
                        </Button>
                    </label>

                    <List>
                        {documents.map((doc) => (
                            <ListItem 
                                key={doc.name}
                                secondaryAction={
                                    <Checkbox
                                        edge="end"
                                        checked={selectedDocuments.includes(doc.name)}
                                        onChange={(e) => {
                                            if (e.target.checked) {
                                                setSelectedDocuments(prev => [...prev, doc.name]);
                                            } else {
                                                setSelectedDocuments(prev => prev.filter(name => name !== doc.name));
                                            }
                                        }}
                                    />
                                }
                            >
                                <ListItemText
                                    primary={doc.name}
                                    secondary={`${(doc.size / 1024).toFixed(2)} KB`}
                                />
                            </ListItem>
                        ))}
                    </List>
                </Box>
            </Drawer>
            <Snackbar 
                open={!!uploadError} 
                autoHideDuration={6000} 
                onClose={() => setUploadError(null)}
            >
                <Alert onClose={() => setUploadError(null)} severity="error">
                    {uploadError}
                </Alert>
            </Snackbar>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                <FormControlLabel
                    control={
                        <Switch
                            checked={useRag}
                            onChange={(e) => setUseRag(e.target.checked)}
                        />
                    }
                    label="Utiliser RAG"
                />
                <Typography gutterBottom>
                    Temperature: {temperature}
                </Typography>
                <Slider
                    value={temperature}
                    onChange={(_, value) => setTemperature(value as number)}
                    min={0}
                    max={1}
                    step={0.1}
                    sx={{ width: 200 }}
                />
            </Box>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {selectedDocuments.map(doc => (
                    <Chip
                        key={doc}
                        label={doc}
                        onDelete={() => setSelectedDocuments(prev => prev.filter(name => name !== doc))}
                        size="small"
                    />
                ))}
            </Box>
        </Box>
    );
};
