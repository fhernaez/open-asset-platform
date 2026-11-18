import { LogoutOutlined, PlusOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Avatar, Button, Dropdown, Form, Input, Layout, Menu, Modal, Select, Space, Typography, message } from "antd";
import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { createProject, createTenant, listProjects } from "../api/endpoints";
import { useAuth } from "../auth/AuthProvider";
import { useAppContext } from "../contexts/AppContext";
import { SCREENS } from "../features/flags";

const { Header, Sider, Content } = Layout;

export default function MainLayout() {
  const { user, logout } = useAuth();
  const { tenantId, setTenantId, projectId, setProjectId, tenants, loading } = useAppContext();
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const [tenantModalOpen, setTenantModalOpen] = useState(false);
  const [projectModalOpen, setProjectModalOpen] = useState(false);
  const [tenantForm] = Form.useForm();
  const [projectForm] = Form.useForm();

  const projectsQuery = useQuery({
    queryKey: ["projects", tenantId],
    queryFn: () => listProjects(tenantId ?? ""),
    enabled: Boolean(tenantId),
  });
  const projects = projectsQuery.data?.results ?? [];

  const tenantMutation = useMutation({
    mutationFn: createTenant,
    onSuccess: (tenant) => {
      message.success(t("types.createSuccess"));
      setTenantModalOpen(false);
      tenantForm.resetFields();
      queryClient.invalidateQueries({ queryKey: ["tenants"] });
      setTenantId(tenant.id);
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const projectMutation = useMutation({
    mutationFn: createProject,
    onSuccess: (project) => {
      message.success(t("types.createSuccess"));
      setProjectModalOpen(false);
      projectForm.resetFields();
      queryClient.invalidateQueries({ queryKey: ["projects", tenantId] });
      setProjectId(project.id);
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const menuItems = useMemo(
    () =>
      SCREENS.map((screen) => ({
        key: screen.key,
        label: t(screen.labelKey),
      })),
    [t],
  );

  const selectedKey = useMemo(() => {
    const path = location.pathname.split("/")[1];
    return SCREENS.some((s) => s.key === path) ? path : "assets";
  }, [location.pathname]);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth={0}>
        <div style={{ color: "#fff", padding: 16, fontWeight: 600 }}>{t("app.title")}</div>
        <Menu
          theme="dark"
          mode="inline"
          items={menuItems}
          selectedKeys={[selectedKey]}
          onClick={({ key }) => navigate(`/${key}`)}
        />
      </Sider>
      <Layout>
        <Header
          style={{
            background: "#fff",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 12,
            paddingInline: 16,
          }}
        >
          <Space wrap>
            <Select
              style={{ minWidth: 200 }}
              placeholder={t("common.organization")}
              loading={loading}
              value={tenantId}
              onChange={(value) => {
                setTenantId(value);
                setProjectId(undefined);
              }}
              options={tenants.map((item) => ({ value: item.id, label: item.name }))}
            />
            <Button icon={<PlusOutlined />} onClick={() => setTenantModalOpen(true)}>
              {t("org.create")}
            </Button>
            <Select
              style={{ minWidth: 200 }}
              placeholder={t("common.project")}
              disabled={!tenantId}
              value={projectId}
              allowClear
              onChange={(value) => setProjectId(value)}
              options={projects}
            />
            <Button icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setProjectModalOpen(true)}>
              {t("project.create")}
            </Button>
          </Space>
          <Space>
            <Typography.Text>{user?.email}</Typography.Text>
            <Dropdown
              menu={{
                items: [
                  {
                    key: "logout",
                    icon: <LogoutOutlined />,
                    label: t("auth.logout"),
                    onClick: () => {
                      logout();
                      navigate("/login");
                    },
                  },
                ],
              }}
            >
              <Button type="text">
                <Avatar size="small" style={{ background: "#1677ff" }}>
                  {user?.email?.charAt(0).toUpperCase()}
                </Avatar>
              </Button>
            </Dropdown>
          </Space>
        </Header>
        <Content style={{ padding: 24 }}>
          <Outlet />
          <Typography.Text type="secondary" style={{ display: "block", marginTop: 16, fontSize: 12 }}>
            OAP {__APP_VERSION__}
          </Typography.Text>
        </Content>
      </Layout>

      <Modal
        title={t("org.create")}
        open={tenantModalOpen}
        onCancel={() => setTenantModalOpen(false)}
        onOk={() => tenantForm.submit()}
        confirmLoading={tenantMutation.isPending}
      >
        <Form
          form={tenantForm}
          layout="vertical"
          onFinish={(values: { name: string; slug: string }) => tenantMutation.mutate(values)}
        >
          <Form.Item name="name" label={t("org.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="slug" label={t("org.slug")} rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={t("project.create")}
        open={projectModalOpen}
        onCancel={() => setProjectModalOpen(false)}
        onOk={() => projectForm.submit()}
        confirmLoading={projectMutation.isPending}
      >
        <Form
          form={projectForm}
          layout="vertical"
          onFinish={(values: { name: string; code: string }) => {
            if (!tenantId) return;
            projectMutation.mutate({ tenant: tenantId, ...values });
          }}
        >
          <Form.Item name="name" label={t("assets.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="code" label={t("project.code")} rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  );
}
