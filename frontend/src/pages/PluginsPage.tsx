import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Alert, Empty, Popconfirm, Switch, Table, Tag, Typography, message } from "antd";
import { useTranslation } from "react-i18next";
import { listPlugins, setPluginEnabled } from "../api/endpoints";
import type { PluginSummary } from "../api/types";

export default function PluginsPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();

  const plugins = useQuery({ queryKey: ["plugins"], queryFn: () => listPlugins() });

  const toggleMutation = useMutation({
    mutationFn: ({ slug, enabled }: { slug: string; enabled: boolean }) => setPluginEnabled(slug, enabled),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["plugins"] }),
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  if (plugins.isError) {
    return <Alert type="error" showIcon message={t("plugins.loadError")} />;
  }
  if (!plugins.data || plugins.data.length === 0) {
    return <Empty description={t("plugins.noData")} />;
  }

  return (
    <div style={{ maxWidth: 960 }}>
      <Typography.Title level={4} style={{ margin: 0 }}>
        {t("plugins.title")}
      </Typography.Title>
      <Table<PluginSummary>
        rowKey="slug"
        dataSource={plugins.data}
        loading={plugins.isLoading}
        pagination={false}
        style={{ marginTop: 16 }}
        columns={[
          { title: t("plugins.slug"), dataIndex: "slug" },
          { title: t("plugins.name"), dataIndex: "name" },
          { title: t("plugins.version"), dataIndex: "version" },
          {
            title: t("plugins.core"),
            dataIndex: "is_core",
            render: (v: boolean) => (v ? <Tag>core</Tag> : <Tag color="purple">plugin</Tag>),
          },
          {
            title: t("plugins.health"),
            dataIndex: "health",
            render: (v: string) => <Tag color={v === "healthy" ? "green" : "default"}>{v}</Tag>,
          },
          {
            title: t("plugins.enabled"),
            render: (_, record) => (
              <Popconfirm
                title={t("plugins.toggleConfirm")}
                disabled={record.is_core || record.locked}
                onConfirm={() => toggleMutation.mutate({ slug: record.slug, enabled: !record.enabled })}
              >
                <Switch
                  checked={record.enabled}
                  disabled={record.is_core || record.locked}
                  loading={toggleMutation.isPending}
                />
              </Popconfirm>
            ),
          },
          {
            title: t("plugins.locked"),
            dataIndex: "locked",
            render: (v: boolean) => (v ? <Tag color="orange">{t("plugins.lockedTag")}</Tag> : null),
          },
        ]}
      />
    </div>
  );
}
