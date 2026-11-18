import { SaveOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Alert, Button, Card, Empty, Form, Input, Select, Space, Table, Tag, Typography, message } from "antd";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { listUsers, updateTenant } from "../api/endpoints";
import { useAppContext } from "../contexts/AppContext";

export default function AdminPage() {
  const { t } = useTranslation();
  const { tenant, tenantId } = useAppContext();
  const queryClient = useQueryClient();
  const [form] = Form.useForm();

  const users = useQuery({ queryKey: ["users"], queryFn: () => listUsers() });

  useEffect(() => {
    if (tenant) {
      form.setFieldsValue({ name: tenant.name, slug: tenant.slug, locale: tenant.locale ?? "es" });
    }
  }, [tenant, form]);

  const mutation = useMutation({
    mutationFn: (input: { name: string; slug: string; locale: string }) =>
      updateTenant(tenantId ?? "", input),
    onSuccess: () => {
      message.success(t("admin.saved"));
      queryClient.invalidateQueries({ queryKey: ["tenants"] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%", maxWidth: 960 }}>
      <Typography.Title level={4} style={{ margin: 0 }}>
        {t("admin.title")}
      </Typography.Title>

      <Card title={t("admin.orgSettings")}>
        <Form
          form={form}
          layout="vertical"
          onFinish={(values) => mutation.mutate(values)}
        >
          <Form.Item name="name" label={t("org.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="slug" label={t("org.slug")} rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
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
          <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={mutation.isPending}>
            {t("common.save")}
          </Button>
        </Form>
      </Card>

      <Card title={t("admin.users")}>
        {users.isError && <Alert type="error" showIcon message={t("admin.usersError")} />}
        {users.data?.results.length === 0 && <Empty />}
        {(users.data?.results.length ?? 0) > 0 && (
          <Table
            rowKey="id"
            size="small"
            dataSource={users.data?.results ?? []}
            loading={users.isLoading}
            pagination={false}
            columns={[
              { title: t("auth.email"), dataIndex: "email" },
              { title: t("admin.fullName"), dataIndex: "full_name" },
              {
                title: t("admin.platformAdmin"),
                dataIndex: "is_platform_admin",
                render: (v: boolean) => (v ? <Tag color="blue">admin</Tag> : null),
              },
            ]}
          />
        )}
      </Card>
    </Space>
  );
}
