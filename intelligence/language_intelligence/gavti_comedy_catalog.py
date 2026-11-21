"""
Authentic Varhadi / Gavti Marathi Relatable Comedy Catalog matching demo.mp4.
Features the exact verbal expressions, regional dialect markers (मा, हो का व, बकऱ्या, तुले, आम्हाले),
and multi-character situational comedy (Mother in Saree, Orange Hair Boy, Purple Hair Friend).
"""

from typing import Dict, Any, List
import random

class GavtiComedyCatalog:
    """
    Catalog of hilarious, everyday Maharashtrian situational comedy episodes.
    """

    SCENARIOS: List[Dict[str, Any]] = [
        {
            "id": "msrtc_bus_tour_scold",
            "title_marathi": "एसटी बसची सफर आणि आईचा राडा",
            "environment": "msrtc_bus_stand",
            "hook": "बहिणमाय मी फक्त फिरावाले चाललो आई, कोणता युद्ध लढाले नाही! आता पैसे देऊन दे तिकिटीचे!",
            "situation": "मस्त्या गिस्त्या नाही करायचा मा! तुया बापानं दिलं न रं तुले दोनशेची नोट, आता का किडनी विकू का तुझ्यासाठी बकऱ्या!",
            "intrigue": "अजी काकू तुम्ही टेन्शन नको घेवा! मी आहो याच्या सोबत, यानं काही केलं न त याच्या अंगावरून बस चालवतो मी!",
            "twist": "मारशील का रे माझ्या पोराला बकऱ्या! बापाचा गाव हो का व? बाबू तू आपली काळजी घे जो मा!",
            "payoff": "या बसमधी तुम्ही दोघंच जण दिसत्यान रे? अहो काकू, बाकीचे पोरं गरीब आहेत, सीटाच्या खाली बसल्यात!",
            "cta": "कशी वाटली मग लालपरीची सफर? अशाच अस्सल वऱ्हाडी कॉमेडीसाठी लगेच सबस्क्राईब ठोका की मा!"
        },
        {
            "id": "night_restaurant_bill",
            "title_marathi": "हॉटेलमधली पार्टी आणि मित्राचे बहाणे",
            "environment": "night_terrace_ferris_wheel",
            "hook": "अर्रर्र गड्या! एवढ्या मोठ्या हॉटेलमध्ये आणून बसवलं आणि आता म्हणतो खिशात पाकीटच नाही!",
            "situation": "काय रं बब्या, मी काय मुद्दाम विसरलो का? मगाशी घाईघाईत घरातच पॅन्ट बदलली की मा!",
            "intrigue": "बघा राव मित्रांची जात! मेनू कार्डवरची सगळी महागडी भाजी मागवली आणि बिलाच्या वेळेस गपगार!",
            "twist": "आणि तो वेटर तिकडून तीनदा बिल घेऊन आलाय, डोळे मोठे करून बघतोय आपल्याकडं!",
            "payoff": "काही काळजी नको करू, मी त्या वेटरला सांगतो की हा आकाशपाळण्यावर चक्कर येऊन पडलाय!",
            "cta": "असा कंजूस मित्र तुमचा बी हाय का? लगेच त्याला शेअर करा आणि सबस्क्राईब दाबा मा!"
        },
        {
            "id": "college_result_fear",
            "title_marathi": "कॉलेजचा निकाल आणि बापाची भीती",
            "environment": "college_corridor",
            "hook": "अर्रर्र गड्या! आज कॉलेजचा रिझल्ट हाय आणि बापानं सकाळीच काठी काढून ठेवलीये घरात!",
            "situation": "काय रं बब्या, मग अभ्यास करताना काय झोपा काढत होता का? आता रडून काय फायदा!",
            "intrigue": "आरं मी पूर्ण पेपर भरून आलो होतो, पण सरांनी लाल पेनाने रांगोळीच काढली वाटते!",
            "twist": "आणि नेमके शेजारचे काका विचारतात, 'काय मग बब्या, किती टक्के पडले?'",
            "payoff": "मी सांगून टाकलं, 'काका, मला १०० पैकी १०० मिळालेत... फक्त दोन विषयात मिळून!'",
            "cta": "निकाल ऐकून हसून हसून पोट दुखलं असेल तर लगेच आपल्या चॅनेलला सबस्क्राईब ठोका मा!"
        },
        {
            "id": "mobile_battery_cut",
            "title_marathi": "मोबाईलची बॅटरी आणि अचानक गेलेली लाईट",
            "environment": "village_katta",
            "hook": "अर्रर्र गड्या! मोबाईलची बॅटरी १ टक्क्यावर आली आणि नेमकी लाईटच गेली की मा!",
            "situation": "काय रं बब्या, मग आता काय मेणबत्तीवर मोबाईल चार्ज करणार का?",
            "intrigue": "आरं हसू नको, गावातल्या डीपीलाच थेट वायर जोडायचा विचार हाय माझा!",
            "twist": "आरं येड्या, असा झटका बसेल ना की थेट चंद्रावर पोहोचशील बकऱ्या!",
            "payoff": "म्हणून डोस्कं चालवून शेजारच्या काकांचा पॉवर बँक गुपचूप आणलाय मी!",
            "cta": "कशी वाटली मग आयडिया? भावांनो, लगेच सबस्क्राईबचं बटन दाबा की मा!"
        },
        {
            "id": "wedding_gulabjamun",
            "title_marathi": "लग्नाची पंगत आणि शेवटचे गुलाबजाम",
            "environment": "village_katta",
            "hook": "अर्रर्र गड्या! पंगतीत बसलो आणि माझ्या पानात येईपर्यंत गुलाबजाम संपले की मा!",
            "situation": "आरं बब्या, मगाशी वरातीमध्ये दोन तास नाचत होता, उशीर झाला ना मग!",
            "intrigue": "अहो पण वाढणाऱ्या पोराने पुढच्या पानात तीन-तीन गुलाबजाम टाकले राव!",
            "twist": "आणि मागून आचारी ओरडला की आता जिलेबी बी संपली, फक्त भात उरलाय!",
            "payoff": "काही काळजी करू नका, मी थेट आचाऱ्याच्या तंबूत जाऊन गरमागरम वाटी घेऊन आलोय!",
            "cta": "लग्नातल्या पंगतीची अशी मज्जा आवडली तर लगेच सबस्क्राईबचं बटन दाबा मा!"
        }
    ]

    @classmethod
    def get_random_scenario(cls) -> Dict[str, Any]:
        """Returns a high-comedy everyday scenario."""
        return random.choice(cls.SCENARIOS)

    @classmethod
    def get_scenario_by_id_or_keyword(cls, keyword: str) -> Dict[str, Any]:
        """Matches a keyword to a scenario or picks the best comedy match."""
        if not keyword:
            return cls.SCENARIOS[0]
        k_lower = keyword.lower()
        for sc in cls.SCENARIOS:
            if sc["id"] in k_lower or sc["title_marathi"] in k_lower or sc.get("environment", "") in k_lower:
                return sc
        # Default to the iconic MSRTC bus stand episode matching demo.mp4!
        return cls.SCENARIOS[0]
