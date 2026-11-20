import { CopyOutlined, PlusOutlined, ReloadOutlined } from "@ant-design/icons";
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
import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import GridLayout, { WidthProvider } from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import {
  applyTemplate,
  createDashboard,
  createWidget,
  deleteWidget,
  exportBundle,
  importBundle,
  listAssets,
  listAttributes,
  listBundles,
  listDashboards,
  listGateways,
  listScenes,
  listSymbols,
  listTemplates,
  telemetryCurrent,
  telemetryHistory,
  telemetryTrend,
  updateWidget,
} from "../api/endpoints";
import type { Dashboard, DashboardWidget, Scene } from "../api/endpoints";
import { useAppContext } from "../contexts/AppContext";
import * as echarts from "echarts";

const ResponsiveGridLayout = WidthProvider(GridLayout) as unknown as React.ComponentType<Record<string, unknown>>;

interface GridItem {
  i: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export default function DashboardsPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [selected, setSelected] = useState<Dashboard | null>(null);
  const [widgetOpen, setWidgetOpen] = useState(false);
  const [editingWidget, setEditingWidget] = useState<DashboardWidget | null>(null);
  const [bundlesOpen, setBundlesOpen] = useState(false);
  const [templatesOpen, setTemplatesOpen] = useState(false);
  const [form] = Form.useForm();
  const [widgetForm] = Form.useForm();

