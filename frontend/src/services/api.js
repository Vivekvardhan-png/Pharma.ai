import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL
});

export const fetchDashboard = async () => {
  const [medicinesRes, alertsRes] = await Promise.all([
    api.get("/inventory/medicines"),
    api.get("/alerts")
  ]);
  return {
    medicines: medicinesRes.data,
    alerts: alertsRes.data
  };
};

export const fetchForecast = (medicineId) =>
  api.get(`/forecast/medicine/${medicineId}`).then((r) => r.data);

export const uploadInventoryFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload/inventory", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};

export const uploadSalesFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload/sales", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};

export const askChatbot = (query) =>
  api.post("/chatbot", { query }).then((r) => r.data);



