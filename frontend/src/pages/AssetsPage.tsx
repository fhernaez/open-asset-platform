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
  Tag,
  Typography,
  message,
} from "antd";
import type { FormInstance } from "antd";
import { useState } from "react";
import {
  createAsset,
  createAttribute,
  listAssets,
  listAttributes,
  listProjects,
  listTenants,
} from "../api/endpoints";
import type { Asset } from "../api/types";

const VALUE_TYPES = [
  { value: "number", label: "Número" },
  { value: "string", label: "Texto" },
  { value: "boolean", label: "Booleano" },
  { value: "json", label: "JSON" },
];

export default function AssetsPage() {
  const queryClient = useQueryClient();
  const [tenantId, setTenantId] = useState<string>();
  const [projectId, setProjectId] = useState<string>();
  const [createOpen, setCreateOpen] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [createForm] = Form.useForm();
  const [attrForm] = Form.useForm();

  const tenants = useQuery({ queryKey: ["tenants"], queryFn: () => listTenants() });
  const projects = useQuery({
    queryKey: ["projects", tenantId],
    queryFn: () => listProjects(tenantId ?? ""),
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

  function onCreate(values: { name: string; external_ref: string }) {
    if (!tenantId) return;
    createMutation.mutate({
      tenant: tenantId,
      project: projectId ?? null,
      name: values.name,
      external_ref: values.external_ref,
    });
  }

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Typography.Title level={4} style={{ margin: 0 }}>
        Activos
      </Typography.Title>
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
        <Button
          icon={<ReloadOutlined />}
          onClick={() => queryClient.invalidateQueries({ queryKey: ["assets"] })}
        >
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
