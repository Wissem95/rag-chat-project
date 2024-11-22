import React from 'react';
import {
    Box,
    Slider,
    Typography,
    Paper,
    IconButton,
    Tooltip,
    Collapse
} from '@mui/material';
import TuneIcon from '@mui/icons-material/Tune';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import { LLMSettings as LLMSettingsType } from '../../types';

interface LLMSettingsProps {
    settings: LLMSettingsType;
    onSettingsChange: (settings: LLMSettingsType) => void;
}

export const LLMSettings: React.FC<LLMSettingsProps> = ({ settings, onSettingsChange }) => {
    const [open, setOpen] = React.useState(false);

    const handleChange = (key: keyof LLMSettingsType) => (_: Event, value: number | number[]) => {
        onSettingsChange({
            ...settings,
            [key]: typeof value === 'number' ? value : value[0]
        });
    };

    return (
        <Paper sx={{ p: 2, mb: 2, backgroundColor: 'background.paper' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <TuneIcon />
                    <Typography variant="h6">Paramètres LLM</Typography>
                </Box>
                <IconButton onClick={() => setOpen(!open)}>
                    <TuneIcon />
                </IconButton>
            </Box>

            <Collapse in={open}>
                <Box sx={{ mt: 2 }}>
                    <Box sx={{ mb: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography>Température</Typography>
                            <Tooltip title="Contrôle la créativité des réponses. Une valeur plus élevée donne des réponses plus créatives mais potentiellement moins précises.">
                                <InfoOutlinedIcon fontSize="small" />
                            </Tooltip>
                        </Box>
                        <Slider
                            value={settings.temperature}
                            onChange={handleChange('temperature')}
                            min={0}
                            max={2}
                            step={0.1}
                            marks={[
                                { value: 0, label: '0' },
                                { value: 1, label: '1' },
                                { value: 2, label: '2' }
                            ]}
                            valueLabelDisplay="auto"
                        />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography>Tokens Maximum</Typography>
                            <Tooltip title="Limite la longueur maximale de la réponse.">
                                <InfoOutlinedIcon fontSize="small" />
                            </Tooltip>
                        </Box>
                        <Slider
                            value={settings.maxTokens}
                            onChange={handleChange('maxTokens')}
                            min={100}
                            max={4000}
                            step={100}
                            marks={[
                                { value: 100, label: '100' },
                                { value: 2000, label: '2000' },
                                { value: 4000, label: '4000' }
                            ]}
                            valueLabelDisplay="auto"
                        />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography>Top P</Typography>
                            <Tooltip title="Contrôle la diversité des réponses.">
                                <InfoOutlinedIcon fontSize="small" />
                            </Tooltip>
                        </Box>
                        <Slider
                            value={settings.topP}
                            onChange={handleChange('topP')}
                            min={0}
                            max={1}
                            step={0.1}
                            marks={[
                                { value: 0, label: '0' },
                                { value: 0.5, label: '0.5' },
                                { value: 1, label: '1' }
                            ]}
                            valueLabelDisplay="auto"
                        />
                    </Box>
                </Box>
            </Collapse>
        </Paper>
    );
};
