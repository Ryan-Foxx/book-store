import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { mainRoutes } from "./main.routes";

import MainLayout from "@/app/layouts/MainLayout";
import NotFoundPage from "@/pages/NotFoundPage";

const router = createBrowserRouter([
    {
        path: "/",
        Component: MainLayout,
        children: mainRoutes,
    },
    {
        path: "*",
        Component: NotFoundPage,
    },
]);

function AppRouter() {
    return <RouterProvider router={router} />;
}

export default AppRouter;
