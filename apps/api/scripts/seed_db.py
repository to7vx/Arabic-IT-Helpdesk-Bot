"""Seed the database with organizations, teams, users, categories, and sample tickets.

Usage:
    uv run python -m scripts.seed_db [--demo]

``--demo`` adds extra rows aimed at demos (more tickets across more dialects).
"""

from __future__ import annotations

import argparse
import asyncio
import random
from datetime import datetime, timedelta, timezone

from passlib.hash import argon2
from sqlalchemy import select

from helpdesk.db import models
from helpdesk.db.session import session_scope

# ---------------------------------------------------------------------------
# Static seed catalog
# ---------------------------------------------------------------------------

CATEGORIES: list[tuple[str, str, str]] = [
    # (slug, name_en, name_ar)
    ("hardware", "Hardware", "أجهزة"),
    ("hardware-printer", "Printer", "طابعة"),
    ("hardware-laptop", "Laptop", "حاسوب محمول"),
    ("hardware-desktop", "Desktop", "حاسوب مكتبي"),
    ("hardware-peripheral", "Peripheral", "ملحقات"),
    ("software", "Software", "برمجيات"),
    ("software-office", "Microsoft Office", "مايكروسوفت أوفيس"),
    ("software-os", "Operating System", "نظام التشغيل"),
    ("software-install", "Installation", "تثبيت"),
    ("software-update", "Update", "تحديث"),
    ("network", "Network", "شبكة"),
    ("network-vpn", "VPN", "في بي إن"),
    ("network-wifi", "Wi-Fi", "واي فاي"),
    ("network-internet", "Internet Access", "وصول إنترنت"),
    ("network-firewall", "Firewall", "جدار حماية"),
    ("account", "Account", "حساب"),
    ("account-password", "Password Reset", "إعادة تعيين كلمة المرور"),
    ("account-mfa", "MFA Issue", "مشكلة في التحقق الثنائي"),
    ("account-access", "Access Request", "طلب صلاحية"),
    ("account-create", "Account Creation", "إنشاء حساب"),
    ("email", "Email", "بريد إلكتروني"),
    ("email-outlook", "Outlook", "أوتلوك"),
    ("email-spam", "Spam", "بريد مزعج"),
    ("email-delivery", "Delivery Issue", "مشكلة تسليم"),
    ("security", "Security", "أمن"),
    ("security-phishing", "Phishing", "تصيد إلكتروني"),
    ("security-malware", "Malware", "برمجيات خبيثة"),
    ("security-incident", "Security Incident", "حادثة أمنية"),
    ("telephony", "Telephony", "اتصالات"),
    ("telephony-handset", "Handset", "سماعة"),
    ("telephony-conference", "Conference Call", "مكالمة جماعية"),
    ("collab", "Collaboration", "تعاون"),
    ("collab-teams", "Microsoft Teams", "مايكروسوفت تيمز"),
    ("collab-zoom", "Zoom", "زووم"),
    ("collab-sharepoint", "SharePoint", "شيربوينت"),
    ("erp", "ERP / Business Apps", "تطبيقات الأعمال"),
    ("erp-sap", "SAP", "ساب"),
    ("erp-oracle", "Oracle", "أوراكل"),
    ("mobile", "Mobile Device", "جهاز جوال"),
    ("mobile-mdm", "MDM Enrollment", "تسجيل في إدارة الأجهزة"),
    ("mobile-app", "Mobile App", "تطبيق جوال"),
    ("backup", "Backup & Restore", "نسخ احتياطي واستعادة"),
    ("printing", "Printing", "طباعة"),
    ("training", "Training", "تدريب"),
    ("procurement", "Procurement", "مشتريات"),
    ("onboarding", "Onboarding", "انضمام"),
    ("offboarding", "Offboarding", "انفكاك"),
    ("other", "Other", "أخرى"),
    ("feedback", "Feedback", "ملاحظات"),
    ("compliance", "Compliance Request", "طلب امتثال"),
]

