"""
================================================================================
  NEW LECTURE QUESTIONS & HOMEWORK SOLVER (src/new_questions.py)
================================================================================
  Contains structured question-and-answer pairs extracted from the professor's
  lecture slides (Slide 1: Questions 1–9, Slide 2: Homework Assignment).
================================================================================
"""

from typing import List, Dict, Any

NEW_LECTURE_QA: List[Dict[str, Any]] = [
    {
        "q_num": 1,
        "question": "1- Who is the author?",
        "source": "Journal Page 303 (Title & Affiliation)",
        "model_answer": (
            "The author of the article is Dr. Philip Hermans. At the time of this research, he was an academic "
            "anthropologist in the Department of Social and Cultural Anthropology at the Catholic University of Leuven "
            "(KU Leuven) in Belgium, and affiliated with the Department of Education at the University of Groningen in the Netherlands. "
            "He conducted extensive ethnographic, educational, and psychological fieldwork investigating the schooling, acculturation, "
            "and social adaptation of Moroccan immigrant youth in Belgium."
        ),
        "additional_explanation": (
            "Why is this the answer? This information is verified on the first page of the journal article (Page 303). "
            "Dr. Hermans is an expert anthropologist whose doctoral dissertation at KU Leuven focused on comparing successful and "
            "unsuccessful Moroccan youth in the Belgian education system. Knowing his background is critical: he is a trained social scientist "
            "conducting hands-on research in Flemish schools, not an outside commentator."
        ),
        "important_to_remember": (
            "• Author: Dr. Philip Hermans\n"
            "• Affiliations: KU Leuven (Belgium) & University of Groningen (Netherlands)\n"
            "• Publication: International Journal of Educational Research, Vol. 31 (1999), pp. 303–316"
        ),
    },
    {
        "q_num": 2,
        "question": "2- What is the article about?",
        "source": "Journal Pages 303–305 (Abstract & Introduction)",
        "model_answer": (
            "The article investigates the emotional repertoires, acculturation, and schooling experiences of Moroccan immigrant "
            "adolescents in Belgium, with a central scientific focus on the moral affects of shame (hshuma) and guilt (dhenb/ndam).\n\n"
            "Specifically, the article addresses a widespread deficit stereotype held by Western teachers, school psychologists, and therapists "
            "in Brussels, who claimed that Moroccan students lack an internalized sense of guilt, moral conscience, and personal responsibility. "
            "To test whether this stereotype was true, Dr. Hermans administered a psychological projective test (the Thematic Apperception Test or TAT) "
            "to 70 Moroccan male adolescents in Belgian secondary schools to empirically examine how they experience and express guilt, shame, "
            "remorse, and moral accountability."
        ),
        "additional_explanation": (
            "Why is this the answer? The article directly responds to an urgent real-world problem: Belgian teachers claimed Moroccan students "
            "were difficult to manage because they supposedly had no internal conscience and only cared if they were caught. Dr. Hermans designed "
            "an objective empirical study to prove whether Moroccans lack guilt or whether Western professionals simply misunderstood their cultural "
            "expression of morality. It connects psychology, anthropology, and educational policy."
        ),
        "important_to_remember": (
            "• Core Problem: Refuting the Western stereotype that Moroccan youth lack guilt.\n"
            "• Research Sample: 70 Moroccan male secondary school adolescents (aged 15–20) in Brussels and Flanders.\n"
            "• Psychological Instrument: Thematic Apperception Test (TAT) scored via George DeVos's cross-cultural manual."
        ),
    },
    {
        "q_num": 3,
        "question": "3- What are the main ideas of the article?",
        "source": "Chapters 1–7 (Full Research Corpus)",
        "model_answer": (
            "The main ideas of the article can be synthesized into five core scientific points:\n\n"
            "1. Historical & Structural Context of Migration: Moroccan migration began through bilateral labor treaties in the 1960s. Although meant to be temporary 'guest workers', families settled permanently. Second- and third-generation youth face persistent structural discrimination and disproportionate tracking into lower vocational school streams (B-stroom).\n"
            "2. Refutation of the Cultural Deficit Stereotype: Empirical testing disproves the Western claim that Moroccan youth lack guilt. Over 68% of the adolescents' narratives displayed acute internal moral suffering, weeping, and self-blame independent of external surveillance.\n"
            "3. The Cultural Anatomy of Shame (Hshuma) vs. Guilt (Dhenb): In Moroccan culture, shame (hshuma) is not humiliating defeat; it is an honorable social code of decency, modesty, and respect. Guilt is mediated through religious sin (dhenb) and familial love rather than secular individualistic legalism.\n"
            "4. The Dialectic of the Gaze: External shame and internal guilt are mutually reinforcing. The external 'gaze of the community' acts as a psychological catalyst that forces the offender to look inward, activating internal conscience and motivating restitution.\n"
            "5. Defensive Behavior as a Structural Reaction: When Moroccan students act defensive or deny wrongdoing in Belgian schools, it is not evidence of an amoral character; it is a psychological defense mechanism used to protect their dignity against institutional discrimination and low teacher expectations."
        ),
        "additional_explanation": (
            "Why is this the answer? These five ideas represent the logical progression of the entire research study: moving from migration history (Chapter 1), "
            "to theoretical critique (Chapters 2–3), to empirical proof (Chapters 4–5), to linguistic analysis (Chapter 6), and finally to educational policy reforms (Chapter 7). "
            "Together, they dismantle the racist idea that Moroccan youth are morally inferior and show that schooling difficulties are caused by cultural misunderstandings and institutional barriers."
        ),
        "important_to_remember": (
            "• Main Idea 1: Empirical refutation of moral deficit theories.\n"
            "• Main Idea 2: 'Hshuma' is social decency; 'Dhenb' is moral sin; 'Ndam' is authentic remorse.\n"
            "• Main Idea 3: The 'Gaze of the Other' activates the inner conscience.\n"
            "• Main Idea 4: Student defensiveness is a shield against systemic discrimination, not a moral flaw."
        ),
    },
    {
        "q_num": 4,
        "question": "4- What is his point view on Moroccan immigrants?",
        "source": "Journal Pages 308, 314–316",
        "model_answer": (
            "Dr. Philip Hermans maintains an empathetic, anti-deficit, culturally responsive, and scientifically objective point of view regarding Moroccan immigrants.\n\n"
            "He firmly rejects and critiques the ethnocentric prejudices of Western educators and therapists who pathologized Moroccan culture as morally primitive "
            "or lacking conscience. Instead, Dr. Hermans portrays Moroccan immigrant adolescents as morally mature individuals who possess rich, sophisticated emotional repertoires. "
            "He demonstrates that their moral commitments are deeply rooted in filial devotion, parental respect, and community solidarity. Furthermore, he emphasizes that the academic "
            "and social difficulties Moroccan youth experience in Belgium are not caused by cultural deficiencies, but by structural inequalities, educational tracking, and pervasive societal discrimination."
        ),
        "additional_explanation": (
            "Why is this the answer? In academic research, a researcher's perspective can either support the dominant power structure (blaming the minority group) or challenge institutional injustice. "
            "Dr. Hermans explicitly challenges the Belgian educational establishment. On Page 308, he calls out the misapplication of Piaget's developmental stages as an unfair evolutionary hierarchy. "
            "Throughout the text, he treats Moroccan youth with deep dignity, proving that their ethical values are just as complex and valid as Western moral codes."
        ),
        "important_to_remember": (
            "• Hermans' Perspective: Anti-deficit, culturally affirmative, and structurally aware.\n"
            "• Core Argument: Moroccan youth do not suffer from moral or cognitive deficits; they suffer from cultural misinterpretation and structural discrimination in schools."
        ),
    },
    {
        "q_num": 5,
        "question": "5- What are the themes of the article?",
        "source": "Journal Pages 303–316 (7 Thematic Domains)",
        "model_answer": (
            "The article encompasses seven interconnected academic themes:\n\n"
            "1. Cross-Cultural Psychology of Moral Affects: The theoretical distinction and interaction between shame (external sanction) and guilt (internal conscience).\n"
            "2. Intercultural Education & Classroom Misunderstandings: The cultural clashes between Belgian educators' individualistic methods and Moroccan parents' collectivist honor codes.\n"
            "3. Post-War Labor Migration & Demographics: The legal and social evolution of Moroccan guest workers into permanent Belgian citizens.\n"
            "4. Empirical Projective Testing (The TAT): The methodological use of ambiguous visual cards and DeVos's cross-cultural scoring system to uncover subconscious moral values.\n"
            "5. Filial Piety & Family-Centered Morality: The profound influence of parental sacrifice, maternal tears, and family honor in motivating moral reformation.\n"
            "6. Sociolinguistic Anthropology: The cultural meaning of Moroccan Arabic terminology including hshuma, hshumiya, dhenb, ndam, and fdiha.\n"
            "7. Institutional Discrimination & Structural Inequality: The impact of lower educational tracking (B-stroom) and employment bias on immigrant youth identity."
        ),
        "additional_explanation": (
            "Why is this the answer? A 'theme' is a recurring subject or central topic explored throughout an academic paper. Dr. Hermans connects psychological themes "
            "(how the human mind feels remorse) with anthropological themes (how languages name emotions) and sociological themes (how laws and schools discriminate against immigrants). "
            "Understanding all seven themes gives students a 360-degree view of intercultural dynamics."
        ),
        "important_to_remember": (
            "• Psychology: Shame vs. Guilt.\n"
            "• Anthropology: The meaning of 'Hshuma' and 'Dhenb'.\n"
            "• Education: Intercultural classroom discipline.\n"
            "• Sociology: Structural discrimination and educational streaming."
        ),
    },
    {
        "q_num": 6,
        "question": "6- Are there any aspects of racism, stereotypes, misconceptions in the text?",
        "source": "Journal Pages 305–308, 314",
        "model_answer": (
            "Yes, the article extensively identifies, documents, and critiques multiple manifestations of stereotypes, misconceptions, and structural racism:\n\n"
            "1. The Deficit Stereotype of the 'Amoral Migrant': Western authors (such as Eppink, 1990, 1992) claimed that Moroccan youth cannot internalize moral rules, do not value honesty or truth, and feel zero guilt unless caught red-handed.\n"
            "2. The 'Manipulative Social Intelligence' Stereotype: Belgian school psychologists and teachers in Brussels stereotyped Moroccan students as possessing an innate, untrustworthy ability to manipulate Westerners while lacking authentic conscience (Page 307).\n"
            "3. The Distortion of Jean Piaget's Moral Stages (Scientific Racism): Belgian educators weaponized Piaget's childhood theory, asserting that Moroccans never develop 'autonomous morality' and remain permanently trapped at the 'heteronomous' stage of an 8-year-old child (Page 308).\n"
            "4. The Kindergarten Misconception ('Loss of Face'): Western teachers publicly reprimanded a child for theft, misinterpreting the Moroccan parents' humiliation and defensive withdrawal as indifference to morality, failing to recognize that public exposure destroyed the family's honor (Page 306).\n"
            "5. Institutional Racism & Systemic Discrimination: Documented bias in job recruitment (Goris, 1997) and systemic educational tracking that automatically diverts Moroccan students into low-prestige vocational streams."
        ),
        "additional_explanation": (
            "Why is this the answer? This question asks students to critically analyze how racism operates in intellectual and educational spaces. "
            "Racism is not just physical violence; it often appears as 'scientific' theories that treat minority cultures as backward or child-like. "
            "Dr. Hermans shows how everyday teachers and psychologists used psychological theories to justify their own prejudices against Moroccan students."
        ),
        "important_to_remember": (
            "• Stereotype 1: Moroccan youth only obey rules to avoid external capture (disproven by Table 1).\n"
            "• Stereotype 2: Moroccan morality is stuck at the childhood level of Piaget's heteronomous stage.\n"
            "• Misconception: Confusing protective family dignity ('loss of face') with lack of moral concern.\n"
            "• Structural Reality: Systemic employment discrimination and vocational school tracking."
        ),
    },
    {
        "q_num": 7,
        "question": "7- What is guilt?",
        "source": "Journal Page 304, 313–314",
        "model_answer": (
            "According to the psychological and anthropological consensus established in the article (Levy & Rosaldo, 1983; Lebra, 1983; Barrett, 1995):\n\n"
            "Guilt is an internal moral emotion that occurs when an individual breaks moral, religious, or ethical rules that have been internalized into their personal conscience.\n\n"
            "Key characteristics of guilt include:\n"
            "• Locus of Evaluation: Internal self-evaluation. It is triggered by one's own conscience, even when no external witnesses are present.\n"
            "• Focus of Concern: Specific negative behavior. The person thinks: 'I committed a bad action,' preserving their belief in their underlying human capability.\n"
            "• Perception of Others: Others appear as injured victims or sufferers who have been harmed by the action.\n"
            "• Psychological State: An active, responsible self who accepts personal agency for their conduct.\n"
            "• Behavioral Outcome: Motivates confession, contrition, apology, positive atonement, and restorative restitution.\n"
            "• Moroccan Cultural Expression: Designated as sh'ur bi d-dhenb (feeling of sin before divine justice) and ndam (heartfelt remorse and contrition)."
        ),
        "additional_explanation": (
            "Why is this the answer? This definition combines the classical psychological literature from Page 304 with the anthropological findings from Pages 313–314. "
            "In simple terms: guilt is that uncomfortable feeling in your stomach that tells you that you hurt someone, making you want to apologize and fix the problem. "
            "It is action-focused and constructive."
        ),
        "important_to_remember": (
            "• Formula for Guilt: Internal Conscience + Action-Specific Evaluation + Victim Concern + Restorative Atonement.\n"
            "• Moroccan Equivalents: 'Dhenb' (transgression/sin against God) and 'Ndam' (remorse)."
        ),
    },
    {
        "q_num": 8,
        "question": "8- What is shame?",
        "source": "Journal Page 304, 313–314",
        "model_answer": (
            "According to the theoretical framework outlined in the article (Levy, 1983; Barrett, 1995; Hermans, 1999):\n\n"
            "Shame is an external moral affect that arises when standards of proper public presentation, social decorum, or cultural honor are violated before an audience.\n\n"
            "Key characteristics of shame include:\n"
            "• Locus of Evaluation: External social surveillance. It implies an external sanction or public exposure.\n"
            "• Focus of Concern: The global self. The person feels that their entire identity is defective, inferior, or humiliated: 'I am fundamentally flawed.'\n"
            "• Perception of Others: Others appear as judging spectators who witness one's personal defeat or disgrace.\n"
            "• Psychological State: A passive, helpless self feeling exposed, immobilized, and powerless.\n"
            "• Behavioral Outcome: Motivates blushing, lowering the gaze, hiding, covering the face, and withdrawing from social contact.\n"
            "• Moroccan Cultural Expression: Designated as hshuma (or hshumiya / heshma), which fundamentally represents propriety, respect, decency, modesty, and discretion in community life."
        ),
        "additional_explanation": (
            "Why is this the answer? This definition synthesizes Page 304 and Pages 313–314. In simple terms: shame is that painful feeling of wanting the ground to swallow you up "
            "when you do something embarrassing or dishonorable in front of other people. While Western psychology often views shame as negative, Dr. Hermans explains that in Moroccan culture, "
            "hshuma is a positive cultural value that keeps society respectful and polite."
        ),
        "important_to_remember": (
            "• Formula for Shame: Public Exposure + Global Self Defect + Audience Spectators + Social Withdrawal.\n"
            "• Moroccan Meaning: 'Hshuma' is social decency, modesty, and mutual respect, not merely humiliation."
        ),
    },
    {
        "q_num": 9,
        "question": "9- How are these two concepts exemplified in the text?",
        "source": "Journal Pages 306, 310–312, 314",
        "model_answer": (
            "The article provides concrete empirical, qualitative, and sociocultural examples demonstrating both guilt and shame:\n\n"
            "1. Exemplification of Guilt:\n"
            "• TAT Plate 3BM (Slumped Figure & Revolver, Table 1): Over 68% of Moroccan youth described a character who committed theft or accidentally injured a friend, returned home, wept alone in bed, and blamed himself. Verbatim quote: 'He arrived home and started to cry. He feels guilty. He blames himself deeply.'\n"
            "• TAT Plate 13MF (Anguish beside Bed, Table 2): Adolescents narrated stories of a young man committing murder in an impulsive moment of anger, immediately followed by overwhelming internal remorse (ndam) and suicidal agony over his moral sin.\n"
            "• Plates 6BM & 7BM (Parental Duty): Sons realizing their academic failure caused their father to weep in bed, provoking genuine moral repentance and reformation to support the family.\n\n"
            "2. Exemplification of Shame:\n"
            "• The Kindergarten Case Study: Moroccan parents experiencing acute humiliation (loss of face / fdiha) when Belgian teachers publicly exposed their child's minor theft to other adults rather than disciplining the child discreetly in class.\n"
            "• The Social Cue 'Hshuma 'Alik': The ubiquitous cultural phrase ('you ought to be ashamed') used across Morocco to remind children and adults to uphold modest decorum and respect social boundaries.\n\n"
            "3. Exemplification of the Dialectical Interaction (Both Together):\n"
            "• In Table 2 (Plate 13MF), 10 adolescents explicitly combined both affects: the character felt internal moral guilt before God (dhenb), while simultaneously fearing the public dishonor and shame brought upon his family lineage (hshuma).\n"
            "• The Dialectic of the Gaze: Dr. Hermans formulates that the external gaze of the community (shame) serves as the mirror that forces the offender to look inward, activating internal conscience and guilt (Page 314)."
        ),
        "additional_explanation": (
            "Why is this the answer? To get full marks on an academic exam, students cannot just provide abstract definitions; they must cite specific evidence from the text. "
            "Dr. Hermans provides real examples from three sources: psychological testing data (TAT Tables 1 and 2), observational school case studies (the kindergarten incident), "
            "and everyday linguistic phrases (hshuma 'alik). Citing these exact examples proves the text's thesis."
        ),
        "important_to_remember": (
            "• Guilt Example: Plate 3BM (68% internal remorse and weeping) and Plate 13MF (murder followed by intense contrition).\n"
            "• Shame Example: The kindergarten theft incident causing family 'loss of face'.\n"
            "• Joint Example: Table 2 narratives where guilt before God is coupled with family shame."
        ),
    },
]

