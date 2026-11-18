import { useEffect, useRef, useState } from "react";
import { Map as MapLibreMap } from "maplibre-gl";
import type { MapMouseEvent } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Alert, Button, Space, Typography } from "antd";
import { useTranslation } from "react-i18next";
import { putMapConfig } from "../api/endpoints";
import type { MapBounds } from "../api/endpoints";

interface Point {
  lng: number;
  lat: number;
}

/**
 * Global map (MapLibre + OpenStreetMap, free). Drag with the mouse to draw the
 * rectangle of bounds where assets are located, then save.
 */
export default function MapConfigEditor({
  projectId,
  initialBounds,
  onSaved,
}: {
  projectId: string;
  initialBounds: MapBounds | null;
  onSaved: () => void;
}) {
  const { t } = useTranslation();
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const anchorRef = useRef<Point | null>(null);
  const [bounds, setBounds] = useState<MapBounds | null>(initialBounds);
  const [rect, setRect] = useState<{ left: string; top: string; width: string; height: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;
    const hasInitial = initialBounds?.north != null && initialBounds?.west != null;
    const center: [number, number] = hasInitial
      ? [
          (initialBounds!.west! + (initialBounds!.east ?? initialBounds!.west!)) / 2,
          (initialBounds!.north! + (initialBounds!.south ?? initialBounds!.north!)) / 2,
        ]
      : [-58.3816, -34.6037];
    const map = new MapLibreMap({
      container: containerRef.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: "© OpenStreetMap contributors",
          },
        },
        layers: [{ id: "osm", type: "raster", source: "osm", minzoom: 0, maxzoom: 19 }],
      },
      center,
      zoom: hasInitial ? 12 : 4,
    });

    function rectFrom(start: Point, end: Point) {
      const north = Math.max(start.lat, end.lat);
      const south = Math.min(start.lat, end.lat);
      const east = Math.max(start.lng, end.lng);
      const west = Math.min(start.lng, end.lng);
      return {
        left: `${((west + 180) / 360) * 100}%`,
        top: `${((90 - north) / 180) * 100}%`,
        width: `${((east - west) / 360) * 100}%`,
        height: `${((north - south) / 180) * 100}%`,
        north,
        south,
        east,
        west,
      };
    }

    map.on("mousedown", (event: MapMouseEvent) => {
      anchorRef.current = { lng: event.lngLat.lng, lat: event.lngLat.lat };
    });
    map.on("mousemove", (event: MapMouseEvent) => {
      if (anchorRef.current) {
        const r = rectFrom(anchorRef.current, { lng: event.lngLat.lng, lat: event.lngLat.lat });
        setRect({ left: r.left, top: r.top, width: r.width, height: r.height });
      }
    });
    map.on("mouseup", (event: MapMouseEvent) => {
      if (anchorRef.current) {
        const r = rectFrom(anchorRef.current, { lng: event.lngLat.lng, lat: event.lngLat.lat });
        anchorRef.current = null;
        setRect(null);
        setBounds({ north: r.north, south: r.south, east: r.east, west: r.west });
      }
    });

    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function save() {
    if (!bounds) return;
    setSaving(true);
    setError(null);
    try {
      await putMapConfig(projectId, bounds);
      onSaved();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Space direction="vertical" style={{ width: "100%" }}>
      <Typography.Text type="secondary">{t("maps.boundsHint")}</Typography.Text>
      <div style={{ position: "relative", width: "100%", height: 420 }}>
        <div ref={containerRef} style={{ position: "absolute", inset: 0 }} />
        {rect && (
          <div
            style={{
              position: "absolute",
              background: "rgba(22,119,255,0.25)",
              border: "2px solid #1677ff",
              pointerEvents: "none",
              left: rect.left,
              top: rect.top,
              width: rect.width,
              height: rect.height,
            }}
          />
        )}
      </div>
      {bounds && (
        <Typography.Text>
          N {bounds.north?.toFixed(4)} · S {bounds.south?.toFixed(4)} · E {bounds.east?.toFixed(4)} · W{" "}
          {bounds.west?.toFixed(4)}
        </Typography.Text>
      )}
      {error && <Alert type="error" showIcon message={error} />}
      <Button type="primary" disabled={!bounds} loading={saving} onClick={save}>
        {t("common.save")}
      </Button>
    </Space>
  );
}
