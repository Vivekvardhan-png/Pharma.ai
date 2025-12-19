import { useState } from "react";
import { Box, Button, Paper, Typography } from "@mui/material";
import { uploadInventoryFile, uploadSalesFile } from "../services/api";

export default function UploadPage() {
  const [invFile, setInvFile] = useState(null);
  const [salesFile, setSalesFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async (type) => {
    try {
      if (type === "inventory" && invFile) {
        await uploadInventoryFile(invFile);
        setMessage("Inventory uploaded successfully.");
      } else if (type === "sales" && salesFile) {
        await uploadSalesFile(salesFile);
        setMessage("Sales uploaded successfully.");
      }
    } catch (e) {
      setMessage(e.response?.data?.detail || "Upload failed");
    }
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Excel Uploads
      </Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1">Inventory file</Typography>
        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={(e) => setInvFile(e.target.files?.[0] || null)}
        />
        <Button
          sx={{ mt: 1 }}
          variant="contained"
          onClick={() => handleUpload("inventory")}
          disabled={!invFile}
        >
          Upload Inventory
        </Button>
      </Paper>
      <Paper sx={{ p: 2 }}>
        <Typography variant="subtitle1">Sales file</Typography>
        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={(e) => setSalesFile(e.target.files?.[0] || null)}
        />
        <Button
          sx={{ mt: 1 }}
          variant="contained"
          onClick={() => handleUpload("sales")}
          disabled={!salesFile}
        >
          Upload Sales
        </Button>
      </Paper>
      {message && (
        <Typography sx={{ mt: 2 }} color="text.secondary">
          {message}
        </Typography>
      )}
    </Box>
  );
}