HOMEWORK_SYNTHESIS_TASK: Dict[str, Any] = {
    "title": "Homework Assignment: Curricular Synthesis of Guilt and Shame",
    "prompt": (
        "Read the Article on the Themes of 'Guilt and Shame' and try to note the most important ideas "
        "tackled in this article. Take into consideration the key concepts dealt with in the previous classes."
    ),
    "model_answer": (
        "A comprehensive academic response to the homework assignment requires synthesizing Dr. Philip Hermans' research with "
        "the four foundational conceptual pillars established in our Global Culture course:\n\n"
        "1. Synthesis with Course Module on Stereotyping & Racial Ideology:\n"
        "In previous classes, we analyzed Paul Gilroy's theory of imperial representations and the cognitive mechanisms of social stereotypes "
        "(essentialism, out-group homogenization, and structural prejudice). In Dr. Hermans' text, this is directly exemplified by the deficit stereotype "
        "created by Western educational professionals. Belgian teachers and psychologists homogenized Moroccan youth as an amoral out-group who allegedly "
        "lack autonomous morality. Dr. Hermans uses rigorous empirical science (the TAT) to dismantle this stereotype, demonstrating that minority students "
        "possess deep moral conscience that ethnocentric Western frameworks failed to recognize.\n\n"
        "2. Synthesis with Course Module on Acculturation & Cultural Maintenance:\n"
        "In our acculturation studies (John Berry's framework of Assimilation, Integration, Separation, and Marginalization), we learned that immigrant adaptation "
        "is a dual-process of cultural maintenance and host contact. Dr. Hermans demonstrates this dynamic in second-generation Moroccan youth in Belgium. "
        "These youngsters maintain their heritage cultural values (filial honor, hshuma, Islamic definitions of dhenb), while navigating Western schooling. "
        "When schools reject their heritage norms, students risk marginalization; when schools practice culturally responsive education, true integration becomes possible.\n\n"
        "3. Synthesis with Course Module on Gender Roles & Filial Socialization:\n"
        "Previous lectures examined how cultural expectations structure gender performance and familial roles. In Dr. Hermans' TAT findings (Plates 6BM and 7BM), "
        "Moroccan male adolescents articulated a family-centered moral code where masculinity is defined by filial responsibility, protecting the mother's tears, "
        "and upholding the father's public dignity. Moral failure is experienced primarily as letting down the family, contrasting sharply with Western individualistic concepts of personal autonomy.\n\n"
        "4. Synthesis with Course Module on Culture Shock & Institutional Barriers:\n"
        "Previous course topics detailed the cognitive dissonance and disorientation of culture shock. In Dr. Hermans' text, culture shock occurs at the institutional "
        "interface between Belgian schools and immigrant homes (the kindergarten incident). When Belgian teachers apply Western 'therapeutic transparency' without "
        "understanding Moroccan 'protective discretion' (satr), cultural clash ensues. Furthermore, the article documents how structural inequality (educational tracking "
        "in the B-stroom and labor market discrimination) induces defensive coping mechanisms in immigrant youth."
    ),
    "additional_explanation": (
        "Why is this the answer? The professor's homework assignment explicitly asked students to connect the reading to 'the key concepts dealt with in the previous classes'. "
        "A superior university paper does not summarize the article in isolation; it builds bridges back to earlier course topics: stereotypes, racism, acculturation models, "
        "gender expectations, and structural inequality. This demonstrates deep academic synthesis."
    ),
    "important_to_remember": (
        "• Synthesis Link 1: Connects deficit models to Paul Gilroy's theories of racial stereotyping.\n"
        "• Synthesis Link 2: Connects Moroccan youth identity to John Berry's acculturation models.\n"
        "• Synthesis Link 3: Connects TAT family narratives to collectivist filial gender expectations.\n"
        "• Synthesis Link 4: Connects school misunderstandings to institutional culture shock and educational tracking."
    ),
}
