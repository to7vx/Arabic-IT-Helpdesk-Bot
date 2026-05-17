// Agent workspace — split pane: conversation on the start side,
// AI copilot panel on the end side. Server-rendered with stub data
// today; Phase 5b wires the typed API client.
import { useTranslations } from 'next-intl';

const STUB_TICKET = {
  public_id: 'TKT-2026-00018',
  title: 'الـ VPN ما يشتغل من البيت',
  description: 'ابغى اشتغل عن بُعد بس الـ VPN يطلع لي خطأ 720.',
  status: 'open',
  priority: 'high',
  requester: 'Layla Al-Mutairi',
  dialect: 'saudi',
  language: 'ar',
};

const STUB_SUGGESTIONS = {
  summary:
    'المستخدم لا يستطيع الاتصال عبر الـ VPN (خطأ 720). آخر إجراء: لم يُجرَ بعد. الخطوة التالية: تطبيق حل إعادة تهيئة WAN Miniport.',
  category: { slug: 'network-vpn', confidence: 0.91 },
  kb: [
    { slug: 'vpn-error-720', title: 'حل خطأ VPN رقم 720 في ويندوز', score: 0.93 },
    { slug: 'vpn-troubleshooting', title: 'استكشاف مشاكل الاتصال عبر VPN', score: 0.78 },
  ],
  urgency: 0.62,
  sentiment: -0.2,
};

export default function AgentWorkspace({ params }: { params: { id: string } }) {
  const t = useTranslations();
  return (
    <main className="mx-auto grid max-w-7xl gap-6 px-6 py-6 lg:grid-cols-[1fr,360px]">
      <section className="space-y-4">
        <div>
          <div className="text-xs text-gray-500">{STUB_TICKET.public_id}</div>
          <h1 className="text-xl font-bold">{STUB_TICKET.title}</h1>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
          <div className="mb-1 text-xs text-gray-500">{STUB_TICKET.requester}</div>
          <p>{STUB_TICKET.description}</p>
        </div>
        <textarea
          placeholder="Type a reply…"
          rows={5}
          className="w-full rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900"
        />
        <div className="text-xs text-gray-500">Ticket ID: {params.id}</div>
      </section>

      <aside className="space-y-4">
        <div className="rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
          <h2 className="mb-2 text-sm font-semibold">AI summary</h2>
          <p className="text-sm">{STUB_SUGGESTIONS.summary}</p>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
          <h2 className="mb-2 text-sm font-semibold">Suggested category</h2>
          <p className="text-sm">
            {STUB_SUGGESTIONS.category.slug}{' '}
            <span className="text-xs text-gray-500">
              ({Math.round(STUB_SUGGESTIONS.category.confidence * 100)}%)
            </span>
          </p>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
          <h2 className="mb-2 text-sm font-semibold">Top KB</h2>
          <ul className="space-y-2 text-sm">
            {STUB_SUGGESTIONS.kb.map((hit) => (
              <li key={hit.slug} className="flex items-center justify-between gap-2">
                <span>{hit.title}</span>
                <span className="text-xs text-gray-500">{Math.round(hit.score * 100)}%</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
          <h2 className="mb-2 text-sm font-semibold">Signals</h2>
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt>Urgency</dt>
            <dd>{Math.round(STUB_SUGGESTIONS.urgency * 100)}%</dd>
            <dt>Sentiment</dt>
            <dd>{STUB_SUGGESTIONS.sentiment.toFixed(2)}</dd>
            <dt>Dialect</dt>
            <dd>{STUB_TICKET.dialect}</dd>
            <dt>Language</dt>
            <dd>{STUB_TICKET.language}</dd>
          </dl>
        </div>
        <div className="text-xs text-gray-500">{t('common.appName')}</div>
      </aside>
    </main>
  );
}
