import { Grid, Paper, Typography } from "@mui/material";

export default function KpiCards({ medicines, alerts }) {
  const totalSkus = medicines.length;
  const lowStockItems = medicines.filter((m) => m.total_stock < 10).length;
  const expiringSoon = 0; // could be filled from dedicated endpoint
  const wastageValue = 0; // placeholder for wastage analytics

  const items = [
    { label: "Total SKUs", value: totalSkus },
    { label: "Low stock items", value: lowStockItems },
    { label: "Expiring soon", value: expiringSoon },
    { label: "Wastage value", value: wastageValue }
  ];

  return (
    <Grid container spacing={2} sx={{ mb: 2 }}>
      {items.map((kpi) => (
        <Grid item xs={12} sm={6} md={3} key={kpi.label}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle2" color="text.secondary">
              {kpi.label}
            </Typography>
            <Typography variant="h5">{kpi.value}</Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}



