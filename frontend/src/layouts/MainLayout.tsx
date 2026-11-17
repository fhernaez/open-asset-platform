import { LogoutOutlined } from "@ant-design/icons";
import { Avatar, Button, Dropdown, Layout, Menu, Space, Typography } from "antd";
import { useMemo } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthProvider";
import { SCREENS } from "../features/flags";

const { Header, Sider, Content } = Layout;

export default function MainLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = useMemo(
    () =>
      SCREENS.map((screen) => ({
        key: screen.key,
        label: screen.label,
      })),
    [],
  );

  const selectedKey = useMemo(() => {
    const path = location.pathname.split("/")[1];
    return SCREENS.some((s) => s.key === path) ? path : "assets";
  }, [location.pathname]);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth={0}>
        <div style={{ color: "#fff", padding: 16, fontWeight: 600 }}>OAP</div>
        <Menu
          theme="dark"
          mode="inline"
          items={menuItems}
          selectedKeys={[selectedKey]}
          onClick={({ key }) => navigate(`/${key}`)}
        />
      </Sider>
      <Layout>
        <Header style={{ background: "#fff", display: "flex", justifyContent: "flex-end", alignItems: "center" }}>
          <Space>
            <Typography.Text>{user?.email}</Typography.Text>
            <Dropdown
              menu={{
                items: [
                  {
                    key: "logout",
                    icon: <LogoutOutlined />,
                    label: "Cerrar sesión",
                    onClick: () => {
                      logout();
                      navigate("/login");
                    },
                  },
                ],
              }}
            >
              <Button type="text">
                <Avatar size="small" style={{ background: "#1677ff" }}>
                  {user?.email?.charAt(0).toUpperCase()}
                </Avatar>
              </Button>
            </Dropdown>
          </Space>
        </Header>
        <Content style={{ padding: 24 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
