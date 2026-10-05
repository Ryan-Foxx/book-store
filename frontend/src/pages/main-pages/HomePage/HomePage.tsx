import { HiOutlineSearch } from "react-icons/hi";
import heroImage from "@/assets/images/hero-book.png";

function HomePage() {
    return (
        <>
            <HeroSection />
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
