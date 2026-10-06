export interface BookItem {
    id: string | number;
    title: string;
    cover: string;
    rating: number;
    price: number;
    discountPercent?: number;
    slug?: string;
}

export interface BookListProps {
    books: BookItem[];
    sectionTitle?: string;
}

export interface BookCardProps {
    book: BookItem;
}

export interface BookCoverProps {
    cover: string;
    title: string;
}

export interface BookRatingProps {
    rating: number;
}

export interface BookPriceProps {
    price: number;
}
