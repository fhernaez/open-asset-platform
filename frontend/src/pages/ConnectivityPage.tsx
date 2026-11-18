import { DeleteOutlined, LinkOutlined, PlusOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Checkbox,
  Drawer,
  Empty,
  Form,
  Input,
  InputNumber,
  Modal,
  Popconfirm,
  Select,
  Space,
  Table,
  Tag,
  Typography,
  message,
} from "antd";
import type { FormInstance } from "antd";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import {
  createBinding,
  createGateway,
  deleteBinding,
  deleteGateway,
  listAssets,
  listAssetTypes,
  listAttributes,
  listBindings,
  listGateways,
} from "../api/endpoints";
import type { Gateway } from "../api/types";
import { useAppContext } from "../contexts/AppContext";

function statusColor(status: string): string {
  return status === "connected" ? "green" : status === "error" ? "red" : "default";
}

export default function ConnectivityPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [selectedGateway, setSelectedGateway] = useState<Gateway | null>(null);
  const [form] = Form.useForm();

  const gateways = useQuery({
    queryKey: ["gateways", tenantId],
    queryFn: () => listGateways({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["gateways", tenantId] });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteGateway(id),
    onSuccess: invalidate,
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Typography.Title level={4} style={{ margin: 0 }}>
        {t("conn.title")}
      </Typography.Title>
      <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
        {t("conn.createGateway")}
      </Button>

      {gateways.isError && <Alert type="error" showIcon message={t("conn.loadError")} />}
      {!gateways.isError && gateways.data?.results.length === 0 && <Empty description={t("conn.noData")} />}

      {(gateways.data?.results.length ?? 0) > 0 && (
        <Table<Gateway>
          rowKey="id"
          dataSource={gateways.data?.results ?? []}
          loading={gateways.isLoading}
          pagination={{ pageSize: 20 }}
          columns={[
            {
              title: t("assets.name"),
              dataIndex: "asset",
              render: (assetId: string) => <span>{assetId.slice(0, 8)}</span>,
            },
            { title: t("conn.protocol"), dataIndex: "protocol", render: (v: string) => <Tag color="purple">{v}</Tag> },
            {
              title: t("conn.status"),
              dataIndex: "connection_status",
              render: (v: string) => <Tag color={statusColor(v)}>{v}</Tag>,
            },
            {
              title: t("common.actions"),
              render: (_, record) => (
                <Space>
                  <Button size="small" icon={<LinkOutlined />} onClick={() => setSelectedGateway(record)}>
                    {t("conn.bindings")}
                  </Button>
                  <Popconfirm title={t("conn.deleteConfirm")} onConfirm={() => deleteMutation.mutate(record.id)}>
                    <Button size="small" danger icon={<DeleteOutlined />} />
                  </Popconfirm>
                </Space>
              ),
            },
          ]}
        />
      )}

      <CreateGatewayModal
        open={createOpen}
        form={form}
        onClose={() => setCreateOpen(false)}
        onCreated={() => {
          setCreateOpen(false);
          form.resetFields();
          invalidate();
        }}
      />

      <BindingsDrawer gateway={selectedGateway} onClose={() => setSelectedGateway(null)} />
    </Space>
  );
}

