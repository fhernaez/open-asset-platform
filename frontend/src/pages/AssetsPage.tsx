import {
  ApiOutlined,
  AppstoreOutlined,
  BuildOutlined,
  BulbOutlined,
  DeleteOutlined,
  HomeOutlined,
  PlusOutlined,
  ReloadOutlined,
  ThunderboltOutlined,
} from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Checkbox,
  Drawer,
  Empty,
  Form,
  Input,
  Modal,
  Popconfirm,
  Select,
  Space,
  Table,
  Tabs,
  Tag,
  Typography,
  message,
} from "antd";
import type { FormInstance } from "antd";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import {
  createAsset,
  createAssetType,
  createAttribute,
  deleteAsset,
  deleteAssetType,
  deleteAttribute,
  listAssets,
  listAssetTypes,
  listAttributes,
  listUnits,
  updateAssetStatus,
  updateAttribute,
} from "../api/endpoints";
import type { Asset, AssetType } from "../api/types";
import { useAppContext } from "../contexts/AppContext";

const VALUE_TYPES = [
  { value: "number", label: "number" },
  { value: "string", label: "string" },
  { value: "boolean", label: "boolean" },
  { value: "json", label: "json" },
];

function slugify(value: string): string {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

const TYPE_ICONS: Record<string, React.ReactNode> = {
  building: <HomeOutlined />,
  floor: <BuildOutlined />,
  room: <AppstoreOutlined />,
  zone: <AppstoreOutlined />,
  ahu: <ApiOutlined />,
  vav: <ApiOutlined />,
  fcu: <ApiOutlined />,
  boiler: <ThunderboltOutlined />,
  chiller: <ThunderboltOutlined />,
  pump: <ThunderboltOutlined />,
  fan: <ThunderboltOutlined />,
  "electricity-meter": <ThunderboltOutlined />,
  "water-meter": <BulbOutlined />,
  "heat-meter": <ThunderboltOutlined />,
  "lighting-zone": <BulbOutlined />,
  "gateway-mqtt": <ApiOutlined />,
  "gateway-modbus-rtu": <ApiOutlined />,
  "gateway-modbus-tcp": <ApiOutlined />,
  "gateway-opcua": <ApiOutlined />,
  "gateway-bacnet": <ApiOutlined />,
  "gateway-snmp": <ApiOutlined />,
  "gateway-can": <ApiOutlined />,
};

function typeIcon(code: string): React.ReactNode {
  return TYPE_ICONS[code] ?? <AppstoreOutlined />;
}

export default function AssetsPage() {
  return (
    <Tabs
      defaultActiveKey="assets"
      items={[
        { key: "assets", label: "Activos", children: <AssetsTab /> },
        { key: "types", label: "Tipologías", children: <AssetTypesTab /> },
      ]}
    />
  );
}

function AssetsTab() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId, projectId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [createForm] = Form.useForm();
  const [attrForm] = Form.useForm();

  const assetTypes = useQuery({
    queryKey: ["asset-types", tenantId],
    queryFn: () => listAssetTypes({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const assets = useQuery({
    queryKey: ["assets", tenantId, projectId],
    queryFn: () => listAssets({ tenant: tenantId, project: projectId ?? undefined }),
    enabled: Boolean(tenantId),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["assets", tenantId, projectId] });

  const createMutation = useMutation({
    mutationFn: createAsset,
    onSuccess: () => {
      message.success(t("assets.createSuccess"));
      setCreateOpen(false);
      createForm.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : t("assets.createError")),
  });

  const statusMutation = useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) => updateAssetStatus(id, status),
    onSuccess: () => invalidate(),
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteAsset(id),
    onSuccess: () => {
      message.success(t("assets.deleteSuccess"));
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  function onCreate(values: { name: string; external_ref: string; asset_type?: string }) {
    if (!tenantId) return;
    createMutation.mutate({
      tenant: tenantId,
      project: projectId ?? null,
      name: values.name,
      external_ref: values.external_ref,
      asset_type: values.asset_type ?? null,
    });
  }

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Space wrap>
        <Button
          icon={<ReloadOutlined />}
          onClick={() => queryClient.invalidateQueries({ queryKey: ["assets"] })}
        >
          {t("common.refresh")}
        </Button>
        <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
          {t("assets.create")}
        </Button>
      </Space>

      {!tenantId && <Empty description={t("assets.noOrg")} />}
      {tenantId && assets.isError && <Alert type="error" showIcon message={t("assets.loadError")} />}
      {tenantId && !assets.isError && assets.data?.results.length === 0 && (
        <Empty description={t("assets.noData")} />
      )}

      {(assets.data?.results.length ?? 0) > 0 && (
        <Table<Asset>
          rowKey="id"
          dataSource={assets.data?.results ?? []}
          loading={assets.isLoading}
          onRow={(record) => ({ onClick: () => setSelectedAsset(record), style: { cursor: "pointer" } })}
          pagination={{ pageSize: 20 }}
          columns={[
            { title: t("assets.name"), dataIndex: "name" },
            { title: t("assets.reference"), dataIndex: "external_ref" },
            {
              title: t("assets.status"),
              dataIndex: "status",
              render: (value: string) => (
                <Tag color={value === "active" ? "green" : value === "retired" ? "orange" : "default"}>
                  {value === "active" ? t("assets.active") : value === "retired" ? t("assets.retired") : t("assets.draft")}
                </Tag>
              ),
            },
            {
              title: t("common.actions"),
              render: (_, record) => (
                <Space onClick={(event) => event.stopPropagation()}>
                  {record.status === "retired" ? (
                    <Button
                      size="small"
                      onClick={() => statusMutation.mutate({ id: record.id, status: "active" })}
                    >
                      {t("assets.activate")}
                    </Button>
                  ) : (
                    <Button
                      size="small"
                      onClick={() => statusMutation.mutate({ id: record.id, status: "retired" })}
                    >
                      {t("assets.retire")}
                    </Button>
                  )}
                  <Popconfirm
                    title={t("assets.deleteConfirm")}
                    onConfirm={() => deleteMutation.mutate(record.id)}
                  >
                    <Button size="small" danger icon={<DeleteOutlined />} />
                  </Popconfirm>
                </Space>
              ),
            },
          ]}
        />
      )}

      <Modal
        title={t("assets.create")}
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => createForm.submit()}
        confirmLoading={createMutation.isPending}
      >
        <Form form={createForm} layout="vertical" onFinish={onCreate}>
          <Form.Item name="name" label={t("assets.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="external_ref" label={t("assets.reference")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="asset_type" label={t("assets.types")}>
            <Select
              allowClear
              placeholder={t("assets.types")}
              options={(assetTypes.data?.results ?? []).map((item) => ({
                value: item.id,
                label: item.kind === "gateway" ? `${item.name} (${t("types.kind.gateway")})` : item.name,
              }))}
            />
          </Form.Item>
        </Form>
      </Modal>

      <AttributesDrawer
        asset={selectedAsset}
        form={attrForm}
        onClose={() => {
          setSelectedAsset(null);
          attrForm.resetFields();
        }}
      />
    </Space>
  );
}

function AssetTypesTab() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [form] = Form.useForm();

  const types = useQuery({
    queryKey: ["asset-types", tenantId],
    queryFn: () => listAssetTypes({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["asset-types", tenantId] });

  const createMutation = useMutation({
    mutationFn: createAssetType,
    onSuccess: () => {
      message.success(t("types.createSuccess"));
      setCreateOpen(false);
      form.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteAssetType(id),
    onSuccess: () => {
      message.success(t("assets.deleteSuccess"));
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  function onCreate(values: {
    name: string;
    code: string;
    kind: string;
    attributes?: { code: string; name?: string; value_type: string; storage_datapoint?: boolean }[];
  }) {
    if (!tenantId) return;
    createMutation.mutate({
      tenant: tenantId,
      name: values.name,
      code: values.code,
      kind: (values.kind as "standard" | "gateway") ?? "standard",
      schema: { attributes: values.attributes ?? [] },
    });
  }

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
        {t("types.create")}
      </Button>

      {!tenantId && <Empty description={t("assets.noOrg")} />}
      {tenantId && types.isError && <Alert type="error" showIcon message={t("types.loadError")} />}
      {tenantId && !types.isError && types.data?.results.length === 0 && (
        <Empty description={t("types.noData")} />
      )}

      {(types.data?.results.length ?? 0) > 0 && (
        <Table<AssetType>
          rowKey="id"
          dataSource={types.data?.results ?? []}
          loading={types.isLoading}
          pagination={{ pageSize: 20 }}
          columns={[
            {
              title: t("types.title"),
              dataIndex: "code",
              render: (code: string, record) => (
                <Space>
                  {typeIcon(code)}
                  <span>{record.name}</span>
                  <Typography.Text type="secondary">({code})</Typography.Text>
                </Space>
              ),
            },
            {
              title: t("common.actions"),
              width: 120,
              render: (_, record) => (
                <Popconfirm title={t("types.deleteConfirm")} onConfirm={() => deleteMutation.mutate(record.id)}>
                  <Button size="small" danger icon={<DeleteOutlined />} />
                </Popconfirm>
              ),
            },
          ]}
        />
      )}

      <Modal
        title={t("types.create")}
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => form.submit()}
        confirmLoading={createMutation.isPending}
        width={720}
      >
        <Form form={form} layout="vertical" onFinish={onCreate} initialValues={{ kind: "standard" }}>
          <Space.Compact block>
            <Form.Item name="name" label={t("assets.name")} rules={[{ required: true }]} style={{ flex: 1 }}>
              <Input />
            </Form.Item>
            <Form.Item name="code" label={t("project.code")} rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]} style={{ flex: 1 }}>
              <Input />
            </Form.Item>
          </Space.Compact>

          <Typography.Text strong>{t("types.attributes")}</Typography.Text>
          <Form.List name="attributes">
            {(fields, { add, remove }) => (
              <div style={{ marginTop: 12 }}>
                {fields.map((field) => (
                  <Space key={field.key} align="baseline" style={{ display: "flex", marginBottom: 8 }}>
                    <Form.Item name={[field.name, "code"]} rules={[{ required: true }]} style={{ marginBottom: 0 }}>
                      <Input placeholder={t("types.attributeCode")} />
                    </Form.Item>
                    <Form.Item name={[field.name, "name"]} style={{ marginBottom: 0 }}>
                      <Input placeholder={t("types.attributeName")} />
                    </Form.Item>
                    <Form.Item name={[field.name, "value_type"]} initialValue="number" rules={[{ required: true }]} style={{ marginBottom: 0 }}>
                      <Select style={{ width: 110 }} options={VALUE_TYPES} />
                    </Form.Item>
                    <Form.Item name={[field.name, "storage_datapoint"]} valuePropName="checked" initialValue={true} style={{ marginBottom: 0 }}>
                      <Checkbox>{t("types.store")}</Checkbox>
                    </Form.Item>
                    <Button type="text" danger onClick={() => remove(field.name)}>
                      {t("common.delete")}
                    </Button>
                  </Space>
                ))}
                <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                  {t("types.addAttribute")}
                </Button>
              </div>
            )}
          </Form.List>
        </Form>
      </Modal>
    </Space>
  );
}

function AttributesDrawer({
  asset,
  form,
  onClose,
}: {
  asset: Asset | null;
  form: FormInstance;
  onClose: () => void;
}) {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const [editing, setEditing] = useState<{ id: string } | null>(null);
  const [editForm] = Form.useForm();

  const attributes = useQuery({
    queryKey: ["attributes", asset?.id],
    queryFn: () => listAttributes(asset?.id ?? ""),
    enabled: Boolean(asset),
  });
  const units = useQuery({ queryKey: ["units"], queryFn: () => listUnits(), enabled: Boolean(asset) });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["attributes", asset?.id] });

  const attrMutation = useMutation({
    mutationFn: createAttribute,
    onSuccess: () => {
      message.success(t("attributes.createSuccess"));
      form.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: Record<string, unknown> }) =>
      updateAttribute(id, input as Parameters<typeof updateAttribute>[1]),
    onSuccess: () => {
      message.success(t("common.save"));
      setEditing(null);
      editForm.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteAttribute(id),
    onSuccess: () => invalidate(),
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  function onCreateAttribute(values: {
    name: string;
    code: string;
    value_type: string;
    unit?: string;
    storage_datapoint: boolean;
  }) {
    if (!asset) return;
    attrMutation.mutate({
      asset: asset.id,
      name: values.name,
      code: values.code,
      value_type: values.value_type,
      storage_datapoint: values.storage_datapoint,
      unit: values.unit ?? null,
    } as Parameters<typeof createAttribute>[0]);
  }

  const unitOptions = (units.data?.results ?? []).map((u) => ({ value: u.symbol, label: u.symbol }));

  return (
    <Drawer
      title={asset ? `${t("attributes.title")} — ${asset.name}` : t("attributes.title")}
      open={Boolean(asset)}
      onClose={onClose}
      width={620}
    >
      <Table
        rowKey="id"
        size="small"
        dataSource={attributes.data?.results ?? []}
        loading={attributes.isLoading}
        pagination={false}
        columns={[
          { title: t("attributes.code"), dataIndex: "code" },
          { title: t("attributes.name"), dataIndex: "name" },
          { title: t("attributes.valueType"), dataIndex: "value_type" },
          { title: t("attributes.unit"), dataIndex: "unit" },
          {
            title: t("attributes.store"),
            dataIndex: "storage_datapoint",
            render: (value: boolean) => (value ? <Tag color="blue">on</Tag> : <Tag>off</Tag>),
          },
          {
            title: t("common.actions"),
            render: (_, record) => (
              <Space>
                <Button
                  size="small"
                  onClick={() => {
                    setEditing({ id: record.id });
                    editForm.setFieldsValue(record);
                  }}
                >
                  {t("common.edit")}
                </Button>
                <Popconfirm title={t("attributes.deleteConfirm")} onConfirm={() => deleteMutation.mutate(record.id)}>
                  <Button size="small" danger icon={<DeleteOutlined />} />
                </Popconfirm>
              </Space>
            ),
          },
        ]}
      />

      <Typography.Title level={5} style={{ marginTop: 16 }}>
        {t("attributes.new")}
      </Typography.Title>
      <Form
        form={form}
        layout="vertical"
        onFinish={onCreateAttribute}
        onValuesChange={(changed, values) => {
          if (changed.name) {
            form.setFieldValue("code", slugify(String(values.name ?? "")));
          }
        }}
      >
        <Form.Item name="name" label={t("attributes.name")} rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item
          name="code"
          label={t("attributes.code")}
          rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}
          extra={t("attributes.codeHelp")}
        >
          <Input />
        </Form.Item>
        <Form.Item name="value_type" label={t("attributes.valueType")} initialValue="number" rules={[{ required: true }]}>
          <Select options={VALUE_TYPES} />
        </Form.Item>
        <Form.Item name="unit" label={t("attributes.unit")}>
          <Select allowClear options={unitOptions} />
        </Form.Item>
        <Form.Item name="storage_datapoint" label={t("attributes.store")} valuePropName="checked" initialValue={true}>
          <Checkbox />
        </Form.Item>
        <Button type="primary" htmlType="submit" loading={attrMutation.isPending}>
          {t("common.create")}
        </Button>
      </Form>

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
          <Form.Item name="name" label={t("attributes.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="code" label={t("attributes.code")} rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
            <Input />
          </Form.Item>
          <Form.Item name="value_type" label={t("attributes.valueType")} rules={[{ required: true }]}>
            <Select options={VALUE_TYPES} />
          </Form.Item>
          <Form.Item name="unit" label={t("attributes.unit")}>
            <Select allowClear options={unitOptions} />
          </Form.Item>
          <Form.Item name="storage_datapoint" label={t("attributes.store")} valuePropName="checked">
            <Checkbox />
          </Form.Item>
        </Form>
      </Modal>
    </Drawer>
  );
}