  const dashboards = useQuery({
    queryKey: ["dashboards", tenantId],
    queryFn: () => listDashboards({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });

  const bundles = useQuery({
    queryKey: ["dashboards-bundles", tenantId],
    queryFn: () => listBundles({ tenant: tenantId }),
    enabled: Boolean(tenantId) && bundlesOpen,
  });

  const templates = useQuery({
    queryKey: ["dashboards-templates", tenantId],
    queryFn: () => listTemplates({ tenant: tenantId }),
    enabled: Boolean(tenantId) && templatesOpen,
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["dashboards", tenantId] });

  const importBundleMutation = useMutation({
    mutationFn: importBundle,
    onSuccess: (dash) => {
      message.success(t("dash.bundleImported"));
      setBundlesOpen(false);
      invalidate();
      setSelected(dash);
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const applyTemplateMutation = useMutation({
    mutationFn: ({ id }: { id: string }) => applyTemplate(id, {}),
    onSuccess: (dash) => {
      message.success(t("dash.templateApplied"));
      setTemplatesOpen(false);
      invalidate();
      setSelected(dash);
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

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
        <Button disabled={!tenantId} onClick={() => setBundlesOpen(true)}>
          {t("dash.bundles")}
        </Button>
        <Button disabled={!tenantId} onClick={() => setTemplatesOpen(true)}>
          {t("dash.templates")}
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

      <Modal
        title={t("dash.bundles")}
        open={bundlesOpen}
        onCancel={() => setBundlesOpen(false)}
        footer={null}
        width={560}
      >
        <Table
          size="small"
          rowKey="id"
          loading={bundles.isLoading}
          dataSource={bundles.data?.results ?? []}
          pagination={false}
          columns={[
            { title: t("assets.name"), dataIndex: "name" },
            {
              title: "",
              render: (_: unknown, record) => (
                <Button
                  size="small"
                  type="primary"
                  loading={importBundleMutation.isPending}
                  onClick={() => importBundleMutation.mutate(record.id)}
                >
                  {t("dash.importBundle")}
                </Button>
              ),
            },
          ]}
        />
      </Modal>

      <Modal
        title={t("dash.templates")}
        open={templatesOpen}
        onCancel={() => setTemplatesOpen(false)}
        footer={null}
        width={560}
      >
        <Table
          size="small"
          rowKey="id"
          loading={templates.isLoading}
          dataSource={templates.data?.results ?? []}
          pagination={false}
          columns={[
            { title: t("assets.name"), dataIndex: "name" },
            { title: t("dash.category"), dataIndex: "category" },
            {
              title: "",
              render: (_: unknown, record) => (
                <Button
                  size="small"
                  type="primary"
                  loading={applyTemplateMutation.isPending}
                  onClick={() => applyTemplateMutation.mutate({ id: record.id })}
                >
                  {t("dash.applyTemplate")}
                </Button>
              ),
            },
          ]}
        />
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
              attribute_ids: widget.config?.attribute_ids ?? undefined,
              scene_id: widget.config?.scene_id ?? undefined,
              gateway_id: widget.config?.gateway_id ?? undefined,
              interval: widget.config?.interval ?? undefined,
              downsample: widget.config?.downsample ?? undefined,
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
            attribute_ids?: string[];
            scene_id?: string;
            gateway_id?: string;
            interval?: string;
            downsample?: string;
          }) => {
            if (!selected && !editingWidget) return;
            const attribute_ids = values.attribute_ids?.length
              ? values.attribute_ids
              : values.attribute_id
                ? [values.attribute_id]
                : [];
            const config = {
              attribute_id: values.attribute_id ?? null,
              attribute_ids,
              scene_id: values.scene_id ?? null,
              gateway_id: values.gateway_id ?? null,
              interval: values.interval ?? null,
              downsample: values.downsample ?? null,
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
                { value: "trend", label: "Tendencia (multi-serie)" },
                { value: "gauge", label: "Gauge" },
                { value: "card", label: "Card" },
                { value: "table", label: "Tabla" },
                { value: "map", label: "Mapa" },
                { value: "gateway", label: "Gateway (estado)" },
              ]}
            />
          </Form.Item>
          <Form.Item noStyle shouldUpdate={(prev, next) => prev.widget_type !== next.widget_type}>
            {({ getFieldValue }) =>
              getFieldValue("widget_type") === "trend" ? <MultiAttributePicker /> : <AttributePicker />
            }
          </Form.Item>
          <Form.Item noStyle shouldUpdate={(prev, next) => prev.widget_type !== next.widget_type}>
            {({ getFieldValue }) =>
              getFieldValue("widget_type") === "trend" ? (
                <Space wrap>
                  <Form.Item name="interval" label={t("dash.trendInterval")} initialValue="1m">
                    <Select
                      style={{ width: 140 }}
                      options={[
                        { value: "10s", label: "10s" },
                        { value: "1m", label: "1m" },
                        { value: "5m", label: "5m" },
                        { value: "15m", label: "15m" },
                        { value: "1h", label: "1h" },
                        { value: "1d", label: "1d" },
                      ]}
                    />
                  </Form.Item>
                  <Form.Item name="downsample" label={t("dash.trendDownsample")} initialValue="avg">
                    <Select
                      style={{ width: 140 }}
                      options={[
                        { value: "avg", label: "Promedio" },
                        { value: "lttb", label: "LTTB" },
                        { value: "none", label: "Sin reducir" },
                      ]}
                    />
                  </Form.Item>
                </Space>
              ) : null
            }
          </Form.Item>
          <ScenePicker />
          <GatewayPicker />
        </Form>
      </Modal>
    </Space>
  );
}

function MultiAttributePicker() {
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
      <Form.Item name="trend_asset_id" label={t("assets.title")}>
        <Select
          onChange={(value) => setAssetId(value)}
          options={(assets.data?.results ?? []).map((a) => ({ value: a.id, label: a.name }))}
        />
      </Form.Item>
      <Form.Item name="attribute_ids" label={t("dash.trendAttributes")}>
        <Select
          mode="multiple"
          disabled={!assetId}
          options={(attributes.data?.results ?? []).map((a) => ({ value: a.id, label: `${a.code} (${a.name})` }))}
        />
      </Form.Item>
    </>
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
  const updateLayout = useMutation({
    mutationFn: ({ id, input }: { id: string; input: Partial<DashboardWidget> }) => updateWidget(id, input),
  });
  const exportMutation = useMutation({
    mutationFn: () => exportBundle(dashboard.id, { name: `${dashboard.name} (bundle)` }),
    onSuccess: () => message.success(t("dash.bundleExported")),
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });
  const layout = useMemo(
    () =>
      dashboard.widgets.map((widget) => ({
        i: widget.id as string,
        x: widget.x,
        y: widget.y,
        w: Math.max(1, widget.w),
        h: Math.max(1, widget.h),
      })),
    [dashboard.widgets],
  );
  return (
    <Card
      title={dashboard.name}
      extra={
        <Space>
          <Button icon={<CopyOutlined />} loading={exportMutation.isPending} onClick={() => exportMutation.mutate()}>
            {t("dash.exportBundle")}
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={onWidget}>
            {t("dash.newWidget")}
          </Button>
          <Button onClick={onClose}>{t("common.cancel")}</Button>
        </Space>
      }
    >
      <ResponsiveGridLayout
        className="layout"
        layouts={{ lg: layout }}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
        rowHeight={60}
        margin={[12, 12]}
        draggableHandle=".widget-drag-handle"
        onLayoutChange={(rawItems: unknown) => {
          const items = rawItems as unknown as GridItem[];
          for (const item of items) {
            const widget = dashboard.widgets.find((w) => w.id === item.i);
            if (!widget) continue;
            if (widget.x !== item.x || widget.y !== item.y || widget.w !== item.w || widget.h !== item.h) {
              updateLayout.mutate({ id: item.i, input: { x: item.x, y: item.y, w: item.w, h: item.h } });
            }
          }
        }}
      >
        {dashboard.widgets.map((widget) => (
          <div key={widget.id}>
            <Card
              size="small"
              className="widget-drag-handle"
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
          </div>
        ))}
      </ResponsiveGridLayout>
      {dashboard.widgets.length === 0 && <Empty description={t("dash.noWidgets")} />}
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
  if (widget.widget_type === "trend") {
    return <TrendWidget widget={widget} />;
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

function TrendWidget({ widget }: { widget: DashboardWidget }) {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const ref = useRef<HTMLDivElement>(null);
  const attributeIds = (widget.config?.attribute_ids as string[] | undefined) ?? [];
  const interval = (widget.config?.interval as string | undefined) ?? "1m";
  const downsample = (widget.config?.downsample as string | undefined) ?? "avg";
  const trend = useQuery({
    queryKey: ["trend", attributeIds.join(","), interval, downsample],
    queryFn: () =>
      telemetryTrend({
        attributes: attributeIds,
        tenant: tenantId ?? undefined,
        interval,
        downsample,
      }),
    enabled: attributeIds.length > 0 && Boolean(tenantId),
    refetchInterval: 30000,
  });
  useEffect(() => {
    if (!ref.current || !trend.data?.series.length) return;
    const chart = echarts.init(ref.current);
    const series = trend.data.series;
    const yAxisIds = series.map((_, index) => `axis-${index}`);
    chart.setOption({
      tooltip: { trigger: "axis" },
      legend: { data: series.map((s) => `${s.name}${s.unit ? ` (${s.unit})` : ""}`), top: 0 },
      grid: { left: 48, right: series.length > 1 ? 56 : 16, top: 28, bottom: 48 },
      xAxis: { type: "time" },
      yAxis: series.map((s, index) => ({
        id: yAxisIds[index],
        type: "value",
        position: index === 0 ? "left" : "right",
        offset: index > 0 ? (index - 1) * 48 : 0,
        axisLabel: { formatter: s.unit ? `{value} ${s.unit}` : "{value}" },
      })),
      dataZoom: [{ type: "inside" }, { type: "slider", height: 18, bottom: 6 }],
      series: series.map((s, index) => ({
        name: `${s.name}${s.unit ? ` (${s.unit})` : ""}`,
        type: "line",
        yAxisIndex: index,
        yAxisId: yAxisIds[index],
        showSymbol: false,
        connectNulls: false,
        data: s.points.map((p) => [p.ts, p.gap ? null : p.value]),
      })),
    });
    return () => chart.dispose();
  }, [trend.data]);
  if (attributeIds.length === 0) return <Empty description={t("dash.selectAttribute")} />;
  if (!trend.data?.series.length) return <Empty description={t("tel.noHistory")} />;
  return <div ref={ref} style={{ height: 220 }} />;
}

function MapWidget({ sceneId }: { sceneId?: string }) {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const scenes = useQuery({
    queryKey: ["scenes", tenantId],
    queryFn: () => listScenes({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const symbols = useQuery({
    queryKey: ["symbols"],
    queryFn: listSymbols,
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
              width: 18,
              height: 18,
              transform: "translate(-50%, -50%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "50%",
              background: "#e6f4ff",
              border: "1px solid #1677ff",
              color: "#1677ff",
              fontSize: 10,
            }}
          >
            {symbols.data?.symbols.some((s) => s.key === pl.symbol) ? (
              <Typography.Text style={{ fontSize: 10, color: "#1677ff" }}>
                {pl.symbol?.slice(0, 2).toUpperCase()}
              </Typography.Text>
            ) : (
              <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#1677ff" }} />
            )}
          </div>
        ))}
    </div>
  );
}
