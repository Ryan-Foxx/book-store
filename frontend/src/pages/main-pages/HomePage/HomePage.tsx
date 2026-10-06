import { Link } from "react-router-dom";
import { HiOutlineSearch } from "react-icons/hi";

import { BOOKS } from "./constants/books";
import { POPULAR_CATEGORIES } from "./constants/popular-categories";
import type { CategoryCardProps } from "./types/popular-category";
import type {
    SuggestedBookCardProps,
    SuggestedBookInfoProps,
    SuggestedBooksProps,
} from "./types/suggested-book";

import heroImage from "@/assets/images/hero-book.png";
import BookList from "@/components/BookList";

function HomePage() {
    return (
        <>
            <HeroSection />
            <PopularCategories />
            <BookList books={BOOKS} sectionTitle="محبوب‌ترین کتاب‌ها" />
            <SuggestedBooks books={BOOKS} />
            <NewsletterSection />
        </>
    );
}

export default HomePage;

// ==============================================================================================================================
function HeroSection() {
    return (
        <>
            <section className="bg-linear-to-b from-orange-50/50 to-white py-8 sm:py-12">
                <div className="container flex flex-col items-center justify-between gap-8 md:flex-row md:gap-4">
                    {/* Text Content & Search Box */}
                    <div className="order-2 flex w-full max-w-xl flex-col items-start gap-y-6 md:order-1 md:w-1/2">
                        <h1 className="font-MorabbaBold text-2xl leading-snug text-slate-900 sm:text-4xl md:text-5xl">
                            به دنیای جدیدی قدم بگذارید و به یک ماجراجویی خواندنی
                            بروید!
                        </h1>

                        <p className="max-w-lg text-sm leading-7 text-slate-600 sm:text-base">
                            کتابخانه‌ای گسترده از دسته‌بندی‌های مختلف اکشن،
                            معمایی، رمانتیک، برای سرگرمی و یادگیری...
                        </p>

                        {/* Search Input */}
                        <div className="relative w-full max-w-md">
                            <input
                                type="text"
                                placeholder="اسم کتاب، ژانر، نویسنده..."
                                className="font-DanaRegular w-full rounded-full border border-slate-200 py-3.5 pr-13 pl-4 text-sm shadow-sm transition-all outline-none focus:border-orange-300 focus:ring-2 focus:ring-orange-100 sm:text-base"
                            />
                            <button
                                type="button"
                                className="absolute top-1/2 right-3 -translate-y-1/2 rounded-full bg-slate-900 p-2 text-white transition-colors hover:bg-slate-700"
                                aria-label="Search"
                            >
                                <HiOutlineSearch className="h-5 w-5" />
                            </button>
                        </div>
                    </div>

                    {/* Illustration Image */}
                    <div className="order-1 flex w-full justify-center md:order-2 md:w-1/2 md:justify-end">
                        <img
                            src={heroImage}
                            alt="Reading a book illustration"
                            className="w-full max-w-sm object-contain sm:max-w-md"
                        />
                    </div>
                </div>
            </section>
        </>
    );
}

// ========================================== Main Section: Popular Categories Component ==========================================
function PopularCategories() {
    return (
        <section
            className="bg-slate-50 py-10 sm:py-14"
            aria-labelledby="popular-categories-heading"
        >
            <div className="container">
                {/* Section Title */}
                <div className="mb-6 sm:mb-8">
                    <h2
                        id="popular-categories-heading"
                        className="font-MorabbaBold text-xl text-slate-900 sm:text-2xl"
                    >
                        محبوب ترین دسته بندی‌ها
                    </h2>
                </div>

                <div className="xs:grid-cols-2 grid grid-cols-1 gap-3.5 sm:gap-4 md:grid-cols-3 lg:grid-cols-4">
                    {POPULAR_CATEGORIES.map((category) => (
                        <CategoryCard key={category.id} category={category} />
                    ))}
                </div>
            </div>
        </section>
    );
}

// Sub-Component: Single Category Card
function CategoryCard({ category }: CategoryCardProps) {
    return (
        <Link
            to={category.link || "#"}
            className="group flex items-center justify-between overflow-hidden rounded-2xl border border-slate-100 bg-slate-50/70 p-3 shadow-xs transition-all duration-300 hover:-translate-y-1 hover:border-slate-200 hover:bg-white hover:shadow-md sm:p-4"
        >
            {/* Category Title */}
            <span className="font-DanaMedium text-sm text-slate-800 transition-colors group-hover:text-orange-500 sm:text-base">
                {category.title}
            </span>

            {/* Category Thumbnail / Illustration */}
            <div className="h-12 w-12 shrink-0 overflow-hidden rounded-xl sm:h-14 sm:w-14">
                <img
                    src={category.image}
                    alt={category.title}
                    className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
                    loading="lazy"
                />
            </div>
        </Link>
    );
}

