import { Spin } from "antd";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./auth/AuthProvider";
import ErrorBoundary from "./components/ErrorBoundary";
import { SCREENS, isScreenImplemented } from "./features/flags";
import MainLayout from "./layouts/MainLayout";
import AdminPage from "./pages/AdminPage";
import AssetsPage from "./pages/AssetsPage";
import ComingSoonPage from "./pages/ComingSoonPage";
import ConnectivityPage from "./pages/ConnectivityPage";
import DashboardsPage from "./pages/DashboardsPage";
import LoginPage from "./pages/LoginPage";
import MapsPage from "./pages/MapsPage";
import PluginsPage from "./pages/PluginsPage";
import TelemetryPage from "./pages/TelemetryPage";

function ProtectedLayout() {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Spin size="large" />
      </div>
    );
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return <MainLayout />;
}

const IMPLEMENTED_PAGES: Record<string, React.ReactNode> = {
  assets: <AssetsPage />,
  connectivity: <ConnectivityPage />,
  telemetry: <TelemetryPage />,
  plugins: <PluginsPage />,
  dashboards: <DashboardsPage />,
  maps: <MapsPage />,
  admin: <AdminPage />,
};

function screenElement(key: string) {
  if (isScreenImplemented(key) && IMPLEMENTED_PAGES[key]) {
    return IMPLEMENTED_PAGES[key];
  }
  const screen = SCREENS.find((s) => s.key === key);
  if (!screen) {
    return <ComingSoonPage gate="G2" labelKey="common.unknownScreen" />;
  }
  return <ComingSoonPage gate={screen.gate} labelKey={screen.labelKey} />;
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedLayout />}>
            <Route path="/" element={<Navigate to="/assets" replace />} />
            {SCREENS.map((screen) => (
              <Route key={screen.key} path={`/${screen.key}`} element={screenElement(screen.key)} />
            ))}
            <Route path="*" element={<ComingSoonPage gate="G2" labelKey="common.unknownScreen" />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}
