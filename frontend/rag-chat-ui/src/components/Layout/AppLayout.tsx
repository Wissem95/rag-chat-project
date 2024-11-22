import { FC, ReactNode } from 'react';
import { Box, Container } from '@mui/material';
import { Header } from '../Layout/Header';

interface AppLayoutProps {
    children: ReactNode;
}

export const AppLayout: FC<AppLayoutProps> = ({ children }) => {
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Header />
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    pt: '64px', // Hauteur de la barre d'outils
                    pb: 3,
                    px: 2
                }}
            >
                <Container maxWidth="lg">
                    {children}
                </Container>
            </Box>
        </Box>
    );
};
