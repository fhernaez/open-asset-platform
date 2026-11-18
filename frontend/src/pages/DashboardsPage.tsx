import { PlusOutlined, ReloadOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Alert, Button, Card, Col, Empty, Form, Input, Modal, Row, Select, Space, Tag, Typography, message } from "antd";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import {
  createDashboard,
  createWidget,
  deleteWidget,
  listAssets,
  listAttributes,
  listDashboards,
  listScenes,
  telemetryCurrent,
  telemetryHistory,
} from "../api/endpoints";
import type { Dashboard, DashboardWidget, Scene } from "../api/endpoints";
import { useAppContext } from "../contexts/AppContext";
import * as echarts from "echarts";
import { useEffect, useRef } from "react";

export default function DashboardsPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [selected, setSelected] = useState<Dashboard | null>(null);
  const [widgetOpen, setWidgetOpen] = useState(false);
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
          onWidget={() => setWidgetOpen(true)}
          onDeleteWidget={(id) => deleteMutation.mutate(id)}
          onClose={() => setSelected(null)}
        />
      )}

      <Modal
        title={t("dash.newWidget")}
        open={widgetOpen}
        onCancel={() => setWidgetOpen(false)}
        onOk={() => widgetForm.submit()}
        confirmLoading={widgetMutation.isPending}
        width={640}
      >
        <Form
          form={widgetForm}
          layout="vertical"
          initialValues={{ widget_type: "line", w: 6, h: 3 }}
          onFinish={(values: { title: string; widget_type: string; attribute_id: string; scene_id?: string }) => {
            if (!selected) return;
            widgetMutation.mutate({
              dashboard: selected.id,
              title: values.title,
              widget_type: values.widget_type as DashboardWidget["widget_type"],
              x: 0,
              y: 0,
              w: 6,
              h: 3,
              config: {
                attribute_id: values.attribute_id ?? null,
                scene_id: values.scene_id ?? null,
              },
            });
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
              ]}
            />
          </Form.Item>
          <AttributePicker />
          <ScenePicker />
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

function DashboardEditor({
  dashboard,
  onWidget,
  onDeleteWidget,
  onClose,
}: {
  dashboard: Dashboard;
  onWidget: () => void;
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
              extra={<Button size="small" danger onClick={() => widget.id && onDeleteWidget(widget.id)}>✕</Button>}
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
    enabled: Boolean(attributeId) && widget.widget_type === "card",
  });
  if (widget.widget_type === "card") {
    return (
      <Typography.Title level={2}>
        {String((current.data as { value?: unknown })?.value ?? "—")}
      </Typography.Title>
    );
  }
  if (widget.widget_type === "line") {
    return <LineWidget attributeId={attributeId} />;
  }
  if (widget.widget_type === "map") {
    return <MapWidget sceneId={widget.config?.scene_id as string | undefined} />;
  }
  return <Typography.Text type="secondary">{widget.widget_type}</Typography.Text>;
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
