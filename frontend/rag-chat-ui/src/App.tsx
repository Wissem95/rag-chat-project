import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { AppLayout } from './components/Layout/AppLayout';
import { ChatWindow } from './components/Chat/ChatWindow';
import { ConversationList } from './components/Conversations/ConversationList';
import { darkTheme } from './theme';

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <AppLayout>
          <Routes>
            <Route path="/" element={<ConversationList />} />
            <Route path="/chat/:conversationId?" element={<ChatWindow />} />
          </Routes>
        </AppLayout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
