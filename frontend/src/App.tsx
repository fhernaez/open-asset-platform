import { useCallback, useEffect, useState } from "react";
import { apiFetch, login, setToken } from "./api";

interface Asset {
  id: string;
  name: string;
  external_ref: string;
  status: string;
}

interface Tenant {
  id: string;
  name: string;
  slug: string;
}

interface Project {
  id: string;
  tenant: string;
  name: string;
  code: string;
}

export default function App() {
  const [authed, setAuthed] = useState<boolean>(() => Boolean(localStorage.getItem("oap.access")));
  if (!authed) {
    return <Login onSuccess={() => setAuthed(true)} />;
  }
  return <Dashboard onLogout={() => { setToken(null); setAuthed(false); }} />;
}

function Login({ onSuccess }: { onSuccess: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      onSuccess();
    } catch {
      setError("Invalid credentials");
    }
  }

  return (
    <form onSubmit={submit} style={{ maxWidth: 360, margin: "80px auto" }}>
      <h1>Open Asset Platform</h1>
      <label>Email <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required /></label>
      <label>Password <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required /></label>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button type="submit">Sign in</button>
    </form>
  );
}

function Dashboard({ onLogout }: { onLogout: () => void }) {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [tenantId, setTenantId] = useState("");
  const [projectId, setProjectId] = useState("");
  const [newAsset, setNewAsset] = useState("");

  useEffect(() => {
    apiFetch<{ results: Tenant[] }>("/platform/tenants/").then((r) => setTenants(r.results)).catch(() => {});
  }, []);

  useEffect(() => {
    if (!tenantId) return;
    apiFetch<{ results: Project[] }>(`/platform/projects/?tenant=${tenantId}`).then((r) => setProjects(r.results)).catch(() => {});
  }, [tenantId]);

  const loadAssets = useCallback(async () => {
    const q = projectId ? `?project=${projectId}` : "";
    const r = await apiFetch<{ results: Asset[] }>(`/assets/assets/${q}`);
    setAssets(r.results);
  }, [projectId]);

  useEffect(() => {
    if (projectId) loadAssets();
  }, [projectId, loadAssets]);

  async function createAsset(e: React.FormEvent) {
    e.preventDefault();
    if (!tenantId || !projectId) return;
    await apiFetch("/assets/assets/", {
      method: "POST",
      body: JSON.stringify({ tenant: tenantId, project: projectId, name: newAsset, external_ref: newAsset }),
    });
    setNewAsset("");
    loadAssets();
  }

  return (
    <div style={{ padding: 24 }}>
      <header style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>OAP Assets</h1>
        <button onClick={onLogout}>Sign out</button>
      </header>
      <label>Tenant{" "}
        <select value={tenantId} onChange={(e) => setTenantId(e.target.value)}>
          <option value="">—</option>
          {tenants.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
        </select>
      </label>{" "}
      <label>Project{" "}
        <select value={projectId} onChange={(e) => setProjectId(e.target.value)}>
          <option value="">—</option>
          {projects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
      </label>
      <form onSubmit={createAsset} style={{ margin: "16px 0" }}>
        <input value={newAsset} onChange={(e) => setNewAsset(e.target.value)} placeholder="New asset name" />
        <button type="submit">Add asset</button>
      </form>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr><th>Name</th><th>Ref</th><th>Status</th></tr>
        </thead>
        <tbody>
          {assets.map((a) => (
            <tr key={a.id}><td>{a.name}</td><td>{a.external_ref}</td><td>{a.status}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
