import { Link } from "react-router-dom";
import { HiOutlineBookOpen, HiChevronUp } from "react-icons/hi2";

// Types & Nav Configurations
interface FooterLinkItem {
    label: string;
    href: string;
    isAnchor?: boolean;
}

const MAIN_NAV_LINKS: FooterLinkItem[] = [
    { label: "خانه", href: "/" },
    { label: "فروشگاه", href: "store" },
    { label: "دسته‌بندی", href: "category" },
];

const SUPPORT_LINKS: FooterLinkItem[] = [
    { label: "سوالات متداول", href: "/#faq-section", isAnchor: true },
    { label: "سیاست‌ها و قوانین", href: "#" },
    { label: "تماس با ما", href: "contact-us" },
    { label: "درباره ما", href: "about-us" },
];

const TRACKING_LINKS: FooterLinkItem[] = [
    { label: "گزارش", href: "#" },
    { label: "پیگیری سفارش", href: "#" },
];

// Main Footer Component
function Footer() {
    const currentYear = new Intl.NumberFormat("fa-IR", {
        useGrouping: false,
    }).format(new Date().getFullYear());

    // Smooth scroll to top function
    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    return (
        <footer
            className="relative border-t border-slate-200 bg-white"
            aria-labelledby="footer-heading"
        >
            <h2 id="footer-heading" className="sr-only">
                پاورقی
            </h2>

            {/* Back to Top Button */}
            <button
                onClick={scrollToTop}
                aria-label="بازگشت به ابتدای صفحه"
                className="absolute -top-6 left-1/2 flex h-12 w-12 -translate-x-1/2 items-center justify-center rounded-full bg-white text-slate-400 shadow-md ring-1 ring-slate-200 transition-all hover:text-orange-600 hover:shadow-lg focus:outline-none sm:-top-7 sm:h-14 sm:w-14"
            >
                <HiChevronUp className="h-6 w-6 cursor-pointer sm:h-8 sm:w-8" />
            </button>

            <div className="container mx-auto px-4 py-16 sm:py-20">
                <div className="flex flex-col gap-y-10 md:flex-row md:flex-wrap md:justify-between lg:flex-nowrap">
                    {/* Brand Column - fixed width on desktop */}
                    <div className="w-full md:max-w-xs">
                        <FooterBrand />
                    </div>

                    {/* Navigation Columns */}
                    <div className="flex flex-1 flex-wrap justify-between gap-8 md:mr-12 lg:mr-20">
                        <FooterLinkGroup
                            title="منوی اصلی"
                            links={MAIN_NAV_LINKS}
                        />
                        <FooterLinkGroup
                            title="پشتیبانی"
                            links={SUPPORT_LINKS}
                        />
                        <FooterLinkGroup
                            title="پیگیری‌ها"
                            links={TRACKING_LINKS}
                        />
                    </div>
                </div>
            </div>

            {/* Copyright Sub-footer */}
            <div className="border-t border-slate-100 bg-slate-50 py-5">
                <div className="container mx-auto px-4 text-center">
                    <p className="font-Dana text-[11px] leading-6 text-slate-500 sm:text-xs">
                        تمامی حقوق مادی و معنوی برای وب‌سایت فصل کتاب محفوظ است
                        © {currentYear}
                    </p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;

// Sub-Components
function FooterBrand() {
    return (
        <div className="flex flex-col items-start gap-4">
            <Link
                to="/"
                className="group flex items-center gap-2.5 text-slate-900"
            >
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500 text-white shadow-lg shadow-orange-200 transition-colors group-hover:bg-orange-600">
                    <HiOutlineBookOpen className="h-6 w-6" />
                </div>
                <span className="font-MorabbaBold text-2xl tracking-tight">
                    فصل کتاب
                </span>
            </Link>

            <p className="font-Dana text-[13px] leading-7 text-slate-500">
                اگر نتوانید راهی برای تغییر کلمات خود بیابید، نمی‌توانید طرز فکر
                خود را تغییر دهید.
            </p>
            <span className="font-DanaMedium text-[11px] text-slate-400">
                — دسپیناتولو کوئلیو
            </span>
        </div>
    );
}

function FooterLinkGroup({
    title,
    links,
}: {
    title: string;
    links: FooterLinkItem[];
}) {
    return (
        <div className="flex min-w-30 flex-col gap-4">
            <h3 className="font-MorabbaBold text-base text-slate-900">
                {title}
            </h3>
            <ul className="flex flex-col gap-3">
                {links.map((link) => (
                    <li key={link.label}>
                        {link.isAnchor ? (
                            /* Simple <a> tag for hash scrolling within the same page */
                            <a
                                href={link.href}
                                className="font-Dana inline-block text-[13px] text-slate-600 transition-colors hover:text-orange-600"
                            >
                                {link.label}
                            </a>
                        ) : (
                            <Link
                                to={link.href}
                                className="font-Dana inline-block text-[13px] text-slate-600 transition-colors hover:text-orange-600"
                            >
                                {link.label}
                            </Link>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
}
