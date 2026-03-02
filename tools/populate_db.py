"""
Populate sample data tailored to this project's models.

This file adapts a richer Faker-based population script to the current
`edziennik` project structure. Run from project root with:

    python tools/populate_db.py

It bootstraps Django and uses the ORM. The script is careful to set
required fields (e.g. student's birth date, teacher phone) and to use
get_or_create or bulk operations where sensible.
"""

import os
import sys
import random
import django
from faker import Faker
from datetime import date, timedelta, time
from decimal import Decimal

# Ensure project root is importable when run as a script
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Use the project's settings (force override to avoid relying on external env vars)
os.environ["DJANGO_SETTINGS_MODULE"] = "edziennik.settings"
try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    print("Ensure you run this from the project root and that Django is installed.")
    raise

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

# Project models (adapted to this repo)
from users.models import Klasa, Nauczyciel, Uczen, Adres, Rodzic
from utils.models import Przedmiot
from grades.models import Ocena, OcenaOkresowa, OcenaKoncowa, ZachowaniePunkty
from attendance.models import Frekwencja, StatusyObecnosci
from timetables.models import (
    GodzinyLekcyjne,
    Zajecia,
    DniTygodnia,
    PlanWpis,
    PlanyZajec,
    Wydarzenie,
)
from django.utils import timezone
from utils.models import Temat, PracaDomowa


fake = Faker("pl_PL")

NUM_NAUCZYCIELE = 40
MIN_UCZNIOWIE_PER_KLASA = 20
MAX_UCZNIOWIE_PER_KLASA = 30
MAX_OCENY_PER_UCZEN_PRZEDMIOT = 5
MAX_OBECNOSCI_PER_UCZEN_PER_DAY = 4
MAX_PUNKTY_ZACHOWANIA_PER_UCZEN = 8
SCHOOL_YEAR_START = date(2024, 9, 1)
SCHOOL_YEAR_END = date(2025, 5, 19)

POSSIBLE_GRADE_VALUES = [
    Decimal("1.00"),
    Decimal("1.75"),
    Decimal("2.00"),
    Decimal("2.75"),
    Decimal("3.00"),
    Decimal("3.75"),
    Decimal("4.00"),
    Decimal("4.75"),
    Decimal("5.00"),
    Decimal("5.75"),
    Decimal("6.00"),
]
WAGA_OCEN = [1, 2, 3, 4, 5]

POSITIVE_BEHAVIOR_POINTS = [1, 2, 3, 5, 10]
NEGATIVE_BEHAVIOR_POINTS = [-1, -2, -3, -5, -10, -15]

POSITIVE_BEHAVIOR_DESCRIPTIONS = [
    "Pomoc koleżance/koledze w nauce",
    "Aktywny udział w zajęciach",
    "Wzorowe zachowanie podczas lekcji",
    "Pomoc nauczycielowi",
    "Inicjatywa w działaniach klasowych",
]

NEGATIVE_BEHAVIOR_DESCRIPTIONS = [
    "Zakłócanie porządku na lekcji",
    "Nieodpowiednie zachowanie wobec nauczyciela",
    "Brak szacunku dla kolegów",
    "Niewłaściwe korzystanie z telefonu",
]

# Pre-hash a common password once to avoid repeated expensive PBKDF2 hashing during bulk creation
from django.contrib.auth.hashers import make_password

HASHED_PASSWORD = make_password("password123")


def normalize_phone(raw_phone: str) -> str:
    """Return phone with digits only and Polish country code (48) prefix if missing.
    Removes spaces, parentheses, plus signs, dashes, etc.
    Examples: '+48 123 456 789' -> '48123456789'
    """
    if not raw_phone:
        # fallback to a fake local number
        raw_phone = fake.phone_number()
    digits = "".join(ch for ch in raw_phone if ch.isdigit())
    if not digits:
        digits = "".join(str(fake.random_int(min=0, max=9)) for _ in range(9))
    # if it doesn't start with country code 48, add it
    if not digits.startswith("48"):
        digits = "48" + digits
    return digits


