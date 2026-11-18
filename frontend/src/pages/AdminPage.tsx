import { PlusOutlined, SaveOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Card,
  Empty,
  Form,
  Input,
  Modal,
  Popconfirm,
  Select,
  Space,
  Switch,
  Table,
  Tabs,
  Tag,
  message,
} from "antd";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  createProject,
  deleteProject,
  listProjects,
  listTenants,
  listUsers,
  updateTenant,
} from "../api/endpoints";
import type { Project, Tenant } from "../api/types";
import { useAppContext } from "../contexts/AppContext";
import { slugify } from "../utils/slugify";

interface UserRow {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_platform_admin: boolean;
  locale?: string;
  timezone?: string;
}

export default function AdminPage() {
  const { t } = useTranslation();
  return (
    <Tabs
      defaultActiveKey="settings"
      items={[
        { key: "settings", label: t("admin.settingsTab"), children: <SettingsTab /> },
        { key: "users", label: t("admin.users"), children: <UsersTab /> },
        { key: "projects", label: t("common.project"), children: <ProjectsTab /> },
      ]}
    />
  );
}

function SettingsTab() {
  const { t } = useTranslation();
  const { tenant, tenantId } = useAppContext();
  const queryClient = useQueryClient();
  const [form] = Form.useForm();

  useEffect(() => {
    if (tenant) {
      form.setFieldsValue({
        name: tenant.name,
        slug: tenant.slug,
        locale: tenant.locale ?? "es",
        timezone: tenant.timezone ?? "America/Argentina/Buenos_Aires",
      });
    }
  }, [tenant, form]);

  const mutation = useMutation({
    mutationFn: (input: { name: string; slug: string; locale: string; timezone: string }) =>
      updateTenant(tenantId ?? "", input),
    onSuccess: () => {
      message.success(t("admin.saved"));
      queryClient.invalidateQueries({ queryKey: ["tenants"] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Card title={t("admin.orgSettings")} style={{ maxWidth: 640 }}>
      <Form form={form} layout="vertical" onFinish={(values) => mutation.mutate(values)}>
        <Form.Item name="name" label={t("org.name")} rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="slug" label={t("common.code")} rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
          <Input />
        </Form.Item>
        <Form.Item name="locale" label={t("admin.locale")}>
          <Select
            options={[
              { value: "es", label: "Español" },
              { value: "en", label: "English" },
            ]}
          />
        </Form.Item>
        <Form.Item name="timezone" label={t("admin.timezone")}>
          <Select
            showSearch
            options={[
              { value: "America/Argentina/Buenos_Aires", label: "America/Argentina/Buenos_Aires" },
              { value: "Europe/Madrid", label: "Europe/Madrid" },
              { value: "UTC", label: "UTC" },
            ]}
          />
        </Form.Item>
        <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={mutation.isPending}>
          {t("common.save")}
        </Button>
      </Form>
    </Card>
  );
}

function UsersTab() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const [createOpen, setCreateOpen] = useState(false);
  const [editing, setEditing] = useState<UserRow | null>(null);
  const [form] = Form.useForm();
  const [editForm] = Form.useForm();

  const users = useQuery({ queryKey: ["users"], queryFn: () => listUsers() });
  const tenants = useQuery({ queryKey: ["tenants"], queryFn: () => listTenants() });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["users"] });

  const createMutation = useMutation({
    mutationFn: (input: Record<string, unknown>) =>
      fetch("/api/v1/platform/users/", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("oap.access")}` },
        body: JSON.stringify(input),
      }).then((r) => {
        if (!r.ok) return r.json().then((b) => Promise.reject(new Error(b.detail ?? "Error")));
        return r.json();
      }),
    onSuccess: () => {
      message.success(t("admin.userCreated"));
      setCreateOpen(false);
      form.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: Record<string, unknown> }) =>
      fetch(`/api/v1/platform/users/${id}/`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("oap.access")}` },
        body: JSON.stringify(input),
      }).then((r) => {
        if (!r.ok) return r.json().then((b) => Promise.reject(new Error(b.detail ?? "Error")));
        return r.json();
      }),
    onSuccess: () => {
      message.success(t("common.save"));
      setEditing(null);
      editForm.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const toggleMutation = useMutation({
    mutationFn: ({ id, active }: { id: string; active: boolean }) =>
      updateMutation.mutateAsync({ id, input: { is_active: active } }),
    onSuccess: invalidate,
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Button type="primary" icon={<PlusOutlined />} onClick={() => setCreateOpen(true)}>
        {t("admin.newUser")}
      </Button>
      {users.isError && <Alert type="error" showIcon message={t("admin.usersError")} />}
      {users.data?.results.length === 0 && <Empty />}
      {(users.data?.results.length ?? 0) > 0 && (
        <Table<UserRow>
          rowKey="id"
          dataSource={users.data?.results ?? []}
          loading={users.isLoading}
          pagination={false}
          columns={[
            { title: t("auth.email"), dataIndex: "email" },
            { title: t("admin.fullName"), dataIndex: "full_name" },
            { title: t("admin.locale"), dataIndex: "locale", render: (v?: string) => v ?? "—" },
            { title: t("admin.timezone"), dataIndex: "timezone", render: (v?: string) => v ?? "—" },
            {
              title: t("admin.platformAdmin"),
              dataIndex: "is_platform_admin",
              render: (v: boolean) => (v ? <Tag color="blue">admin</Tag> : null),
            },
            {
              title: t("admin.active"),
              render: (_, record) => (
                <Switch
                  size="small"
                  checked={record.is_active}
                  onChange={(checked) => toggleMutation.mutate({ id: record.id, active: checked })}
                />
              ),
            },
            {
              title: t("common.actions"),
              render: (_, record) => (
                <Button
                  size="small"
                  onClick={() => {
                    setEditing(record);
                    editForm.setFieldsValue(record);
                  }}
                >
                  {t("common.edit")}
                </Button>
              ),
            },
          ]}
        />
      )}

      <Modal
        title={t("admin.newUser")}
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => form.submit()}
        confirmLoading={createMutation.isPending}
        width={560}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{ locale: "es", timezone: "America/Argentina/Buenos_Aires" }}
          onFinish={(values: { email: string; full_name: string; password: string; locale: string; timezone: string; tenant?: string; role?: string }) =>
            createMutation.mutate(values)
          }
        >
          <Form.Item name="email" label={t("auth.email")} rules={[{ required: true, type: "email" }]}>
            <Input />
          </Form.Item>
          <Form.Item name="full_name" label={t("admin.fullName")}>
            <Input />
          </Form.Item>
          <Form.Item name="password" label={t("admin.initialPassword")} rules={[{ required: true, min: 8 }]}>
            <Input.Password />
          </Form.Item>
          <Form.Item name="locale" label={t("admin.locale")}>
            <Select
              options={[
                { value: "es", label: "Español" },
                { value: "en", label: "English" },
              ]}
            />
          </Form.Item>
          <Form.Item name="timezone" label={t("admin.timezone")}>
            <Select
              showSearch
              options={[
                { value: "America/Argentina/Buenos_Aires", label: "America/Argentina/Buenos_Aires" },
                { value: "Europe/Madrid", label: "Europe/Madrid" },
                { value: "UTC", label: "UTC" },
              ]}
            />
          </Form.Item>
          <Form.Item name="tenant" label={t("common.organization")}>
            <Select
              options={(tenants.data?.results ?? []).map((item: Tenant) => ({ value: item.id, label: item.name }))}
            />
          </Form.Item>
          <Form.Item name="role" label={t("admin.role")}>
            <Select
              options={[
                { value: "tenant_admin", label: "tenant_admin" },
                { value: "operator", label: "operator" },
                { value: "viewer", label: "viewer" },
              ]}
            />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={t("common.edit")}
        open={Boolean(editing)}
        onCancel={() => setEditing(null)}
        onOk={() => editForm.submit()}
        confirmLoading={updateMutation.isPending}
      >
        <Form
          form={editForm}
          layout="vertical"
          onFinish={(values) => {
            if (editing) updateMutation.mutate({ id: editing.id, input: values });
          }}
        >
          <Form.Item name="full_name" label={t("admin.fullName")}>
            <Input />
          </Form.Item>
          <Form.Item name="locale" label={t("admin.locale")}>
            <Select
              options={[
                { value: "es", label: "Español" },
                { value: "en", label: "English" },
              ]}
            />
          </Form.Item>
          <Form.Item name="timezone" label={t("admin.timezone")}>
            <Select
              showSearch
              options={[
                { value: "America/Argentina/Buenos_Aires", label: "America/Argentina/Buenos_Aires" },
                { value: "Europe/Madrid", label: "Europe/Madrid" },
                { value: "UTC", label: "UTC" },
              ]}
            />
          </Form.Item>
        </Form>
      </Modal>
    </Space>
  );
}

