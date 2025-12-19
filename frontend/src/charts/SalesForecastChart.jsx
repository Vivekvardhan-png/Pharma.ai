import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";

export default function SalesForecastChart({ history, forecast }) {
  const data = [
    ...history.map((p) => ({ date: p.date, history: p.quantity, forecast: null })),
    ...forecast.map((p) => ({ date: p.date, history: null, forecast: p.quantity }))
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="history" stroke="#1976d2" dot={false} name="Actual" />
        <Line type="monotone" dataKey="forecast" stroke="#ff9800" dot={false} name="Forecast" />
      </LineChart>
    </ResponsiveContainer>
  );
}




