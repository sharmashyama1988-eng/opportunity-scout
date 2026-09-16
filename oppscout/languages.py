"""Multilingual Support & Universal Language Registry for Opportunity Scout.
Supports every language in the world, with instant selection for top global & Indian languages,
and freeform text input for any other global language or dialect.
"""

from typing import Dict, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

# Top quick-select languages: code -> (English Name, Native/Display Name, ISO lang code)
POPULAR_LANGUAGES: Dict[str, Tuple[str, str, str]] = {
    "1": ("English", "English (Global / International Business)", "en"),
    "2": ("Hinglish", "Hinglish (Hindi + English - Practical & Fast)", "hi-Latn"),
    "3": ("Hindi", "हिन्दी (Hindi - शुद्ध व व्यावहारिक)", "hi"),
    "4": ("Spanish", "Español (Spanish)", "es"),
    "5": ("French", "Français (French)", "fr"),
    "6": ("German", "Deutsch (German)", "de"),
    "7": ("Japanese", "日本語 (Japanese)", "ja"),
    "8": ("Mandarin", "中文 (Mandarin / Chinese)", "zh"),
    "9": ("Arabic", "العربية (Arabic)", "ar"),
    "10": ("Portuguese", "Português (Portuguese)", "pt"),
    "11": ("Bengali", "বাংলা (Bengali)", "bn"),
    "12": ("Tamil", "தமிழ் (Tamil)", "ta"),
    "13": ("Telugu", "తెలుగు (Telugu)", "te"),
    "14": ("Marathi", "मराठी (Marathi)", "mr"),
    "15": ("Gujarati", "ગુજરાતી (Gujarati)", "gu"),
    "16": ("Russian", "Русский (Russian)", "ru"),
    "17": ("Italian", "Italiano (Italian)", "it"),
    "18": ("Korean", "한국어 (Korean)", "ko"),
    "19": ("Turkish", "Türkçe (Turkish)", "tr"),
    "20": ("Urdu", "اردو (Urdu)", "ur"),
    "21": ("Punjabi", "ਪੰਜਾਬੀ (Punjabi)", "pa"),
}

# Aliases for fast smart matching
LANGUAGE_ALIASES = {
    "en": "English", "english": "English",
    "hinglish": "Hinglish", "roman hindi": "Hinglish", "hing": "Hinglish",
    "hi": "Hindi", "hindi": "Hindi", "हिन्दी": "Hindi", "हिंदी": "Hindi",
    "es": "Spanish", "spanish": "Spanish", "español": "Spanish", "espanol": "Spanish",
    "fr": "French", "french": "French", "français": "French", "francais": "French",
    "de": "German", "german": "German", "deutsch": "German",
    "ja": "Japanese", "japanese": "Japanese", "日本語": "Japanese", "nihongo": "Japanese",
    "zh": "Mandarin", "chinese": "Mandarin", "mandarin": "Mandarin", "中文": "Mandarin",
    "ar": "Arabic", "arabic": "Arabic", "العربية": "Arabic",
    "pt": "Portuguese", "portuguese": "Portuguese", "português": "Portuguese",
    "bn": "Bengali", "bengali": "Bengali", "বাংলা": "Bengali", "bangla": "Bengali",
    "ta": "Tamil", "tamil": "Tamil", "தமிழ்": "Tamil",
    "te": "Telugu", "telugu": "Telugu", "తెలుగు": "Telugu",
    "mr": "Marathi", "marathi": "Marathi", "मराठी": "Marathi",
    "gu": "Gujarati", "gujarati": "Gujarati", "ગુજરાતી": "Gujarati",
    "ru": "Russian", "russian": "Russian", "русский": "Russian",
    "it": "Italian", "italian": "Italian", "italiano": "Italian",
    "ko": "Korean", "korean": "Korean", "한국어": "Korean",
    "tr": "Turkish", "turkish": "Turkish", "türkçe": "Turkish",
    "ur": "Urdu", "urdu": "Urdu", "اردو": "Urdu",
    "pa": "Punjabi", "punjabi": "Punjabi", "ਪੰਜਾਬੀ": "Punjabi",
}


