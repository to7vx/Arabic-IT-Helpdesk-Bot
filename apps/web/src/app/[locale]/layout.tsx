import type { Metadata } from 'next';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Suspense } from 'react';

import { locales, type Locale } from '@/i18n';
import { dirFor } from '@/lib/utils';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: {
    default: 'Arabic IT Helpdesk',
    template: '%s — Arabic IT Helpdesk',
  },
  description: 'Open-source bilingual IT helpdesk with Arabic NLP.',
};

type Props = {
  children: React.ReactNode;
  params: { locale: string };
};

export function generateStaticParams(): { locale: string }[] {
  return locales.map((l) => ({ locale: l }));
}

export default async function RootLayout({ children, params: { locale } }: Props) {
  if (!locales.includes(locale as Locale)) notFound();
  const messages = await getMessages();
  return (
    <html lang={locale} dir={dirFor(locale)} suppressHydrationWarning>
      <body className="min-h-screen bg-white text-gray-900 antialiased dark:bg-gray-900 dark:text-gray-100">
        <NextIntlClientProvider locale={locale} messages={messages}>
          <Suspense>{children}</Suspense>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
