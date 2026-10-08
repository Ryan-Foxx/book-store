import { useState } from "react";
import { NavLink } from "react-router-dom";

import {
    HiOutlineChevronDown,
    HiOutlineMenu,
    HiOutlineShoppingCart,
    HiOutlineUser,
    HiOutlineX,
} from "react-icons/hi";
import bookLogo from "@/assets/images/book-logo.png";

type NavLinkItem = {
    readonly id: number;
    readonly title: string;
    readonly address: string;
};

const NAV_LINKS: readonly NavLinkItem[] = [
    { id: 1, title: "خانه", address: "/" },
    { id: 2, title: "فروشگاه", address: "store" },
    { id: 3, title: "دسته بندی", address: "category" },
    { id: 4, title: "درباره‌ما", address: "about-us" },
    { id: 5, title: "تماس باما", address: "contact-us" },
];

/* ---------------- Main NavBar Component ---------------- */
function NavBar() {
    const [isMenuOpen, setIsMenuOpen] = useState<boolean>(false);
    const [isLogin, setIsLogin] = useState<boolean>(false);

    const handleToggleMenu = (): void => {
        setIsMenuOpen((prev) => !prev);
    };

    const handleCloseMenu = (): void => {
        setIsMenuOpen(false);
    };

    const handleToggleLogin = (): void => {
        setIsLogin((prev) => !prev);
    };

    return (
        <>
            {/* Header stays sticky with full blur effect */}
            <header className="sticky top-0 z-30 w-full border-b border-slate-100 bg-white/95 shadow-xs backdrop-blur-md">
                <div className="container">
                    <nav className="flex h-16 items-center justify-between sm:h-20">
                        {/* Brand & Hamburger */}
                        <div className="flex items-center gap-x-2 sm:gap-x-3">
                            <button
                                type="button"
                                onClick={handleToggleMenu}
                                className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-700 transition-colors hover:bg-slate-100 sm:h-10 sm:w-10 lg:hidden"
                            >
                                <HiOutlineMenu className="h-5 w-5 sm:h-6 sm:w-6" />
                            </button>
                            <NavBrand />
                        </div>

                        {/* Desktop Navigation Links */}
                        <div className="hidden lg:block">
                            <ul className="font-DanaDemiBold flex items-center gap-x-6 text-base text-slate-700 *:transition-colors *:hover:text-orange-500 xl:gap-x-8 xl:text-lg">
                                {NAV_LINKS.map((link) => (
                                    <li key={link.id}>
                                        <NavLink to={link.address}>
                                            {link.title}
                                        </NavLink>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* Cart & Auth Controls */}
                        <div className="flex items-center gap-x-2 sm:gap-x-5">
                            <button
                                type="button"
                                className="relative flex h-9 w-9 cursor-pointer items-center justify-center rounded-lg text-slate-700 transition-colors hover:bg-slate-100 sm:h-10 sm:w-10"
                            >
                                <HiOutlineShoppingCart className="h-5 w-5 sm:h-7 sm:w-7" />
                            </button>

                            <NavUserAuth
                                isLogin={isLogin}
                                onToggleLogin={handleToggleLogin}
                            />
                        </div>
                    </nav>
                </div>
            </header>

            {/* Mobile Sidebar is OUTSIDE header so fixed positioning is viewport-relative */}
            <NavMobileDrawer
                isOpen={isMenuOpen}
                isLogin={isLogin}
                onClose={handleCloseMenu}
                onToggleLogin={handleToggleLogin}
            />
        </>
    );
}

export default NavBar;

/* ---------------- Nav Brand ---------------- */
function NavBrand() {
    return (
        <a href="#" className="flex items-center gap-x-1.5 sm:gap-x-2">
            <img
                src={bookLogo}
                alt="Book Season Logo"
                className="h-8 w-8 object-contain sm:h-11 sm:w-11"
            />
            <span className="font-MorabbaBold text-base text-slate-900 min-[360px]:text-lg sm:text-2xl">
                فصل کتاب
            </span>
        </a>
    );
}

/* ---------------- Desktop Auth & User Menu ---------------- */
type NavUserAuthProps = {
    readonly isLogin: boolean;
    readonly onToggleLogin: () => void;
};

function NavUserAuth({ isLogin, onToggleLogin }: NavUserAuthProps) {
    const [isOpen, setIsOpen] = useState<boolean>(false);

    const handleToggle = (): void => {
        setIsOpen((prev) => !prev);
    };

    if (!isLogin) {
        return (
            <button
                type="button"
                onClick={onToggleLogin}
                className="flex cursor-pointer items-center gap-x-1.5 rounded-lg bg-orange-500 px-2.5 py-2 text-white transition-colors hover:bg-orange-600 sm:px-4 sm:py-2.5"
            >
                <HiOutlineUser className="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
                <span className="font-IRANYekanXRegular hidden text-xs sm:inline sm:text-sm">
                    ورود / ثبت نام
                </span>
            </button>
        );
    }

    return (
        <div className="relative">
            <button
                type="button"
                onClick={handleToggle}
                className="flex cursor-pointer items-center gap-x-1 rounded-lg bg-orange-500 px-2.5 py-2 text-white transition-colors hover:bg-orange-600 sm:px-3 sm:py-2.5"
            >
                <HiOutlineChevronDown
                    className={`h-4 w-4 transition-transform duration-300 ${
                        isOpen ? "rotate-180" : ""
                    }`}
                />
                <span className="font-DanaDemiBold text-xs sm:text-sm">
                    علی رضایی
                </span>
            </button>

            {/* Desktop Collapsible Dropdown */}
            <div
                className={`absolute top-full left-0 z-10 mt-2 grid w-36 overflow-hidden rounded-xl bg-white shadow-xl ring-1 ring-slate-900/5 transition-[grid-template-rows,opacity] duration-300 ease-in-out sm:w-44 ${
                    isOpen
                        ? "grid-rows-[1fr] opacity-100"
                        : "pointer-events-none grid-rows-[0fr] opacity-0"
                }`}
            >
                <div className="min-h-0 overflow-hidden">
                    <div className="font-DanaMedium flex flex-col divide-y divide-slate-100 p-1.5 text-xs text-slate-700 sm:text-sm">
                        <a
                            onClick={handleToggle}
                            href="#"
                            className="rounded-lg px-3 py-2 transition-colors hover:bg-orange-50 hover:text-orange-500"
                        >
                            پروفایل کاربری
                        </a>
                        <a
                            onClick={handleToggle}
                            href="#"
                            className="rounded-lg px-3 py-2 transition-colors hover:bg-orange-50 hover:text-orange-500"
                        >
                            سفارش‌ها
                        </a>
                        <button
                            type="button"
                            onClick={() => {
                                setIsOpen(false);
                                onToggleLogin();
                            }}
                            className="w-full rounded-lg px-3 py-2 text-right text-rose-500 transition-colors hover:bg-rose-50"
                        >
                            خروج از حساب
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

/* ---------------- Mobile Sidebar Drawer ---------------- */
type NavMobileDrawerProps = {
    readonly isOpen: boolean;
    readonly isLogin: boolean;
    readonly onClose: () => void;
    readonly onToggleLogin: () => void;
};

function NavMobileDrawer({
    isOpen,
    isLogin,
    onClose,
    onToggleLogin,
}: NavMobileDrawerProps) {
    const [isOptionsOpen, setIsOptionsOpen] = useState<boolean>(false);

    return (
        <>
            {/* Backdrop */}
            {isOpen && (
                <div
                    onClick={onClose}
                    className="fixed inset-0 z-20 bg-black/40 backdrop-blur-xs transition-opacity lg:hidden"
                    aria-hidden="true"
                />
            )}

            {/* Drawer Content */}
            <aside
                className={`fixed inset-y-0 inset-s-0 z-30 flex w-72 max-w-[calc(100vw-3rem)] flex-col bg-white p-4 shadow-2xl transition-transform duration-300 ease-in-out sm:p-5 lg:hidden ${
                    isOpen
                        ? "translate-x-0"
                        : "-translate-x-full rtl:translate-x-full"
                }`}
            >
                {/* Header */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                    <NavBrand />
                    <button
                        type="button"
                        onClick={onClose}
                        className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition-colors hover:bg-slate-100"
                    >
                        <HiOutlineX className="h-5 w-5" />
                    </button>
                </div>

                {/* Navigation Links */}
                <nav className="mt-4 flex-1 overflow-y-auto">
                    <ul className="font-DanaDemiBold flex flex-col gap-y-2 text-sm text-slate-700">
                        {NAV_LINKS.map((link) => (
                            <li key={link.id}>
                                <NavLink
                                    className="block rounded-lg px-3 py-2 transition-colors hover:bg-orange-50 hover:text-orange-500"
                                    onClick={onClose}
                                    to={link.address}
                                >
                                    {link.title}
                                </NavLink>
                            </li>
                        ))}
                    </ul>
                </nav>

                {/* Footer Auth Section */}
                <div className="border-t border-slate-100 pt-4">
                    {isLogin ? (
                        <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-2">
                            <button
                                type="button"
                                onClick={() =>
                                    setIsOptionsOpen((prev) => !prev)
                                }
                                className="flex w-full items-center justify-between rounded-lg bg-orange-500 px-3 py-2 text-white transition-colors hover:bg-orange-600"
                            >
                                <span className="font-DanaMedium text-xs">
                                    علی رضایی
                                </span>
                                <HiOutlineChevronDown
                                    className={`h-4 w-4 transition-transform duration-300 ${
                                        isOptionsOpen ? "rotate-180" : ""
                                    }`}
                                />
                            </button>

                            {/* Mobile Collapsible Submenu */}
                            <div
                                className={`grid overflow-hidden transition-[grid-template-rows,opacity] duration-300 ease-in-out ${
                                    isOptionsOpen
                                        ? "grid-rows-[1fr] opacity-100"
                                        : "grid-rows-[0fr] opacity-0"
                                }`}
                            >
                                <div className="min-h-0 overflow-hidden">
                                    <div className="font-DanaRegular flex flex-col gap-y-1 pt-2 text-xs text-slate-700">
                                        <a
                                            href="#"
                                            onClick={onClose}
                                            className="rounded-md px-3 py-1.5 transition-colors hover:bg-white hover:text-orange-500"
                                        >
                                            پروفایل کاربری
                                        </a>
                                        <a
                                            href="#"
                                            onClick={onClose}
                                            className="rounded-md px-3 py-1.5 transition-colors hover:bg-white hover:text-orange-500"
                                        >
                                            سفارش‌ها
                                        </a>
                                        <button
                                            type="button"
                                            onClick={() => {
                                                setIsOptionsOpen(false);
                                                onToggleLogin();
                                                onClose();
                                            }}
                                            className="w-full rounded-md px-3 py-1.5 text-right text-rose-500 transition-colors hover:bg-rose-50"
                                        >
                                            خروج از حساب
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <button
                            type="button"
                            onClick={() => {
                                onToggleLogin();
                                onClose();
                            }}
                            className="font-IRANYekanXRegular flex w-full items-center justify-center gap-x-2 rounded-lg bg-orange-500 py-2.5 text-center text-xs text-white transition-colors hover:bg-orange-600 min-[360px]:text-sm"
                        >
                            <HiOutlineUser className="h-4 w-4" />
                            <span>ورود یا ثبت‌نام</span>
                        </button>
                    )}
                </div>
            </aside>
        </>
    );
}
