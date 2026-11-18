import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Alert, Button, Card, Col, Descriptions, Empty, Form, InputNumber, Modal, Row, Select, Space, Statistic, Tag, Typography, message } from "antd";
import type { FormInstance } from "antd";
import * as echarts from "echarts";
import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  effectivePolicy,
  gatewayStoragePolicy,
  listAssets,
  listAttributes,
  listGateways,
  telemetryCurrent,
  telemetryHistory,
  telemetryStats,
} from "../api/endpoints";
import { useAppContext } from "../contexts/AppContext";

export default function TelemetryPage() {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const [assetId, setAssetId] = useState<string>();
  const [attributeId, setAttributeId] = useState<string>();
  const [gatewayId, setGatewayId] = useState<string>();
  const [policyOpen, setPolicyOpen] = useState(false);
  const [policyForm] = Form.useForm();

  const assets = useQuery({
    queryKey: ["assets", tenantId],
    queryFn: () => listAssets({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const gateways = useQuery({
    queryKey: ["gateways", tenantId],
    queryFn: () => listGateways({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const attributes = useQuery({
    queryKey: ["attributes", assetId],
    queryFn: () => listAttributes(assetId ?? ""),
    enabled: Boolean(assetId),
  });
  const current = useQuery({
    queryKey: ["current", attributeId],
    queryFn: () => telemetryCurrent(attributeId ?? ""),
    enabled: Boolean(attributeId),
  });
  const stats = useQuery({
    queryKey: ["stats", attributeId],
    queryFn: () => telemetryStats(attributeId ?? ""),
    enabled: Boolean(attributeId),
  });
  const policy = useQuery({
    queryKey: ["policy", attributeId, gatewayId],
    queryFn: () => effectivePolicy(attributeId ?? "", gatewayId),
    enabled: Boolean(attributeId),
  });

  const attribute = useMemo(
    () => (attributes.data?.results ?? []).find((a) => a.id === attributeId),
    [attributes.data, attributeId],
  );

  const selectedGateway = useMemo(
    () => (gateways.data?.results ?? []).find((g) => g.id === gatewayId),
    [gateways.data, gatewayId],
  );

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Typography.Title level={4} style={{ margin: 0 }}>
        {t("tel.title")}
      </Typography.Title>
      <Space wrap>
        <Select
          style={{ minWidth: 220 }}
          placeholder={t("assets.title")}
          value={assetId}
          onChange={(value) => {
            setAssetId(value);
            setAttributeId(undefined);
          }}
          options={(assets.data?.results ?? []).map((a) => ({ value: a.id, label: a.name }))}
        />
        <Select
          style={{ minWidth: 220 }}
          placeholder={t("attributes.title")}
          disabled={!assetId}
          value={attributeId}
          onChange={(value) => setAttributeId(value)}
          options={(attributes.data?.results ?? []).map((a) => ({ value: a.id, label: a.code }))}
        />
        <Select
          style={{ minWidth: 220 }}
          placeholder={t("conn.title")}
          allowClear
          value={gatewayId}
          onChange={(value) => setGatewayId(value)}
          options={(gateways.data?.results ?? []).map((g) => ({ value: g.id, label: g.protocol }))}
        />
        <Button
          type="primary"
          disabled={!attributeId || !gatewayId}
          onClick={() => {
            policyForm.setFieldsValue({
              mode: (policy.data as { mode?: string })?.mode ?? "on_change",
            });
            setPolicyOpen(true);
          }}
        >
          {t("tel.editGatewayPolicy")}
        </Button>
      </Space>

      {!attributeId && <Empty description={t("tel.noData")} />}
      {selectedGateway && (
        <Card size="small" title={t("conn.title")}>
          <Space wrap>
            <Tag color="purple">{selectedGateway.protocol}</Tag>
            <Tag color={selectedGateway.connection_status === "connected" ? "green" : "default"}>
              {selectedGateway.connection_status}
            </Tag>
            <Typography.Text type="secondary">{selectedGateway.asset_name}</Typography.Text>
          </Space>
        </Card>
      )}
      {attributeId && (
        <>
          <Row gutter={16}>
            <Col span={6}>
              <Card>
                <Statistic
                  title={t("tel.current")}
                  value={String((current.data as { value?: unknown })?.value ?? "—")}
                  valueStyle={{ color: (current.data as { quality?: string })?.quality === "invalid" ? "#cf1322" : "#1677ff" }}
                />
                <Typography.Text type="secondary">
                  {(current.data as { quality?: string })?.quality ?? ""}
                </Typography.Text>
              </Card>
            </Col>
            {stats.data && (
              <>
                <Col span={4}>
                  <Card>
                    <Statistic title={t("tel.received")} value={stats.data.totals.received} />
                  </Card>
                </Col>
                <Col span={4}>
                  <Card>
                    <Statistic title={t("tel.accepted")} value={stats.data.totals.accepted} />
                  </Card>
                </Col>
                <Col span={5}>
                  <Card>
                    <Statistic title={t("tel.filteredEqual")} value={stats.data.totals.filtered_equal} />
                  </Card>
                </Col>
                <Col span={5}>
                  <Card>
                    <Statistic title={t("tel.filteredQuota")} value={stats.data.totals.filtered_quota} />
                  </Card>
                </Col>
              </>
            )}
          </Row>

          <Card title={t("tel.history")}>
            <HistoryChart attributeId={attributeId} />
          </Card>

          <Card title={t("tel.policy")}>
            {policy.isError && <Alert type="error" showIcon message={t("tel.policyError")} />}
            {policy.data && (
              <Descriptions column={2} size="small">
                <Descriptions.Item label={t("tel.mode")}>
                  <Tag color="blue">{(policy.data as { mode?: string }).mode}</Tag>
                </Descriptions.Item>
                <Descriptions.Item label="max_samples">
                  {(policy.data as { max_samples?: { count?: number | null; window?: string | null } }).max_samples?.count ?? "—"} /{" "}
                  {(policy.data as { max_samples?: { count?: number | null; window?: string | null } }).max_samples?.window ?? "—"}
                </Descriptions.Item>
                <Descriptions.Item label={t("tel.source")}>
                  {(policy.data as { source?: string }).source}
                </Descriptions.Item>
              </Descriptions>
            )}
          </Card>
        </>
      )}

      <PolicyModal
        open={policyOpen}
        form={policyForm}
        gatewayId={gatewayId}
        attribute={attribute}
        onClose={() => setPolicyOpen(false)}
      />
    </Space>
  );
}

function HistoryChart({ attributeId }: { attributeId: string }) {
  const { t } = useTranslation();
  const ref = useRef<HTMLDivElement>(null);
  const history = useQuery({
    queryKey: ["history", attributeId],
    queryFn: () => telemetryHistory(attributeId),
    enabled: Boolean(attributeId),
    refetchInterval: 15000,
  });

  useEffect(() => {
    if (!ref.current || !history.data) return;
    const chart = echarts.init(ref.current);
    const points = history.data.points;
    chart.setOption({
      grid: { left: 60, right: 20, top: 20, bottom: 30 },
      xAxis: { type: "time" },
      yAxis: { type: "value" },
      tooltip: { trigger: "axis" },
      series: [
        {
          type: "line",
          showSymbol: false,
          data: points.map((p) => [p.ts, p.value]),
        },
      ],
    });
    return () => chart.dispose();
  }, [history.data]);

  if (!history.data || history.data.points.length === 0) {
    return <Empty description={t("tel.noHistory")} />;
  }
  return <div ref={ref} style={{ height: 300 }} />;
}

function PolicyModal({
  open,
  form,
  gatewayId,
  attribute,
  onClose,
}: {
  open: boolean;
  form: FormInstance;
  gatewayId?: string;
  attribute?: { id: string } | undefined;
  onClose: () => void;
}) {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: ({ id, policy }: { id: string; policy: Record<string, unknown> }) => gatewayStoragePolicy(id, policy),
    onSuccess: () => {
      message.success(t("common.save"));
      onClose();
      queryClient.invalidateQueries({ queryKey: ["policy"] });
      queryClient.invalidateQueries({ queryKey: ["gateways"] });
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Modal
      title={t("tel.editGatewayPolicy")}
      open={open}
      onCancel={onClose}
      onOk={() => form.submit()}
      confirmLoading={mutation.isPending}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={(values: { mode: string; count?: number; window?: string }) => {
          if (!gatewayId) return;
          mutation.mutate({
            id: gatewayId,
            policy: {
              mode: values.mode,
              max_samples: { count: values.count ?? 60, window: values.window ?? "PT1H" },
            },
          });
        }}
      >
        <Form.Item name="mode" label={t("tel.mode")} initialValue="on_change" rules={[{ required: true }]}>
          <Select
            options={[
              { value: "on_change", label: "on_change" },
              { value: "all", label: "all" },
              { value: "min_interval", label: "min_interval" },
            ]}
          />
        </Form.Item>
        <Form.Item name="count" label="max_samples.count">
          <InputNumber min={1} style={{ width: "100%" }} />
        </Form.Item>
        <Form.Item name="window" label="max_samples.window">
          <Select
            options={[
              { value: "PT1H", label: "1 hora" },
              { value: "PT24H", label: "24 horas" },
              { value: "P7D", label: "7 días" },
            ]}
          />
        </Form.Item>
      </Form>
      {attribute && (
        <Typography.Text type="secondary">
          {t("tel.policyHint")}
        </Typography.Text>
      )}
    </Modal>
  );
}