USERS: list[tuple[str, str, str, str]] = [
    # (email, role, name_en, name_ar)
    ("admin@example.com", "admin", "Admin User", "مدير النظام"),
    ("ahmed.agent@example.com", "agent", "Ahmed Al-Saud", "أحمد آل سعود"),
    ("fatima.agent@example.com", "agent", "Fatima Al-Zahrani", "فاطمة الزهراني"),
    ("khalid.agent@example.com", "agent", "Khalid Al-Otaibi", "خالد العتيبي"),
    ("sara.agent@example.com", "agent", "Sara Al-Qahtani", "سارة القحطاني"),
    ("maha.manager@example.com", "manager", "Maha Al-Harbi", "مها الحربي"),
    ("omar.manager@example.com", "manager", "Omar Al-Ghamdi", "عمر الغامدي"),
    ("layla.user@example.com", "end_user", "Layla Al-Mutairi", "ليلى المطيري"),
    ("noor.user@example.com", "end_user", "Noor Al-Anazi", "نور العنزي"),
    ("yusuf.user@example.com", "end_user", "Yusuf Al-Shahrani", "يوسف الشهراني"),
    ("hana.user@example.com", "end_user", "Hana Al-Faleh", "هناء الفالح"),
    ("ali.user@example.com", "end_user", "Ali Al-Dosari", "علي الدوسري"),
    ("reem.user@example.com", "end_user", "Reem Al-Sulaiman", "ريم السليمان"),
    ("mohammed.user@example.com", "end_user", "Mohammed Al-Hassan", "محمد الحسن"),
    ("aisha.user@example.com", "end_user", "Aisha Al-Najjar", "عائشة النجار"),
    ("badr.user@example.com", "end_user", "Badr Al-Rasheed", "بدر الرشيد"),
    ("salma.user@example.com", "end_user", "Salma Al-Mansour", "سلمى المنصور"),
    ("tariq.user@example.com", "end_user", "Tariq Al-Khalil", "طارق الخليل"),
    ("dina.user@example.com", "end_user", "Dina Al-Yamani", "دينا اليماني"),
    ("hassan.user@example.com", "end_user", "Hassan Al-Bakr", "حسن البكر"),
]

TEAMS: list[tuple[str, str, str, list[str]]] = [
    # (slug, name_en, name_ar, skills)
    ("hardware", "Hardware Support", "دعم الأجهزة", ["hardware", "printing"]),
    ("network", "Network Operations", "عمليات الشبكة", ["network", "vpn", "wifi"]),
    ("apps", "Business Applications", "تطبيقات الأعمال", ["software", "erp", "collab", "email"]),
    ("security", "Security & Compliance", "الأمن والامتثال", ["security", "compliance"]),
    ("onboarding", "Onboarding & Accounts", "الانضمام والحسابات", ["account", "onboarding", "offboarding"]),
]

