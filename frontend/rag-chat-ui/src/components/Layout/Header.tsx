import { FC } from 'react';
import { 
    AppBar, 
    Toolbar, 
    Typography, 
    IconButton,
    useTheme
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

export const Header: FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const theme = useTheme();

    const showBackButton = location.pathname !== '/';

    return (
        <AppBar position="fixed" sx={{ zIndex: theme.zIndex.drawer + 1 }}>
            <Toolbar>
                {showBackButton && (
                    <IconButton
                        edge="start"
                        color="inherit"
                        onClick={() => navigate(-1)}
                        sx={{ mr: 2 }}
                    >
                        <ArrowBackIcon />
                    </IconButton>
                )}
                
                <Typography 
                    variant="h6" 
                    component="div"
                    sx={{ 
                        cursor: 'pointer',
                        flexGrow: 1,
                        fontWeight: 'bold'
                    }}
                    onClick={() => navigate('/')}
                >
                    RAG Chat
                </Typography>
            </Toolbar>
        </AppBar>
    );
};
