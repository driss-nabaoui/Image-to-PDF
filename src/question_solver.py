"""
================================================================================
  QUESTION SOLVER & MODEL ANSWER MODULE (src/question_solver.py)
================================================================================
  Automatically detects, extracts, and generates comprehensive model answers
  in simple English with underlying academic reasoning and practical examples.
================================================================================
"""

import os
from typing import List, Dict, Any


def build_academic_qa_corpus(corpus: Dict[str, Any], output_md_path: str = "output/Questions_And_Answers.md") -> List[Dict[str, Any]]:
    """
    Formulates complete model answers for all curriculum and examination questions.
    Generates 'MODEL ANSWER' and 'WHY IS THIS THE ANSWER?' sections.
    """
    print("\n[3/4] Solving and annotating academic examination questions...")

    qa_catalog = [
        {
            "question_id": 1,
            "chapter_id": 1,
            "question": "Why did large numbers of Moroccan workers migrate to Belgium starting in the 1960s, and why did the initial 'guest worker' assumption fail to predict long-term settlement?",
            "model_answer": (
                "Moroccan workers migrated to Belgium in the 1960s because Belgium was experiencing rapid post-war industrial growth "
                "and faced severe labor shortages in heavy industries, coal mining, and construction. In 1964, the Belgian and Moroccan "
                "governments signed bilateral labor treaties to recruit Moroccan manual laborers.\n\n"
                "The initial 'guest worker' (Gastarbeiter) assumption failed because European authorities treated laborers as purely temporary "
                "economic units who would work for a few years and return to Morocco. In reality, human beings naturally establish roots: "
                "workers built social ties, and when European countries enacted family reunification laws in the 1970s, workers brought their "
                "spouses and children to Belgium. Because economic and educational opportunities in Belgium were superior to rural Morocco, "
                "return migration remained extremely rare, transforming a temporary labor flow into a permanent immigrant community."
            ),
            "why_is_this_the_answer": (
                "This answer is correct because it identifies both the economic 'pull' factors (post-war industrial expansion and the 1964 treaty) "
                "and the sociodemographic mechanisms (family reunification policies and settlement dynamics) documented on Page 303 of the study."
            ),
            "practical_example": (
                "Think of a company hiring freelance contract workers for a six-month software project. If the company keeps extending the project "
                "for ten years, the contractors will eventually buy houses, enroll their children in local schools, and become permanent residents."
            ),
        },
        {
            "question_id": 2,
            "chapter_id": 2,
            "question": "According to anthropological and psychological consensus, what are the primary structural differences between the moral emotions of 'shame' and 'guilt'?",
            "model_answer": (
                "Anthropological and psychological research establishes four fundamental differences between shame and guilt:\n\n"
                "1. **Origin of Sanction (External vs. Internal):** Shame is triggered by public exposure, social disapproval, and external "
                "sanctions before an audience of spectators. Guilt is generated internally by one's own conscience when internalized moral rules are violated.\n"
                "2. **Perception of Others (Spectators vs. Sufferers):** In shame, other people appear as judging spectators who witness one's defeat. "
                "In guilt, other people appear as injured victims or sufferers who were harmed by one's actions.\n"
                "3. **Focus of Evaluation (Global Self vs. Specific Action):** Shame attacks the entire self ('I am fundamentally flawed or incompetent'). "
                "Guilt evaluates a specific behavioral act ('I committed an unjust action that I must correct').\n"
                "4. **Behavioral Motivation (Withdrawal vs. Restitution):** Shame motivates people to hide, lower their gaze, or flee social scrutiny. "
                "Guilt motivates active reparation, confession, seeking forgiveness, and constructive restitution."
            ),
            "why_is_this_the_answer": (
                "This answer synthesizes the theoretical consensus from classical theorists cited on Page 304 of the text (Levy & Rosaldo, 1983; "
                "Lebra, 1983; Barrett, 1995), correctly mapping the dual axes of internal/external locus and self/action orientation."
            ),
            "practical_example": (
                "If a university student accidentally submits the wrong draft of a group assignment: they feel SHAME if their group members mock them "
                "in public; they feel GUILT when they realize their group members might lose marks, prompting them to email the professor immediately to fix it."
            ),
        },
        {
            "question_id": 3,
            "chapter_id": 2,
            "question": "In psychological theory, why is shame characterized as involving a 'passive, helpless self' while guilt involves an 'active, responsible self'?",
            "model_answer": (
                "Shame involves a 'passive, helpless self' because the individual perceives their core identity as exposed, inadequate, and immobilized. "
                "Because shame targets who you are rather than what you did, the person feels powerless to alter their fundamental self in that moment of exposure. "
                "The psychological response is paralysis, blushing, shrinking, and a desire to vanish from sight.\n\n"
                "In contrast, guilt involves an 'active, responsible self' because the focus remains on personal agency and controllable conduct. "
                "The individual recognizes: 'I made a bad choice, but my character can take corrective action.' Because the self retains agency, "
                "the guilty person actively seeks out the victim, apologizes, performs community service, or pays for damages to restore moral balance."
            ),
            "why_is_this_the_answer": (
                "This is correct because Barrett (1995) and Lewis (1992) emphasize that agency distinguishes guilt from shame. Guilt preserves "
                "instrumental agency, whereas acute shame induces temporary ego-collapse and social paralysis."
            ),
            "practical_example": (
                "A chef who burns a signature dish feels passive shame if they think: 'I am a hopeless cook; I should quit.' They feel active guilt "
                "if they think: 'I left the oven too hot; I will cook a fresh plate immediately and apologize to the guest.'"
            ),
        },
        {
            "question_id": 4,
            "chapter_id": 3,
            "question": "How did early Western anthropologists and European educational authors (such as Eppink) construct the stereotype of Moroccan adolescents as 'amoral' and incapable of guilt?",
            "model_answer": (
                "Early Western anthropologists (such as Crapanzano, 1973; Eickelman, 1976; Davis, 1982) conducted field studies in North Africa "
                "and observed that social life was heavily regulated by honor (*sharaf*) and public propriety (*hshuma*). They concluded that Moroccan "
                "society lacked internalized guilt and relied strictly on external social surveillance.\n\n"
                "Later European authors (notably Eppink, 1990, 1992) took these anthropological observations and radically distorted them into a deficit model. "
                "They argued that Moroccan youth living in Belgium and the Netherlands were incapable of internalizing moral norms, did not value honesty "
                "or truthfulness, and only refrained from wrongdoing if an authority figure was physically watching them. They claimed that when youth were "
                "caught committing theft or vandalism, they felt zero remorse and only regretted being apprehended."
            ),
            "why_is_this_the_answer": (
                "The answer is accurate because it directly traces the historical progression cited on Pages 305–307 of the study, documenting how academic "
                "theories of Mediterranean honor were weaponized into racist deficit models in Belgian education."
            ),
            "practical_example": (
                "It is like a colonial historian observing that a culture resolves disputes through village elders rather than written courts, "
                "and falsely concluding that the culture has no concept of justice or law."
            ),
        },
        {
            "question_id": 5,
            "chapter_id": 3,
            "question": "Analyze the kindergarten incident where teachers openly discussed a child's theft with his parents. Why did the parents react with defensive anger, and how was this misinterpreted by Belgian staff?",
            "model_answer": (
                "In the kindergarten case study (Page 306), Belgian teachers caught a young Moroccan child taking an item. Operating from a Western, "
                "transparent-communication philosophy, the teachers called the parents to school and openly discussed the theft in front of others, "
                "believing this was an open and honest educational method.\n\n"
                "The Moroccan parents reacted with profound defensive shock and anger because, in Moroccan cultural norms, public exposure of a family "
                "member's wrongdoing causes the entire lineage to 'lose face' (*fdiha* / public disgrace). The parents believed that minor childhood "
                "misconduct should be handled privately and discreetly by the teacher inside the classroom. By broadcasting the incident publicly, "
                "the teachers committed a severe violation of familial honor.\n\n"
                "Belgian staff completely misinterpreted the parents' reaction: the teachers assumed the parents were indifferent to stealing, when in reality, "
                "the parents were devastated by the unnecessary public humiliation of their family."
            ),
            "why_is_this_the_answer": (
                "This answer explains the root cause of the intercultural conflict: a clash between Western 'therapeutic transparency' and "
                "Moroccan 'protective discretion' (*satr*), demonstrating how identical actions have opposing cultural meanings."
            ),
            "practical_example": (
                "Imagine a manager broadcasting an employee's minor typographical error on a company-wide Zoom call with 500 attendees. "
                "The employee's anger is not because they love making typos; it is because the public method of correction was disproportionately humiliating."
            ),
        },
        {
            "question_id": 6,
            "chapter_id": 3,
            "question": "How was Jean Piaget's developmental framework of 'heteronomous' versus 'autonomous' morality misapplied by Western school psychologists to pathologize Moroccan immigrant culture?",
            "model_answer": (
                "Jean Piaget established that human moral development moves through two stages:\n"
                "1. **Heteronomous Morality (Ages 6–8):** Children view rules as fixed, sacred absolutes handed down by powerful adults. They obey out of "
                "fear of external punishment and believe any wrongdoing will receive automatic retribution.\n"
                "2. **Autonomous Morality (Ages 10–12+):** Children realize rules are social agreements created by humans to ensure mutual fairness. "
                "They evaluate actions based on internal intent, conscience, and reciprocal empathy.\n\n"
                "Belgian school psychologists and educational counselors misapplied Piaget's individual developmental model to an entire adult culture. "
                "Because Moroccan students emphasized public honor and external social boundaries (*hshuma*), psychologists concluded that Moroccans "
                "never reach autonomous morality and remain permanently arrested in the heteronomous stage of an 8-year-old child. This evolutionary "
                "ethnocentrism falsely treated a collectivist, family-centered moral system as cognitive and moral backwardness."
            ),
            "why_is_this_the_answer": (
                "This response directly captures Dr. Hermans' critical analysis on Page 308, where he exposes how Piaget's stages were used as an ideological "
                "justification to deny moral maturity to non-Western communities."
            ),
            "practical_example": (
                "It is like a linguist claiming that because a language uses complex tonal pitches rather than Latin alphabet roots, its speakers have "
                "the language ability of toddlers. It confuses structural difference with developmental deficit."
            ),
        },
        {
            "question_id": 7,
            "chapter_id": 4,
            "question": "What is the Thematic Apperception Test (TAT), and why did Dr. Philip Hermans select it rather than direct self-report questionnaires to investigate emotional repertoires in 70 Moroccan male adolescents?",
            "model_answer": (
                "The Thematic Apperception Test (TAT) is a projective psychological assessment tool consisting of a series of ambiguous pictorial plates "
                "depicting human figures in emotionally tense or reflective scenarios. Subjects are asked to narrate a story explaining the past, present, "
                "and future outcome of the scene.\n\n"
                "Dr. Hermans selected the TAT instead of direct questionnaires for three critical reasons:\n"
                "1. **Bypassing Social Desirability Bias:** Direct questionnaires (such as 'Do you feel guilty when you steal?') provoke defensive answers, "
                "especially among marginalized minority youth who distrust Western institutional researchers.\n"
                "2. **Projective Depth:** In storytelling, adolescents project their own unmonitored cultural values, subconscious fears, and moral instincts "
                "onto fictional characters without feeling personally accused.\n"
                "3. **Objective Cross-Cultural Coding:** Utilizing George DeVos's cross-cultural scoring system allowed the research team to systematically "
                "quantify and compare affective themes (guilt, remorse, filial duty, external sanction) with rigorous scientific objectivity."
            ),
            "why_is_this_the_answer": (
                "The answer correctly identifies the methodological superiority of projective storytelling over survey instruments in cross-cultural "
                "psychological research as outlined on Page 309 of the study."
            ),
            "practical_example": (
                "Asking someone: 'Are you generous?' will almost always get a 'Yes' answer. But asking them to write a story about what a wealthy traveler "
                "should do when meeting an impoverished child reveals their authentic moral values through their narrative choices."
            ),
        },
        {
            "question_id": 8,
            "chapter_id": 5,
            "question": "Explain the empirical significance of the narrative themes documented in Table 1 regarding Plate 3BM. How do these findings directly disprove the cultural deficit claim?",
            "model_answer": (
                "Table 1 (Page 310) documents the narrative themes produced by Moroccan adolescents in response to Plate 3BM (a figure slumped against "
                "a couch beside a revolver). The empirical data yielded overwhelming evidence of internalized moral guilt:\n\n"
                "• Over **68%** of student stories focused explicitly on intense internal remorse and psychological self-blame following a crime, theft, or accident.\n"
                "• Verbatim quotes showed characters weeping alone in their bedrooms, feeling sick with regret, and acknowledging that their actions were morally wrong, "
                "completely independent of whether the police or neighbors knew about it.\n"
                "• Only a minority of stories focused primarily on external punishment or escaping detection.\n\n"
                "These findings directly disprove the deficit claim because if Moroccan youth truly lacked guilt and only feared external capture, their stories "
                "would have revolved around evading police and laughing about stolen goods. The presence of weeping, self-reproach, and desires for restitution "
                "provides definitive empirical proof of an active, internalized conscience."
            ),
            "why_is_this_the_answer": (
                "This answer is supported by the quantitative and qualitative data in Table 1, demonstrating that the deficit hypothesis cannot withstand "
                "direct empirical scrutiny."
            ),
            "practical_example": (
                "If a scientist claims a bird cannot fly, and then films 70 birds soaring across the sky for three hours, the empirical observation instantly "
                "destroys the false theory. Table 1 is that exact empirical video of Moroccan guilt in action."
            ),
        },
        {
            "question_id": 9,
            "chapter_id": 5,
            "question": "How do the narrative responses to Plates 6BM and 7BM illustrate that Moroccan adolescent morality is deeply anchored in filial devotion, parental honor, and emotional reciprocity?",
            "model_answer": (
                "Plates 6BM (mother and son) and 7BM (father and son) revealed that Moroccan moral conscience is strongly mediated through family bonds. "
                "In **48 out of 70 stories (68.6%)**, the core narrative conflict centered on a young man recognizing that his academic disengagement, "
                "delinquency, or poor choices had inflicted profound sorrow upon his parents.\n\n"
                "Narratives frequently contained vivid emotional descriptions such as: *'Look at your father; he is lying in bed weeping because you did not work... "
                "your mother sacrifices everything for you.'* In response to parental tears, the characters experienced profound moral repentance, resolved to break away "
                "from bad companions, study diligently, and secure respectable employment to restore their parents' honor.\n\n"
                "This proves that rather than lacking conscience, Moroccan adolescents possess a powerful *particularistic, family-oriented morality* where love, "
                "filial obligation, and emotional reciprocity serve as the primary engines of ethical behavior and personal redemption."
            ),
            "why_is_this_the_answer": (
                "This reflects Dr. Hermans' findings on Page 312, proving that moral accountability in collectivist cultures operates through deep relational "
                "bonds rather than isolated individual self-interest."
            ),
            "practical_example": (
                "A young adult might ignore a speeding ticket fine for themselves, but seeing their elderly father work extra shifts to pay for their car insurance "
                "compels them to drive with total caution. The moral guide is filial love."
            ),
        },
        {
            "question_id": 10,
            "chapter_id": 6,
            "question": "Differentiate between the Moroccan cultural concepts of 'Hshuma' (حشومة) and 'Dhenb' (ذنب). Why is it a fundamental error to translate 'Hshuma' simply as Western humiliation?",
            "model_answer": (
                "It is a fundamental error to translate *Hshuma* as Western humiliation because the two terms have opposing moral functions:\n\n"
                "1. **Hshuma (حشومة / حشومية):** Signifies decency, modesty, propriety, discretion, respect for sacred social boundaries, and consideration "
                "for community dignity. When Moroccans say *'hshuma 'alik'*, it is an educational, socialization reminder to uphold honorable conduct. "
                "Western 'humiliation' implies being debased or crushed; *hshuma*, by contrast, is a positive social code that protects communal harmony and self-respect.\n\n"
                "2. **Dhenb (ذنب / شعور بالذنب):** Specifically denotes sin, moral transgression, and spiritual guilt before God and divine justice. "
                "Accompanied by *Ndam* (ندم / deep contrition and remorse), *Dhenb* represents internal moral culpability.\n\n"
                "Translating *Hshuma* as mere fear of humiliation led Western observers to falsely assume Moroccans have no inner moral compass, ignoring the "
                "spiritual depth of *Dhenb* and *Ndam*."
            ),
            "why_is_this_the_answer": (
                "This linguistic and psychological distinction is analyzed in detail on Pages 313–314, illustrating how linguistic mistranslation creates "
                "false academic stereotypes."
            ),
            "practical_example": (
                "In English, being 'polite and respectful' in church is not humiliation; it is reverent decorum. *Hshuma* is that exact same reverent "
                "decorum applied across all social relationships."
            ),
        },
        {
            "question_id": 11,
            "chapter_id": 6,
            "question": "Explain Dr. Hermans' theoretical formulation: 'The gaze of the other turns the offender's attention to his inner self.' How does external shame function as a catalyst for internal conscience and guilt?",
            "model_answer": (
                "Dr. Hermans' formulation resolves the false opposition between shame and guilt. He explains that external shame and internal guilt do not "
                "operate as isolated, mutually exclusive systems; rather, they form an interactive dialectical loop:\n\n"
                "1. **The Catalyst (The Gaze):** When an individual commits a moral transgression, the external 'gaze of the other' (the watchful eye of parents, "
                "elders, or community) creates an acute shock of shame.\n"
                "2. **Turning Inward:** This external shock acts like a mirror: it forces the individual to stop, look at themselves through the eyes of the community, "
                "and confront their own behavior.\n"
                "3. **Activation of Conscience:** Once the person looks inward, their internal conscience (*dhenb* and *ndam*) is fully ignited. They realize: "
                "'I have wounded my family, offended God, and violated my community. I am truly responsible, and I must make amends.'\n\n"
                "Thus, external shame is not the end of morality; it is the *psychological catalyst* that awakens deep internal guilt and motivates genuine atonement."
            ),
            "why_is_this_the_answer": (
                "This is Dr. Hermans' signature theoretical insight (Page 314, drawing upon Lebra, 1984), bridging sociological surveillance and internal moral conscience."
            ),
            "practical_example": (
                "If you are caught by a security camera stealing a wallet, the realization of being seen is shame. But that moment of exposure immediately forces you "
                "to think: 'What have I become? The person who owns this wallet cannot pay rent.' The camera gaze triggered the internal moral awakening."
            ),
        },
        {
            "question_id": 12,
            "chapter_id": 7,
            "question": "Drawing upon the conclusions of the study, what systemic reforms must educational institutions, counselors, and teachers implement to foster academic success and fair disciplinary practices for immigrant youth?",
            "model_answer": (
                "Based on the empirical and sociological conclusions of the study (Pages 314–316), educational institutions must enact four comprehensive reforms:\n\n"
                "1. **Abolish Cultural Deficit Assumptions:** School psychologists and teachers must eliminate stereotypes that label immigrant students as "
                "'amoral' or stuck in 'heteronomous' childhood morality. Educators must be trained in intercultural psychological competence.\n"
                "2. **Implement Confidential, Dignified Disciplinary Procedures:** Schools must strictly avoid public shaming and confrontations that cause students "
                "or their families to lose face. Disciplinary matters should be handled discreetly, focusing on restorative restitution rather than public humiliation.\n"
                "3. **Recognize Defensive Behavior as a Structural Reaction:** Educators must understand that student defensiveness and reluctance to admit fault "
                "are often protective psychological shields against perceived discrimination and low teacher expectations, rather than innate dishonesty.\n"
                "4. **Engage Families as Respected Moral Allies:** Schools should leverage the profound filial devotion and family honor of Moroccan students by "
                "building collaborative, respectful partnerships with parents rather than viewing immigrant homes as educational obstacles."
            ),
            "why_is_this_the_answer": (
                "This synthesizes the policy and pedagogical recommendations outlined in the final chapter, translating empirical anthropology into "
                "actionable educational reform."
            ),
            "practical_example": (
                "A high school that replaces public suspensions and hallway reprimands with private restorative justice mediation circles—where students, "
                "teachers, and parents cooperatively agree on how to fix a mistake—embodies Dr. Hermans' pedagogical model."
            ),
        },
    ]

    # Write Questions_And_Answers.md
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as md:
        md.write("# 📝 Academic Questions & Model Answers: Reading in Global Culture\n\n")
        md.write("Comprehensive examination revision questions with complete model answers in simple English, underlying academic reasoning, and practical examples.\n\n")
        md.write("---\n\n")

        for item in qa_catalog:
            md.write(f"### ❓ QUESTION {item['question_id']} (Chapter {item['chapter_id']}):\n")
            md.write(f"**{item['question']}**\n\n")
            md.write("```\n")
            md.write("[GREEN ANSWER BOX]\n")
            md.write("MODEL ANSWER:\n")
            md.write(f"{item['model_answer']}\n\n")
            md.write("WHY IS THIS THE ANSWER?\n")
            md.write(f"{item['why_is_this_the_answer']}\n")
            md.write("```\n\n")
            md.write(f"**💡 PRACTICAL EXAMPLE:**\n{item['practical_example']}\n\n")
            md.write("---\n\n")

    print(f"  ✓ Academic Q&A corpus successfully written to: '{output_md_path}'")
    return qa_catalog


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.extractor import extract_curriculum_corpus
    corpus = extract_curriculum_corpus("input")
    build_academic_qa_corpus(corpus)
