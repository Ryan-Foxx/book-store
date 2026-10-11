import type { IconType } from "react-icons";
import {
    HiOutlineClock,
    HiOutlineEnvelope,
    HiOutlineMapPin,
    HiOutlinePhone,
} from "react-icons/hi2";

interface ContactMethod {
    id: number;
    title: string;
    value: string;
    description: string;
    href?: string;
    icon: IconType;
}

const CONTACT_METHODS: ContactMethod[] = [
    {
        id: 1,
        title: "ایمیل",
        value: "support@example.com",
        description: "برای پرسش‌ها و درخواست‌های پشتیبانی",
        href: "mailto:support@example.com",
        icon: HiOutlineEnvelope,
    },
    {
        id: 2,
        title: "تلفن",
        value: "۰۲۱-۱۲۳۴۵۶۷۸",
        description: "شنبه تا چهارشنبه، ساعت ۹ تا ۱۷",
        href: "tel:+982112345678",
        icon: HiOutlinePhone,
    },
    {
        id: 3,
        title: "نشانی",
        value: "نشانی مجموعه",
        description: "نشانی محل فعالیت مجموعه را اینجا وارد کنید.",
        icon: HiOutlineMapPin,
    },
];

function ContactUsPage() {
    return (
        <main className="bg-slate-50">
            <ContactHero />

            <section
                className="container mx-auto px-4 py-10 sm:py-14 lg:py-16"
                aria-labelledby="contact-content-title"
            >
                <h2 id="contact-content-title" className="sr-only">
                    راه‌های ارتباط با فصل کتاب
                </h2>

                <div className="grid min-w-0 gap-6 lg:grid-cols-[0.9fr_1.1fr] lg:gap-8">
                    <ContactInformation />
                    <ContactForm />
                </div>
            </section>
        </main>
    );
}

export default ContactUsPage;

function ContactHero() {
    return (
        <section className="border-b border-slate-200 bg-white">
            <div className="container mx-auto px-4 py-12 text-center sm:py-16">
                <span className="font-Dana inline-flex rounded-full bg-orange-100 px-3 py-1 text-xs text-orange-700">
                    ارتباط با ما
                </span>

                <h1 className="font-MorabbaBold mt-4 text-3xl leading-tight text-slate-900 sm:text-4xl">
                    چطور می‌توانیم کمکتان کنیم؟
                </h1>

                <p className="font-Dana mx-auto mt-4 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base sm:leading-8">
                    اگر پرسشی دارید یا به راهنمایی نیاز دارید، از راه‌های
                    ارتباطی زیر استفاده کنید یا پیام خود را برای ما بنویسید.
                </p>
            </div>
        </section>
    );
}

