import { Link } from "react-router-dom";
import {
    HiOutlineAcademicCap,
    HiOutlineArrowLeft,
    HiOutlineBeaker,
    HiOutlineBriefcase,
    HiOutlineClock,
    HiOutlineHeart,
    HiOutlineLightBulb,
    HiOutlineMagnifyingGlass,
    HiOutlineSparkles,
    HiOutlineUserGroup,
} from "react-icons/hi2";
import type { IconType } from "react-icons";
import compoundEffect from "@/assets/images/books/compound-effect.jpg";

/* ---------------- Types & Mock Data ---------------- */
interface CategoryItem {
    readonly id: number;
    readonly title: string;
    readonly slug: string;
    readonly bookCount: number;
    readonly description: string;
    readonly icon: IconType;
    readonly badgeColor: string;
    readonly imageUrl: string;
}

const CATEGORIES_DATA: readonly CategoryItem[] = [
    {
        id: 1,
        title: "روانشناسی و خودسازی",
        slug: "psychology",
        bookCount: 142,
        description: "کتاب‌های رشد فردی، انگیزش و تمرکز ذهن",
        icon: HiOutlineLightBulb,
        badgeColor: "bg-amber-50 text-amber-600 group-hover:bg-amber-500",
        imageUrl: compoundEffect,
    },
    {
        id: 2,
        title: "ادبیات داستانی و رمان",
        slug: "fiction",
        bookCount: 230,
        description: "شاهکارهای ادبیات جهان، داستان و رمان‌های پرفروش",
        icon: HiOutlineHeart,
        badgeColor: "bg-rose-50 text-rose-600 group-hover:bg-rose-500",
        imageUrl: compoundEffect,
    },
    {
        id: 3,
        title: "مدیریت و کسب‌وکار",
        slug: "business",
        bookCount: 98,
        description: "استراتژی‌های مالی، رهبری تیم و راه‌اندازی استارتاپ",
        icon: HiOutlineBriefcase,
        badgeColor: "bg-blue-50 text-blue-600 group-hover:bg-blue-500",
        imageUrl: compoundEffect,
    },
    {
        id: 4,
        title: "علمی و پژوهشی",
        slug: "science",
        bookCount: 76,
        description: "علوم پایه، فیزیک، کیهان‌شناسی و مقالات تحلیلی",
        icon: HiOutlineBeaker,
        badgeColor: "bg-emerald-50 text-emerald-600 group-hover:bg-emerald-500",
        imageUrl: compoundEffect,
    },
    {
        id: 5,
        title: "تاریخ و تمدن",
        slug: "history",
        bookCount: 114,
        description: "رویدادهای سرنوشت‌ساز جهان و تاریخ کهن",
        icon: HiOutlineClock,
        badgeColor: "bg-stone-100 text-stone-600 group-hover:bg-stone-600",
        imageUrl: compoundEffect,
    },
    {
        id: 6,
        title: "جامعه‌شناسی و فلسفه",
        slug: "philosophy",
        bookCount: 89,
        description: "تأملات فکری، جریان‌های اجتماعی و نقدهای مدرن",
        icon: HiOutlineUserGroup,
        badgeColor: "bg-purple-50 text-purple-600 group-hover:bg-purple-500",
        imageUrl: compoundEffect,
    },
    {
        id: 7,
        title: "هنر و سینما",
        slug: "art",
        bookCount: 52,
        description: "طراحی، عکاسی، نمایشنامه‌ها و مبانی فیلم‌سازی",
        icon: HiOutlineSparkles,
        badgeColor: "bg-pink-50 text-pink-600 group-hover:bg-pink-500",
        imageUrl: compoundEffect,
    },
    {
        id: 8,
        title: "آموزش و کنکور",
        slug: "education",
        bookCount: 165,
        description: "منابع آموزشی، تست‌ها و کتاب‌های دانشگاهی",
        icon: HiOutlineAcademicCap,
        badgeColor: "bg-cyan-50 text-cyan-600 group-hover:bg-cyan-500",
        imageUrl: compoundEffect,
    },
];

const STATIC_PAGES = [1, 2, 3, 4, 5] as const;
const persianFormatter = new Intl.NumberFormat("fa-IR");

/* ---------------- Main Page Component ---------------- */
function CategoryPage() {
    return (
        <main className="py-8 sm:py-12">
            <div className="container">
                {/* Header & Search Hero */}
                <header className="mb-10 text-center sm:mb-12">
                    <span className="font-DanaMedium text-xs text-orange-600 sm:text-sm">
                        موضوعات و گرایش‌ها
                    </span>
                    <h1 className="font-MorabbaBold mt-2 text-2xl text-slate-900 sm:text-3xl lg:text-4xl">
                        دسته‌بندی‌های کتاب
                    </h1>
                    <p className="font-DanaRegular mx-auto mt-2.5 max-w-lg text-xs text-slate-500 sm:text-sm">
                        موضوع مورد علاقه خود را پیدا کنید و در میان صدها کتاب
                        منتخب کاوش نمایید.
                    </p>

                    {/* Centered Search Bar */}
                    <div className="mx-auto mt-6 max-w-xl">
                        <CategorySearch />
                    </div>
                </header>

                {/* Categories Grid Presentation */}
                <CategoryGrid categories={CATEGORIES_DATA} />

                {/* Static Pagination Controls */}
                <CategoryPagination />
            </div>
        </main>
    );
}

export default CategoryPage;

