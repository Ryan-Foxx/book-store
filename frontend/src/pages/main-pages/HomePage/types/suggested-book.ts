export interface SuggestedBook {
    id: string | number;
    title: string;
    cover: string;
    rating: number;
    price: number;
    discountPercent?: number;
    slug?: string;
}

export interface SuggestedBooksProps {
    books: SuggestedBook[];
}

export interface SuggestedBookCardProps {
    book: SuggestedBook;
}

export interface SuggestedBookInfoProps {
    book: SuggestedBook;
}
