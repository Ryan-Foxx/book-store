import { useState, type ReactNode } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
// import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const createQueryClient = () =>
    new QueryClient({
        defaultOptions: {
            queries: {
                gcTime: 5 * 60_000,
                staleTime: 1 * 60_000,
                refetchOnWindowFocus: false,
                retry: 1,
            },
        },
    });

function QueryProvider({ children }: { children: ReactNode }) {
    const [queryClient] = useState(createQueryClient);

    return (
        <QueryClientProvider client={queryClient}>
            {children}
            {/* {import.meta.env.DEV && (
                <ReactQueryDevtools initialIsOpen={false} />
            )} */}
        </QueryClientProvider>
    );
}

export default QueryProvider;
