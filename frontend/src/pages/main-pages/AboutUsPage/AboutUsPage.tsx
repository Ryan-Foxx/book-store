import {
    HiOutlineBookOpen,
    HiOutlineUsers,
    HiOutlineSparkles,
    HiOutlineHeart,
} from "react-icons/hi2";

// Static Data
interface AboutFeatureItem {
    id: number;
    title: string;
    description: string;
    icon: React.ReactNode;
}

const ABOUT_FEATURES: AboutFeatureItem[] = [
    {
        id: 1,
        title: "دسترسی آسان به کتاب‌ها",
        description:
            "ما تلاش می‌کنیم مجموعه‌ای متنوع از کتاب‌های عمومی، تخصصی و آموزشی را در محیطی ساده و کاربرپسند در اختیار شما قرار دهیم.",
        icon: <HiOutlineBookOpen className="h-6 w-6" />,
    },
    {
        id: 2,
        title: "همراهی با جامعه کتاب‌دوستان",
        description:
            "فصل کتاب جایی برای گردهم آمدن علاقه‌مندان به مطالعه است؛ جایی برای کشف عنوان‌های تازه و انتخاب‌های ارزشمند.",
        icon: <HiOutlineUsers className="h-6 w-6" />,
    },
    {
        id: 3,
        title: "تجربه‌ای ساده و دلنشین",
        description:
            "ما تجربه کاربری روان، طراحی مینیمال و دسترسی سریع به بخش‌های مختلف سایت را یکی از مهم‌ترین اولویت‌های خود می‌دانیم.",
        icon: <HiOutlineSparkles className="h-6 w-6" />,
    },
    {
        id: 4,
        title: "عشق به مطالعه",
        description:
            "باور داریم کتاب فقط یک کالا نیست، بلکه پلی برای رشد فردی، آگاهی بیشتر و ساختن دنیایی بهتر است.",
        icon: <HiOutlineHeart className="h-6 w-6" />,
    },
];

// Main Component
function AboutUsPage() {
    return (
        <main className="bg-slate-50">
            <AboutHeroSection />
            <AboutStorySection />
            <AboutFeaturesSection />
            <AboutValuesSection />
        </main>
    );
}

export default AboutUsPage;

