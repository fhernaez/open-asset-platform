import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Alert, Button, Card, Form, Input, Typography } from "antd";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthProvider";

interface LoginForm {
  email: string;
  password: string;
}

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onFinish(values: LoginForm) {
    setSubmitting(true);
    setError(null);
    try {
      await login(values.email, values.password);
      navigate("/assets");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Credenciales inválidas");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f5f5f5" }}>
      <Card style={{ width: 380 }}>
        <Typography.Title level={3} style={{ textAlign: "center" }}>
          Open Asset Platform
        </Typography.Title>
        {error && <Alert type="error" message={error} showIcon style={{ marginBottom: 16 }} />}
        <Form<LoginForm> onFinish={onFinish} layout="vertical" requiredMark={false}>
          <Form.Item name="email" label="Email" rules={[{ required: true, type: "email" }]}>
            <Input prefix={<MailOutlined />} autoComplete="username" />
          </Form.Item>
          <Form.Item name="password" label="Contraseña" rules={[{ required: true }]}>
            <Input.Password prefix={<LockOutlined />} autoComplete="current-password" />
          </Form.Item>
          <Button type="primary" htmlType="submit" block loading={submitting}>
            Ingresar
          </Button>
        </Form>
      </Card>
    </div>
  );
}
