import { useTranslations } from 'next-intl';
import Link from 'next/link';

import { LanguageToggle } from '@/components/shared/language-toggle';

export default function HomePage() {
  const t = useTranslations();
  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <header className="mb-12 flex items-center justify-between">
        <div className="text-lg font-semibold">{t('common.appName')}</div>
        <LanguageToggle />
      </header>

      <section className="rounded-3xl border border-gray-200 bg-gradient-to-br from-brand-50 to-white p-12 dark:border-gray-800 dark:from-brand-900/30 dark:to-gray-900">
        <h1 className="text-4xl font-bold leading-tight text-gray-900 dark:text-white sm:text-5xl">
          {t('home.heroTitle')}
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-gray-700 dark:text-gray-300">{t('home.heroBody')}</p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href="/tickets"
            className="rounded-xl bg-brand-600 px-5 py-3 text-sm font-medium text-white shadow hover:bg-brand-700"
          >
            {t('home.ctaPrimary')}
          </Link>
          <a
            href="https://arabic-helpdesk.dev"
            className="rounded-xl border border-gray-300 bg-white px-5 py-3 text-sm font-medium text-gray-900 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
          >
            {t('home.ctaSecondary')}
          </a>
        </div>
      </section>

      <section className="mt-12 grid gap-6 sm:grid-cols-3">
        <FeatureCard title={t('home.featureNlpTitle')} body={t('home.featureNlpBody')} />
        <FeatureCard title={t('home.featureBilingualTitle')} body={t('home.featureBilingualBody')} />
        <FeatureCard title={t('home.featurePdplTitle')} body={t('home.featurePdplBody')} />
      </section>
    </main>
  );
}

function FeatureCard({ title, body }: { title: string; body: string }) {
  return (
    <article className="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900">
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">{body}</p>
    </article>
  );
}