// Sub Components
function AboutHeroSection() {
    return (
        <section className="border-b border-slate-200 bg-white">
            <div className="container mx-auto px-4 py-12 sm:py-16 lg:py-20">
                <div className="grid items-center gap-8 lg:grid-cols-2 lg:gap-12">
                    <div className="order-2 lg:order-1">
                        <span className="inline-flex rounded-full bg-orange-100 px-3 py-1 text-xs text-orange-700">
                            درباره ما
                        </span>

                        <h1 className="font-MorabbaBold mt-4 text-3xl leading-tight text-slate-900 sm:text-4xl lg:text-5xl">
                            فصل کتاب، همراهی برای کشف دنیای مطالعه
                        </h1>

                        <p className="font-Dana mt-5 text-sm leading-7 text-slate-600 sm:text-base sm:leading-8">
                            ما در فصل کتاب تلاش می‌کنیم فضایی ساده، دلنشین و
                            قابل اعتماد برای علاقه‌مندان به کتاب فراهم کنیم؛
                            جایی که پیدا کردن، بررسی و انتخاب کتاب‌ها به
                            تجربه‌ای راحت و لذت‌بخش تبدیل شود.
                        </p>
                    </div>

                    <div className="order-1 lg:order-2">
                        <div className="rounded-3xl border border-orange-100 bg-linear-to-br from-orange-50 via-white to-amber-50 p-6 shadow-sm sm:p-8">
                            <div className="flex items-center gap-3">
                                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-orange-500 text-white shadow-lg shadow-orange-200">
                                    <HiOutlineBookOpen className="h-7 w-7" />
                                </div>
                                <div>
                                    <h2 className="font-MorabbaBold text-2xl text-slate-900 sm:text-3xl">
                                        فصل کتاب
                                    </h2>
                                    <p className="font-Dana text-xs text-slate-500 sm:text-sm">
                                        برای کسانی که مطالعه را جدی می‌گیرند
                                    </p>
                                </div>
                            </div>

                            <div className="xs:grid-cols-2 mt-6 grid grid-cols-1 gap-4">
                                <AboutStatCard
                                    title="تنوع موضوعی"
                                    value="گسترده"
                                />
                                <AboutStatCard
                                    title="تجربه کاربری"
                                    value="ساده"
                                />
                                <AboutStatCard
                                    title="مناسب برای"
                                    value="کتاب‌دوستان"
                                />
                                <AboutStatCard
                                    title="هدف ما"
                                    value="انتخاب بهتر"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

function AboutStorySection() {
    return (
        <section className="bg-slate-50">
            <div className="container mx-auto px-4 py-12 sm:py-16">
                <div className="mx-auto max-w-4xl rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 lg:p-10">
                    <div className="flex flex-col gap-4">
                        <span className="inline-flex w-fit rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                            داستان ما
                        </span>

                        <h2 className="font-MorabbaBold text-2xl text-slate-900 sm:text-3xl">
                            چرا فصل کتاب شکل گرفت؟
                        </h2>

                        <p className="font-Dana text-sm leading-7 text-slate-600 sm:text-base sm:leading-8">
                            ایده فصل کتاب از یک دغدغه ساده شکل گرفت: اینکه پیدا
                            کردن کتاب خوب، نباید سخت و زمان‌بر باشد. ما خواستیم
                            بستری ایجاد کنیم که کاربران بتوانند در آن با آرامش،
                            کتاب‌های مختلف را ببینند، مقایسه کنند و انتخاب
                            آگاهانه‌تری داشته باشند.
                        </p>

                        <p className="font-Dana text-sm leading-7 text-slate-600 sm:text-base sm:leading-8">
                            تمرکز ما روی سادگی، نظم در نمایش محتوا و تجربه‌ای
                            است که حس خوبی به مخاطب بدهد. ما باور داریم هر کتاب
                            می‌تواند شروع یک تغییر باشد و وظیفه ما این است که
                            مسیر رسیدن به آن را هموارتر کنیم.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}

function AboutFeaturesSection() {
    return (
        <section className="bg-white">
            <div className="container mx-auto px-4 py-12 sm:py-16">
                <div className="mb-8 text-center sm:mb-10">
                    <span className="inline-flex rounded-full bg-orange-100 px-3 py-1 text-xs text-orange-700">
                        آنچه برای ما مهم است
                    </span>
                    <h2 className="font-MorabbaBold mt-4 text-2xl text-slate-900 sm:text-3xl">
                        ویژگی‌های اصلی فصل کتاب
                    </h2>
                    <p className="font-Dana mx-auto mt-3 max-w-2xl text-sm leading-7 text-slate-500 sm:text-base">
                        ما تلاش می‌کنیم تجربه‌ای قابل اعتماد، ساده و کاربردی
                        برای کاربران فراهم کنیم تا انتخاب کتاب به فرآیندی دلنشین
                        تبدیل شود.
                    </p>
                </div>

                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                    {ABOUT_FEATURES.map((feature) => (
                        <AboutFeatureCard key={feature.id} feature={feature} />
                    ))}
                </div>
            </div>
        </section>
    );
}

function AboutValuesSection() {
    return (
        <section className="bg-slate-50">
            <div className="container mx-auto px-4 py-12 sm:py-16">
                <div className="grid gap-6 lg:grid-cols-2">
                    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
                        <h2 className="font-MorabbaBold text-2xl text-slate-900 sm:text-3xl">
                            مأموریت ما
                        </h2>
                        <p className="font-Dana mt-4 text-sm leading-7 text-slate-600 sm:text-base sm:leading-8">
                            ایجاد بستری کاربرمحور برای معرفی و ارائه کتاب‌ها، به
                            شکلی که کاربران بتوانند با کمترین پیچیدگی و بیشترین
                            وضوح، کتاب مناسب خود را پیدا کنند.
                        </p>
                    </div>

                    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
                        <h2 className="font-MorabbaBold text-2xl text-slate-900 sm:text-3xl">
                            چشم‌انداز ما
                        </h2>
                        <p className="font-Dana mt-4 text-sm leading-7 text-slate-600 sm:text-base sm:leading-8">
                            تبدیل شدن به یکی از تجربه‌های دوست‌داشتنی و قابل
                            اعتماد در فضای آنلاین کتاب؛ جایی که کاربران برای کشف
                            و انتخاب کتاب همیشه به آن برگردند.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}

function AboutFeatureCard({ feature }: { feature: AboutFeatureItem }) {
    return (
        <article className="rounded-3xl border border-slate-200 bg-slate-50 p-5 transition-all hover:-translate-y-1 hover:border-orange-200 hover:shadow-md">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-orange-100 text-orange-600">
                {feature.icon}
            </div>

            <h3 className="font-MorabbaBold mt-4 text-xl text-slate-900">
                {feature.title}
            </h3>

            <p className="font-Dana mt-3 text-sm leading-7 text-slate-600">
                {feature.description}
            </p>
        </article>
    );
}

function AboutStatCard({ title, value }: { title: string; value: string }) {
    return (
        <div className="rounded-2xl border border-slate-200 bg-white px-4 py-4 text-center">
            <p className="font-Dana text-xs text-slate-500">{title}</p>
            <p className="font-DanaMedium mt-2 text-sm text-slate-800">
                {value}
            </p>
        </div>
    );
}
