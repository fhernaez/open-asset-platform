import { ClockCircleOutlined } from "@ant-design/icons";
import { Empty, Typography } from "antd";
import { useTranslation } from "react-i18next";
import type { Gate } from "../features/flags";

export default function ComingSoonPage({ gate, labelKey }: { gate: Gate; labelKey: string }) {
  const { t } = useTranslation();
  return (
    <Empty
      image={<ClockCircleOutlined style={{ fontSize: 64, color: "#bfbfbf" }} />}
      description={
        <Typography.Text type="secondary">
          {t(labelKey)} — {t("comingSoon.availableIn", { gate })}
        </Typography.Text>
      }
    />
  );
}
