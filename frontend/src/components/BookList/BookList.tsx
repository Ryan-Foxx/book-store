import { Link } from "react-router-dom";
import { FaStar } from "react-icons/fa";
import type {
    BookCardProps,
    BookCoverProps,
    BookListProps,
    BookPriceProps,
    BookRatingProps,
} from "./types/book";

// Utils & Helpers
const priceFormatter = new Intl.NumberFormat("fa-IR");

function formatPrice(price: number): string {
    return `${priceFormatter.format(price)} تومان`;
}

// Main Component
function BookList({ books, sectionTitle }: BookListProps) {
    return (
        <section className="py-8 sm:py-12" aria-label={sectionTitle}>
            <div className="container">
                <h2 className="font-MorabbaBold mb-6 text-lg text-slate-900 sm:text-2xl">
                    {sectionTitle}
                </h2>

                <div className="xs:gap-3.5 grid grid-cols-2 gap-2.5 sm:gap-4 md:grid-cols-3 lg:grid-cols-4">
                    {books.map((book) => (
                        <BookCard key={book.id} book={book} />
                    ))}
                </div>
            </div>
        </section>
    );
}

export default BookList;

// Sub-Components
function BookCard({ book }: BookCardProps) {
    return (
        <article className="group flex flex-col justify-between rounded-2xl border border-slate-100 bg-white p-2 shadow-xs transition-all duration-300 hover:-translate-y-1.5 hover:border-slate-200 hover:shadow-xl hover:shadow-slate-200/50 sm:p-3.5">
            {/* Top Area: Cover */}
            <BookCover cover={book.cover} title={book.title} />

            {/* Bottom Area: Info */}
            <div className="mt-2.5 flex min-w-0 flex-1 flex-col justify-between gap-y-2.5">
                {/* Book Title as Standalone Link */}
                <h3
                    className="font-DanaMedium truncate text-xs text-slate-800 sm:text-sm"
                    title={book.title}
                >
                    <Link
                        to={`books/${book.id}`}
                        className="rounded-sm transition-colors duration-200 hover:text-orange-600 focus:ring-1 focus:ring-orange-400 focus:outline-none"
                    >
                        {book.title}
                    </Link>
                </h3>

                {/* Footer Info: Price on Right, Rating on Left */}
                <div className="flex items-center justify-between gap-1 border-t border-slate-50 pt-2">
                    <BookPrice price={book.price} />
                    <BookRating rating={book.rating} />
                </div>
            </div>
        </article>
    );
}

function BookCover({ cover, title }: BookCoverProps) {
    return (
        <div className="aspect-3/4 w-full overflow-hidden rounded-lg bg-slate-100">
            <img
                src={cover}
                alt={`جلد کتاب ${title}`}
                className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                loading="lazy"
            />
        </div>
    );
}

function BookRating({ rating }: BookRatingProps) {
    return (
        <div className="flex shrink-0 items-center gap-1">
            <div
                className="hidden items-center gap-0.5 text-amber-400 sm:flex"
                aria-hidden="true"
            >
                <FaStar className="h-3 w-3" />
                <FaStar className="h-3 w-3" />
                <FaStar className="h-3 w-3" />
                <FaStar className="h-3 w-3" />
                <FaStar className="h-3 w-3" />
            </div>

            <FaStar
                className="h-3 w-3 text-amber-400 sm:hidden"
                aria-hidden="true"
            />

            <span className="font-IRANYekanXMedium text-xs text-slate-500 sm:text-sm">
                {priceFormatter.format(rating)}
            </span>
        </div>
    );
}

function BookPrice({ price }: BookPriceProps) {
    return (
        <div className="shrink-0">
            <span className="font-DanaMedium text-xs whitespace-nowrap text-slate-900 sm:text-sm">
                {formatPrice(price)}
            </span>
        </div>
    );
}
