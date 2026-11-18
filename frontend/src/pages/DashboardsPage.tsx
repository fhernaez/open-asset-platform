import { PlusOutlined, ReloadOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Card,
  Col,
  Empty,
  Form,
  Input,
  Modal,
  Popconfirm,
  Row,
  Select,
  Space,
  Table,
  Tag,
  Typography,
  message,
} from "antd";
import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  createDashboard,
  createWidget,
  deleteWidget,
  listAssets,
  listAttributes,
  listDashboards,
  listGateways,
  listScenes,
  telemetryCurrent,
  telemetryHistory,
  updateWidget,
} from "../api/endpoints";
import type { Dashboard, DashboardWidget, Scene } from "../api/endpoints";
import { useAppContext } from "../contexts/AppContext";
import * as echarts from "echarts";

export default function DashboardsPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [selected, setSelected] = useState<Dashboard | null>(null);
  const [widgetOpen, setWidgetOpen] = useState(false);
  const [editingWidget, setEditingWidget] = useState<DashboardWidget | null>(null);
  const [form] = Form.useForm();
  const [widgetForm] = Form.useForm();

  const dashboards = useQuery({
    queryKey: ["dashboards", tenantId],
    queryFn: () => listDashboards({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["dashboards", tenantId] });

  const createMutation = useMutation({
    mutationFn: createDashboard,
    onSuccess: (dash) => {
      message.success(t("dash.created"));
      setCreateOpen(false);
      form.resetFields();
      invalidate();
      setSelected(dash);
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const widgetMutation = useMutation({
    mutationFn: createWidget,
    onSuccess: () => {
      message.success(t("dash.widgetCreated"));
      setWidgetOpen(false);
      widgetForm.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const updateWidgetMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: Partial<DashboardWidget> }) => updateWidget(id, input),
    onSuccess: () => {
      message.success(t("common.save"));
      setWidgetOpen(false);
      setEditingWidget(null);
      widgetForm.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteWidget,
    onSuccess: invalidate,
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Space wrap>
        <Typography.Title level={4} style={{ margin: 0 }}>
          {t("dash.title")}
        </Typography.Title>
        <Button icon={<ReloadOutlined />} onClick={invalidate}>
          {t("common.refresh")}
        </Button>
        <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
          {t("dash.create")}
        </Button>
      </Space>

      {dashboards.isError && <Alert type="error" showIcon message={t("dash.loadError")} />}
      {!dashboards.isError && dashboards.data?.results.length === 0 && <Empty description={t("dash.noData")} />}

      <Row gutter={16}>
        {(dashboards.data?.results ?? []).map((dash) => (
          <Col key={dash.id} span={8}>
            <Card
              hoverable
              title={dash.name}
              extra={<Tag>{dash.widgets.length}</Tag>}
              onClick={() => setSelected(dash)}
            >
              {t("dash.widgets")}: {dash.widgets.length}
            </Card>
          </Col>
        ))}
      </Row>

      <Modal
        title={t("dash.create")}
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => form.submit()}
        confirmLoading={createMutation.isPending}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={(values: { name: string }) => {
            if (!tenantId) return;
            createMutation.mutate({ tenant: tenantId, name: values.name });
          }}
        >
          <Form.Item name="name" label={t("assets.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      {selected && (
        <DashboardEditor
          dashboard={selected}
          onWidget={() => {
            setEditingWidget(null);
            widgetForm.resetFields();
            setWidgetOpen(true);
          }}
          onEditWidget={(widget) => {
            setEditingWidget(widget);
            widgetForm.setFieldsValue({
              title: widget.title,
              widget_type: widget.widget_type,
              attribute_id: widget.config?.attribute_id ?? undefined,
              scene_id: widget.config?.scene_id ?? undefined,
              gateway_id: widget.config?.gateway_id ?? undefined,
            });
            setWidgetOpen(true);
          }}
          onDeleteWidget={(id) => deleteMutation.mutate(id)}
          onClose={() => setSelected(null)}
        />
      )}

      <Modal
        title={editingWidget ? t("common.edit") : t("dash.newWidget")}
        open={widgetOpen}
        onCancel={() => {
          setWidgetOpen(false);
          setEditingWidget(null);
        }}
        onOk={() => widgetForm.submit()}
        confirmLoading={widgetMutation.isPending || updateWidgetMutation.isPending}
        width={640}
      >
        <Form
          form={widgetForm}
          layout="vertical"
          initialValues={{ widget_type: "line", w: 6, h: 3 }}
          onFinish={(values: {
            title: string;
            widget_type: string;
            attribute_id?: string;
            scene_id?: string;
            gateway_id?: string;
          }) => {
            if (!selected && !editingWidget) return;
            const config = {
              attribute_id: values.attribute_id ?? null,
              scene_id: values.scene_id ?? null,
              gateway_id: values.gateway_id ?? null,
            };
            if (editingWidget) {
              updateWidgetMutation.mutate({
                id: editingWidget.id as string,
                input: { title: values.title, widget_type: values.widget_type as DashboardWidget["widget_type"], config },
              });
            } else {
              widgetMutation.mutate({
                dashboard: selected!.id,
                title: values.title,
                widget_type: values.widget_type as DashboardWidget["widget_type"],
                x: 0,
                y: 0,
                w: 6,
                h: 3,
                config,
              });
            }
          }}
        >
          <Form.Item name="title" label={t("dash.widgetTitle")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="widget_type" label={t("dash.widgetType")} rules={[{ required: true }]}>
            <Select
              options={[
                { value: "line", label: "Línea" },
                { value: "gauge", label: "Gauge" },
                { value: "card", label: "Card" },
                { value: "table", label: "Tabla" },
                { value: "map", label: "Mapa" },
                { value: "gateway", label: "Gateway (estado)" },
              ]}
            />
          </Form.Item>
          <AttributePicker />
          <ScenePicker />
          <GatewayPicker />
        </Form>
      </Modal>
    </Space>
  );
}

function AttributePicker() {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const [assetId, setAssetId] = useState<string>();
  const assets = useQuery({
    queryKey: ["assets", tenantId],
    queryFn: () => listAssets({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const attributes = useQuery({
    queryKey: ["attributes", assetId],
    queryFn: () => listAttributes(assetId ?? ""),
    enabled: Boolean(assetId),
  });
  return (
    <>
      <Form.Item name="asset_id" label={t("assets.title")}>
        <Select
          onChange={(value) => setAssetId(value)}
          options={(assets.data?.results ?? []).map((a) => ({ value: a.id, label: a.name }))}
        />
      </Form.Item>
      <Form.Item name="attribute_id" label={t("attributes.title")}>
        <Select
          disabled={!assetId}
          options={(attributes.data?.results ?? []).map((a) => ({ value: a.id, label: a.code }))}
        />
      </Form.Item>
    </>
  );
}

function ScenePicker() {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const scenes = useQuery({
    queryKey: ["scenes", tenantId],
    queryFn: () => listScenes({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  return (
    <Form.Item name="scene_id" label={t("maps.scene")}>
      <Select
        allowClear
        options={(scenes.data?.results ?? []).map((s) => ({ value: s.id, label: s.name }))}
      />
    </Form.Item>
  );
}

function GatewayPicker() {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const gateways = useQuery({
    queryKey: ["gateways", tenantId],
    queryFn: () => listGateways({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  return (
    <Form.Item name="gateway_id" label={t("conn.selectGateway")}>
      <Select
        allowClear
        options={(gateways.data?.results ?? []).map((g) => ({
          value: g.id,
          label: `${g.asset_name ?? g.protocol} (${g.protocol})`,
        }))}
      />
    </Form.Item>
  );
}

function DashboardEditor({
  dashboard,
  onWidget,
  onEditWidget,
  onDeleteWidget,
  onClose,
}: {
  dashboard: Dashboard;
  onWidget: () => void;
  onEditWidget: (widget: DashboardWidget) => void;
  onDeleteWidget: (id: string) => void;
  onClose: () => void;
}) {
  const { t } = useTranslation();
  return (
    <Card
      title={dashboard.name}
      extra={
        <Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={onWidget}>
            {t("dash.newWidget")}
          </Button>
          <Button onClick={onClose}>{t("common.cancel")}</Button>
        </Space>
      }
    >
      <Row gutter={[16, 16]}>
        {dashboard.widgets.map((widget) => (
          <Col key={widget.id} span={Math.min(24, Math.max(6, widget.w * 2))}>
            <Card
              size="small"
              title={widget.title || widget.widget_type}
              extra={
                <Space>
                  <Button size="small" onClick={() => onEditWidget(widget)}>
                    {t("common.edit")}
                  </Button>
                  <Popconfirm
                    title={t("dash.deleteWidgetConfirm")}
                    onConfirm={() => widget.id && onDeleteWidget(widget.id)}
                  >
                    <Button size="small" danger>
                      {t("common.delete")}
                    </Button>
                  </Popconfirm>
                </Space>
              }
            >
              <WidgetRenderer widget={widget} />
            </Card>
          </Col>
        ))}
        {dashboard.widgets.length === 0 && <Empty description={t("dash.noWidgets")} />}
      </Row>
    </Card>
  );
}

function WidgetRenderer({ widget }: { widget: DashboardWidget }) {
  const attributeId = widget.config?.attribute_id as string | undefined;
  const current = useQuery({
    queryKey: ["current", attributeId],
    queryFn: () => telemetryCurrent(attributeId ?? ""),
    enabled: Boolean(attributeId) && ["card", "gauge", "stat"].includes(widget.widget_type),
  });
  if (widget.widget_type === "card" || widget.widget_type === "stat") {
    return (
      <Typography.Title level={2}>
        {String((current.data as { value?: unknown })?.value ?? "—")}
      </Typography.Title>
    );
  }
  if (widget.widget_type === "gauge") {
    return <GaugeWidget attributeId={attributeId} />;
  }
  if (widget.widget_type === "table") {
    return <TableWidget attributeId={attributeId} />;
  }
  if (widget.widget_type === "gateway") {
    return <GatewayStatusWidget gatewayId={widget.config?.gateway_id as string | undefined} />;
  }
  if (widget.widget_type === "line") {
    return <LineWidget attributeId={attributeId} />;
  }
  if (widget.widget_type === "map") {
    return <MapWidget sceneId={widget.config?.scene_id as string | undefined} />;
  }
  return <Typography.Text type="secondary">{widget.widget_type}</Typography.Text>;
}

function GaugeWidget({ attributeId }: { attributeId?: string }) {
  const { t } = useTranslation();
  const ref = useRef<HTMLDivElement>(null);
  const current = useQuery({
    queryKey: ["current", attributeId],
    queryFn: () => telemetryCurrent(attributeId ?? ""),
    enabled: Boolean(attributeId),
    refetchInterval: 10000,
  });
  useEffect(() => {
    if (!ref.current) return;
    const value = Number((current.data as { value?: unknown })?.value ?? 0);
    const chart = echarts.init(ref.current);
    chart.setOption({
      series: [{ type: "gauge", progress: { show: true }, detail: { formatter: "{value}" }, data: [{ value }] }],
    });
    return () => chart.dispose();
  }, [current.data]);
  if (!attributeId) return <Empty description={t("dash.selectAttribute")} />;
  return <div ref={ref} style={{ height: 160 }} />;
}

function TableWidget({ attributeId }: { attributeId?: string }) {
  const { t } = useTranslation();
  const history = useQuery({
    queryKey: ["history", attributeId],
    queryFn: () => telemetryHistory(attributeId ?? ""),
    enabled: Boolean(attributeId),
    refetchInterval: 15000,
  });
  const points = (history.data?.points ?? []).slice(-10).reverse();
  if (!attributeId) return <Empty description={t("dash.selectAttribute")} />;
  return (
    <Table
      size="small"
      pagination={false}
      rowKey="ts"
      dataSource={points}
      columns={[
        { title: "ts", dataIndex: "ts", render: (v: string) => v.slice(11, 19) },
        { title: "value", dataIndex: "value" },
      ]}
    />
  );
}

function GatewayStatusWidget({ gatewayId }: { gatewayId?: string }) {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const gateways = useQuery({
    queryKey: ["gateways", tenantId],
    queryFn: () => listGateways({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const gateway = (gateways.data?.results ?? []).find((g) => g.id === gatewayId);
  if (!gatewayId) return <Empty description={t("dash.selectGateway")} />;
  if (!gateway) return <Empty description={t("dash.gatewayNotFound")} />;
  return (
    <Space>
      <Typography.Text>{gateway.asset_name ?? gateway.protocol}</Typography.Text>
      <Tag color={gateway.connection_status === "connected" ? "green" : "default"}>
        {gateway.connection_status}
      </Tag>
    </Space>
  );
}

function LineWidget({ attributeId }: { attributeId?: string }) {
  const { t } = useTranslation();
  const ref = useRef<HTMLDivElement>(null);
  const history = useQuery({
    queryKey: ["history", attributeId],
    queryFn: () => telemetryHistory(attributeId ?? ""),
    enabled: Boolean(attributeId),
    refetchInterval: 15000,
  });
  useEffect(() => {
    if (!ref.current || !history.data?.points.length) return;
    const chart = echarts.init(ref.current);
    chart.setOption({
      grid: { left: 40, right: 10, top: 10, bottom: 20 },
      xAxis: { type: "time" },
      yAxis: { type: "value" },
      series: [{ type: "line", showSymbol: false, data: history.data.points.map((p) => [p.ts, p.value]) }],
    });
    return () => chart.dispose();
  }, [history.data]);
  if (!history.data?.points.length) return <Empty description={t("tel.noHistory")} />;
  return <div ref={ref} style={{ height: 200 }} />;
}

function MapWidget({ sceneId }: { sceneId?: string }) {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const scenes = useQuery({
    queryKey: ["scenes", tenantId],
    queryFn: () => listScenes({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const scene = (scenes.data?.results ?? []).find((s: Scene) => s.id === sceneId);
  if (!scene || scene.layers.length === 0) {
    return <Empty description={t("maps.noLayers")} />;
  }
  const layer = scene.layers[0];
  return (
    <div style={{ position: "relative", width: "100%", height: 220, overflow: "hidden" }}>
      {layer.image_url && <img src={layer.image_url} alt={layer.name} style={{ width: "100%", height: "100%", objectFit: "contain" }} />}
      {scene.placements
        .filter((pl) => pl.layer === layer.id || pl.layer === null)
        .map((pl) => (
          <div
            key={pl.id}
            title={pl.asset_name}
            style={{
              position: "absolute",
              left: `${((pl.x ?? 0.5) * 100).toFixed(1)}%`,
              top: `${((pl.y ?? 0.5) * 100).toFixed(1)}%`,
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#1677ff",
              transform: "translate(-50%, -50%)",
            }}
          />
        ))}
    </div>
  );
}
