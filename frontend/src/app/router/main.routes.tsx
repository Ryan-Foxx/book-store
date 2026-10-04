import type { RouteObject } from "react-router-dom";

import HomePage from "@/pages/main-pages/HomePage";
import StorePage from "@/pages/main-pages/StorePage";
import CategoryPage from "@/pages/main-pages/CategoryPage";
import AboutUsPage from "@/pages/main-pages/AboutUsPage";
import ContactUsPage from "@/pages/main-pages/ContactUsPage";

export const mainRoutes: RouteObject[] = [
    {
        index: true,
        Component: HomePage,
    },
    {
        path: "store",
        Component: StorePage,
    },
    {
        path: "category",
        Component: CategoryPage,
    },
    {
        path: "about-us",
        Component: AboutUsPage,
    },
    {
        path: "contact-us",
        Component: ContactUsPage,
    },
];