function ProjectsTab() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [form] = Form.useForm();

  const projects = useQuery({
    queryKey: ["projects", tenantId],
    queryFn: () => listProjects(tenantId ?? ""),
    enabled: Boolean(tenantId),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["projects", tenantId] });

  const createMutation = useMutation({
    mutationFn: createProject,
    onSuccess: () => {
      message.success(t("admin.projectCreated"));
      setCreateOpen(false);
      form.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteProject(id),
    onSuccess: invalidate,
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
        {t("project.create")}
      </Button>
      <Table<Project>
        rowKey="id"
        dataSource={projects.data?.results ?? []}
        loading={projects.isLoading}
        pagination={false}
        columns={[
          { title: t("assets.name"), dataIndex: "name" },
          { title: t("common.code"), dataIndex: "code" },
          { title: t("admin.lifecycle"), dataIndex: "lifecycle_status" },
          {
            title: t("common.actions"),
            render: (_, record) => (
              <Popconfirm title={t("admin.projectDeleteConfirm")} onConfirm={() => deleteMutation.mutate(record.id)}>
                <Button size="small" danger>
                  {t("common.delete")}
                </Button>
              </Popconfirm>
            ),
          },
        ]}
      />
      <Modal
        title={t("project.create")}
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => form.submit()}
        confirmLoading={createMutation.isPending}
      >
        <Form
          form={form}
          layout="vertical"
          onValuesChange={(changed, values) => {
            if ("name" in changed && typeof values.name === "string") {
              form.setFieldValue("code", slugify(values.name));
            }
          }}
          onFinish={(values: { name: string; code: string }) => {
            if (!tenantId) return;
            createMutation.mutate({ tenant: tenantId, name: values.name, code: values.code });
          }}
        >
          <Form.Item name="name" label={t("assets.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item
            name="code"
            label={t("common.code")}
            rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}
            extra={t("common.codeHelp")}
          >
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </Space>
  );
}
