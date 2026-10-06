import biography from "@/assets/images/categories/biography.png";
import mystery from "@/assets/images/categories/mystery.png";
import art from "@/assets/images/categories/art.png";
import humor from "@/assets/images/categories/humor.png";
import personalDevelopment from "@/assets/images/categories/personal-development.png";
import romance from "@/assets/images/categories/romance.png";
import psychology from "@/assets/images/categories/psychology.png";
import action from "@/assets/images/categories/action.png";

import type { CategoryItem } from "@/pages/main-pages/HomePage/types/category";

export const POPULAR_CATEGORIES: CategoryItem[] = [
    {
        id: 1,
        title: "زندگینامه",
        image: biography,
        link: "category",
    },
    {
        id: 2,
        title: "اکشن",
        image: action,
        link: "category",
    },
    {
        id: 3,
        title: "معمایی",
        image: mystery,
        link: "category",
    },
    {
        id: 4,
        title: "هنری",
        image: art,
        link: "category",
    },
    {
        id: 5,
        title: "طنز",
        image: humor,
        link: "category",
    },
    {
        id: 6,
        title: "توسعه فردی",
        image: personalDevelopment,
        link: "category",
    },
    {
        id: 7,
        title: "عاشقانه",
        image: romance,
        link: "category",
    },
    {
        id: 8,
        title: "روان شناسی",
        image: psychology,
        link: "category",
    },
];