function CreateGatewayModal({
  open,
  form,
  onClose,
  onCreated,
}: {
  open: boolean;
  form: FormInstance;
  onClose: () => void;
  onCreated: () => void;
}) {
  const { t } = useTranslation();
  const { tenantId, projectId } = useAppContext();
  const [schema, setSchema] = useState<Record<string, unknown>[]>([]);

  const types = useQuery({
    queryKey: ["asset-types", tenantId],
    queryFn: () => listAssetTypes({ tenant: tenantId, kind: "gateway" }),
    enabled: Boolean(tenantId),
  });
  const assets = useQuery({
    queryKey: ["assets", tenantId, projectId],
    queryFn: () => listAssets({ tenant: tenantId, project: projectId ?? undefined }),
    enabled: Boolean(tenantId),
  });
  const gateways = useQuery({
    queryKey: ["gateways", tenantId],
    queryFn: () => listGateways({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });

  const gatewayAssetIds = new Set((gateways.data?.results ?? []).map((g) => g.asset));
  const candidateAssets = (assets.data?.results ?? []).filter(
    (a) => !gatewayAssetIds.has(a.id) && types.data?.results?.some((t) => t.id === a.asset_type),
  );

  const mutation = useMutation({
    mutationFn: createGateway,
    onSuccess: () => {
      message.success(t("conn.createSuccess"));
      onCreated();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  function onAssetChange(assetId: string) {
    const asset = candidateAssets.find((a) => a.id === assetId);
    const type = (types.data?.results ?? []).find((t) => t.id === asset?.asset_type);
    setSchema(((type?.schema as Record<string, unknown>)?.connection_schema as Record<string, unknown>[]) ?? []);
    form.setFieldValue("config", undefined);
  }

  function onFinish(values: { asset: string; config?: Record<string, unknown> }) {
    const asset = candidateAssets.find((a) => a.id === values.asset);
    const type = (types.data?.results ?? []).find((t) => t.id === asset?.asset_type);
    const code = type?.code ?? "";
    const protocol = code === "gateway" ? String(values.config?.protocol ?? "mqtt") : code.replace(/^gateway-/, "");
    if (!tenantId) return;
    mutation.mutate({
      tenant: tenantId,
      project: projectId ?? null,
      asset: values.asset,
      protocol,
      config: values.config ?? {},
    });
  }

  return (
    <Modal title={t("conn.createGateway")} open={open} onCancel={onClose} onOk={() => form.submit()} confirmLoading={mutation.isPending} width={640}>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item name="asset" label={t("conn.gatewayAsset")} rules={[{ required: true }]}>
          <Select
            onChange={onAssetChange}
            options={candidateAssets.map((a) => ({ value: a.id, label: a.name }))}
            notFoundContent={t("conn.noGatewayAssets")}
          />
        </Form.Item>
        {schema.map((field) => {
          const f = field as Record<string, unknown>;
          const fname = f.field as string;
          const ftype = f.type as string;
          const label = ((f.label_i18n as Record<string, string>) ?? {})["es"] ?? fname;
          const rules = f.required ? [{ required: true }] : [];
          if (ftype === "bool") {
            return (
              <Form.Item key={fname} name={["config", fname]} label={label} valuePropName="checked" rules={rules}>
                <Checkbox />
              </Form.Item>
            );
          }
          if (ftype === "select") {
            const options = (f.options as { value: string }[] | undefined) ?? [];
            return (
              <Form.Item key={fname} name={["config", fname]} label={label} rules={rules} initialValue={f.default as string | undefined}>
                <Select options={options.map((o) => ({ value: o.value, label: o.value }))} />
              </Form.Item>
            );
          }
          const isSecret = ftype === "secret";
          const isInt = ftype === "int";
          return (
            <Form.Item key={fname} name={["config", fname]} label={label} rules={rules} initialValue={f.default as string | number | undefined}>
              {isSecret ? <Input.Password /> : isInt ? <InputNumber style={{ width: "100%" }} /> : <Input />}
            </Form.Item>
          );
        })}
      </Form>
    </Modal>
  );
}

function BindingsDrawer({ gateway, onClose }: { gateway: Gateway | null; onClose: () => void }) {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const [form] = Form.useForm();

  const bindings = useQuery({
    queryKey: ["bindings", gateway?.id],
    queryFn: () => listBindings(gateway?.id ?? ""),
    enabled: Boolean(gateway),
  });
  const assets = useQuery({
    queryKey: ["assets"],
    queryFn: () => listAssets(),
    enabled: Boolean(gateway),
  });
  const [assetId, setAssetId] = useState<string>();
  const attributes = useQuery({
    queryKey: ["attributes", assetId],
    queryFn: () => listAttributes(assetId ?? ""),
    enabled: Boolean(assetId),
  });

  const createMutation = useMutation({
    mutationFn: createBinding,
    onSuccess: () => {
      message.success(t("conn.bindingCreated"));
      form.resetFields();
      setAssetId(undefined);
      queryClient.invalidateQueries({ queryKey: ["bindings", gateway?.id] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteBinding(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["bindings", gateway?.id] }),
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Drawer title={t("conn.bindings")} open={Boolean(gateway)} onClose={onClose} width={640}>
      <Table
        rowKey="id"
        size="small"
        dataSource={bindings.data?.results ?? []}
        loading={bindings.isLoading}
        pagination={false}
        columns={[
          { title: t("attributes.code"), dataIndex: "attribute", render: (v: string) => v.slice(0, 8) },
          { title: t("conn.address"), dataIndex: "address" },
          { title: t("conn.mapping"), dataIndex: "mapping" },
          {
            title: t("common.actions"),
            render: (_, record) => (
              <Popconfirm title={t("conn.deleteBindingConfirm")} onConfirm={() => deleteMutation.mutate(record.id)}>
                <Button size="small" danger icon={<DeleteOutlined />} />
              </Popconfirm>
            ),
          },
        ]}
      />
      <Typography.Title level={5} style={{ marginTop: 16 }}>
        {t("conn.newBinding")}
      </Typography.Title>
      <Form
        form={form}
        layout="vertical"
        onFinish={(values: { asset: string; attribute: string; address: string; mapping?: string }) => {
          if (!gateway) return;
          createMutation.mutate({ gateway: gateway.id, ...values });
        }}
      >
        <Form.Item name="asset" label={t("assets.title")} rules={[{ required: true }]}>
          <Select
            onChange={(value) => setAssetId(value)}
            options={(assets.data?.results ?? []).map((a) => ({ value: a.id, label: a.name }))}
          />
        </Form.Item>
        <Form.Item name="attribute" label={t("attributes.title")} rules={[{ required: true }]}>
          <Select
            disabled={!assetId}
            options={(attributes.data?.results ?? []).map((a) => ({ value: a.id, label: a.code }))}
          />
        </Form.Item>
        <Form.Item name="address" label={t("conn.address")} rules={[{ required: true }]}>
          <Input placeholder="site/+/temp" />
        </Form.Item>
        <Form.Item name="mapping" label={t("conn.mapping")}>
          <Input placeholder="data.temperature" />
        </Form.Item>
        <Button type="primary" htmlType="submit" loading={createMutation.isPending}>
          {t("common.create")}
        </Button>
      </Form>
    </Drawer>
  );
}
