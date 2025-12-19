import { useState } from "react";
import {
  Box,
  Button,
  Paper,
  TextField,
  Typography,
  List,
  ListItem,
  ListItemText
} from "@mui/material";
import { askChatbot } from "../services/api";

export default function ChatbotPage() {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!query.trim()) return;
    const userMsg = { from: "user", text: query };
    setHistory((h) => [...h, userMsg]);
    setLoading(true);
    try {
      const res = await askChatbot(query);
      const botMsg = { from: "bot", text: res.text, raw: res };
      setHistory((h) => [...h, botMsg]);
    } finally {
      setLoading(false);
      setQuery("");
    }
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>
        AI Inventory Assistant
      </Typography>
      <Paper sx={{ p: 2, mb: 2, height: 400, overflow: "auto" }}>
        <List>
          {history.map((m, idx) => (
            <ListItem key={idx} alignItems="flex-start">
              <ListItemText
                primary={m.from === "user" ? "You" : "Assistant"}
                secondary={m.text}
              />
            </ListItem>
          ))}
          {history.length === 0 && (
            <Typography color="text.secondary">
              Try questions like &quot;How many Paracetamol are left?&quot; or
              &quot;Which medicines expire this week?&quot;
            </Typography>
          )}
        </List>
      </Paper>
      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          size="small"
          placeholder="Ask a question about inventory..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") send();
          }}
        />
        <Button variant="contained" onClick={send} disabled={loading}>
          Send
        </Button>
      </Box>
    </Box>
  );
}




