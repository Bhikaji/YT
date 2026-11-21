"""
Authentic Gavti Rangdi Marathi Relatable Everyday Comedy Catalog.
Provides 100% non-educational, simple, everyday relatable comedy scenarios that
any common Maharashtrian person (rural, urban, young, old) understands and laughs at immediately.
Uses ZERO critical/difficult vocabulary and ZERO English prompt text.
"""

from typing import Dict, Any, List
import random

class GavtiComedyCatalog:
    """
    Catalog of hilarious, everyday Maharashtrian situational comedy episodes.
    """

    SCENARIOS: List[Dict[str, Any]] = [
        {
            "id": "mobile_battery_cut",
            "title_marathi": "मोबाईलची बॅटरी आणि अचानक गेलेली लाईट",
            "hook": "अर्रर्र गड्या! मोबाईलची बॅटरी १ टक्क्यावर आणि नेमकी लाईटच गेली की!",
            "situation": "काय रं बब्या, मग आता काय मेणबत्तीवर मोबाईल चार्ज करणार का?",
            "intrigue": "आरं हसू नको, गावातल्या डीपीलाच थेट वायर जोडायचा विचार हाय माझा!",
            "twist": "आरं येड्या, असा झटका बसेल ना की थेट चंद्रावर पोहोचशील!",
            "payoff": "म्हणून डोस्कं चालवून शेजारच्या काकांचा पॉवर बँक गुपचूप आणलाय मी!",
            "cta": "कशी वाटली मग आयडिया? भावांनो, लगेच सबस्क्राईबचं बटन दाबा की!"
        },
        {
            "id": "bike_petrol_friend",
            "title_marathi": "गाडीतलं पेट्रोल आणि मित्राचे नखरे",
            "hook": "अर्रर्र गड्या! भर उन्हात गाडीचं पेट्रोल संपलं आणि हा मित्र धक्का बी मारत नाही!",
            "situation": "आरं बब्या, मी आजच नवीन चप्पल घातलीये, माती उडेल ना पायावर!",
            "intrigue": "बघा राव मित्रांची जात! पार्टीला सगळ्यात पुढं आणि धक्क्याला पळ काढणार!",
            "twist": "आरं पण पुढं पाच किलोमीटर एक बी पेट्रोल पंप नाहीये गड्या!",
            "payoff": "मग तूच गाडीवर बस, मी ढकलतो आणि पुढच्या टपरीवर चहा पाज मला!",
            "cta": "तुमचा बी असाच मित्र हाय का? लगेच शेअर करा आणि सबस्क्राईब ठोका!"
        },
        {
            "id": "borrowed_money_excuse",
            "title_marathi": "उसने घेतलेले पाचशे रुपये आणि अतरंगी बहाणे",
            "hook": "अर्रर्र गड्या! मागच्या महिन्यात ५०० रुपये नेले आणि आता फोन बी उचलत नाही!",
            "situation": "काय रं बब्या, फोन लावला तर तो काय म्हणतोय?",
            "intrigue": "फोन केला की म्हणतो हॅलो आवाज येत नाही, नेटवर्कचा प्रॉब्लेम हाय!",
            "twist": "आणि तिकडे चौकात स्वतः गरमागरम वडापाव दाबत उभा हाय गड्या!",
            "payoff": "थांब आता, दुसऱ्या नंबरवरून फोन करून सांगतो तुझी लॉटरी लागलीये!",
            "cta": "पैसे बुडवणाऱ्या मित्रांना धडा शिकवण्यासाठी चॅनेलला लगेच सबस्क्राईब करा!"
        },
        {
            "id": "wedding_gulabjamun",
            "title_marathi": "लग्नाची पंगत आणि शेवटचे गुलाबजाम",
            "hook": "अर्रर्र गड्या! पंगतीत बसलो आणि माझ्या पानात येईपर्यंत गुलाबजाम संपले की!",
            "situation": "आरं बब्या, मगाशी वरातीमध्ये दोन तास नाचत होता, उशीर झाला ना मग!",
            "intrigue": "अहो पण वाढणाऱ्या पोराने पुढच्या पानात तीन-तीन गुलाबजाम टाकले राव!",
            "twist": "आणि मागून आचारी ओरडला की आता जिलेबी बी संपली, फक्त भात उरलाय!",
            "payoff": "काही काळजी करू नका, मी थेट आचाऱ्याच्या तंबूत जाऊन गरमागरम वाटी घेऊन आलोय!",
            "cta": "लग्नातल्या पंगतीची अशी मज्जा आवडली तर लगेच सबस्क्राईबचं बटन दाबा!"
        },
        {
            "id": "extra_sugar_tea",
            "title_marathi": "टपरीवरचा कडक चहा आणि पाहुण्यांची गंमत",
            "hook": "अर्रर्र गड्या! पाहुणे आले म्हणून चहात साखरेचा अर्धा डबाच ओतला की!",
            "situation": "काय रं बब्या, चहा आणलास की साखरेचा पाक आणलास पाजायला?",
            "intrigue": "अहो पाहुणे, आमच्याकडे पाहुण्यांचा आदर असाच गोड गोड करतात!",
            "twist": "पण पाहुणे म्हणतात मला शुगर हाय, मी बिनसाखरेचा चहा पितो!",
            "payoff": "मग काय, वरून पाणी ओतून चहाचा रस बनवला आणि पाहुण्यांनी एका घोटात संपवला!",
            "cta": "अशा गोड पाहुण्यांचे किस्से आवडले असतील तर आत्ताच सबस्क्राईब करा!"
        },
        {
            "id": "online_parcel_shock",
            "title_marathi": "ऑनलाइन मागवलेला फोन आणि पार्सलमध्ये भलताच घोळ",
            "hook": "अर्रर्र गड्या! सेलमध्ये ५० हजाराचा फोन मागवला आणि पार्सल आलं!",
            "situation": "काय रं बब्या, मग एवढा का थरथर कापतोयस? डबा उघडून बघ की!",
            "intrigue": "आरं डबा उघडला आणि आतमध्ये कपडे धुण्याचा साबण निघाला की!",
            "twist": "आणि बिलावर लिहिलंय की 'स्वच्छ राहा, सुंदर राहा'!",
            "payoff": "म्हणून म्हणतो ऑनलाईनवर अक्कल गहाण ठेवू नका, दुकानात जाऊनच वस्तू घ्या!",
            "cta": "हसून हसून पोट दुखलं असेल तर लगेच आपल्या चॅनेलला सबस्क्राईब ठोका!"
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
            if sc["id"] in k_lower or sc["title_marathi"] in k_lower:
                return sc
        # Default to mobile battery cut - universally relatable comedy
        return cls.SCENARIOS[0]
