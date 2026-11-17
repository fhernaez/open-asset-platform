import { PlusOutlined, ReloadOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Checkbox,
  Drawer,
  Form,
  Input,
  Modal,
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
import {
  createAsset,
  createAssetType,
  createAttribute,
  createProject,
  createTenant,
  listAssets,
  listAssetTypes,
  listAttributes,
  listProjects,
  listTenants,
} from "../api/endpoints";
import type { Asset, AssetType } from "../api/types";

const VALUE_TYPES = [
  { value: "number", label: "Número" },
  { value: "string", label: "Texto" },
  { value: "boolean", label: "Booleano" },
  { value: "json", label: "JSON" },
];

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
  const queryClient = useQueryClient();
  const [tenantId, setTenantId] = useState<string>();
  const [projectId, setProjectId] = useState<string>();
  const [createOpen, setCreateOpen] = useState(false);
  const [tenantModalOpen, setTenantModalOpen] = useState(false);
  const [projectModalOpen, setProjectModalOpen] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [createForm] = Form.useForm();
  const [tenantForm] = Form.useForm();
  const [projectForm] = Form.useForm();
  const [attrForm] = Form.useForm();

  const tenants = useQuery({ queryKey: ["tenants"], queryFn: () => listTenants() });
  const projects = useQuery({
    queryKey: ["projects", tenantId],
    queryFn: () => listProjects(tenantId ?? ""),
    enabled: Boolean(tenantId),
  });
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

  const createMutation = useMutation({
    mutationFn: createAsset,
    onSuccess: () => {
      message.success("Activo creado");
      setCreateOpen(false);
      createForm.resetFields();
      queryClient.invalidateQueries({ queryKey: ["assets"] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error al crear activo"),
  });

  const tenantMutation = useMutation({
    mutationFn: createTenant,
    onSuccess: () => {
      message.success("Organización creada");
      setTenantModalOpen(false);
      tenantForm.resetFields();
      queryClient.invalidateQueries({ queryKey: ["tenants"] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error al crear organización"),
  });

  const projectMutation = useMutation({
    mutationFn: createProject,
    onSuccess: (project) => {
      message.success("Proyecto creado");
      setProjectModalOpen(false);
      projectForm.resetFields();
      queryClient.invalidateQueries({ queryKey: ["projects", tenantId] });
      setProjectId(project.id);
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error al crear proyecto"),
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

  function onTenantCreate(values: { name: string; slug: string }) {
    tenantMutation.mutate(values);
  }

  function onProjectCreate(values: { name: string; code: string }) {
    if (!tenantId) return;
    projectMutation.mutate({ tenant: tenantId, ...values });
  }

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Space wrap>
        <Select
          style={{ minWidth: 240 }}
          placeholder="Organización"
          loading={tenants.isLoading}
          value={tenantId}
          onChange={(value) => {
            setTenantId(value);
            setProjectId(undefined);
          }}
          options={(tenants.data?.results ?? []).map((t) => ({ value: t.id, label: t.name }))}
        />
        <Button icon={<PlusOutlined />} onClick={() => setTenantModalOpen(true)}>
          Nueva organización
        </Button>
        <Select
          style={{ minWidth: 240 }}
          placeholder="Proyecto (opcional)"
          disabled={!tenantId}
          loading={projects.isFetching}
          value={projectId}
          allowClear
          onChange={(value) => setProjectId(value)}
          options={(projects.data?.results ?? []).map((p) => ({ value: p.id, label: p.name }))}
        />
        <Button icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setProjectModalOpen(true)}>
          Nuevo proyecto
        </Button>
        <Button icon={<ReloadOutlined />} onClick={() => queryClient.invalidateQueries({ queryKey: ["assets"] })}>
          Refrescar
        </Button>
        <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
          Crear activo
        </Button>
      </Space>

      {tenants.isError && <Alert type="error" showIcon message="No se pudieron cargar las organizaciones." />}

      <Table<Asset>
        rowKey="id"
        dataSource={assets.data?.results ?? []}
        loading={assets.isLoading}
        onRow={(record) => ({ onClick: () => setSelectedAsset(record), style: { cursor: "pointer" } })}
        pagination={{ pageSize: 20 }}
        columns={[
          { title: "Nombre", dataIndex: "name" },
          { title: "Referencia", dataIndex: "external_ref" },
          {
            title: "Estado",
            dataIndex: "status",
            render: (value: string) => <Tag color={value === "active" ? "green" : "default"}>{value}</Tag>,
          },
        ]}
      />

      <Modal
        title="Nueva organización"
        open={tenantModalOpen}
        onCancel={() => setTenantModalOpen(false)}
        onOk={() => tenantForm.submit()}
        confirmLoading={tenantMutation.isPending}
      >
        <Form form={tenantForm} layout="vertical" onFinish={onTenantCreate}>
          <Form.Item name="name" label="Nombre" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="slug" label="Slug" rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Nuevo proyecto"
        open={projectModalOpen}
        onCancel={() => setProjectModalOpen(false)}
        onOk={() => projectForm.submit()}
        confirmLoading={projectMutation.isPending}
      >
        <Form form={projectForm} layout="vertical" onFinish={onProjectCreate}>
          <Form.Item name="name" label="Nombre" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="code" label="Código" rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Crear activo"
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => createForm.submit()}
        confirmLoading={createMutation.isPending}
      >
        <Form form={createForm} layout="vertical" onFinish={onCreate}>
          <Form.Item name="name" label="Nombre" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="external_ref" label="Referencia externa" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="asset_type" label="Tipología">
            <Select
              allowClear
              placeholder="Sin tipología"
              options={(assetTypes.data?.results ?? []).map((t) => ({
                value: t.id,
                label: t.kind === "gateway" ? `${t.name} (gateway)` : t.name,
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
  const queryClient = useQueryClient();
  const [tenantId, setTenantId] = useState<string>();
  const [createOpen, setCreateOpen] = useState(false);
  const [form] = Form.useForm();

  const tenants = useQuery({ queryKey: ["tenants"], queryFn: () => listTenants() });
  const types = useQuery({
    queryKey: ["asset-types", tenantId],
    queryFn: () => listAssetTypes({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });

  const createMutation = useMutation({
    mutationFn: createAssetType,
    onSuccess: () => {
      message.success("Tipología creada");
      setCreateOpen(false);
      form.resetFields();
      queryClient.invalidateQueries({ queryKey: ["asset-types", tenantId] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error al crear tipología"),
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
      <Space wrap>
        <Select
          style={{ minWidth: 240 }}
          placeholder="Organización"
          loading={tenants.isLoading}
          value={tenantId}
          onChange={(value) => setTenantId(value)}
          options={(tenants.data?.results ?? []).map((t) => ({ value: t.id, label: t.name }))}
        />
        <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
          Nueva tipología
        </Button>
      </Space>

      <Table<AssetType>
        rowKey="id"
        dataSource={types.data?.results ?? []}
        loading={types.isLoading}
        pagination={{ pageSize: 20 }}
        columns={[
          { title: "Código", dataIndex: "code" },
          { title: "Nombre", dataIndex: "name" },
          {
            title: "Tipo",
            dataIndex: "kind",
            render: (value: string) => (value === "gateway" ? <Tag color="purple">gateway</Tag> : <Tag>estándar</Tag>),
          },
          {
            title: "Atributos de plantilla",
            render: (_, record) => record.schema?.attributes?.length ?? 0,
          },
        ]}
      />

      <Modal
        title="Nueva tipología"
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => form.submit()}
        confirmLoading={createMutation.isPending}
        width={720}
      >
        <Form form={form} layout="vertical" onFinish={onCreate} initialValues={{ kind: "standard" }}>
          <Space.Compact block>
            <Form.Item name="name" label="Nombre" rules={[{ required: true }]} style={{ flex: 1 }}>
              <Input />
            </Form.Item>
            <Form.Item name="code" label="Código" rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]} style={{ flex: 1 }}>
              <Input />
            </Form.Item>
            <Form.Item name="kind" label="Tipo" style={{ width: 160 }}>
              <Select
                options={[
                  { value: "standard", label: "Estándar" },
                  { value: "gateway", label: "Gateway" },
                ]}
              />
            </Form.Item>
          </Space.Compact>

          <Typography.Text strong>Atributos de plantilla (se crean al crear un activo con esta tipología)</Typography.Text>
          <Form.List name="attributes">
            {(fields, { add, remove }) => (
              <div style={{ marginTop: 12 }}>
                {fields.map((field) => (
                  <Space key={field.key} align="baseline" style={{ display: "flex", marginBottom: 8 }}>
                    <Form.Item name={[field.name, "code"]} rules={[{ required: true }]} style={{ marginBottom: 0 }}>
                      <Input placeholder="código" />
                    </Form.Item>
                    <Form.Item name={[field.name, "name"]} style={{ marginBottom: 0 }}>
                      <Input placeholder="nombre" />
                    </Form.Item>
                    <Form.Item name={[field.name, "value_type"]} initialValue="number" rules={[{ required: true }]} style={{ marginBottom: 0 }}>
                      <Select style={{ width: 120 }} options={VALUE_TYPES} />
                    </Form.Item>
                    <Form.Item name={[field.name, "storage_datapoint"]} valuePropName="checked" initialValue={true} style={{ marginBottom: 0 }}>
                      <Checkbox>store</Checkbox>
                    </Form.Item>
                    <Button type="text" danger onClick={() => remove(field.name)}>
                      Quitar
                    </Button>
                  </Space>
                ))}
                <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                  Agregar atributo
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
  const queryClient = useQueryClient();
  const attributes = useQuery({
    queryKey: ["attributes", asset?.id],
    queryFn: () => listAttributes(asset?.id ?? ""),
    enabled: Boolean(asset),
  });
  const attrMutation = useMutation({
    mutationFn: createAttribute,
    onSuccess: () => {
      message.success("Atributo creado");
      form.resetFields();
      queryClient.invalidateQueries({ queryKey: ["attributes", asset?.id] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error al crear atributo"),
  });

  function onCreateAttribute(values: { name: string; code: string; value_type: string; storage_datapoint: boolean }) {
    if (!asset) return;
    attrMutation.mutate({ asset: asset.id, ...values });
  }

  return (
    <Drawer
      title={asset ? `Atributos — ${asset.name}` : "Atributos"}
      open={Boolean(asset)}
      onClose={onClose}
      width={560}
    >
      <Table
        rowKey="id"
        size="small"
        dataSource={attributes.data?.results ?? []}
        loading={attributes.isLoading}
        pagination={false}
        columns={[
          { title: "Código", dataIndex: "code" },
          { title: "Nombre", dataIndex: "name" },
          { title: "Tipo", dataIndex: "value_type" },
          {
            title: "Store",
            dataIndex: "storage_datapoint",
            render: (value: boolean) => (value ? <Tag color="blue">on</Tag> : <Tag>off</Tag>),
          },
        ]}
      />
      <Typography.Title level={5} style={{ marginTop: 16 }}>
        Nuevo atributo
      </Typography.Title>
      <Form form={form} layout="vertical" onFinish={onCreateAttribute}>
        <Form.Item name="name" label="Nombre" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="code" label="Código" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="value_type" label="Tipo de valor" initialValue="number" rules={[{ required: true }]}>
          <Select options={VALUE_TYPES} />
        </Form.Item>
        <Form.Item name="storage_datapoint" label="Almacenar datapoints" valuePropName="checked" initialValue={true}>
          <Checkbox />
        </Form.Item>
        <Button type="primary" htmlType="submit" loading={attrMutation.isPending}>
          Crear atributo
        </Button>
      </Form>
    </Drawer>
  );
}
