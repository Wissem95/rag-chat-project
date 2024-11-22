import { FC, useState, useEffect } from 'react';
import {
    Box,
    Button,
    Paper,
    Typography,
    List,
    ListItem,
    ListItemText,
    CircularProgress
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

interface Document {
    name: string;
    size: number;
}

export const DocumentUpload: FC = () => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchDocuments = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await fetch('http://localhost:8000/api/documents/list');
            if (!response.ok) {
                throw new Error('Failed to fetch documents');
            }
            const data = await response.json();
            setDocuments(data.documents || []);
        } catch (error) {
            console.error('Error fetching documents:', error);
            setError('Failed to load documents');
            setDocuments([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDocuments();
    }, []);

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        if (!event.target.files?.length) return;

        try {
            setUploading(true);
            setError(null);
            const formData = new FormData();
            
            for (let i = 0; i < event.target.files.length; i++) {
                formData.append('files', event.target.files[i]);
            }

            const response = await fetch('http://localhost:8000/api/documents/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            await fetchDocuments();
        } catch (error) {
            console.error('Upload error:', error);
            setError('Failed to upload documents');
        } finally {
            setUploading(false);
        }
    };

    return (
        <Paper elevation={3} sx={{ p: 2, m: 2 }}>
            <Typography variant="h6" gutterBottom>
                Documents
            </Typography>

            {error && (
                <Typography color="error" sx={{ mb: 2 }}>
                    {error}
                </Typography>
            )}

            <Box sx={{ mb: 2 }}>
                <input
                    accept=".txt,.md,.pdf"
                    style={{ display: 'none' }}
                    id="raised-button-file"
                    multiple
                    type="file"
                    onChange={handleFileUpload}
                />
                <label htmlFor="raised-button-file">
                    <Button
                        variant="contained"
                        component="span"
                        startIcon={<CloudUploadIcon />}
                        disabled={uploading}
                    >
                        {uploading ? 'Uploading...' : 'Upload Documents'}
                    </Button>
                </label>
            </Box>

            {loading ? (
                <CircularProgress />
            ) : documents.length === 0 ? (
                <Typography color="text.secondary" align="center">
                    No documents found
                </Typography>
            ) : (
                <List>
                    {documents.map((doc, index) => (
                        <ListItem key={index}>
                            <ListItemText
                                primary={doc.name}
                                secondary={`Size: ${(doc.size / 1024).toFixed(2)} KB`}
                            />
                        </ListItem>
                    ))}
                </List>
            )}
        </Paper>
    );
};
