import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";
import { AuthProvider } from "./auth/AuthProvider";

function renderApp() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <App />
      </AuthProvider>
    </QueryClientProvider>,
  );
}

describe("App", () => {
  it("renders the login screen when unauthenticated", () => {
    renderApp();
    expect(screen.getByText("Open Asset Platform")).toBeTruthy();
  });
});
