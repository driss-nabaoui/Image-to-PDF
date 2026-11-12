"""
================================================================================
  SIMPLE EXPLANATION ENGINE MODULE (src/explanation_engine.py)
================================================================================
  Generates clear, comprehensive explanations in simple English for every
  academic concept, definition, and theoretical model in the curriculum.
================================================================================
"""

import os
from typing import List, Dict, Any


def build_curriculum_explanations(corpus: Dict[str, Any], output_md_path: str = "output/Explained_Study_Notes.md") -> List[Dict[str, Any]]:
    """
    Constructs comprehensive simple English explanations for each chapter in the corpus.
    Applies real-life analogies, breaks down complex jargon, and generates 'What You Should Remember'.
    """
    print("\n[2/4] Generating simple English pedagogical explanations...")

    explanations_catalog = [
        {
            "chapter_id": 1,
            "chapter_title": "Historical & Demographic Background of Moroccan Migration",
            "explanations": [
                {
                    "concept": "Post-WWII Labor Migration & Bilateral Treaties",
                    "simple_text": (
                        "After the Second World War in the 1950s and 1960s, countries like Belgium were rebuilding their factories, "
                        "coal mines, and construction projects. They needed many workers, but they did not have enough local people to do "
                        "these physically hard jobs. So, the Belgian government made formal agreements (bilateral treaties) with the Moroccan "
                        "government to bring Moroccan workers to Belgium. These workers were originally called 'guest workers' because European "
                        "governments expected them to work for a few years and then return home. However, people are human beings, not machines: "
                        "they built lives, brought their wives and children through family reunification, and stayed permanently."
                    ),
                    "practical_example": (
                        "Imagine a student who travels to another city for a summer job. At first, they only plan to stay for two months. "
                        "However, they find stable work, make friends, bring their family to live with them, and end up staying for 40 years. "
                        "This is exactly how temporary guest workers became permanent Belgian citizens."
                    ),
                    "why_it_matters": "Students must understand that Moroccan migration was actively invited by European governments for economic reasons, not an accidental or illegal arrival.",
                },
                {
                    "concept": "Educational Tracking & The 'B-Stroom' Pipeline",
                    "simple_text": (
                        "Educational tracking means that schools separate students into different academic paths when they are young. "
                        "In Belgium, there is a general academic path (which prepares students for university) and a vocational path "
                        "(called 'B-stroom', which prepares students for manual trades like plumbing or mechanics). Research shows that "
                        "Moroccan students were systematically pushed into the lower vocational tracks very early, even when they were capable "
                        "of academic success. Teachers and counselors often assumed that because a student's parents did not speak French or Dutch, "
                        "the student could not succeed in university tracks."
                    ),
                    "practical_example": (
                        "Think of an airport where people with foreign passports are automatically sent to a slower, secondary line before "
                        "anyone even inspects their travel documents. In schools, educational tracking acted like this automatic diversion, "
                        "limiting students' future university opportunities."
                    ),
                    "why_it_matters": "It explains why academic achievement gaps are caused by unfair school sorting systems, rather than a lack of intelligence or ambition in students.",
                },
            ],
            "what_to_remember": [
                "Moroccan migration to Belgium was initiated by 1964 bilateral labor agreements to solve factory and mining labor shortages.",
                "The 'guest worker' idea failed because migrants brought their families and established permanent communities.",
                "Second- and third-generation youth were born in Belgium but faced structural tracking into low-prestige vocational school tracks.",
            ],
        },
        {
            "chapter_id": 2,
            "chapter_title": "Psychological Taxonomy: Shame vs. Guilt",
            "explanations": [
                {
                    "concept": "The Fundamental Difference Between Shame and Guilt",
                    "simple_text": (
                        "Psychologists distinguish between shame and guilt based on where the punishment comes from and how you feel about yourself:\n"
                        "• SHAME is an EXTERNAL emotion. It happens when other people see you fail, break a social rule, or look foolish. "
                        "In shame, other people are 'spectators' watching you. You feel that your ENTIRE SELF is small, weak, and defective. "
                        "When people feel shame, their natural reaction is to hide, cover their face, or disappear.\n"
                        "• GUILT is an INTERNAL emotion. It happens when your own conscience tells you that you did something morally wrong, "
                        "even if nobody saw you. In guilt, other people are 'sufferers' who were hurt by what you did. You feel bad about "
                        "your SPECIFIC ACTION, not your whole self. When people feel guilt, their natural reaction is to apologize, fix the mistake, "
                        "and make amends."
                    ),
                    "practical_example": (
                        "If you accidentally spill coffee on a classmate's laptop in a crowded library:\n"
                        "- You feel SHAME when everyone in the library stares at you and laughs, making you want to run away.\n"
                        "- You feel GUILT when you realize your classmate lost their important assignment, motivating you to pay for the repairs."
                    ),
                    "why_it_matters": "Understanding this distinction helps university students evaluate whether people act morally because of external social pressure or internal ethical principles.",
                },
                {
                    "concept": "The Passive Self (Shame) vs. The Active Self (Guilt)",
                    "simple_text": (
                        "In psychological theory, shame creates a 'passive, helpless self' because you feel you cannot change who you are. "
                        "You think: 'I am a stupid, bad person.' Guilt, however, creates an 'active, responsible self' because you recognize that "
                        "you chose to commit an action, which means you have the power to repair it. You think: 'I am a good person who made a bad "
                        "choice, and I will fix it.'"
                    ),
                    "practical_example": (
                        "A child who fails a test and cries: 'I am dumb' is experiencing shame. A child who says: 'I did not study enough; "
                        "I will study three hours tonight' is experiencing healthy moral guilt and personal responsibility."
                    ),
                    "why_it_matters": "It explains why shame can cause anger and withdrawal, while guilt leads to constructive personal growth.",
                },
            ],
            "what_to_remember": [
                "Shame is triggered by public exposure and external sanctions (other people as watching spectators).",
                "Guilt is triggered by internal conscience and moral transgression (other people as suffering victims).",
                "Shame attacks the global self ('I am bad'), while guilt evaluates the specific action ('I did something bad').",
                "Both emotions exist universally in all human beings, but cultures express and emphasize them differently.",
            ],
        },
        {
            "chapter_id": 3,
            "chapter_title": "Western Professional Stereotypes & The Distortion of Piaget",
            "explanations": [
                {
                    "concept": "The Deficit Stereotype of 'Amoral Migrants'",
                    "simple_text": (
                        "During the 1980s and 1990s, some Western anthropologists and educators created a harmful stereotype about Moroccan people. "
                        "They claimed that Moroccan culture is purely a 'shame culture' where people only care about being caught by police or neighbors. "
                        "They argued that Moroccan youth do not care about honesty or truth, and feel zero guilt if nobody catches them. "
                        "This is called a 'cultural deficit model'—a biased theory that falsely claims a minority group is morally inferior or backward."
                    ),
                    "practical_example": (
                        "Imagine if a teacher assumed that because an international student comes from another country, they have no internal morals "
                        "and will always cheat on exams unless someone watches them every second. That is an unfair deficit stereotype."
                    ),
                    "why_it_matters": "Students must learn to identify and critique ethnocentric prejudices disguised as academic research.",
                },
                {
                    "concept": "The Kindergarten Case: Public Shaming vs. Loss of Face",
                    "simple_text": (
                        "In a famous case study, Belgian kindergarten teachers caught a small Moroccan child taking a toy. The teachers called the "
                        "parents into school and openly talked about the child's theft in front of others. The teachers thought they were being modern "
                        "and open. But for the Moroccan parents, this was a disaster. In Moroccan culture, exposing a family member's wrongdoing in public "
                        "causes the entire family to 'lose face' (fdiha/hshuma). The parents felt attacked and humiliated. They believed the teachers "
                        "should have punished the child quietly in class rather than dishonoring the family. The teachers completely misread the parents' "
                        "defensive anger as 'they don't care about stealing!'"
                    ),
                    "practical_example": (
                        "If a doctor shouted your private medical issues in the crowded hospital waiting room, you would feel furious and humiliated. "
                        "You wouldn't be angry because you are sick; you would be angry because your private dignity was violated in public."
                    ),
                    "why_it_matters": "Shows how cultural misunderstandings occur when teachers confuse private dignity with a lack of moral concern.",
                },
                {
                    "concept": "How Jean Piaget's Moral Theory Was Misapplied",
                    "simple_text": (
                        "Jean Piaget was a famous Swiss child psychologist who discovered that young children (ages 6 to 8) obey rules because "
                        "they are afraid of adult punishment (called 'heteronomous morality'). As children grow older (ages 10 to 12), they develop "
                        "'autonomous morality'—they understand that rules are based on fairness, cooperation, and internal conscience. "
                        "Belgian school psychologists distorted this theory. They claimed that Moroccan adults never reach autonomous morality "
                        "and remain stuck at the moral level of 8-year-old children! This was an unscientific, colonial insult that treated an entire "
                        "culture as mentally and morally childish."
                    ),
                    "practical_example": (
                        "It is like claiming that because someone plays football using different defensive tactics, they do not know the rules of sports. "
                        "Moroccan morality is not childish; it is rooted in family honor and religious accountability rather than secular Western individualism."
                    ),
                    "why_it_matters": "Teaches students how legitimate scientific theories can be weaponized to justify discrimination against immigrants.",
                },
            ],
            "what_to_remember": [
                "Deficit models falsely pathologized Moroccan students as lacking conscience and honesty.",
                "The kindergarten incident highlights the difference between private discipline and public familial humiliation ('loss of face').",
                "Piaget's stages of heteronomous vs. autonomous morality were ethnocentrically abused to treat minority cultures as intellectually childish.",
            ],
        },
        {
            "chapter_id": 4,
            "chapter_title": "Empirical Research Methodology: The Cross-Cultural TAT",
            "explanations": [
                {
                    "concept": "What is the Thematic Apperception Test (TAT)?",
                    "simple_text": (
                        "The Thematic Apperception Test (TAT) is a psychological projective test. Instead of answering direct yes/no questions, "
                        "a person is shown black-and-white drawings showing people in ambiguous, dramatic situations (for example, a person crying "
                        "next to a gun, or a son talking to his mother). The person is asked: 'Tell me a story about what is happening here, what led "
                        "up to this, and how it will end.' Because the picture is unclear, the person projects their own real emotions, cultural values, "
                        "and moral beliefs into the story without realizing it."
                    ),
                    "practical_example": (
                        "Think of looking at shapes in clouds. Two people look at the same cloud: one sees an eagle, and the other sees a dragon. "
                        "What you see reveals what is already inside your imagination. Similarly, what a student sees in a TAT drawing reveals their real conscience."
                    ),
                    "why_it_matters": "Projective tests allow researchers to test deep feelings of guilt and remorse without relying on direct survey questions.",
                },
                {
                    "concept": "George DeVos's Cross-Cultural Scoring Method",
                    "simple_text": (
                        "George DeVos was a pioneer in cross-cultural psychology at UC Berkeley. He created a scientific system to score TAT stories "
                        "across different world cultures. Instead of assuming everyone thinks like an American or Belgian, his system systematically "
                        "counts specific emotional themes: Did the character feel remorse? Did they worry about their mother's honor? Did they want to "
                        "apologize? Dr. Hermans used DeVos's method to objectively measure guilt in 70 Moroccan male teenagers."
                    ),
                    "practical_example": (
                        "It is like a standardized referee scoring sheet in sports: every time a player displays a specific move (like remorse, "
                        "weeping, or seeking forgiveness), it is officially recorded and verified."
                    ),
                    "why_it_matters": "Guarantees that Dr. Hermans' findings are backed by empirical scientific data, not personal opinions.",
                },
            ],
            "what_to_remember": [
                "The TAT uses ambiguous visual drawings to uncover subconscious feelings and cultural moral values.",
                "Dr. Hermans tested 70 Moroccan male adolescents (ages 15–20) in Flemish and Brussels secondary schools.",
                "DeVos's scoring manual provided an objective, cross-culturally validated psychological metric.",
            ],
        },
        {
            "chapter_id": 5,
            "chapter_title": "Empirical Evidence & Quantitative Findings: Disproving the Myth",
            "explanations": [
                {
                    "concept": "What Table 1 (Plate 3BM) Proves About Guilt",
                    "simple_text": (
                        "Plate 3BM shows a figure lying on a bench with a revolver on the floor. If the Belgian teachers were right and Moroccans "
                        "only care about getting caught, the Moroccan students would have said: 'He is hiding from the police so he doesn't go to jail.' "
                        "Instead, the overwhelming majority of students (over 68%) created stories of intense INTERNAL GUILT. In their stories, the character "
                        "cries alone in his room, feels sick with regret for stealing or hurting a friend, and blames himself. This provided rock-solid "
                        "scientific proof that Moroccan youth feel deep, internal moral guilt."
                    ),
                    "practical_example": (
                        "If someone accidentally scratches a parked car and leaves a note with their phone number to pay for it when nobody was looking, "
                        "that proves they have an internal conscience. The students' stories demonstrated this exact same internal moral compass."
                    ),
                    "why_it_matters": "Directly invalidates 30 years of biased anthropological assertions that Moroccan culture has no concept of guilt.",
                },
                {
                    "concept": "Filial Remorse: Maternal Tears & The Weeping Father (Plates 6BM & 7BM)",
                    "simple_text": (
                        "In Western psychology, guilt is often framed in solitary, individualistic terms ('I broke my personal code'). "
                        "In Moroccan culture, guilt is deeply connected to family love and filial respect. In 48 out of 70 stories (almost 70%), "
                        "the teenagers described sons feeling immense moral anguish because they made their parents cry. One student wrote: "
                        "'Look at your father, he is in bed crying because you failed in school... Because of his mother's sorrow, the son changes his "
                        "life, finds an honest job, and restores his family's pride.' This proves that moral reformation is motivated by deep love for parents."
                    ),
                    "practical_example": (
                        "A student might not care about losing points on an exam for themselves, but seeing their mother work two cleaning jobs to pay "
                        "for their tuition makes them study all night. That is filial love operating as a powerful moral engine."
                    ),
                    "why_it_matters": "Shows that collectivist, family-centered morality is just as powerful and ethical as Western individualist morality.",
                },
            ],
            "what_to_remember": [
                "Table 1 proves that over 68% of Moroccan youth narratives on Plate 3BM expressed internal guilt, tears, and self-blame.",
                "Table 2 shows that on Plate 13MF, murder/conflict provoked intense remorse, contrition, and thoughts of atonement.",
                "Plates 6BM and 7BM revealed that moral conscience is strongly mediated through love and responsibility toward parents.",
            ],
        },
        {
            "chapter_id": 6,
            "chapter_title": "Linguistic & Cultural Codification: 'Hshuma' vs. 'Dhenb'",
            "explanations": [
                {
                    "concept": "The Real Meaning of 'Hshuma' (حشومة)",
                    "simple_text": (
                        "Westerners often translate 'hshuma' as 'shame', thinking it means humiliation or feeling inferior. In Moroccan culture, "
                        "this is completely inaccurate! 'Hshuma' actually means modesty, respect, decency, politeness, and discretion. "
                        "When someone has 'hshumiya', it means they are well-raised, considerate of other people's feelings, and behave with dignity. "
                        "Saying 'hshuma 'alik' to someone is a gentle reminder: 'Please remember your manners and respect our community.'"
                    ),
                    "practical_example": (
                        "It is like a person who dresses appropriately at a funeral or lowers their voice in a quiet hospital out of respect for grieving families. "
                        "They are not doing it out of humiliation; they are doing it out of dignity and respect ('hshuma')."
                    ),
                    "why_it_matters": "Prevents educators from viewing 'hshuma' as a primitive emotion, showing it is a sophisticated code of social ethics.",
                },
                {
                    "concept": "The Religious Dimensions of Guilt: 'Dhenb' (ذنب) and 'Ndam' (ندم)",
                    "simple_text": (
                        "When a Moroccan person feels guilt, they use the words 'Dhenb' (sin / breaking divine law) and 'Ndam' (remorse / contrition). "
                        "Because Moroccan culture is deeply influenced by Islamic ethics, moral wrongdoing is seen as a spiritual violation against God "
                        "and divine justice, not just a secular mistake. That is why Moroccans do not use Western clinical psychology words to talk about guilt; "
                        "they express it through spiritual and religious values."
                    ),
                    "practical_example": (
                        "A patient might describe sadness as 'having a heavy heart' rather than saying 'I am suffering from clinical depression.' "
                        "The emotion is 100% real, but the cultural vocabulary is spiritual and poetic rather than medical."
                    ),
                    "why_it_matters": "Explains why Western psychologists who only looked for secular terms failed to see Moroccan guilt.",
                },
                {
                    "concept": "The Dialectic of the Gaze: How Shame Wakes Up Conscience",
                    "simple_text": (
                        "Dr. Hermans discovered that in Moroccan culture, shame and guilt are not enemies; they work together like two sides of a coin! "
                        "When other people see you do something wrong (the external 'gaze of the community'), it causes a flash of shame. "
                        "That flash of shame forces you to stop and look inside yourself. Once you look inside, your internal conscience (guilt) wakes up, "
                        "and you realize: 'I hurt someone; I must make amends and fix this.' Shame is the mirror; guilt is the reflection inside."
                    ),
                    "practical_example": (
                        "Imagine you are speeding on the highway and suddenly see your neighbor in the next car. That momentary shock makes you look at your "
                        "speedometer, realize you are driving dangerously, and slow down to drive safely. The external glance awakened your internal judgment."
                    ),
                    "why_it_matters": "This is Dr. Hermans' most famous theoretical contribution to cross-cultural psychology.",
                },
            ],
            "what_to_remember": [
                "Hshuma is not humiliation; it is a positive social ethic of respect, decency, and modesty.",
                "Dhenb represents moral/religious transgression, while Ndam represents authentic contrition and remorse.",
                "The 'Gaze of the Other' serves as the catalyst that activates internal self-examination and moral responsibility.",
            ],
        },
        {
            "chapter_id": 7,
            "chapter_title": "Sociostructural Realities & Intercultural Pedagogical Reforms",
            "explanations": [
                {
                    "concept": "Why Moroccan Students Act Defensive in Western Schools",
                    "simple_text": (
                        "When teachers ask Moroccan students: 'Why did you get in trouble?' the students often say: 'It wasn't my fault; the teacher "
                        "hates me.' Western teachers call this 'lacking personal responsibility.' But Dr. Hermans explains the sociological reality: "
                        "Moroccan youth face constant discrimination in housing, jobs, and schools. When you are surrounded by an unfair system, "
                        "admitting fault makes you feel completely defenseless. Denying fault is a psychological shield (a defense mechanism) used "
                        "to protect one's self-esteem against a hostile environment."
                    ),
                    "practical_example": (
                        "In a soccer match, if the referee has been unfairly giving your team yellow cards all game, you are much less likely to admit "
                        "to an accidental foul because you know the referee is already biased against you. You put up your guard."
                    ),
                    "why_it_matters": "Helps educators understand student defensiveness as a response to systemic bias rather than a character defect.",
                },
                {
                    "concept": "How Intercultural Schools Should Handle Discipline",
                    "simple_text": (
                        "To create successful, fair schools, educators must adopt four key practices:\n"
                        "1. **Never publicly humiliate students or their families:** Discipline must be private and respectful so nobody loses face.\n"
                        "2. **Recognize family loyalty:** Involve parents as respected partners rather than judging them.\n"
                        "3. **Stop using deficit stereotypes:** Treat immigrant students as morally mature individuals with rich emotional lives.\n"
                        "4. **Encourage restitution instead of shame:** Focus on helping the student fix the harm they caused rather than making them feel defective."
                    ),
                    "practical_example": (
                        "A principal who pulls a student aside into a private office, speaks warmly, and says: 'I know you are better than this; "
                        "how can we solve this together?' will achieve 100 times better results than a principal who screams at the student in the hallway."
                    ),
                    "why_it_matters": "Provides practical, actionable policies for university students studying education, psychology, and social work.",
                },
            ],
            "what_to_remember": [
                "Student defensiveness is often a psychological shield against real institutional discrimination and low teacher expectations.",
                "Effective intercultural education requires private, respectful discipline that protects family dignity.",
                "Restorative justice (making amends) works far better than public shaming and punitive tracking.",
            ],
        },
    ]

    # Write Explained_Study_Notes.md
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as md:
        md.write("# 💡 Explained Study Notes: Reading in Global Culture\n\n")
        md.write("Comprehensive pedagogical explanations written in Simple English with practical examples, analogies, and revision summaries.\n\n")
        md.write("---\n\n")

        for ch in explanations_catalog:
            md.write(f"## Chapter {ch['chapter_id']}: {ch['chapter_title']}\n\n")
            for item in ch["explanations"]:
                md.write(f"### 📌 Academic Concept: {item['concept']}\n\n")
                md.write(f"**SIMPLE EXPLANATION:**\n{item['simple_text']}\n\n")
                md.write(f"**PRACTICAL REAL-WORLD EXAMPLE:**\n{item['practical_example']}\n\n")
                md.write(f"**WHY IT MATTERS FOR UNIVERSITY STUDENTS:**\n{item['why_it_matters']}\n\n")
                md.write("```\n")
                md.write(f"[BLUE EXPLANATION BOX] Concept: {item['concept']}\n")
                md.write("```\n\n")
            
            md.write("### 🧠 WHAT YOU SHOULD REMEMBER:\n")
            for point in ch["what_to_remember"]:
                md.write(f"- {point}\n")
            md.write("\n---\n\n")

    print(f"  ✓ Explained study notes successfully written to: '{output_md_path}'")
    return explanations_catalog


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.extractor import extract_curriculum_corpus
    corpus = extract_curriculum_corpus("input")
    build_curriculum_explanations(corpus)