def normalize_language_choice(user_input: str) -> Tuple[str, str]:
    """Normalizes any user input (digit, alias, or custom language name)
    into a clean (Language Name, ISO Code).
    """
    clean_val = user_input.strip()
    if not clean_val:
        return "English", "en"

    # 1. Number lookup
    if clean_val in POPULAR_LANGUAGES:
        name, _, iso = POPULAR_LANGUAGES[clean_val]
        return name, iso

    # 2. Alias lookup
    lower_val = clean_val.lower()
    if lower_val in LANGUAGE_ALIASES:
        resolved_name = LANGUAGE_ALIASES[lower_val]
        for num, (name, _, iso) in POPULAR_LANGUAGES.items():
            if name.lower() == resolved_name.lower():
                return resolved_name, iso
        return resolved_name, "en"

    # 3. Custom language input (Any world language e.g. Vietnamese, Swahili, Polish, Dutch)
    custom_name = clean_val.capitalize()
    return custom_name, "en"


def prompt_user_language() -> Tuple[str, str]:
    """Displays an elegant, comprehensive language selection panel and prompts the user FIRST.
    Allows choosing popular languages by number, or typing ANY language in the world.
    """
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
        expand=True,
    )
    table.add_column("Col1", style="cyan")
    table.add_column("Col2", style="cyan")
    table.add_column("Col3", style="cyan")

    items = list(POPULAR_LANGUAGES.items())
    col_size = 7
    for i in range(col_size):
        row = []
        for c in range(3):
            idx = c * col_size + i
            if idx < len(items):
                key, (name, display, _) = items[idx]
                row.append(f"[bold yellow][{key}][/bold yellow] {display}")
            else:
                row.append("")
        table.add_row(*row)

    console.print()
    console.print(
        Panel(
            table,
            title="[bold gold1]🌐 STEP 1: CHOOSE YOUR PREFERRED LANGUAGE / अपनी भाषा चुनें[/bold gold1]",
            subtitle="[dim]All outputs (Dossiers 1, 2, 3, HTML Report, Mom Test scripts & Coaching) will be produced in this language[/dim]",
            border_style="gold1",
        )
    )
    console.print("[dim]💡 Tip: Enter a number [1-21], or type ANY language name in the world (e.g. 'Spanish', 'Hindi', 'Hinglish', 'Marathi', 'Russian', 'Dutch', etc.)[/dim]")

    raw_choice = Prompt.ask(
        "[bold gold1]Select Language / भाषा चुनें (Press Enter for English)[/bold gold1]",
        default="1"
    )

    lang_name, lang_code = normalize_language_choice(raw_choice)
    console.print(f"[bold green]✔ Preferred Language Locked:[/bold green] [bold white]{lang_name}[/bold white] [dim]({lang_code})[/dim]\n")
    return lang_name, lang_code


