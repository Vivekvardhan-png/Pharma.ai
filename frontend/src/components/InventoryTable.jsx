import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from "@mui/material";

export default function InventoryTable({ medicines }) {
  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>SKU</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Category (AI)</TableCell>
            <TableCell align="right">Stock</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {medicines.map((m) => (
            <TableRow key={m.id}>
              <TableCell>{m.sku}</TableCell>
              <TableCell>{m.name}</TableCell>
              <TableCell>{m.ai_category || m.category || "-"}</TableCell>
              <TableCell align="right">{m.total_stock}</TableCell>
            </TableRow>
          ))}
          {medicines.length === 0 && (
            <TableRow>
              <TableCell colSpan={4}>
                <Typography align="center" color="text.secondary">
                  No inventory yet. Upload Excel files to get started.
                </Typography>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}



