import type { BookItem } from "@/components/BookList/types/book";
import compoundEffect from "@/assets/images/books/compound-effect.jpg";

export const BOOKS: BookItem[] = [
    {
        id: 1,
        title: "عادت های اتمی",
        cover: compoundEffect,
        rating: 4.5,
        price: 320000,
    },
    {
        id: 2,
        title: "چگونه کمال گرا نباشیم",
        cover: compoundEffect,
        rating: 4,
        price: 100000,
        discountPercent: 20,
    },
    {
        id: 3,
        title: "اثر مرکب",
        cover: compoundEffect,
        rating: 2,
        price: 347000,
    },
    {
        id: 4,
        title: "معجزه انضبات شخصی",
        cover: compoundEffect,
        rating: 4.5,
        price: 111000,
    },
    {
        id: 5,
        title: "هنر گفت و گو",
        cover: compoundEffect,
        rating: 5,
        price: 358000,
        discountPercent: 10,
    },
    {
        id: 6,
        title: "7 عادت مردمان موثر",
        cover: compoundEffect,
        rating: 2.5,
        price: 952000,
    },
    {
        id: 7,
        title: "باشگاه پنج صبحی ها",
        cover: compoundEffect,
        rating: 1.5,
        price: 752000,
        discountPercent: 20,
    },
    {
        id: 8,
        title: "کار عمیق",
        cover: compoundEffect,
        rating: 2,
        price: 128000,
        discountPercent: 30,
    },
];
