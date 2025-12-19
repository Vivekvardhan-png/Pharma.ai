import { useEffect, useState } from "react";
import { Box, CircularProgress, Grid, Paper, Typography } from "@mui/material";
import { fetchDashboard, fetchForecast } from "../services/api";
import KpiCards from "../components/KpiCards";
import InventoryTable from "../components/InventoryTable";
import SalesForecastChart from "../charts/SalesForecastChart";

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [medicines, setMedicines] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [forecast, setForecast] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const d = await fetchDashboard();
        setMedicines(d.medicines);
        setAlerts(d.alerts);
        if (d.medicines.length > 0) {
          const f = await fetchForecast(d.medicines[0].id);
          setForecast(f);
        }
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Dashboard
      </Typography>
      <KpiCards medicines={medicines} alerts={alerts} />
      <Grid container spacing={2}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="subtitle1" sx={{ mb: 1 }}>
              Forecast vs Actual
            </Typography>
            {forecast ? (
              <SalesForecastChart history={forecast.history} forecast={forecast.forecast} />
            ) : (
              <Typography color="text.secondary">No forecast data.</Typography>
            )}
          </Paper>
          <InventoryTable medicines={medicines} />
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" sx={{ mb: 1 }}>
              Alerts
            </Typography>
            {alerts.map((a) => (
              <Box
                key={a.id}
                sx={{
                  mb: 1,
                  p: 1,
                  borderRadius: 1,
                  bgcolor:
                    a.priority === "critical"
                      ? "error.light"
                      : a.priority === "warning"
                      ? "warning.light"
                      : "info.light"
                }}
              >
                <Typography variant="caption" sx={{ fontWeight: 600 }}>
                  {a.type.toUpperCase()} - {a.priority.toUpperCase()}
                </Typography>
                <Typography variant="body2">{a.message}</Typography>
              </Box>
            ))}
            {alerts.length === 0 && (
              <Typography color="text.secondary">No alerts.</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}




