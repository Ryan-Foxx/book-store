import { useState } from "react";
import {
    HiOutlineChevronDown,
    HiOutlineMagnifyingGlass,
} from "react-icons/hi2";

import BookList from "@/components/BookList";
import { BOOKS } from "@/pages/main-pages/HomePage/constants/books";

/* ---------------- Types & Constants ---------------- */
type SortOption = {
    readonly id: string;
    readonly label: string;
};

const SORT_OPTIONS: readonly SortOption[] = [
    { id: "newest", label: "جدیدترین" },
    { id: "oldest", label: "قدیمی‌ترین" },
    { id: "cheapest", label: "ارزان‌ترین" },
    { id: "most-expensive", label: "گران‌ترین" },
];

const STATIC_PAGES = [1, 2, 3, 4, 5] as const;
const persianFormatter = new Intl.NumberFormat("fa-IR");

/* ---------------- Main Page Component ---------------- */
function StorePage() {
    return (
        <main className="py-8 sm:py-12">
            <div className="container">
                {/* Header Title */}
                <header className="mb-6">
                    <h1 className="font-MorabbaBold text-2xl text-slate-900 sm:text-3xl">
                        فروشگاه کتاب
                    </h1>
                </header>

                {/* Search & Sort Controls Section */}
                <StoreFiltersBar />
            </div>

            {/* Book List Presentation */}
            <BookList books={BOOKS} sectionTitle="همه کتاب‌ها" />

            {/* Static Pagination Controls */}
            <StorePagination />
        </main>
    );
}

export default StorePage;

/* ---------------- Sub-Component: Filters Bar Wrapper ---------------- */
function StoreFiltersBar() {
    return (
        <section
            className="grid grid-cols-1 gap-3.5 sm:grid-cols-[minmax(0,1fr)_220px]"
            aria-label="کنترل‌های جست‌وجو و مرتب‌سازی"
        >
            <StoreSearch />
            <StoreSortDropdown />
        </section>
    );
}

/* ---------------- Sub-Component: Search Input ---------------- */
function StoreSearch() {
    return (
        <div>
            <label
                htmlFor="store-search"
                className="font-DanaMedium mb-1.5 block text-xs text-slate-600 sm:text-sm"
            >
                جست‌وجوی کتاب
            </label>
            <div className="relative">
                <input
                    id="store-search"
                    type="search"
                    placeholder="جست‌وجوی نام کتاب، نویسنده..."
                    className="font-DanaRegular w-full rounded-xl border border-slate-200 bg-white py-2.5 pr-10 pl-3.5 text-xs text-slate-800 transition-colors outline-none placeholder:text-slate-400 focus:border-orange-500 focus:ring-1 focus:ring-orange-500 sm:text-sm"
                    readOnly
                />
                <HiOutlineMagnifyingGlass
                    className="pointer-events-none absolute top-1/2 right-3 h-5 w-5 -translate-y-1/2 text-slate-400"
                    aria-hidden="true"
                />
            </div>
        </div>
    );
}

/* ---------------- Sub-Component: Custom Sort Dropdown ---------------- */
function StoreSortDropdown() {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [selectedOption, setSelectedOption] = useState<SortOption>(
        SORT_OPTIONS[0],
    );

    const handleToggle = (): void => {
        setIsOpen((prev) => !prev);
    };

    const handleSelect = (option: SortOption): void => {
        setSelectedOption(option);
        setIsOpen(false);
    };

    return (
        <div className="relative">
            <label
                id="sort-dropdown-label"
                className="font-DanaMedium mb-1.5 block text-xs text-slate-600 sm:text-sm"
            >
                مرتب‌سازی بر اساس
            </label>

            {/* Trigger Button */}
            <button
                type="button"
                onClick={handleToggle}
                aria-haspopup="listbox"
                aria-expanded={isOpen}
                aria-labelledby="sort-dropdown-label"
                className="flex h-10.5 w-full cursor-pointer items-center justify-between rounded-xl border border-slate-200 bg-white px-3.5 text-xs text-slate-800 transition-colors hover:border-slate-300 focus:border-orange-500 focus:ring-1 focus:ring-orange-500 sm:text-sm"
            >
                <span className="font-DanaRegular">{selectedOption.label}</span>
                <HiOutlineChevronDown
                    className={`h-4 w-4 text-slate-500 transition-transform duration-300 ${
                        isOpen ? "rotate-180" : ""
                    }`}
                    aria-hidden="true"
                />
            </button>

            {/* Dropdown Menu Popup */}
            <div
                className={`absolute top-full right-0 z-20 mt-1.5 grid w-full overflow-hidden rounded-xl border border-slate-100 bg-white shadow-xl transition-[grid-template-rows,opacity] duration-300 ease-in-out ${
                    isOpen
                        ? "grid-rows-[1fr] opacity-100"
                        : "pointer-events-none grid-rows-[0fr] opacity-0"
                }`}
            >
                <div className="min-h-0 overflow-hidden">
                    <ul
                        role="listbox"
                        aria-labelledby="sort-dropdown-label"
                        className="font-DanaRegular flex flex-col p-1.5 text-xs text-slate-700 sm:text-sm"
                    >
                        {SORT_OPTIONS.map((option) => {
                            const isSelected = option.id === selectedOption.id;

                            return (
                                <li
                                    key={option.id}
                                    role="option"
                                    aria-selected={isSelected}
                                >
                                    <button
                                        type="button"
                                        onClick={() => handleSelect(option)}
                                        className={`flex w-full cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-right transition-colors ${
                                            isSelected
                                                ? "font-DanaMedium bg-orange-50 text-orange-600"
                                                : "hover:bg-slate-50 hover:text-orange-500"
                                        }`}
                                    >
                                        <span>{option.label}</span>
                                        {isSelected && (
                                            <span className="h-1.5 w-1.5 rounded-full bg-orange-500" />
                                        )}
                                    </button>
                                </li>
                            );
                        })}
                    </ul>
                </div>
            </div>
        </div>
    );
}

/* ---------------- Sub-Component: Pagination ---------------- */
function StorePagination() {
    return (
        <nav
            className="container mt-8 flex items-center justify-center gap-x-2"
            aria-label="صفحه‌بندی کتاب‌ها"
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
