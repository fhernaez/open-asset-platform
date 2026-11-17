import { ClockCircleOutlined } from "@ant-design/icons";
import { Empty, Typography } from "antd";
import type { Gate } from "../features/flags";

export default function ComingSoonPage({ gate, label }: { gate: Gate; label: string }) {
  return (
    <Empty
      image={<ClockCircleOutlined style={{ fontSize: 64, color: "#bfbfbf" }} />}
      description={
        <Typography.Text type="secondary">
          {label} — disponible en etapa {gate}
        </Typography.Text>
      }
    />
  );
}
