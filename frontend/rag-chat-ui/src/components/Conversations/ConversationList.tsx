import { FC, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    List, 
    ListItem, 
    ListItemButton, 
    ListItemText, 
    Paper, 
    Typography,
    Button,
    IconButton,
    Skeleton
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';

interface Conversation {
    id: string;
    title: string;
    timestamp: string;
    messageCount: number;
}

export const ConversationList: FC = () => {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const fetchConversations = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://localhost:8000/api/conversations');
            if (!response.ok) throw new Error('Failed to fetch conversations');
            const data = await response.json();
            setConversations(data.conversations || []);
        } catch (error) {
            console.error('Error fetching conversations:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id: string, e: React.MouseEvent) => {
        e.stopPropagation();
        try {
            const response = await fetch(`http://localhost:8000/api/conversations/${id}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Failed to delete conversation');
            await fetchConversations();
        } catch (error) {
            console.error('Error deleting conversation:', error);
        }
    };

    useEffect(() => {
        fetchConversations();
        // Rafraîchir toutes les 5 secondes
        const interval = setInterval(fetchConversations, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <Paper elevation={3} sx={{ p: 2, backgroundColor: 'background.paper' }}>
            <Button
                fullWidth
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => navigate('/chat')}
                sx={{ mb: 2 }}
            >
                Nouvelle conversation
            </Button>

            <Typography variant="h6" sx={{ mb: 2 }}>
                Conversations
            </Typography>

            <List>
                {loading ? (
                    [...Array(3)].map((_, i) => (
                        <ListItem key={i} disablePadding>
                            <Skeleton variant="rectangular" height={60} width="100%" />
                        </ListItem>
                    ))
                ) : conversations.length === 0 ? (
                    <Typography color="text.secondary" align="center">
                        Aucune conversation
                    </Typography>
                ) : (
                    conversations.map((conv) => (
                        <ListItem 
                            key={conv.id} 
                            disablePadding
                            secondaryAction={
                                <IconButton 
                                    edge="end" 
                                    aria-label="delete"
                                    onClick={(e) => handleDelete(conv.id, e)}
                                >
                                    <DeleteIcon />
                                </IconButton>
                            }
                        >
                            <ListItemButton onClick={() => navigate(`/chat/${conv.id}`)}>
                                <ListItemText 
                                    primary={conv.title || 'Nouvelle conversation'}
                                    secondary={
                                        <>
                                            <Typography variant="body2" color="text.secondary">
                                                {new Date(conv.timestamp).toLocaleString()}
                                            </Typography>
                                            {conv.messageCount > 0 && (
                                                <Typography variant="body2" color="text.secondary">
                                                    {conv.messageCount} messages
                                                </Typography>
                                            )}
                                        </>
                                    }
                                />
                            </ListItemButton>
                        </ListItem>
                    ))
                )}
            </List>
        </Paper>
    );
};