// ========================================== Utils & Helpers: SuggestedBooks ==========================================
const priceFormatter = new Intl.NumberFormat("fa-IR");

function formatPrice(price: number): string {
    return `${priceFormatter.format(price)} تومان`;
}

// Main Section: SuggestedBooks
function SuggestedBooks({ books }: SuggestedBooksProps) {
    return (
        <section className="bg-slate-50 py-8 sm:py-12">
            <div className="container">
                <h2 className="font-MorabbaBold mb-6 text-lg text-slate-900 sm:text-2xl">
                    {"کتاب‌های پیشنهادی"}
                </h2>

                <div className="xs:grid-cols-2 grid grid-cols-1 gap-3 sm:gap-4 lg:grid-cols-4">
                    {books.map((book) => (
                        <SuggestedBookCard key={book.id} book={book} />
                    ))}
                </div>
            </div>
        </section>
    );
}

// Sub-Components: SuggestedBooks
function SuggestedBookCard({ book }: SuggestedBookCardProps) {
    return (
        <article className="group flex items-stretch justify-between gap-3 rounded-xl border border-slate-200 bg-white p-3 transition-all duration-300 hover:-translate-y-1 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-200/60">
            {/* Text Content (Right side in RTL) */}
            <SuggestedBookInfo book={book} />

            {/* Book Cover (Left side in RTL) */}
            <div className="h-28 w-20 shrink-0 overflow-hidden rounded-md sm:h-32 sm:w-24">
                <img
                    src={book.cover}
                    alt={`جلد کتاب ${book.title}`}
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                    loading="lazy"
                />
            </div>
        </article>
    );
}

function SuggestedBookInfo({ book }: SuggestedBookInfoProps) {
    return (
        <div className="flex min-w-0 flex-1 flex-col justify-between gap-y-2">
            <h3
                className="font-DanaMedium line-clamp-2 text-sm leading-6 text-slate-800"
                title={book.title}
            >
                <Link
                    to={`books/${book.id}`}
                    className="rounded-sm transition-colors duration-200 hover:text-orange-600 focus:ring-1 focus:ring-orange-400 focus:outline-none"
                >
                    {book.title}
                </Link>
            </h3>

            {/* Price */}
            <span className="font-DanaMedium text-xs whitespace-nowrap text-slate-900 sm:text-sm">
                {formatPrice(book.price)}
            </span>
        </div>
    );
}

// ========================================== Newsletter Section (Static UI) ==========================================
function NewsletterSection() {
    return (
        <section className="py-16 sm:py-20">
            <div className="container mx-auto px-4">
                <div className="mx-auto flex max-w-2xl flex-col items-center text-center">
                    {/* Title */}
                    <h2
                        id="newsletter-title"
                        className="font-MorabbaBold text-2xl text-slate-800 sm:text-3xl"
                    >
                        به اجتماع ما بپیوندید!
                    </h2>

                    {/* Description */}
                    <p className="font-Dana mt-3 max-w-xl text-xs leading-6 text-slate-500 sm:text-sm sm:leading-7">
                        آدرس ایمیل خود را برای دریافت به‌روزرسانی‌های منظم و
                        همچنین اخبار رویدادهای آینده و پیشنهادات خاص وارد کنید.
                    </p>

                    {/* Static Form */}
                    <form
                        onSubmit={(e) => e.preventDefault()}
                        className="mt-8 flex w-full max-w-md items-center rounded-full bg-white p-1.5 shadow-sm ring-1 ring-slate-200 focus-within:ring-2 focus-within:ring-slate-800"
                    >
                        {/* Submit Button */}
                        <button
                            type="button"
                            className="font-DanaMedium shrink-0 rounded-full bg-slate-900 px-6 py-2 text-xs text-white transition-colors duration-200 hover:bg-slate-800 sm:px-8 sm:py-2.5 sm:text-sm"
                        >
                            ثبت
                        </button>

                        {/* Input Field */}
                        <input
                            type="email"
                            placeholder="ایمیل خود را وارد کنید"
                            className="font-Dana min-w-0 flex-1 bg-transparent px-4 text-xs text-slate-700 placeholder-slate-400 outline-none sm:text-sm"
                        />
                    </form>
                </div>
            </div>
        </section>
    );
}
