import { useTranslations } from 'next-intl';

export default function KbPage() {
  const t = useTranslations();
  return (
    <main className="mx-auto max-w-5xl px-6 py-8">
      <h1 className="mb-6 text-2xl font-bold">{t('kb.title')}</h1>
      <input
        type="search"
        placeholder={t('kb.searchPlaceholder')}
        className="mb-6 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 dark:border-gray-700 dark:bg-gray-900"
      />
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Phase 5b wires this to GET /api/v1/kb. Today the seed corpus lives in data/kb-seed.
      </p>
    </main>
  );
}
