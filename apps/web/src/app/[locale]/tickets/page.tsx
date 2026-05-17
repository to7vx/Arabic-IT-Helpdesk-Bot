import { useTranslations } from 'next-intl';
import Link from 'next/link';

import { Button } from '@/components/ui/button';

// In Phase 5 this is server-rendered with stubbed data. Phase 5b
// wires the typed API client to /api/v1/tickets once auth lands.
const STUB_TICKETS = [
  {
    id: '1',
    public_id: 'TKT-2026-00012',
    title: 'الـ VPN ما يشتغل من البيت',
    status: 'open',
    priority: 'high',
    requester: 'Layla Al-Mutairi',
  },
  {
    id: '2',
    public_id: 'TKT-2026-00013',
    title: 'Outlook crashes on launch after update',
    status: 'pending',
    priority: 'medium',
    requester: 'Ahmed Al-Saud',
  },
  {
    id: '3',
    public_id: 'TKT-2026-00014',
    title: 'نسيت كلمة السر للحساب',
    status: 'resolved',
    priority: 'low',
    requester: 'Noor Al-Anazi',
  },
];

const STATUS_PALETTE: Record<string, string> = {
  new: 'bg-blue-100 text-blue-800',
  open: 'bg-amber-100 text-amber-800',
  pending: 'bg-purple-100 text-purple-800',
  resolved: 'bg-emerald-100 text-emerald-800',
  closed: 'bg-gray-100 text-gray-700',
};

export default function TicketsPage() {
  const t = useTranslations();
  return (
    <main className="mx-auto max-w-5xl px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">{t('tickets.title')}</h1>
        <Button asChild>
          <Link href="/tickets/new">{t('tickets.newTicket')}</Link>
        </Button>
      </div>

      <ul className="divide-y divide-gray-200 overflow-hidden rounded-2xl border border-gray-200 bg-white dark:divide-gray-800 dark:border-gray-800 dark:bg-gray-900">
        {STUB_TICKETS.map((ticket) => (
          <li key={ticket.id} className="flex items-center gap-4 p-4">
            <div className="flex-1">
              <div className="text-xs text-gray-500">{ticket.public_id}</div>
              <Link href={`/tickets/${ticket.id}`} className="text-base font-medium hover:underline">
                {ticket.title}
              </Link>
              <div className="mt-1 text-xs text-gray-600 dark:text-gray-400">{ticket.requester}</div>
            </div>
            <span
              className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${STATUS_PALETTE[ticket.status] ?? ''}`}
            >
              {t(`tickets.status.${ticket.status}` as never)}
            </span>
            <span className="text-xs text-gray-500">
              {t(`tickets.priority.${ticket.priority}` as never)}
            </span>
          </li>
        ))}
      </ul>
    </main>
  );
}
