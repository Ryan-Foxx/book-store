import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";

import StoreProvider from "@/app/providers/StoreProvider.tsx";
import "@/app/styles/globals.css";

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <StoreProvider>
            <App />
        </StoreProvider>
    </StrictMode>,
);
