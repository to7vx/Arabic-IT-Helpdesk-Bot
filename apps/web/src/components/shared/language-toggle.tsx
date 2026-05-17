'use client';

import { useLocale, useTranslations } from 'next-intl';
import { usePathname, useRouter } from 'next/navigation';
import { useTransition } from 'react';

export function LanguageToggle() {
  const t = useTranslations();
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();
  const [pending, startTransition] = useTransition();

  const target = locale === 'ar' ? 'en' : 'ar';
  const next = pathname.replace(`/${locale}`, `/${target}`);

  return (
    <button
      onClick={() => startTransition(() => router.replace(next))}
      disabled={pending}
      className="rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-900 hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
      aria-label="Toggle language"
    >
      {t('common.languageToggle')}
    </button>
  );
}
