import { Alert, Button } from "antd";
import { Component } from "react";
import type { ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

/** Catches render errors so a failure in one screen never blanks the whole app. */
export default class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error("OAP render error:", error, info);
  }

  render(): ReactNode {
    if (this.state.error) {
      return (
        <div style={{ padding: 24 }}>
          <Alert
            type="error"
            showIcon
            message="Error al renderizar la pantalla"
            description={String(this.state.error.message ?? this.state.error)}
            action={
              <Button size="small" onClick={() => this.setState({ error: null })}>
                Reintentar
              </Button>
            }
          />
        </div>
      );
    }
    return this.props.children;
  }
}
