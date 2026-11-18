import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Card,
  Empty,
  Form,
  Input,
  InputNumber,
  Modal,
  Select,
  Space,
  Typography,
  Upload,
  message,
} from "antd";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import MapConfigEditor from "../components/MapConfigEditor";
import {
  addSceneLayer,
  createPlacement,
  createScene,
  deletePlacement,
  getMapConfig,
  listAssets,
  listScenes,
} from "../api/endpoints";
import type { Scene } from "../api/endpoints";
import { useAppContext } from "../contexts/AppContext";

export default function MapsPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { tenantId, projectId } = useAppContext();
  const [createOpen, setCreateOpen] = useState(false);
  const [selected, setSelected] = useState<Scene | null>(null);
  const [layerOpen, setLayerOpen] = useState(false);
  const [form] = Form.useForm();
  const [layerForm] = Form.useForm();
  const [layerImage, setLayerImage] = useState<File | null>(null);

  const scenes = useQuery({
    queryKey: ["scenes", tenantId],
    queryFn: () => listScenes({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });
  const mapConfig = useQuery({
    queryKey: ["map-config", projectId],
    queryFn: () => getMapConfig(projectId ?? ""),
    enabled: Boolean(projectId),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["scenes", tenantId] });

  const createMutation = useMutation({
    mutationFn: createScene,
    onSuccess: () => {
      message.success(t("maps.sceneCreated"));
      setCreateOpen(false);
      form.resetFields();
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const layerMutation = useMutation({
    mutationFn: (input: { sceneId: string; key: string; name?: string; image: File }) =>
      addSceneLayer(input.sceneId, input),
    onSuccess: () => {
      message.success(t("maps.layerCreated"));
      setLayerOpen(false);
      layerForm.resetFields();
      setLayerImage(null);
      invalidate();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Space wrap>
        <Typography.Title level={4} style={{ margin: 0 }}>
          {t("maps.title")}
        </Typography.Title>
        <Button type="primary" icon={<PlusOutlined />} disabled={!tenantId} onClick={() => setCreateOpen(true)}>
          {t("maps.createScene")}
        </Button>
      </Space>

      <Card title={t("maps.globalMap")}>
        {projectId ? (
          <MapConfigEditor
            projectId={projectId}
            initialBounds={mapConfig.data?.bounds ?? null}
            onSaved={() => queryClient.invalidateQueries({ queryKey: ["map-config", projectId] })}
          />
        ) : (
          <Empty description={t("maps.selectProject")} />
        )}
      </Card>

      {scenes.isError && <Alert type="error" showIcon message={t("maps.loadError")} />}
      {!scenes.isError && scenes.data?.results.length === 0 && <Empty description={t("maps.noData")} />}

      <Space wrap>
        {(scenes.data?.results ?? []).map((scene) => (
          <Card
            key={scene.id}
            hoverable
            title={scene.name}
            style={{ width: 260 }}
            onClick={() => setSelected(scene)}
          >
            {t("maps.layers")}: {scene.layers.length} · {t("maps.placements")}: {scene.placements.length}
          </Card>
        ))}
      </Space>

      <Modal
        title={t("maps.createScene")}
        open={createOpen}
        onCancel={() => setCreateOpen(false)}
        onOk={() => form.submit()}
        confirmLoading={createMutation.isPending}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={(values: { name: string; description?: string }) => {
            if (!tenantId) return;
            createMutation.mutate({ tenant: tenantId, name: values.name, description: values.description });
          }}
        >
          <Form.Item name="name" label={t("assets.name")} rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="description" label={t("maps.description")}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      {selected && (
        <SceneEditor
          scene={selected}
          onAddLayer={() => setLayerOpen(true)}
          onClose={() => setSelected(null)}
          onChanged={invalidate}
        />
      )}

      <Modal
        title={t("maps.addLayer")}
        open={layerOpen}
        onCancel={() => setLayerOpen(false)}
        onOk={() => {
          if (!selected || !layerImage) return;
          layerMutation.mutate({
            sceneId: selected.id,
            key: layerForm.getFieldValue("key") ?? "layer",
            name: layerForm.getFieldValue("name"),
            image: layerImage,
          });
        }}
        confirmLoading={layerMutation.isPending}
      >
        <Form form={layerForm} layout="vertical">
          <Form.Item name="key" label={t("maps.layerKey")} rules={[{ required: true, pattern: /^[a-z0-9-]+$/ }]}>
            <Input />
          </Form.Item>
          <Form.Item name="name" label={t("assets.name")}>
            <Input />
          </Form.Item>
          <Upload
            accept="image/*"
            maxCount={1}
            beforeUpload={(file) => {
              setLayerImage(file);
              return false;
            }}
          >
            <Button icon={<UploadOutlined />}>{t("maps.selectImage")}</Button>
          </Upload>
        </Form>
      </Modal>
    </Space>
  );
}

function SceneEditor({
  scene,
  onAddLayer,
  onClose,
  onChanged,
}: {
  scene: Scene;
  onAddLayer: () => void;
  onClose: () => void;
  onChanged: () => void;
}) {
  const { t } = useTranslation();
  const { tenantId } = useAppContext();
  const [assetId, setAssetId] = useState<string>();
  const [layerId, setLayerId] = useState<string>();
  const [x, setX] = useState<number>(0.5);
  const [y, setY] = useState<number>(0.5);

  const assets = useQuery({
    queryKey: ["assets", tenantId],
    queryFn: () => listAssets({ tenant: tenantId }),
    enabled: Boolean(tenantId),
  });

  const placementMutation = useMutation({
    mutationFn: createPlacement,
    onSuccess: () => {
      message.success(t("maps.placementCreated"));
      onChanged();
    },
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const deleteMutation = useMutation({
    mutationFn: deletePlacement,
    onSuccess: onChanged,
    onError: (err) => message.error(err instanceof Error ? err.message : "Error"),
  });

  const layer = scene.layers.find((l) => l.id === layerId) ?? scene.layers[0];

  return (
    <Card
      title={scene.name}
      extra={
        <Space>
          <Button icon={<PlusOutlined />} onClick={onAddLayer}>
            {t("maps.addLayer")}
          </Button>
          <Button onClick={onClose}>{t("common.cancel")}</Button>
        </Space>
      }
    >
      <Space wrap style={{ marginBottom: 12 }}>
        <Select
          style={{ minWidth: 200 }}
          placeholder={t("assets.title")}
          value={assetId}
          onChange={setAssetId}
          options={(assets.data?.results ?? []).map((a) => ({ value: a.id, label: a.name }))}
        />
        <Select
          style={{ minWidth: 160 }}
          placeholder={t("maps.layer")}
          value={layerId}
          onChange={setLayerId}
          options={scene.layers.map((l) => ({ value: l.id, label: l.name || l.key }))}
        />
        <InputNumber value={x} min={0} max={1} step={0.01} onChange={(v) => setX(Number(v ?? 0))} addonBefore="x" />
        <InputNumber value={y} min={0} max={1} step={0.01} onChange={(v) => setY(Number(v ?? 0))} addonBefore="y" />
        <Button
          type="primary"
          disabled={!assetId || !layer}
          onClick={() =>
            placementMutation.mutate({ scene: scene.id, layer: layer.id, asset: assetId ?? "", x, y, z: 0 })
          }
        >
          {t("maps.addPlacement")}
        </Button>
      </Space>

      <div
        style={{ position: "relative", width: "100%", height: 420, background: "#f0f0f0", overflow: "hidden" }}
        onClick={(event) => {
          if (!layer || !assetId) return;
          const rect = event.currentTarget.getBoundingClientRect();
          setX(Number(((event.clientX - rect.left) / rect.width).toFixed(3)));
          setY(Number(((event.clientY - rect.top) / rect.height).toFixed(3)));
          placementMutation.mutate({
            scene: scene.id,
            layer: layer.id,
            asset: assetId,
            x: Number(((event.clientX - rect.left) / rect.width).toFixed(3)),
            y: Number(((event.clientY - rect.top) / rect.height).toFixed(3)),
            z: 0,
          });
        }}
      >
        {layer?.image_url && (
          <img src={layer.image_url} alt={layer.name} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
        )}
        {scene.placements.map((pl) => (
          <div
            key={pl.id}
            title={pl.asset_name}
            onClick={(event) => {
              event.stopPropagation();
              deleteMutation.mutate(pl.id);
            }}
            style={{
              position: "absolute",
              left: `${((pl.x ?? 0.5) * 100).toFixed(2)}%`,
              top: `${((pl.y ?? 0.5) * 100).toFixed(2)}%`,
              width: 14,
              height: 14,
              borderRadius: "50%",
              background: "#1677ff",
              border: "2px solid #fff",
              transform: "translate(-50%, -50%)",
              cursor: "pointer",
            }}
          />
        ))}
      </div>
      {scene.layers.length === 0 && <Empty description={t("maps.noLayers")} />}
    </Card>
  );
}
