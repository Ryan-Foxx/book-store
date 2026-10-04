import { Provider } from "react-redux";
import type { ReactNode } from "react";
import { store } from "@/app/store";

type StoreProviderProps = {
    children: ReactNode;
};

function StoreProvider({ children }: StoreProviderProps) {
    return <Provider store={store}>{children}</Provider>;
}

export default StoreProvider;
