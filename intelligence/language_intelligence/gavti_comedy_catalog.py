"""
Authentic Varhadi / Gavti Marathi Relatable Comedy Catalog matching demo.mp4.
Features the exact verbal expressions, regional dialect markers (मा, हो का व, बकऱ्या, तुले, आम्हाले),
hilarious everyday Gavti roasting / affectionate cuss words (भडव्या, मुडद्या, येड्या, काळ्या तोंडाच्या, फुकट्या, मारीन एक मुस्काटात, आयला),
and canonical multi-character situational comedy featuring:
- ganya (गण्या): Hero boy with fiery orange spiky hair, red-and-white striped shirt
- shanti (शांताबाई / शांती): Furious mother in royal blue saree, violet blouse, red bindi
- rohya (रोह्या): Sarcastic best friend with side-swept purple hair, pure white shirt
- sonya (सोन्या): Mischievous brother/friend with golden hair, yellow striped shirt
- yogya (योग्या): Cool friend with cyan shirt
- aakya (आक्या): Village katta dude with sunglasses and vest
"""

from typing import Dict, Any, List
import random

class GavtiComedyCatalog:
    """
    Catalog of hilarious, everyday Maharashtrian situational comedy episodes.
    100% understandable for all audiences, zero educational jargon, packed with rural energy.
    """

    SCENARIOS: List[Dict[str, Any]] = [
        {
            "id": "crocodile_river_warning",
            "title_marathi": "मगरीची नदी आणि पाटलाची पाटी",
            "environment": "river_crocodile_bank",
            "char1_id": "ganya",
            "char1_name": "गण्या",
            "char2_id": "rohya",
            "char2_name": "रोह्या",
            "char3_id": "rohya",
            "char3_name": "रोह्या",
            "hook": "अहा गड्या! पाटीवर काय लिहिलंय, 'मगरी येथे पोहत नाहीत'! म्हणजे पाण्यात एकबी मगर नाही भडव्या, आपण खुशाल पोहू शकतो!",
            "situation": "धपकन उडी मारली पाण्यात! काय थंडगार पाणी हाय मा, गावातल्या उकाड्यापेक्षा इथं पोहायला लय भारी वाटतंय!",
            "intrigue": "अरे देवा! आयला भडव्या! ही काय मागं खरीखुरी मगर आली रे मुडद्या! पळा पळा, जीव वाचवा!",
            "twist": "अरे रोह्या येड्या, पाटीवर लिहिलं होतं 'मगरी येथे पोहत नाहीत', मग नदीत काय तुझ्या बापाची मगर आली का भडव्या!",
            "payoff": "अरे मुडद्या, मगरीच्या पुढे उद्गारवाचक चिन्ह लावायचं राहिलं होतं! त्याचा अर्थ 'मगरी आहेत! येथे पोहू नये!' असा होता!",
            "cta": "अशी जर व्याकरणाची चूक झाली ना येड्या, तर मगर गिळून टाकील! व्हिडिओ आवडला तर सबस्क्राईब ठोका की मा!"
        },
        {
            "id": "msrtc_bus_tour_scold",
            "title_marathi": "एसटी बसची सफर आणि आईचा राडा",
            "environment": "msrtc_bus_stand",
            "char1_id": "ganya",
            "char1_name": "गण्या",
            "char2_id": "shanti",
            "char2_name": "शांताबाई",
            "char3_id": "rohya",
            "char3_name": "रोह्या",
            "hook": "बहिणमाय मी फक्त फिरावाले चाललो आई, कोणता युद्ध लढाले नाही! आता पैसे देऊन दे तिकिटीचे!",
            "situation": "मस्त्या गिस्त्या नाही करायचा मा! तुया बापानं दिलं न रं तुले दोनशेची नोट, आता का किडनी विकू का तुझ्यासाठी बकऱ्या, मुडद्या!",
            "intrigue": "अजी काकू तुम्ही टेन्शन नको घेवा! मी आहो याच्या सोबत, यानं काही केलं न त या भडव्याच्या अंगावरून बस चालवतो मी!",
            "twist": "मारीन एक मुस्काटात! मारशील का रे माझ्या पोराला येड्या! बापाचा गाव हो का व? गण्या तू आपली काळजी घे जो मा!",
            "payoff": "काकू, या बसमधी बाकीचे पोरं दिसत नाहीत? अहो ते सगळे फुकट्या सारखे सीटाच्या खाली लपून बसल्यात!",
            "cta": "कशी वाटली मग लालपरीची सफर? अशाच अस्सल वऱ्हाडी गावठी कॉमेडीसाठी लगेच सबस्क्राईब ठोका की मा!"
        },
        {
            "id": "village_katta_roasting",
            "title_marathi": "गावातला कट्टा आणि उधारीचा चहा",
            "environment": "village_katta",
            "char1_id": "ganya",
            "char1_name": "गण्या",
            "char2_id": "rohya",
            "char2_name": "रोह्या",
            "char3_id": "shanti",
            "char3_name": "शांताबाई",
            "hook": "आयला रोह्या, सकाळपासून चहा पाजतो म्हणतोस आणि खिशात एक रुपया बी नाही भडव्या!",
            "situation": "काय रं गण्या, सोन्याने मगाशीच हजार रुपये उसने नेले, आता काय झाडाला पैसे लागतात का बकऱ्या!",
            "intrigue": "आरं मुडद्यांनो, मी काय पळून चाललो का? तिकडे शांताबाई काठी घेऊन आपल्यालाच शोधत येतीये!",
            "twist": "काळ्या तोंडाच्या येड्यांनो! दिवसभर कट्ट्यावर बसून चकाट्या पिटता, अक्कल गहाण ठेवली का रे फुकट्यांनो!",
            "payoff": "शांताबाई शांत व्हा! आम्ही काय चहा पित नव्हतो, सोन्याला एमपीएससीचा फॉर्म भरायला शिकवत होतो!",
            "cta": "गावातल्या कट्ट्याची ही गावठी गंमत आवडली असेल तर लगेच सबस्क्राईबचं बटन दाबा मा!"
        },
        {
            "id": "night_restaurant_bill",
            "title_marathi": "हॉटेलमधली पार्टी आणि बिलाचा घोळ",
            "environment": "night_terrace_ferris_wheel",
            "char1_id": "ganya",
            "char1_name": "गण्या",
            "char2_id": "rohya",
            "char2_name": "रोह्या",
            "char3_id": "shanti",
            "char3_name": "शांताबाई",
            "hook": "अर्रर्र गड्या! एवढ्या मोठ्या हॉटेलमध्ये आणून बसवलं आणि आता म्हणतो खिशात पाकीटच नाही भडव्या!",
            "situation": "काय रं गण्या, मी काय मुद्दाम विसरलो का? मगाशी घाईघाईत घरातच पॅन्ट बदलली की मा, डोस्कं फिरवू नको!",
            "intrigue": "बघा राव मित्रांची जात! मेनू कार्डवरची सगळी महागडी भाजी मागवली आणि बिलाच्या वेळेस गपगार, काळ्या तोंडाच्या!",
            "twist": "आणि तो वेटर तिकडून तीनदा बिल घेऊन आलाय, डोळे मोठे करून बघतोय आपल्याकडं, मारीन एक मुस्काटात!",
            "payoff": "काही काळजी नको करू येड्या, मी त्या वेटरला सांगतो की हा आकाशपाळण्यावर चक्कर येऊन पडलाय!",
            "cta": "असा कंजूस मित्र तुमचा बी हाय का? लगेच त्याला शेअर करा आणि सबस्क्राईब दाबा मा!"
        },
        {
            "id": "college_result_fear",
            "title_marathi": "कॉलेजचा निकाल आणि बापाची भीती",
            "environment": "college_corridor",
            "char1_id": "ganya",
            "char1_name": "गण्या",
            "char2_id": "rohya",
            "char2_name": "रोह्या",
            "char3_id": "shanti",
            "char3_name": "शांताबाई",
            "hook": "अर्रर्र गड्या! आज कॉलेजचा निकाल हाय आणि बापानं सकाळीच बांबू काढून ठेवलाय घरात भडव्या!",
            "situation": "काय रं गण्या, मग वर्षभर काय कट्ट्यावर माश्या मारत होता का? आता रडून काय फायदा बकऱ्या!",
            "intrigue": "आरं मुडद्या, मी पूर्ण उत्तरपत्रिका भरून आलो होतो, पण सरांनी लाल पेनाने रांगोळीच काढली वाटते!",
            "twist": "आणि नेमके शेजारचे काका विचारतात, 'काय मग गण्या, किती टक्के पडले रे?' मारीन एक मुस्काटात!",
            "payoff": "मी सांगून टाकलं, 'काका, मला १०० पैकी १०० मिळालेत... फक्त दोन विषयात मिळून!'",
            "cta": "निकाल ऐकून हसून हसून पोट दुखलं असेल तर लगेच आपल्या चॅनेलला सबस्क्राईब ठोका मा!"
        },
        {
            "id": "mobile_battery_cut",
            "title_marathi": "मोबाईलची बॅटरी आणि अचानक गेलेली लाईट",
            "environment": "village_katta",
            "char1_id": "ganya",
            "char1_name": "गण्या",
            "char2_id": "sonya",
            "char2_name": "सोन्या",
            "char3_id": "rohya",
            "char3_name": "रोह्या",
            "hook": "आयला गड्या! मोबाईलची बॅटरी १ टक्क्यावर आली आणि नेमकी लाईटच गेली की मा, डोस्कं फिरलं भडव्या!",
            "situation": "काय रं गण्या, मग आता काय मेणबत्तीवर मोबाईल चार्ज करणार का रे येड्या!",
            "intrigue": "आरं हसू नको बकऱ्या, गावातल्या डीपीलाच थेट वायर जोडायचा विचार हाय माझा!",
            "twist": "आरं मुडद्या, असा झटका बसेल ना की थेट चंद्रावर पोहोचशील, काळ्या तोंडाच्या!",
            "payoff": "म्हणून डोस्कं चालवून शेजारच्या काकांचा पॉवर बँक गुपचूप आणलाय मी!",
            "cta": "कशी वाटली मग आयडिया? भावांनो, लगेच सबस्क्राईबचं बटन दाबा की मा!"
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