# Sample ticket templates: (title_template, body_template, language, dialect, suggested_category_slug)
TICKET_SEED: list[tuple[str, str, str, str, str]] = [
    ("لا أستطيع طباعة من جهازي",
     "السلام عليكم، الطابعة في مكتبي ما تطبع. حاولت إعادة التشغيل وما زالت لا تستجيب. الرقم: HP-1234",
     "ar", "saudi", "hardware-printer"),
    ("Outlook keeps crashing on launch",
     "Every time I open Outlook 2024 it crashes within 5 seconds. Reinstalled twice. Windows 11, machine ID DELL-5567.",
     "en", "msa", "email-outlook"),
    ("الـ VPN ما يشتغل من البيت",
     "ابغى اشتغل عن بُعد بس الـ VPN يطلع لي خطأ 720. جربت من جوال وكمبيوتر. اسم المستخدم a.alsaud",
     "ar", "saudi", "network-vpn"),
    ("نسيت كلمة السر",
     "لو سمحت، نسيت كلمة المرور لحسابي. ايميلي: layla.user@example.com",
     "ar", "msa", "account-password"),
    ("Need MFA reset urgently — flying tomorrow",
     "My TOTP app was on a phone that's now broken. I leave on a business trip in 18 hours and cannot log in.",
     "en", "msa", "account-mfa"),
    ("مايكروسوفت تيمز ما يفتح الكاميرا",
     "في اجتماع مهم بعد ساعة، Teams ما يحس بالكاميرا. ويندوز 11.",
     "ar", "saudi", "collab-teams"),
    ("msh 3aref el password bta3 el wifi el jdeed",
     "Plz send the new wifi password for the 5th floor, thanks",
     "ar", "arabizi", "network-wifi"),
    ("Spam attack on finance team mailboxes",
     "5+ finance staff received the same phishing email with a malicious xlsx. Need block + investigation.",
     "en", "msa", "security-phishing"),
    ("طلب صلاحية مجلد المالية",
     "أحتاج صلاحية قراءة على مجلد المالية على شيربوينت. المدير وافق بالإيميل المرفق.",
     "ar", "msa", "account-access"),
    ("SAP login error — message code MSG-3055",
     "SAP GUI returns MSG-3055 when I log in. Cleared cache, no luck. User: a.alsaud@example.com",
     "en", "msa", "erp-sap"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_password_hash(password: str) -> str:
    return argon2.using(time_cost=2, memory_cost=19 * 1024, parallelism=1).hash(password)


def public_id(n: int) -> str:
    return f"TKT-{datetime.now(timezone.utc):%Y}-{n:05d}"


# ---------------------------------------------------------------------------
# Main seed routine
# ---------------------------------------------------------------------------

async def seed(demo: bool) -> None:
    async with session_scope() as session:
        # ---- Organization ----
        existing = await session.scalar(
            select(models.Organization).where(models.Organization.slug == "default")
        )
        if existing is None:
            org = models.Organization(
                slug="default",
                name_en="Default Organization",
                name_ar="المؤسسة الافتراضية",
            )
            session.add(org)
            await session.flush()
        else:
            org = existing

        # ---- Teams ----
        teams: dict[str, models.Team] = {}
        for slug, name_en, name_ar, skills in TEAMS:
            existing_team = await session.scalar(
                select(models.Team).where(models.Team.org_id == org.id, models.Team.slug == slug)
            )
            if existing_team is None:
                team = models.Team(
                    org_id=org.id, slug=slug, name_en=name_en, name_ar=name_ar, skills=skills
                )
                session.add(team)
                await session.flush()
                teams[slug] = team
            else:
                teams[slug] = existing_team

        # ---- Users ----
        users: dict[str, models.User] = {}
        for email, role, name_en, name_ar in USERS:
            existing_user = await session.scalar(
                select(models.User).where(models.User.email == email)
            )
            if existing_user is None:
                user = models.User(
                    org_id=org.id,
                    email=email,
                    role=role,
                    name_en=name_en,
                    name_ar=name_ar,
                    locale_pref="ar" if "user" in email or role == "agent" else "en",
                    password_hash=make_password_hash("DemoPassword!123"),
                )
                session.add(user)
                await session.flush()
                users[email] = user
            else:
                users[email] = existing_user

        # ---- Categories ----
        categories: dict[str, models.Category] = {}
        parent_map = {
            "hardware-printer": "hardware", "hardware-laptop": "hardware",
            "hardware-desktop": "hardware", "hardware-peripheral": "hardware",
            "software-office": "software", "software-os": "software",
            "software-install": "software", "software-update": "software",
            "network-vpn": "network", "network-wifi": "network",
            "network-internet": "network", "network-firewall": "network",
            "account-password": "account", "account-mfa": "account",
            "account-access": "account", "account-create": "account",
            "email-outlook": "email", "email-spam": "email", "email-delivery": "email",
            "security-phishing": "security", "security-malware": "security",
            "security-incident": "security",
            "telephony-handset": "telephony", "telephony-conference": "telephony",
            "collab-teams": "collab", "collab-zoom": "collab",
            "collab-sharepoint": "collab",
            "erp-sap": "erp", "erp-oracle": "erp",
            "mobile-mdm": "mobile", "mobile-app": "mobile",
        }
        # First pass: parents.
        for slug, name_en, name_ar in CATEGORIES:
            if slug in parent_map:
                continue
            existing_cat = await session.scalar(
                select(models.Category).where(
                    models.Category.org_id == org.id, models.Category.slug == slug
                )
            )
            if existing_cat is None:
                cat = models.Category(org_id=org.id, slug=slug, name_en=name_en, name_ar=name_ar)
                session.add(cat)
                await session.flush()
                categories[slug] = cat
            else:
                categories[slug] = existing_cat
        # Second pass: children.
        for slug, name_en, name_ar in CATEGORIES:
            if slug not in parent_map:
                continue
            parent = categories[parent_map[slug]]
            existing_cat = await session.scalar(
                select(models.Category).where(
                    models.Category.org_id == org.id, models.Category.slug == slug
                )
            )
            if existing_cat is None:
                cat = models.Category(
                    org_id=org.id, slug=slug, name_en=name_en, name_ar=name_ar,
                    parent_id=parent.id,
                )
                session.add(cat)
                await session.flush()
                categories[slug] = cat
            else:
                categories[slug] = existing_cat

        # ---- Tickets ----
        end_users = [u for email, u in users.items() if "user" in email]
        agents = [u for email, u in users.items() if "agent" in email]
        rng = random.Random(42)
        target = 500 if demo else 50
        existing_ticket_count = await session.scalar(
            select(models.Ticket.id).limit(1)
        )
        if existing_ticket_count is None:
            for i in range(target):
                template = TICKET_SEED[i % len(TICKET_SEED)]
                title, body, lang, dialect, cat_slug = template
                requester = rng.choice(end_users)
                assignee = rng.choice(agents) if rng.random() < 0.7 else None
                category = categories.get(cat_slug)
                created = datetime.now(timezone.utc) - timedelta(days=rng.randint(0, 30))
                ticket = models.Ticket(
                    public_id=public_id(i + 1),
                    org_id=org.id,
                    requester_id=requester.id,
                    assignee_id=assignee.id if assignee else None,
                    team_id=teams[rng.choice(list(teams.keys()))].id,
                    category_id=category.id if category else None,
                    title=title,
                    description=body,
                    language_detected=lang,
                    dialect_detected=dialect,
                    status=rng.choice(["new", "open", "pending", "resolved", "closed"]),
                    priority=rng.choice(["low", "medium", "high", "urgent"]),
                    source="web",
                    created_at=created,
                )
                session.add(ticket)
                if (i + 1) % 100 == 0:
                    await session.flush()
        print("Database seeded.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Seed a richer demo dataset")
    args = parser.parse_args()
    asyncio.run(seed(demo=args.demo))


if __name__ == "__main__":
    main()
