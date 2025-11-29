import polib
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LOCALE_DIR = BASE / 'locale'

# translations mapping: language_code -> { msgid: msgstr }
TRANSLATIONS = {
    'af': {
        "Latest News": "Jongste Nuus",
        "Home": "Tuis",
        "Categories": "Kategorieë",
        "Add Post": "Voeg Pos By",
        "Login": "Aanmeld",
        "Sign up": "Teken In",
        "Logout": "Afmeld",
        "Language": "Taal",
        "By": "Deur",
        "Category": "Kategorie",
        "No articles yet.": "Nog geen artikels nie.",
        "Signed in as": "Aangemeld as",
        "News App": "Nuus Toep",
    },
    'zu': {
        "Latest News": "Izindaba Zakamuva",
        "Home": "Ikhaya",
        "Categories": "Izigaba",
        "Add Post": "Engeza Okuthunyelwe",
        "Login": "Ngena",
        "Sign up": "Bhalisa",
        "Logout": "Phuma",
        "Language": "Ulimi",
        "By": "Ngu",
        "Category": "Isigaba",
        "No articles yet.": "Azikho izindatshana okwamanje.",
        "Signed in as": "Ungenile njenge",
        "News App": "Uhlelo lwezindaba",
    },
    'xh': {
        "Latest News": "Iindaba Zakutsha",
        "Home": "Ikhaya",
        "Categories": "Izigaba",
        "Add Post": "Yongeza Iposi",
        "Login": "Ngena",
        "Sign up": "Bhalisa",
        "Logout": "Phuma",
        "Language": "Ulwimi",
        "By": "Ngu",
        "Category": "Isigaba",
        "No articles yet.": "Akukho iindaba okwethutyana.",
        "Signed in as": "Ungene njengom",
        "News App": "Isicelo seendaba",
    },
    'st': {
        "Latest News": "Ditaba Tsa Morao",
        "Home": "Lehae",
        "Categories": "Dikategori",
        "Add Post": "Eketsa Thuto",
        "Login": "Kena",
        "Sign up": "Ingwalelo",
        "Logout": "Tsamaea",
        "Language": "Puo",
        "By": "Ke",
        "Category": "Sehlopha",
        "No articles yet.": "Ha ho litaba hajoale.",
        "Signed in as": "O kene e le",
        "News App": "Kopo ea Litaba",
    },
    'tn': {
        "Latest News": "Dintlha tsa Bosigo",
        "Home": "Lehae",
        "Categories": "Mekgwa",
        "Add Post": "Oketsa Phetolelo",
        "Login": "Kena",
        "Sign up": "Ine",
        "Logout": "Tsaya",
        "Language": "Puo",
        "By": "Ka",
        "Category": "Sehlopha",
        "No articles yet.": "Ga go na diteng gape.",
        "Signed in as": "O kene jaaka",
        "News App": "App ya Ditaba",
    },
}

def update_po_for_lang(lang_code, translations):
    po_path = LOCALE_DIR / lang_code / 'LC_MESSAGES' / 'django.po'
    if not po_path.exists():
        print(f"po not found for {lang_code}: {po_path}")
        return
    po = polib.pofile(str(po_path))
    changed = 0
    for entry in po:
        if entry.msgid in translations:
            new = translations[entry.msgid]
            if entry.msgstr != new:
                entry.msgstr = new
                changed += 1
    if changed:
        po.save()
        print(f"Updated {changed} entries in {po_path}")
    else:
        print(f"No updates needed for {lang_code}")

def main():
    for lang, trans in TRANSLATIONS.items():
        update_po_for_lang(lang, trans)

if __name__ == '__main__':
    main()