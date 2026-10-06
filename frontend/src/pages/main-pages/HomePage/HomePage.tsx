import { Link } from "react-router-dom";
import { HiOutlineSearch } from "react-icons/hi";

import { POPULAR_CATEGORIES } from "./constants/popular-categories";
import type { CategoryCardProps } from "./types/category";

import heroImage from "@/assets/images/hero-book.png";

function HomePage() {
    return (
        <>
            <HeroSection />
            <PopularCategories />
        </>
    );
}

export default HomePage;

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

// Main Section: Popular Categories Component
function PopularCategories() {
    return (
        <section
            className="py-10 sm:py-14"
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
