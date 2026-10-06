export interface CategoryItem {
    id: number | string;
    title: string;
    image: string;
    link?: string;
}

export interface CategoryCardProps {
    category: CategoryItem;
}