function ContactInformation() {
    return (
        <section className="min-w-0" aria-labelledby="contact-info-title">
            <div className="mb-5">
                <h2
                    id="contact-info-title"
                    className="font-MorabbaBold text-2xl text-slate-900"
                >
                    راه‌های ارتباطی
                </h2>
                <p className="font-Dana mt-2 text-sm leading-7 text-slate-500">
                    یکی از روش‌های زیر را برای ارتباط با ما انتخاب کنید.
                </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
                {CONTACT_METHODS.map((method) => (
                    <ContactMethodCard key={method.id} method={method} />
                ))}
            </div>

            <div className="mt-4 rounded-2xl border border-orange-100 bg-orange-50 p-5 sm:p-6">
                <div className="flex items-start gap-3">
                    <HiOutlineClock
                        className="mt-0.5 h-6 w-6 shrink-0 text-orange-600"
                        aria-hidden="true"
                    />
                    <div>
                        <h3 className="font-MorabbaBold text-lg text-slate-900">
                            زمان پاسخ‌گویی
                        </h3>
                        <p className="font-Dana mt-2 text-sm leading-7 text-slate-600">
                            پیام‌های شما را در روزهای کاری بررسی می‌کنیم و در
                            اولین فرصت پاسخ می‌دهیم.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}

function ContactMethodCard({ method }: { method: ContactMethod }) {
    const Icon = method.icon;
    const content = (
        <>
            <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-orange-100 text-orange-600">
                <Icon className="h-5 w-5" aria-hidden="true" />
            </span>

            <span className="min-w-0">
                <span className="font-MorabbaBold block text-lg text-slate-900">
                    {method.title}
                </span>
                <span
                    className="font-Dana mt-1 block text-sm wrap-break-word text-slate-700"
                    dir={
                        method.href?.startsWith("mailto:") ||
                        method.href?.startsWith("tel:")
                            ? "ltr"
                            : undefined
                    }
                >
                    {method.value}
                </span>
                <span className="font-Dana mt-1 block text-xs leading-6 text-slate-500">
                    {method.description}
                </span>
            </span>
        </>
    );

    if (method.href) {
        return (
            <a
                href={method.href}
                className="flex min-w-0 items-start gap-4 rounded-2xl border border-slate-200 bg-white p-4 transition-colors hover:border-orange-200 hover:bg-orange-50/40 sm:p-5"
            >
                {content}
            </a>
        );
    }

    return (
        <div className="flex min-w-0 items-start gap-4 rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
            {content}
        </div>
    );
}

function ContactForm() {
    return (
        <section
            className="min-w-0 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7 lg:p-8"
            aria-labelledby="contact-form-title"
        >
            <div className="mb-6">
                <h2
                    id="contact-form-title"
                    className="font-MorabbaBold text-2xl text-slate-900"
                >
                    برای ما پیام بفرستید
                </h2>
                <p className="font-Dana mt-2 text-sm leading-7 text-slate-500">
                    اطلاعات زیر را وارد کنید تا بتوانیم بهتر راهنمایی‌تان کنیم.
                </p>
            </div>

            <form
                onSubmit={(event) => event.preventDefault()}
                className="space-y-5"
            >
                <div className="grid gap-5 sm:grid-cols-2">
                    <div>
                        <label
                            htmlFor="contact-name"
                            className="font-DanaMedium mb-2 block text-sm text-slate-700"
                        >
                            نام و نام خانوادگی
                        </label>
                        <input
                            id="contact-name"
                            name="name"
                            type="text"
                            autoComplete="name"
                            placeholder="نام شما"
                            className="font-Dana w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 transition outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="contact-email"
                            className="font-DanaMedium mb-2 block text-sm text-slate-700"
                        >
                            ایمیل
                        </label>
                        <input
                            id="contact-email"
                            name="email"
                            type="email"
                            autoComplete="email"
                            placeholder="you@example.com"
                            dir="ltr"
                            className="font-Dana w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-left text-sm text-slate-900 transition outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
                        />
                    </div>
                </div>

                <div>
                    <label
                        htmlFor="contact-subject"
                        className="font-DanaMedium mb-2 block text-sm text-slate-700"
                    >
                        موضوع پیام
                    </label>
                    <input
                        id="contact-subject"
                        name="subject"
                        type="text"
                        placeholder="موضوع پیام شما"
                        className="font-Dana w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 transition outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
                    />
                </div>

                <div>
                    <label
                        htmlFor="contact-message"
                        className="font-DanaMedium mb-2 block text-sm text-slate-700"
                    >
                        متن پیام
                    </label>
                    <textarea
                        id="contact-message"
                        name="message"
                        rows={5}
                        placeholder="پیام خود را اینجا بنویسید..."
                        className="font-Dana w-full resize-y rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-7 text-slate-900 transition outline-none placeholder:text-slate-400 focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
                    />
                </div>

                <button
                    type="button"
                    aria-label="ارسال پیام؛ فرم هنوز به سامانه ارسال متصل نشده است"
                    className="font-DanaMedium w-full rounded-xl bg-orange-500 px-5 py-3 text-sm text-white transition-colors hover:bg-orange-600 focus:ring-2 focus:ring-orange-300 focus:ring-offset-2 focus:outline-none sm:w-auto"
                >
                    ارسال پیام
                </button>

                <p className="font-Dana text-xs leading-6 text-slate-400">
                    این فرم فعلاً نمایشی است و هنوز به سامانه‌ی ارسال پیام متصل
                    نشده است.
                </p>
            </form>
        </section>
    );
}