/* ---------------- Sub-Component: Category Search ---------------- */
function CategorySearch() {
    return (
        <div className="relative">
            <input
                type="search"
                id="category-search"
                placeholder="جست‌وجوی عنوان یا دسته‌بندی موضوعی..."
                className="font-DanaRegular w-full rounded-2xl border border-slate-200 bg-white py-3 pr-11 pl-4 text-xs text-slate-800 shadow-xs transition-colors outline-none placeholder:text-slate-400 focus:border-orange-500 focus:ring-1 focus:ring-orange-500 sm:py-3.5 sm:text-sm"
                readOnly
            />
            <HiOutlineMagnifyingGlass
                className="pointer-events-none absolute top-1/2 right-3.5 h-5 w-5 -translate-y-1/2 text-slate-400"
                aria-hidden="true"
            />
        </div>
    );
}

/* ---------------- Sub-Component: Grid Container ---------------- */
interface CategoryGridProps {
    readonly categories: readonly CategoryItem[];
}

function CategoryGrid({ categories }: CategoryGridProps) {
    return (
        <section
            aria-label="فهرست دسته‌بندی‌ها"
            className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-5 lg:grid-cols-3 xl:grid-cols-4"
        >
            {categories.map((category) => (
                <CategoryCard key={category.id} category={category} />
            ))}
        </section>
    );
}

/* ---------------- Sub-Component: Category Card ---------------- */
interface CategoryCardProps {
    readonly category: CategoryItem;
}

function CategoryCard({ category }: CategoryCardProps) {
    const Icon = category.icon;

    return (
        <Link
            to={`/store?category=${category.slug}`}
            className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-slate-100 bg-white p-5 shadow-xs transition-all duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-md"
        >
            {/* Background Image Layer with Opacity */}
            <img
                src={category.imageUrl}
                alt=""
                aria-hidden="true"
                loading="lazy"
                className="pointer-events-none absolute inset-0 h-full w-full object-cover opacity-10 transition-transform duration-500 ease-out group-hover:scale-105 group-hover:opacity-15"
            />

            {/* Gradient Overlay for seamless blending with card's white background */}
            <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0 bg-linear-to-t from-white via-white/80 to-transparent"
            />

            {/* Top Row: Icon Badge & Book Counter */}
            <div className="relative z-10 flex items-center justify-between">
                <div
                    className={`flex h-12 w-12 items-center justify-center rounded-xl transition-colors duration-300 group-hover:text-white ${category.badgeColor}`}
                >
                    <Icon className="h-6 w-6" aria-hidden="true" />
                </div>

                <span className="font-DanaMedium rounded-full bg-slate-100/80 px-2.5 py-1 text-[11px] text-slate-600 backdrop-blur-xs transition-colors group-hover:bg-orange-50 group-hover:text-orange-600 sm:text-xs">
                    {persianFormatter.format(category.bookCount)} کتاب
                </span>
            </div>

            {/* Middle: Title & Description */}
            <div className="relative z-10 mt-4">
                <h2 className="font-MorabbaBold text-base text-slate-800 transition-colors group-hover:text-orange-600 sm:text-lg">
                    {category.title}
                </h2>
                <p className="font-DanaRegular mt-1.5 line-clamp-2 text-xs leading-relaxed text-slate-500">
                    {category.description}
                </p>
            </div>

            {/* Bottom: Action Link Indicator */}
            <div className="relative z-10 mt-5 flex items-center justify-between border-t border-slate-100 pt-3.5">
                <span className="font-DanaMedium text-xs text-slate-600 transition-colors group-hover:text-orange-600">
                    مشاهده کتاب‌ها
                </span>
                <HiOutlineArrowLeft
                    className="h-4 w-4 text-slate-400 transition-transform duration-300 group-hover:-translate-x-1 group-hover:text-orange-500"
                    aria-hidden="true"
                />
            </div>
        </Link>
    );
}

/* ---------------- Sub-Component: Pagination ---------------- */
function CategoryPagination() {
    return (
        <nav
            className="mt-10 flex items-center justify-center gap-x-2 sm:mt-12"
            aria-label="صفحه‌بندی دسته‌بندی‌ها"
        >
            <button
                type="button"
                aria-label="صفحه قبلی"
                className="font-DanaMedium flex h-9 items-center justify-center rounded-xl border border-slate-200 bg-white px-3 text-xs text-slate-400 transition-colors sm:h-10 sm:px-4 sm:text-sm"
                disabled
            >
                قبلی
            </button>

            {STATIC_PAGES.map((page) => {
                const isActive = page === 1;

                return (
                    <button
                        key={page}
                        type="button"
                        aria-label={`صفحه ${persianFormatter.format(page)}`}
                        aria-current={isActive ? "page" : undefined}
                        className={`font-DanaMedium flex h-9 w-9 items-center justify-center rounded-xl text-xs transition-colors sm:h-10 sm:w-10 sm:text-sm ${
                            isActive
                                ? "bg-orange-500 text-white shadow-xs"
                                : "border border-slate-200 bg-white text-slate-700 hover:border-orange-200 hover:text-orange-500"
                        }`}
                    >
                        {persianFormatter.format(page)}
                    </button>
                );
            })}

            <button
                type="button"
                aria-label="صفحه بعدی"
                className="font-DanaMedium flex h-9 items-center justify-center rounded-xl border border-slate-200 bg-white px-3 text-xs text-slate-700 transition-colors hover:border-orange-200 hover:text-orange-500 sm:h-10 sm:px-4 sm:text-sm"
            >
                بعدی
            </button>
        </nav>
    );
}
