import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ConfigProvider } from "antd";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { AuthProvider } from "./auth/AuthProvider";

async function enableMocks(): Promise<void> {
  if (import.meta.env.VITE_ENABLE_MOCKS !== "true") {
    return;
  }
  const { worker } = await import("./mocks/browser");
  await worker.start({ onUnhandledRequest: "bypass" });
}

const queryClient = new QueryClient();

enableMocks().then(() => {
  ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <ConfigProvider theme={{ token: { colorPrimary: "#1677ff" } }}>
          <AuthProvider>
            <App />
          </AuthProvider>
        </ConfigProvider>
      </QueryClientProvider>
    </React.StrictMode>,
  );
});