def create_unique_user(username_prefix="user"):
    first_name = fake.first_name()
    last_name = fake.last_name()
    # username should consist only of first and last name per request
    base_username = f"{first_name.lower()}_{last_name.lower()}"
    username = base_username
    # ensure uniqueness by appending a small numeric suffix if needed
    counter = 1
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{base_username}{counter}"
    # keep email unique to avoid collisions
    unique_suffix = fake.unique.uuid4()[:6]
    email = f"{first_name.lower()}.{last_name.lower()}.{unique_suffix}@example.com"
    # we use a pre-hashed password to avoid repeated PBKDF2 work
    password = HASHED_PASSWORD

    # we already ensured username uniqueness above; ensure email uniqueness as a fallback
    if User.objects.filter(email=email).exists():
        email = f"{first_name.lower()}.{last_name.lower()}.{fake.unique.uuid4()[:6]}@example.com"

    try:
        # create user with already-hashed password (faster for fixtures)
        user = User.objects.create(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = True
        user.save()
        return user
    except Exception as e:
        print(f"Error creating user {username}: {e}")
        return None


@transaction.atomic
def populate_klasy():
    print("Populating Klasy...")
    roczniki = ["1", "2", "3", "4", "5"]
    litery_klas = ["aT", "bT", "cT", "aL", "bL"]
    litery_klas_dla_rocznika_5_zabronione = ["aL", "bL"]
    created = []
    for rocznik in roczniki:
        for litera in litery_klas:
            if rocznik == "5" and litera in litery_klas_dla_rocznika_5_zabronione:
                continue
            # per request: Klasa.nazwa should be the letter(s) only and numer the year
            nazwa_litera = litera
            numer_val = int(rocznik)
            klasa, _ = Klasa.objects.get_or_create(nazwa=nazwa_litera, numer=numer_val)
            created.append(klasa)
    print(f"  Created/ensured {len(created)} klasy")
    return Klasa.objects.filter(nazwa__in=[k.nazwa for k in created])


@transaction.atomic
def populate_przedmioty():
    print("Populating Przedmioty...")
    przedmioty_data = [
        "Trening Mentalny",
        "WF",
        "Język Angielski",
        "Biznes i Zarządzanie",
        "Matematyka",
        "Fizyka",
        "Informatyka",
        "Biologia",
        "Historia",
        "Grafika Komputerowa (Specjalizacja)",
        "Język Polski",
        "Język Hiszpański",
        "Chemia",
        "Geografia",
        "Religia",
        "IT (Specjalizacja)",
    ]
    created = []
    for nazwa in przedmioty_data:
        # sanitize name: remove "(Specjalizacja)" and surrounding whitespace
        clean_nazwa = nazwa.replace("(Specjalizacja)", "").strip()
        # create a short name per request:
        # - single-word names: use 3 or 4 first letters
        # - two-word names: first letter of first word + first three letters of second word
        parts = clean_nazwa.split()
        if len(parts) == 0:
            skrot = clean_nazwa[:50]
        elif len(parts) == 1:
            take = random.choice([3, 4])
            skrot = parts[0][:take]
        else:
            # make sure second part has at least 3 letters
            second_part = parts[1]
            skrot = parts[0][0] + second_part[:3]
        skrot = skrot[:50]
        # decide if this is an additional subject randomly for variety
        dodatkowy = random.random() < 0.12
        # assign a sequential number if not present (use current count + 1)
        current_count = Przedmiot.objects.count()
        numer_val = current_count + len(created) + 1

        p, created_flag = Przedmiot.objects.get_or_create(
            nazwa=clean_nazwa,
            defaults={
                "nazwa_skrocona": skrot,
                "numer": numer_val,
                "czy_dodatkowy": dodatkowy,
            },
        )
        # if existed but fields are empty, update them so we don't leave blanks
        changed = False
        if not p.nazwa_skrocona:
            p.nazwa_skrocona = skrot
            changed = True
        if p.numer is None:
            p.numer = numer_val
            changed = True
        if p.czy_dodatkowy is None:
            p.czy_dodatkowy = dodatkowy
            changed = True
        if changed:
            p.save()
        created.append(p)
    print(f"  Created/ensured {len(created)} przedmioty")
    return Przedmiot.objects.filter(nazwa__in=przedmioty_data)


@transaction.atomic
def populate_nauczyciele(przedmioty, klasy):
    print("Populating Nauczyciele...")
    nauczyciele_instances = []
    for i in range(NUM_NAUCZYCIELE):
        user = create_unique_user(username_prefix="teacher")
        if not user:
            continue
        telefon = normalize_phone(fake.phone_number())
        nauczyciele_instances.append(Nauczyciel(user=user, telefon=telefon))

    if nauczyciele_instances:
        created_nauczyciele = Nauczyciel.objects.bulk_create(nauczyciele_instances)
        print(f"  Bulk created {len(nauczyciele_instances)} nauczyciele")

        # Update user_ids manually because bulk_create doesn't trigger signals
        users_to_update = []
        for n in created_nauczyciele:
            n.user.user_id = n.id
            users_to_update.append(n.user)
        User.objects.bulk_update(users_to_update, ["user_id"])

    # assign subjects to some teachers (M2M exists on Przedmiot.nauczyciele)
    nauczyciele_qs = Nauczyciel.objects.all()
    przedmioty_list = list(przedmioty)
    for nauczyciel in nauczyciele_qs:
        if przedmioty_list:
            sample = random.sample(przedmioty_list, k=min(3, len(przedmioty_list)))
            for p in sample:
                p.nauczyciele.add(nauczyciel)

    # Ensure each Przedmiot has at least one assigned Nauczyciel (do not leave M2M empty)
    all_przedmioty = Przedmiot.objects.all()
    nauczyciele_list = list(nauczyciele_qs)
    for p in all_przedmioty:
        if p.nauczyciele.count() == 0 and nauczyciele_list:
            p.nauczyciele.add(random.choice(nauczyciele_list))

    # assign wychowawcy for classes
    nauczyciele_list = list(nauczyciele_qs)
    random.shuffle(nauczyciele_list)
    klasy_list = list(klasy)
    for i, kl in enumerate(klasy_list):
        if i < len(nauczyciele_list):
            kl.wychowawca = nauczyciele_list[i]
            kl.save()

    return Nauczyciel.objects.all()


@transaction.atomic
def populate_uczniowie(klasy):
    print("Populating Uczniowie...")
    uczniowie_instances = []
    for kl in klasy:
        n = random.randint(MIN_UCZNIOWIE_PER_KLASA, MAX_UCZNIOWIE_PER_KLASA)
        for _ in range(n):
            user = create_unique_user(username_prefix=f"student_{kl.nazwa}")
            if not user:
                continue
            birth = fake.date_of_birth(minimum_age=14, maximum_age=19)
            # create an address record so Uczen.adres is not empty
            adres = Adres.objects.create(
                ulica=fake.street_name(),
                numer_domu=str(fake.random_int(min=1, max=200)),
                numer_mieszkania=str(fake.random_int(min=1, max=200)),
                miasto=fake.city(),
                kod_pocztowy=fake.postcode(),
                kraj=fake.country(),
            )
            telefon_uczen = normalize_phone(fake.phone_number())
            uczniowie_instances.append(
                Uczen(
                    user=user,
                    klasa=kl,
                    telefon=telefon_uczen,
                    data_urodzenia=birth,
                    adres=adres,
                )
            )

    if uczniowie_instances:
        created_uczniowie = Uczen.objects.bulk_create(uczniowie_instances)
        print(f"  Bulk created {len(uczniowie_instances)} uczniowie")

        # Update user_ids manually because bulk_create doesn't trigger signals
        users_to_update = []
        for u in created_uczniowie:
            u.user.user_id = u.id
            users_to_update.append(u.user)
        User.objects.bulk_update(users_to_update, ["user_id"])

    return Uczen.objects.all()


@transaction.atomic
def populate_oceny_i_obecnosci(uczniowie_qs, nauczyciele_qs, przedmioty_qs):
    print("Populating Oceny and Frekwencja...")
    if not (
        uczniowie_qs.exists() and nauczyciele_qs.exists() and przedmioty_qs.exists()
    ):
        print("  Missing prerequisites for grades/attendance")
        return

    oceny_to_create = []
    obecnosci_to_create = []

    status_objs = list(StatusyObecnosci.objects.all())
    if not status_objs:
        for v in ["Obecny", "Nieobecny", "Spóźniony", "Usprawiedliwiony"]:
            StatusyObecnosci.objects.create(Wartosc=v)
        status_objs = list(StatusyObecnosci.objects.all())

    # Ensure there are lesson hours so Frekwencja.godzina_lekcyjna is not left empty
    if GodzinyLekcyjne.objects.count() == 0:
        default_hours = [
            (1, time(8, 0), time(8, 45), 45),
            (2, time(9, 0), time(9, 45), 45),
            (3, time(10, 0), time(10, 45), 45),
            (4, time(11, 0), time(11, 45), 45),
            (5, time(12, 0), time(12, 45), 45),
        ]
        for num, od, do, tr in default_hours:
            GodzinyLekcyjne.objects.create(
                Numer=num, CzasOd=od, CzasDo=do, CzasTrwania=tr
            )
    godziny_list = list(GodzinyLekcyjne.objects.all())

    num_school_days = (SCHOOL_YEAR_END - SCHOOL_YEAR_START).days

    # build a mapping przedmiot.pk -> list of nauczyciel pks (do this once to avoid repeated DB queries)
    przedmiot_nauczyciele_map = {}
    for p in przedmioty_qs.iterator():
        przedmiot_nauczyciele_map[p.pk] = list(
            p.nauczyciele.values_list("pk", flat=True)
        )

    for uczen in uczniowie_qs.iterator():
        for przedmiot in przedmioty_qs.iterator():
            # find precomputed nauczyciel pks for this przedmiot
            pks = przedmiot_nauczyciele_map.get(przedmiot.pk, [])
            if not pks:
                # no teacher for this subject; skip creating grades for it
                continue
            chosen_pk = random.choice(pks)
            nauczyciel_pk = chosen_pk

            for _ in range(random.randint(0, MAX_OCENY_PER_UCZEN_PRZEDMIOT)):
                oc = Ocena(
                    uczen_id=uczen.pk,
                    przedmiot_id=przedmiot.pk,
                    nauczyciel_id=nauczyciel_pk,
                    wartosc=random.choice(POSSIBLE_GRADE_VALUES),
                    waga=random.choice(WAGA_OCEN),
                    opis=(fake.sentence(nb_words=5) if random.random() < 0.6 else ""),
                    czy_punkty=random.choice([True, False]),
                    czy_opisowa=random.choice([True, False]),
                    czy_do_sredniej=random.choice([True, False]),
                )
                oceny_to_create.append(oc)

        # attendance
        for _ in range((num_school_days // 30)):
            day = SCHOOL_YEAR_START + timedelta(days=random.randint(0, num_school_days))
            if day.weekday() >= 5:
                continue
            for _ in range(random.randint(1, MAX_OBECNOSCI_PER_UCZEN_PER_DAY)):
                status = random.choice(status_objs) if status_objs else None
                gl = random.choice(godziny_list) if godziny_list else None
                frek = Frekwencja(
                    Data=day,
                    uczen_id=uczen.pk,
                    godzina_lekcyjna_id=(gl.pk if gl is not None else None),
                    status_id=(status.pk if status is not None else None),
                )
                obecnosci_to_create.append(frek)

    if oceny_to_create:
        Ocena.objects.bulk_create(oceny_to_create, batch_size=500)
        print(f"  Created {len(oceny_to_create)} oceny")

    # Create some OcenaOkresowa and OcenaKoncowa entries
    oceny_okresowe_to_create = []
    oceny_koncowe_to_create = []
    # For each student create a few period/final grades for a random subset of subjects
    for uczen in uczniowie_qs.iterator():
        sampled_przedmioty = random.sample(
            list(przedmioty_qs), k=min(3, max(1, len(list(przedmioty_qs))))
        )
        for przedmiot in sampled_przedmioty:
            # pick a teacher for this subject if available
            nauczyciele_for_subject = nauczyciele_qs.filter(przedmioty=przedmiot)
            nauczyciel = None
            if nauczyciele_for_subject.exists():
                pks = list(nauczyciele_for_subject.values_list("pk", flat=True))
                if pks:
                    chosen_pk = random.choice(pks)
                    nauczyciel = nauczyciele_for_subject.filter(pk=chosen_pk).first()

            # oceny okresowe: create 0-2 per subject (okres 1 or 2)
            for _ in range(random.randint(0, 2)):
                oc_ok = OcenaOkresowa(
                    uczen=uczen,
                    wartosc=random.choice(POSSIBLE_GRADE_VALUES),
                    okres=random.randint(1, 2),
                    przedmiot=przedmiot,
                    nauczyciel=nauczyciel,
                )
                oceny_okresowe_to_create.append(oc_ok)

            # ocena koncowa: create with some probability
            if random.random() < 0.4:
                oc_k = OcenaKoncowa(
                    uczen=uczen,
                    wartosc=random.choice(POSSIBLE_GRADE_VALUES),
                    przedmiot=przedmiot,
                    nauczyciel=nauczyciel,
                )
                oceny_koncowe_to_create.append(oc_k)

    if oceny_okresowe_to_create:
        OcenaOkresowa.objects.bulk_create(oceny_okresowe_to_create, batch_size=500)
        print(f"  Created {len(oceny_okresowe_to_create)} oceny okresowe")
    if oceny_koncowe_to_create:
        OcenaKoncowa.objects.bulk_create(oceny_koncowe_to_create, batch_size=500)
        print(f"  Created {len(oceny_koncowe_to_create)} oceny koncowe")

    if obecnosci_to_create:
        Frekwencja.objects.bulk_create(obecnosci_to_create, batch_size=500)
        print(f"  Created {len(obecnosci_to_create)} frekwencja records")


@transaction.atomic
def populate_punkty_zachowania(uczniowie_qs, nauczyciele_qs):
    print("Populating Punkty Zachowania...")
    if not (uczniowie_qs.exists() and nauczyciele_qs.exists()):
        print("  Missing prerequisites for behavior points")
        return

    to_create = []
    nauczyciele_list = list(nauczyciele_qs.values_list("pk", flat=True))
    for uczen in uczniowie_qs.iterator():
        for _ in range(random.randint(1, MAX_PUNKTY_ZACHOWANIA_PER_UCZEN)):
            if random.random() < 0.7:
                punkty = random.choice(POSITIVE_BEHAVIOR_POINTS)
                opis = random.choice(POSITIVE_BEHAVIOR_DESCRIPTIONS)
            else:
                punkty = random.choice(NEGATIVE_BEHAVIOR_POINTS)
                opis = random.choice(NEGATIVE_BEHAVIOR_DESCRIPTIONS)
            nauczyciel_pk = (
                random.choice(nauczyciele_list) if nauczyciele_list else None
            )
            zp = ZachowaniePunkty(
                uczen_id=uczen.pk,
                punkty=punkty,
                opis=opis,
                nauczyciel_wpisujacy_id=nauczyciel_pk,
            )
            to_create.append(zp)

    if to_create:
        ZachowaniePunkty.objects.bulk_create(to_create, batch_size=500)
        print(f"  Created {len(to_create)} zachowanie punkty")


@transaction.atomic
def ensure_godziny_i_dni():
    print("Ensuring GodzinyLekcyjne and DniTygodnia...")
    created_hours = 0
    if GodzinyLekcyjne.objects.count() == 0:
        default_hours = [
            (1, time(8, 0), time(8, 45), 45),
            (2, time(9, 0), time(9, 45), 45),
            (3, time(10, 0), time(10, 45), 45),
            (4, time(11, 0), time(11, 45), 45),
            (5, time(12, 0), time(12, 45), 45),
            (6, time(13, 0), time(13, 45), 45),
        ]
        for num, od, do, tr in default_hours:
            GodzinyLekcyjne.objects.create(
                Numer=num, CzasOd=od, CzasDo=do, CzasTrwania=tr
            )
            created_hours += 1
    if DniTygodnia.objects.count() == 0:
        days = [
            ("Poniedziałek", 1),
            ("Wtorek", 2),
            ("Środa", 3),
            ("Czwartek", 4),
            ("Piątek", 5),
        ]
        for name, num in days:
            DniTygodnia.objects.create(Nazwa=name, Numer=num)
    print(
        f"  Ensured GodzinyLekcyjne ({GodzinyLekcyjne.objects.count()}) and DniTygodnia ({DniTygodnia.objects.count()})"
    )


@transaction.atomic
def create_zajecia_and_plans():
    print("Populating Zajecia and Plany Zajec...")
    przedmioty = list(Przedmiot.objects.all())
    nauczyciele = list(Nauczyciel.objects.all())
    klasy = list(Klasa.objects.all())
    godziny = list(GodzinyLekcyjne.objects.all())
    dni = list(DniTygodnia.objects.all())

    if not przedmioty or not nauczyciele or not klasy or not godziny or not dni:
        print(
            "  Missing prerequisites (przedmioty/nauczyciele/klasy/godziny/dni). Skipping plans/zajecia."
        )
        return

    zajecia_instances = []
    for p in przedmioty:
        possible = list(p.nauczyciele.all())
        teacher = random.choice(possible) if possible else random.choice(nauczyciele)
        z, _ = Zajecia.objects.get_or_create(przedmiot=p, nauczyciel=teacher)
        zajecia_instances.append(z)

    for kl in klasy:
        plan_start = date.today() - timedelta(days=random.randint(0, 30))
        plan, _ = PlanyZajec.objects.get_or_create(
            klasa=kl, ObowiazujeOdDnia=plan_start
        )
        num_wpisow = random.randint(10, 25)
        for _ in range(num_wpisow):
            godz = random.choice(godziny)
            dzien = random.choice(dni)
            zaj = random.choice(zajecia_instances)
            wpis = PlanWpis.objects.create(
                godzina_lekcyjna=godz, dzien_tygodnia=dzien, zajecia=zaj
            )
            plan.wpisy.add(wpis)
    print(
        f"  Created/ensured {len(zajecia_instances)} Zajecia and plany for {len(klasy)} klas"
    )


@transaction.atomic
def create_wydarzenia_tematy_prace():
    print("Populating Wydarzenia, Tematy, and Prace Domowe...")
    klasy = list(Klasa.objects.all())
    przedmioty = list(Przedmiot.objects.all())
    nauczyciele = list(Nauczyciel.objects.all())

    if not klasy or not przedmioty or not nauczyciele:
        print("  Missing prerequisites for events/tematy/prace domowe. Skipping.")
        return

    wydarzenia_created = 0
    for _ in range(len(klasy) * 3):
        kl = random.choice(klasy)
        pr = random.choice(przedmioty)
        nauc = random.choice(nauczyciele)
        t = fake.catch_phrase()
        opis = fake.paragraph(nb_sentences=2)
        data = timezone.now() + timedelta(days=random.randint(-10, 30))
        Wydarzenie.objects.create(
            tytul=t, opis=opis, data=data, klasa=kl, przedmiot=pr, nauczyciel=nauc
        )
        wydarzenia_created += 1

    tematy_created = 0
    for pr in przedmioty:
        for _ in range(random.randint(1, 3)):
            tresc = fake.sentence(nb_words=6)
            data = date.today() - timedelta(days=random.randint(0, 60))
            numer_lekcji = random.randint(1, 6)
            czas_realizacji = random.choice([30, 45, 60])
            czas_od = time(hour=random.randint(8, 14), minute=0)
            czas_do = (
                timezone.datetime.combine(date.today(), czas_od)
                + timedelta(minutes=czas_realizacji)
            ).time()
            nauc = random.choice(nauczyciele)
            Temat.objects.create(
                tresc=tresc,
                data=data,
                numer_lekcji=numer_lekcji,
                czas_realizacji=czas_realizacji,
                czas_od=czas_od,
                czas_do=czas_do,
                przedmiot=pr,
                nauczyciel=nauc,
            )
            tematy_created += 1

    prace_created = 0
    klasy_cycle = list(klasy)
    for pr in przedmioty:
        for kl in random.sample(klasy_cycle, k=min(3, len(klasy_cycle))):
            nauc = random.choice(nauczyciele)
            opis = fake.paragraph(nb_sentences=2)
            termin = date.today() + timedelta(days=random.randint(1, 30))
            PracaDomowa.objects.create(
                klasa=kl, przedmiot=pr, nauczyciel=nauc, opis=opis, termin=termin
            )
            prace_created += 1

    print(
        f"  Created {wydarzenia_created} wydarzenia, {tematy_created} tematy, {prace_created} prace domowe"
    )


@transaction.atomic
def create_rodzice_for_uczniowie(sample_fraction=0.15):
    print("Populating Rodzice (parents)...")
    uczniowie = list(Uczen.objects.all())
    if not uczniowie:
        print("  No uczniowie found. Skipping rodzice.")
        return

    rodzice_created = 0
    for uc in random.sample(uczniowie, k=max(1, int(len(uczniowie) * sample_fraction))):
        first = fake.first_name()
        last = fake.last_name()
        base_username = f"{first.lower()}_{last.lower()}"
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base_username}{counter}"
        email = f"{first.lower()}.{last.lower()}.{fake.unique.uuid4()[:6]}@example.com"
        user = User.objects.create(
            username=username,
            email=email,
            password=HASHED_PASSWORD,
            first_name=first,
            last_name=last,
        )
        user.is_active = True
        user.save()
        rodzic = Rodzic.objects.create(
            user=user, telefon=normalize_phone(fake.phone_number())
        )
        rodzic.dzieci.add(uc)
        rodzice_created += 1

    print(f"  Created {rodzice_created} rodzice and linked them to uczniowie")


if __name__ == "__main__":
    print("Starting data population process...")

    # Clear some data safely (be conservative in production)
    Ocena.objects.all().delete()
    Frekwencja.objects.all().delete()
    ZachowaniePunkty.objects.all().delete()
    Uczen.objects.all().delete()
    Nauczyciel.objects.all().delete()
    # Remove non-superuser accounts created by prior runs
    User.objects.filter(is_superuser=False).delete()
    Przedmiot.objects.all().delete()
    Klasa.objects.all().delete()

    klasy = populate_klasy()
    przedmioty = populate_przedmioty()
    nauczyciele = populate_nauczyciele(przedmioty, klasy)
    uczniowie = populate_uczniowie(klasy)

    if uczniowie.exists() and nauczyciele.exists() and przedmioty.exists():
        populate_oceny_i_obecnosci(uczniowie, nauczyciele, przedmioty)
        populate_punkty_zachowania(uczniowie, nauczyciele)
    else:
        print("Skipping grades/attendance/behavior population due to missing data")
    # Extra population: schedules, plans, events, topics, homework, parents
    ensure_godziny_i_dni()
    create_zajecia_and_plans()
    create_wydarzenia_tematy_prace()
    create_rodzice_for_uczniowie()

    print("Data population process finished.")
