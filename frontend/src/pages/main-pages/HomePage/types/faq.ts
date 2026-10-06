export interface FaqData {
    id: number;
    question: string;
    answer: string;
}

export interface FaqItemProps {
    faq: FaqData;
    isOpen: boolean;
    onToggle: () => void;
}