# Localized section labels and templates for multilingual dossier generation
LOCALIZED_HEADERS: Dict[str, Dict[str, str]] = {
    "English": {
        "problem_title": "The Real-World Bleeding Neck Problem",
        "customer_title": "Target Customer & Who Pays",
        "workarounds_title": "Current Broken / Clumsy Workarounds",
        "unfair_edge_title": "Founder's Unfair Advantage (Founder-Problem Fit)",
        "mom_test_title": "The Mom Test Customer Interview Script (Opening Question)",
        "validation_title": "48-Hour Day-1 to Day-3 Validation Blueprint (No Heavy Code)",
        "tech_blueprint_title": "High-Ticket Tech Architecture & Anti-Freelancing Blueprint",
        "monetization_title": "Pricing & Monetization Model",
        "earning_title": "Monthly Recurring Earning Potential",
        "mom_test_intro": "When visiting customer offices or industrial yards, do not act like a salesman. Speak as an operational researcher:",
        "mom_test_question": 'Sir, I am conducting operational research with {target} in {location}. In the past 30 days, where did the biggest paperwork delay or unexpected cash loss occur?',
        "objection_intro": "When the customer says: 'Everything is running fine, we have no problems.'",
        "objection_counter": "Sir, certainly operations run, but in the last 30 days did an unverified fuel slip or client payment dispute freeze ₹25,000+? Can I just review your last 5 manual logs? If all is clean, I leave immediately at no charge. If discrepancies are caught, all recovered money is 100% yours!",
        "validation_day1": "DIRECT ACTION: Visit your network connection '{advantage}'. Inspect real paperwork.",
        "validation_day2": "CONCIERGE PROOF: Manually catch ₹5,000 - ₹15,000 in leakage right in front of the owner.",
        "validation_day3": "CLOSE PILOT: Secure a paid pilot before writing any production backend software.",
    },
    "Hinglish": {
        "problem_title": "Asli Dard (The Real-World Bleeding Neck Pain)",
        "customer_title": "Target Customer (Kaun Pareshan Hai Aur Paisa Dega)",
        "workarounds_title": "Current Jugad & Clumsy Workarounds (WhatsApp + Excel Hell)",
        "unfair_edge_title": "Founder Ka Proprietary Edge (Founder-Problem Fit)",
        "mom_test_title": "The Mom Test Customer Interview Script (Pehla Sawal)",
        "validation_title": "48 Ghante Ka Day-1 to Day-3 Validation Blueprint (Bina Heavy Code Ke)",
        "tech_blueprint_title": "High-Ticket B2B Tech Architecture & Anti-Freelancing Blueprint",
        "monetization_title": "Pricing & Monetization Model",
        "earning_title": "Monthly Recurring Earning Potential",
        "mom_test_intro": "Jab customer ke office ya factory/yard mein jayein, SALESMAN mat baniye. Ek operational researcher ki tarah baat kijiye:",
        "mom_test_question": 'Sir, main {location} ke {target} ke saath operational research kar raha hoon. Pichle 30 dino mein sabse bada paperwork delay ya cashflow loss kahan hua tha?',
        "objection_intro": "Jab customer bole: 'Hamara kaam toh sab sahi chal raha hai, koi dikkat nahi hai.'",
        "objection_counter": "Sir, bilkul chal raha hoga, par kya pichle 30 dino mein kisi driver ke slip mein duplicate diesel bill, ya client payment dispute mein ₹25,000+ atka hai? Kya main bas aapke 5 purane record dekh sakta hoon? Agar sab sahi nikla toh main bina ek rupaye liye chala jaunga, aur agar koi gadbad pakdi gayi toh saara bacha hua paisa aapka!",
        "validation_day1": "DIRECT ACTION: Apne network connection '{advantage}' ke paas jayein aur real slips/registers inspect karein.",
        "validation_day2": "CONCIERGE PROOF: Owner ke samne live ₹5,000 - ₹15,000 ki leak ya saved hours pakad ke dikhayein.",
        "validation_day3": "CLOSE PILOT: Bina heavy software banaye first 10 accounts ke sath advance paid pilot sign karein.",
    },
    "Hindi": {
        "problem_title": "वास्तविक जमीनी समस्या (गंभीर परिचालन नुकसान)",
        "customer_title": "लक्षित ग्राहक (जो भुगतान करने के लिए तत्पर हैं)",
        "workarounds_title": "वर्तमान अस्थायी जुगाड़ (कागजी रजिस्टर व एक्सेल की समस्या)",
        "unfair_edge_title": "संस्थापक की व्यक्तिगत बढ़त और नेटवर्क लाभ",
        "mom_test_title": "द मॉम टेस्ट: ग्राहक साक्षात्कार संवाद (शुरुआती सवाल)",
        "validation_title": "48 घंटे का सत्यापन ब्लूप्रिंट (बिना जटिल कोडिंग के)",
        "tech_blueprint_title": "उच्च-मूल्य बी2बी तकनीकी आर्किटेक्चर (नो-फ्रीलांसिंग)",
        "monetization_title": "मूल्य निर्धारण एवं मुद्रीकरण मॉडल",
        "earning_title": "मासिक अनुमानित आय क्षमता",
        "mom_test_intro": "ग्राहक के कार्यालय या कार्यस्थल पर जाते समय सेल्समैन न बनें। एक निष्पक्ष शोधकर्ता की तरह बात करें:",
        "mom_test_question": 'नमस्ते सर, मैं {location} के {target} के साथ परिचालन प्रक्रियाओं पर अध्ययन कर रहा हूँ। पिछले 30 दिनों में कागजी कार्रवाई या चालान में सबसे बड़ा अप्रत्याशित वित्तीय नुकसान कहाँ हुआ?',
        "objection_intro": "जब ग्राहक कहे: 'हमारा सब कुछ सुचारू रूप से चल रहा है, कोई समस्या नहीं है।'",
        "objection_counter": "सर, निश्चय ही सब ठीक चल रहा होगा, लेकिन क्या पिछले महीने ईंधन बिलों या चालान में ₹25,000+ का कोई विवाद फंसा? क्या मैं आपके पिछले 5 रिकॉर्ड्स की निःशुल्क जांच कर सकता हूँ? यदि सब सही रहा तो कोई शुल्क नहीं, और यदि कोई लीकेज पकड़ी गई तो वह पूरी बचत आपकी होगी!",
        "validation_day1": "प्रत्यक्ष कदम: अपने संपर्क सूत्र '{advantage}' से सीधे मिलें और वास्तविक रजिस्टर जांचें।",
        "validation_day2": "प्रायोगिक प्रमाण: मालिक के सामने सीधे ₹5,000 - ₹15,000 की विसंगति या समय की बचत दिखाएं।",
        "validation_day3": "पायलट अनुबंध: कोई बड़ा सॉफ्टवेयर लिखने से पहले ही सशुल्क पायलट एग्रीमेंट हासिल करें।",
    },
    "Spanish": {
        "problem_title": "El Problema Real y Crítico (Fuga Operativa de Capital)",
        "customer_title": "Cliente Objetivo y Quién Paga",
        "workarounds_title": "Soluciones Temporales Precarias (Excel y WhatsApp)",
        "unfair_edge_title": "Ventaja Competitiva del Fundador (Ajuste Fundador-Problema)",
        "mom_test_title": "Guión de Entrevista The Mom Test (Pregunta de Apertura)",
        "validation_title": "Plan de Validación en 48 Horas (Sin Desarrollar Código Pesado)",
        "tech_blueprint_title": "Arquitectura Tecnológica B2B de Alto Valor (Anti-Freelance)",
        "monetization_title": "Modelo de Precios y Monetización",
        "earning_title": "Potencial de Ingresos Mensuales Recurrentes",
        "mom_test_intro": "Al visitar las oficinas del cliente, no actúe como un vendedor. Hable como un investigador de operaciones:",
        "mom_test_question": 'Hola, estoy realizando una investigación operativa con {target} en {location}. En los últimos 30 días, ¿dónde ocurrió el mayor retraso administrativo o pérdida financiera inesperada?',
        "objection_intro": "Cuando el cliente responde: 'Todo funciona bien, no tenemos problemas.'",
        "objection_counter": "Por supuesto que funciona, pero en los últimos 30 días, ¿hubo facturas duplicadas o deducciones disputadas de más de $500? ¿Puedo auditar sus últimos 5 registros gratis? Si todo está bien me retiro sin cobrar nada; si detectamos discrepancias, ¡todo el dinero recuperado es 100% suyo!",
        "validation_day1": "ACCIÓN DIRECTA: Visite su contacto de red '{advantage}' e inspeccione registros manuales reales.",
        "validation_day2": "DEMOSTRACIÓN CONSERJE: Detecte fugas de capital frente al dueño en menos de 24 horas.",
        "validation_day3": "CIERRE DE PILOTO: Asegure un piloto pagado antes de escribir código de producción.",
    },
    "German": {
        "problem_title": "Das Echte Operative Kernproblem (Kapitalverlust)",
        "customer_title": "Zielkunde & Entscheidungsträger",
        "workarounds_title": "Aktuelle Fehleranfällige Notlösungen (Excel-Chaos)",
        "unfair_edge_title": "Der Unfaire Vorteil des Gründers",
        "mom_test_title": "The Mom Test Kundeninterview-Skript (Eröffnungsfrage)",
        "validation_title": "48-Stunden-Validierungsplan (Ohne schwere Softwareentwicklung)",
        "tech_blueprint_title": "High-Ticket B2B Tech-Architektur",
        "monetization_title": "Preise & Monetarisierungsmodell",
        "earning_title": "Monatliches Wiederkehrendes Umsatzpotenzial",
        "mom_test_intro": "Treten Sie beim Kundenbesuch nicht als Verkäufer auf, sondern als operativer Prüfer:",
        "mom_test_question": 'Guten Tag, ich führe eine Prozessanalyse mit {target} in {location} durch. Wo entstand im letzten Monat der größte bürokratische Verzug oder finanzielle Verlust?',
        "objection_intro": "Wenn der Kunde sagt: 'Bei uns läuft alles reibungslos.'",
        "objection_counter": "Das ist verständlich, aber gab es in den letzten 30 Tagen unbemerkte Abrechnungsfehler oder Zahlungsverzüge? Darf ich 5 Stichproben kostenlos prüfen? Wenn alles stimmt, gehe ich sofort. Wenn wir Verluste finden, bleibt das gesparte Geld zu 100% bei Ihnen!",
        "validation_day1": "DIREKTE AKTION: Besuchen Sie Ihren Kontakt '{advantage}' und sichten Sie manuelle Belege.",
        "validation_day2": "MANUELLER BEWEIS: Decken Sie Unstimmigkeiten direkt vor den Augen des Inhabers auf.",
        "validation_day3": "PILOTVERTRAG: Schließen Sie einen bezahlten Pilotvertrag ab, bevor Sie Software programmieren.",
    },
    "French": {
        "problem_title": "Le Véritable Goulot d'Étranglement Opérationnel",
        "customer_title": "Client Cible et Payeur",
        "workarounds_title": "Solutions Manuelles Précaires (Feuilles Excel & WhatsApp)",
        "unfair_edge_title": "Avantage Déterminant du Fondateur",
        "mom_test_title": "Script d'Entretien The Mom Test (Question d'Ouverture)",
        "validation_title": "Plan de Validation en 48 Heures (Sans Coder)",
        "tech_blueprint_title": "Architecture Logicielle B2B à Haute Valeur",
        "monetization_title": "Modèle de Monétisation et Tarification",
        "earning_title": "Potentiel de Revenus Récurrents Mensuels",
        "mom_test_intro": "Ne vous présentez pas comme un vendeur, mais comme un auditeur opérationnel :",
        "mom_test_question": 'Bonjour, je mène une étude opérationnelle avec les {target} à {location}. Au cours des 30 derniers jours, où s’est produit le plus grand retard administratif ou la perte financière la plus lourde ?',
        "objection_intro": "Lorsque le client dit : 'Tout va bien, nous n'avons aucun souci.'",
        "objection_counter": "Certainement, mais au cours des 30 derniers jours, avez-vous eu des doublons de facturation ou des litiges ? Puis-je examiner gratuitement 5 de vos registres ? Si tout est conforme, je pars immédiatement. Si une anomalie est détectée, tout l'argent récupéré vous revient à 100 % !",
        "validation_day1": "ACTION DIRECTE : Rencontrez votre contact '{advantage}' et vérifiez les documents réels.",
        "validation_day2": "PREUVE CONCIERGE : Démontrez une économie immédiate devant le dirigeant.",
        "validation_day3": "PILOTE PAYÉ : Signez un contrat pilote rémunéré avant de développer du code.",
    }
}


def get_localized_headers(language: str) -> Dict[str, str]:
    """Returns localized headers for the given language.
    Falls back gracefully to English if the specific language is not in the static dict.
    """
    for key, headers in LOCALIZED_HEADERS.items():
        if key.lower() == language.lower():
            return headers
    return LOCALIZED_HEADERS["English"]
