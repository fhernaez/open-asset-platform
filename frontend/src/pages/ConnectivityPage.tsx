import { ApiOutlined, DeleteOutlined, LinkOutlined, PlusOutlined } from "@ant-design/icons";
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
  Switch,
  Table,
  Tag,
  Typography,
  message,
} from "antd";
import type { FormInstance } from "antd";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import {
  createAsset,
  createBinding,
  deleteBinding,
  deleteGateway,
  listAssets,
  listAssetTypes,
  listAttributes,
  listBindings,
  listGateways,
  testGatewayConnection,
  updateAttribute,
  updateGatewayConfig,
} from "../api/endpoints";
import type { Asset, AssetAttribute, AssetType, Gateway, GatewayBinding } from "../api/types";
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
  const [editingGateway, setEditingGateway] = useState<Gateway | null>(null);
  const [form] = Form.useForm();
  const [editForm] = Form.useForm();

  const gateways = useQuery({
    queryKey: ["gateways", tenantId],
    queryFn: () => listGateways({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const gatewayTypes = useQuery({
    queryKey: ["asset-types", tenantId],
    queryFn: () => listAssetTypes({ tenant: tenantId, kind: "gateway" }),
    enabled: Boolean(tenantId),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["gateways", tenantId] });

  const editMutation = useMutation({
    mutationFn: ({ id, config }: { id: string; config: Record<string, unknown> }) =>
      updateGatewayConfig(id, config),
    onSuccess: () => {
      message.success(t("common.save"));
      setEditingGateway(null);
      editForm.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteGateway(id),
    onSuccess: invalidate,
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const testMutation = useMutation({
    mutationFn: (id: string) => testGatewayConnection(id),
    onSuccess: (result) => {
      message.info(`${t("conn.testResult")}: ${result.status}${result.detail ? ` — ${result.detail}` : ""}`);
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Space wrap>
        <Typography.Title level={4} style={{ margin: 0 }}>
          {t("conn.title")}
        </Typography.Title>
        <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
          {t("conn.createGateway")}
        </Button>
      </Space>

      {gateways.isError && <Alert type="error" showIcon message={t("conn.loadError")} />}
      {!gateways.isError && gateways.data?.results.length === 0 && <Empty description={t("conn.noData")} />}

      {(gateways.data?.results.length ?? 0) > 0 && (
        <Table<Gateway>
          rowKey="id"
          dataSource={gateways.data?.results ?? []}
          loading={gateways.isLoading}
          pagination={{ pageSize: 20 }}
          columns={[
            { title: t("assets.name"), dataIndex: "asset_name" },
            {
              title: t("conn.protocol"),
              dataIndex: "protocol",
              render: (v: string) => <Tag color="purple">{v}</Tag>,
            },
            {
              title: t("conn.status"),
              dataIndex: "connection_status",
              render: (v: string) => <Tag color={statusColor(v)}>{v}</Tag>,
            },
            {
              title: t("common.actions"),
              render: (_, record) => (
                <Space>
                  <Button size="small" icon={<ApiOutlined />} onClick={() => testMutation.mutate(record.id)}>
                    {t("conn.test")}
                  </Button>
                  <Button
                    size="small"
                    onClick={() => {
                      setEditingGateway(record);
                      editForm.setFieldsValue({ config: record.config });
                    }}
                  >
                    {t("common.edit")}
                  </Button>
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

      <GatewayEditModal
        gateway={editingGateway}
        gatewayTypes={gatewayTypes.data?.results ?? []}
        form={editForm}
        onClose={() => setEditingGateway(null)}
        onSave={(config) => {
          if (editingGateway) editMutation.mutate({ id: editingGateway.id, config });
        }}
        saving={editMutation.isPending}
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

  const mutation = useMutation({
    mutationFn: createAsset,
    onSuccess: () => {
      message.success(t("conn.createSuccess"));
      onCreated();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  function onTypeChange(typeId: string) {
    const type = (types.data?.results ?? []).find((item) => item.id === typeId);
    setSchema(((type?.schema as Record<string, unknown>)?.connection_schema as Record<string, unknown>[]) ?? []);
    form.setFieldValue("gateway_config", undefined);
  }

  function onFinish(values: { name: string; external_ref: string; asset_type: string; gateway_config?: Record<string, unknown> }) {
    if (!tenantId) return;
    mutation.mutate({
      tenant: tenantId,
      project: projectId ?? null,
      name: values.name,
      external_ref: values.external_ref,
      asset_type: values.asset_type,
      gateway_config: values.gateway_config,
    });
  }

  return (
    <Modal
      title={t("conn.createGateway")}
      open={open}
      onCancel={onClose}
      onOk={() => form.submit()}
      confirmLoading={mutation.isPending}
      width={640}
    >
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item name="name" label={t("assets.name")} rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="external_ref" label={t("assets.reference")} rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="asset_type" label={t("assets.types")} rules={[{ required: true }]}>
          <Select
            onChange={onTypeChange}
            options={(types.data?.results ?? []).map((item) => ({ value: item.id, label: item.name }))}
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
              <Form.Item key={fname} name={["gateway_config", fname]} label={label} valuePropName="checked" rules={rules}>
                <Checkbox />
              </Form.Item>
            );
          }
          if (ftype === "select") {
            const options = (f.options as { value: string }[] | undefined) ?? [];
            return (
              <Form.Item
                key={fname}
                name={["gateway_config", fname]}
                label={label}
                rules={rules}
                initialValue={f.default as string | undefined}
              >
                <Select options={options.map((o) => ({ value: o.value, label: o.value }))} />
              </Form.Item>
            );
          }
          const isSecret = ftype === "secret";
          const isInt = ftype === "int";
          return (
            <Form.Item
              key={fname}
              name={["gateway_config", fname]}
              label={label}
              rules={rules}
              initialValue={f.default as string | number | undefined}
            >
              {isSecret ? <Input.Password /> : isInt ? <InputNumber style={{ width: "100%" }} /> : <Input />}
            </Form.Item>
          );
        })}
      </Form>
    </Modal>
  );
}

function GatewayEditModal({
  gateway,
  gatewayTypes,
  form,
  onClose,
  onSave,
  saving,
}: {
  gateway: Gateway | null;
  gatewayTypes: AssetType[];
  form: FormInstance;
  onClose: () => void;
  onSave: (config: Record<string, unknown>) => void;
  saving: boolean;
}) {
  const { t } = useTranslation();
  const type = gatewayTypes.find((item) => item.code === gateway?.asset_code);
  const schema = ((type?.schema as Record<string, unknown>)?.connection_schema as Record<string, unknown>[]) ?? [];

  return (
    <Modal
      title={t("common.edit")}
      open={Boolean(gateway)}
      onCancel={onClose}
      onOk={() => form.submit()}
      confirmLoading={saving}
      width={640}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={(values: { config?: Record<string, unknown> }) => onSave(values.config ?? {})}
      >
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
              <Form.Item key={fname} name={["config", fname]} label={label} rules={rules}>
                <Select options={options.map((o) => ({ value: o.value, label: o.value }))} />
              </Form.Item>
            );
          }
          const isSecret = ftype === "secret";
          const isInt = ftype === "int";
          return (
            <Form.Item key={fname} name={["config", fname]} label={label} rules={rules}>
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
  const { tenantId } = useAppContext();
  const [form] = Form.useForm();
  const [bindingType, setBindingType] = useState<string>("attribute");
  const [assetId, setAssetId] = useState<string>();
  const [deviceId, setDeviceId] = useState<string>();

  const bindings = useQuery({
    queryKey: ["bindings", gateway?.id],
    queryFn: () => listBindings(gateway?.id ?? ""),
    enabled: Boolean(gateway),
  });
  const assets = useQuery({
    queryKey: ["assets", tenantId],
    queryFn: () => listAssets({ tenant: tenantId }),
    enabled: Boolean(gateway),
  });
  const attributes = useQuery({
    queryKey: ["attributes", assetId],
    queryFn: () => listAttributes(assetId ?? ""),
    enabled: Boolean(assetId),
  });
  const deviceAttributes = useQuery({
    queryKey: ["attributes", deviceId],
    queryFn: () => listAttributes(deviceId ?? ""),
    enabled: Boolean(deviceId),
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

  const toggleAttrMutation = useMutation({
    mutationFn: ({ id, active }: { id: string; active: boolean }) =>
      updateAttribute(id, { is_active: active }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["attributes", deviceId] }),
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Drawer title={t("conn.bindings")} open={Boolean(gateway)} onClose={onClose} width={680}>
      <Table<GatewayBinding>
        rowKey="id"
        size="small"
        dataSource={bindings.data?.results ?? []}
        loading={bindings.isLoading}
        pagination={false}
        columns={[
          {
            title: t("conn.bindingType"),
            dataIndex: "binding_type",
            render: (v: string) => <Tag color={v === "device" ? "blue" : "default"}>{v}</Tag>,
          },
          { title: t("assets.name"), dataIndex: "asset_name" },
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
        initialValues={{ binding_type: "attribute" }}
        onFinish={(values: { binding_type: string; asset: string; attribute?: string; address: string; mapping?: string }) => {
          if (!gateway) return;
          createMutation.mutate({
            gateway: gateway.id,
            binding_type: values.binding_type as "attribute" | "device",
            asset: values.asset,
            attribute: values.binding_type === "attribute" ? values.attribute : undefined,
            address: values.address,
            mapping: values.mapping,
          } as Parameters<typeof createBinding>[0]);
        }}
      >
        <Form.Item name="binding_type" label={t("conn.bindingType")} rules={[{ required: true }]}>
          <Select
            onChange={(value) => setBindingType(value)}
            options={[
              { value: "attribute", label: "attribute" },
              { value: "device", label: "device" },
            ]}
          />
        </Form.Item>
        <Form.Item name="asset" label={t("assets.title")} rules={[{ required: true }]}>
          <Select
            onChange={(value) => setAssetId(value)}
            options={(assets.data?.results ?? [])
              .filter((a) => a.id !== gateway?.asset)
              .map((a) => ({ value: a.id, label: a.name }))}
          />
        </Form.Item>
        {bindingType === "attribute" && (
          <Form.Item name="attribute" label={t("attributes.title")} rules={[{ required: true }]}>
            <Select
              disabled={!assetId}
              options={(attributes.data?.results ?? []).map((a: AssetAttribute) => ({ value: a.id, label: a.code }))}
            />
          </Form.Item>
        )}
        <Form.Item name="address" label={t("conn.address")} rules={[{ required: true }]}>
          <Input placeholder="z2m-tg/SN-PRES-01" />
        </Form.Item>
        <Form.Item name="mapping" label={t("conn.mapping")}>
          <Input placeholder="data.temperature" />
        </Form.Item>
        <Button type="primary" htmlType="submit" loading={createMutation.isPending}>
          {t("common.create")}
        </Button>
      </Form>

      <Typography.Title level={5} style={{ marginTop: 24 }}>
        {t("conn.deviceAttributes")}
      </Typography.Title>
      <Select
        style={{ width: "100%", marginBottom: 12 }}
        placeholder={t("conn.selectDevice")}
        value={deviceId}
        onChange={setDeviceId}
        options={(assets.data?.results ?? []).map((a: Asset) => ({ value: a.id, label: a.name }))}
      />
      <Table<AssetAttribute>
        rowKey="id"
        size="small"
        dataSource={deviceAttributes.data?.results ?? []}
        loading={deviceAttributes.isLoading}
        pagination={false}
        columns={[
          { title: t("attributes.code"), dataIndex: "code" },
          {
            title: t("conn.discovered"),
            dataIndex: "auto_discovered",
            render: (v: boolean) => (v ? <Tag color="purple">auto</Tag> : null),
          },
          {
            title: t("conn.active"),
            render: (_, record) => (
              <Switch
                size="small"
                checked={record.is_active}
                onChange={(checked) => toggleAttrMutation.mutate({ id: record.id, active: checked })}
              />
            ),
          },
        ]}
      />
    </Drawer>
  );
}
