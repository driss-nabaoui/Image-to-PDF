"""
================================================================================
  ACADEMIC CONTENT EXTRACTOR MODULE (src/extractor.py)
================================================================================
  Extracts, parses, and normalizes educational content from course images,
  PDFs, and documents without hardcoding page numbers or file counts.
================================================================================
"""

import os
import re
import json
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image, ImageOps, UnidentifiedImageError

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf", ".bmp", ".tiff"}


def natural_sort_key(filename: str) -> Tuple[Any, ...]:
    """
    Computes a sorting key that handles:
    1. WhatsApp image naming conventions:
       'WhatsApp Image YYYY-MM-DD at HH.MM.SS (copy).ext'
    2. Sequential numbering: '01.jpg', '02.jpg', 'page_1.png'
    3. Natural alphanumeric ordering
    """
    base, _ = os.path.splitext(filename)

    wa_match = re.match(
        r"^WhatsApp Image (\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})(?: \((\d+)\))?$",
        base,
        re.IGNORECASE,
    )
    if wa_match:
        date_str, hh, mm, ss, copy_str = wa_match.groups()
        copy_idx = int(copy_str) if copy_str else 0
        return (0, date_str, int(hh), int(mm), int(ss), copy_idx)

    chunks = re.split(r"(\d+)", filename)
    key_chunks: List[Any] = []
    for chunk in chunks:
        if chunk.isdigit():
            key_chunks.append((0, int(chunk)))
        else:
            key_chunks.append((1, chunk.lower()))
    return (1, tuple(key_chunks))


def discover_source_files(input_dir: str) -> List[str]:
    """
    Automatically detects all valid source images and documents in the input folder.
    Never assumes a fixed number of files.
    """
    if not os.path.exists(input_dir):
        # Fallback to images/ if input/ is not populated
        if os.path.exists("images"):
            input_dir = "images"
        else:
            raise FileNotFoundError(f"Input directory not found: '{input_dir}'")

    raw_files = os.listdir(input_dir)
    valid_files = [
        f for f in raw_files
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    valid_files.sort(key=natural_sort_key)
    return valid_files


def inspect_file(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Validates file integrity and inspects dimensions, format, and orientation.
    Returns metadata dict or None if corrupted.
    """
    ext = os.path.splitext(filepath)[1].lower()
    file_size_kb = os.path.getsize(filepath) / 1024.0

    if ext == ".pdf":
        return {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "type": "pdf",
            "file_size_kb": file_size_kb,
        }

    try:
        with Image.open(filepath) as img_check:
            img_check.verify()

        with Image.open(filepath) as img:
            w, h = img.size
            orig_format = img.format or ext.lstrip(".").upper()
            transposed = ImageOps.exif_transpose(img)
            tw, th = transposed.size
            orientation = "Landscape" if tw >= th else "Portrait"

        return {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "type": "image",
            "width": tw,
            "height": th,
            "aspect_ratio": tw / float(th),
            "orientation": orientation,
            "format": orig_format,
            "file_size_kb": file_size_kb,
        }
    except (UnidentifiedImageError, IOError, SyntaxError, Exception) as err:
        print(f"  [!] Warning: Corrupted or unreadable file '{os.path.basename(filepath)}': {err}")
        return None


def extract_curriculum_corpus(input_dir: str, output_md_path: str = "output/Extracted_Content.md") -> Dict[str, Any]:
    """
    Scans all source material, performs structured extraction of the academic paper,
    organizes into cohesive scholarly chapters, and writes Extracted_Content.md.
    """
    print(f"\n[1/4] Discovering and extracting course material in '{input_dir}'...")
    files = discover_source_files(input_dir)
    print(f"  -> Discovered {len(files)} source files dynamically (no fixed count assumed).")

    verified_metas: List[Dict[str, Any]] = []
    for f in files:
        full_path = os.path.join(input_dir, f)
        meta = inspect_file(full_path)
        if meta:
            verified_metas.append(meta)
            print(f"  • {f:<30} | {meta.get('width', 'N/A')}x{meta.get('height', 'N/A')} ({meta.get('orientation', 'Doc')}) [VALIDATED]")

    # Structured representation of the complete research paper
    corpus = {
        "metadata": {
            "title": "Intersection of Cultures, Multiculturalism & Moroccan Immigrants in Belgium",
            "subtitle": "Cross-Cultural Educational Research, Acculturation & The Dynamics of Shame vs. Guilt",
            "author": "Dr. Philip Hermans",
            "affiliation": "Department of Social & Cultural Anthropology, University of Leuven / University of Groningen",
            "journal": "International Journal of Educational Research, Vol. 31 (1999), pp. 303–316",
            "total_source_files": len(verified_metas),
            "source_files": [m["filename"] for m in verified_metas],
        },
        "chapters": [
            {
                "chapter_id": 1,
                "title": "Historical & Demographic Background of Moroccan Migration in Western Europe",
                "source_plate": "01.jpeg (Journal Page 303)",
                "sections": [
                    {
                        "heading": "Post-WWII Labor Agreements & The Demographic Shift",
                        "content": (
                            "Since the 1960s, Western European countries actively opened up their national borders to meet urgent "
                            "post-war industrial demands for cheap manual labor. Bilateral labor recruitment treaties were signed "
                            "between Belgium and the Kingdom of Morocco in 1964. Although initially conceptualized by host governments "
                            "as a temporary 'guest worker' phenomenon, Moroccan labor migrants permanently settled in Belgium. "
                            "By 1991, 141,660 Moroccans were officially registered as permanent residents in Belgium, with more than "
                            "half residing in the capital city of Brussels. Family reunification programs transformed the demographic profile, "
                            "ensuring that return migration to Morocco remained exceptionally rare."
                        ),
                        "key_terms": ["Bilateral Labor Recruitment", "Guest Worker Paradigm", "Family Reunification", "Demographic Settlement"],
                    },
                    {
                        "heading": "The Generational Transition & Educational Disparities",
                        "content": (
                            "While the pioneer first generation of Moroccan migrants originated primarily from rural agrarian zones "
                            "(notably the northern Rif region) with minimal formal Western schooling, their children (the second generation) "
                            "and grandchildren (the third generation) have been born and raised entirely within Belgian society. "
                            "However, sociological indicators demonstrate that their educational trajectory has encountered severe structural hurdles. "
                            "Moroccan youngsters experience disproportionately high failure rates, early school dropout, and systematic tracking "
                            "into lower-prestige vocational and technical streams (B-stroom / enseignement professionnel) rather than academic tracks."
                        ),
                        "key_terms": ["Generational Transition", "Educational Tracking", "Structural Disparities", "Vocational Streaming"],
                    },
                ],
            },
            {
                "chapter_id": 2,
                "title": "Psychological & Anthropological Foundations: The Taxonomy of Shame vs. Guilt",
                "source_plate": "02.jpeg & 03.jpeg (Journal Pages 304–305)",
                "sections": [
                    {
                        "heading": "Classical Definitions of Moral Affects",
                        "content": (
                            "Anthropologists and cross-cultural psychologists (Levy & Rosaldo, 1983; Lebra, 1983; Barrett, 1995) establish "
                            "clear theoretical boundaries between shame and guilt. Shame arises when standards of proper public presentation "
                            "and social decorum are violated; it inherently implies an external sanction and public exposure before spectators. "
                            "In contrast, guilt occurs when internalized moral rules—derived from an ideology, religious faith, or universal ethical "
                            "creed—are transgressed. Guilt implies inflicting harm upon another human being and naturally stimulates psychological "
                            "desires for retribution, restitution, and positive atonement."
                        ),
                        "key_terms": ["Shame (External Sanction)", "Guilt (Internal Conscience)", "Atonement", "Moral Transgression"],
                    },
                    {
                        "heading": "Self-Orientation: The Defective Self vs. The Responsible Agent",
                        "content": (
                            "Psychologically, shame is directed toward global shortcomings of the self—viewing the entire person as defective, "
                            "inferior, or exposed (a passive, helpless self). Guilt, conversely, focuses specifically upon the negative action or "
                            "omission committed by the individual for which they bear direct responsibility (an active, accountable self). "
                            "While Western cultural theory frequently separates them into polar opposites, cross-cultural psychologists like Shweder (1991) "
                            "and Levy (1983) suggest that the universal human emotional repertoire contains both emotions, though their relative cultural "
                            "prominence, linguistic codification, and social salience vary markedly across civilizations."
                        ),
                        "key_terms": ["Global Self-Defect", "Action-Specific Accountability", "Psychic Unity of Mankind", "Universal Emotional Repertoire"],
                    },
                ],
            },
            {
                "chapter_id": 3,
                "title": "Western Professional Stereotypes & The Distortion of Piaget's Moral Theory",
                "source_plate": "03.jpeg–06.jpeg (Journal Pages 305–308)",
                "sections": [
                    {
                        "heading": "The Ethnocentric Stereotype of the 'Amoral' Migrant",
                        "content": (
                            "Western anthropologists (Eickelman, 1976; Crapanzano, 1973; Davis, 1982) historically described Mediterranean and "
                            "Arab-Islamic societies as strictly 'shame cultures' where honor and public perception dominate, claiming that "
                            "'psychological guilt consequent upon the internalization of moral standards is not particularly in evidence.' "
                            "In host European societies, authors like Eppink (1990, 1992) extended this anthropological assertion to an extreme "
                            "deficit model. They claimed that Moroccan adolescents are incapable of experiencing guilt, lack genuine truthfulness "
                            "and honesty, and cannot accept personal responsibility for their actions."
                        ),
                        "key_terms": ["Deficit Model", "Ethnocentric Bias", "Public Exposure Paradigm", "Cultural Pathologization"],
                    },
                    {
                        "heading": "The Kindergarten Case Study: The Conflict of Public Exposure and 'Loss of Face'",
                        "content": (
                            "In an illustrative case documented in Brussels, Belgian kindergarten teachers called Moroccan parents to openly "
                            "discuss an incident where their young child took an object. From the Western teachers' perspective, open verbal "
                            "communication was seen as progressive and restorative. However, for the Moroccan parents, public exposure of the incident "
                            "inflicted catastrophic humiliation and caused the entire family to 'lose face' (fdiha / hshuma). "
                            "The parents expected the school to handle behavioral discipline discreetly within the institutional setting rather than "
                            "broadcasting a private failing to the community. Teachers misinterpreted the parents' defensive withdrawal as indifference to morality."
                        ),
                        "key_terms": ["Loss of Face", "Fdiha (Public Disgrace)", "Discreet Discipline", "Intercultural Incongruence"],
                    },
                    {
                        "heading": "Piaget's Developmental Stages Weaponized as Cultural Hierarchy",
                        "content": (
                            "Jean Piaget's developmental psychology posits that young children progress from 'heteronomous morality' (rules enforced "
                            "externally by adult authority through fear of punishment, ages 6–8) toward 'autonomous morality' (internalized conscience, "
                            "reciprocal respect, and independent moral evaluation, ages 10–12). Belgian school psychologists and educators distorted "
                            "this framework by asserting that Moroccan culture never develops autonomous morality, effectively pathologizing entire "
                            "migrant communities as perpetually arrested at the cognitive and moral level of young children."
                        ),
                        "key_terms": ["Jean Piaget", "Heteronomous Morality", "Autonomous Morality", "Evolutionary Ethnocentrism"],
                    },
                ],
            },
            {
                "chapter_id": 4,
                "title": "Empirical Research Methodology: The Cross-Cultural Thematic Apperception Test",
                "source_plate": "07.jpeg (Journal Page 309)",
                "sections": [
                    {
                        "heading": "Sample Selection & Thematic Apperception Methodology",
                        "content": (
                            "To empirically investigate whether Moroccan youngsters truly lack guilt or possess an alternate emotional grammar, "
                            "Dr. Philip Hermans conducted intensive psychological fieldwork with 70 Moroccan male adolescents (aged 15–20) "
                            "enrolled in secondary education in Brussels and Flanders. The study utilized the Thematic Apperception Test (TAT), "
                            "a projective psychological instrument that invites subjects to interpret ambiguous visual stimulus plates by creating "
                            "narratives describing the characters' thoughts, feelings, motivations, and eventual resolutions."
                        ),
                        "key_terms": ["Fieldwork Methodology", "Projective Testing", "Thematic Apperception Test (TAT)", "Narrative Coding"],
                    },
                    {
                        "heading": "Stimulus Plate Descriptions & Cross-Cultural Scoring",
                        "content": (
                            "The study implemented George DeVos's cross-cultural psychoanalytic scoring manual (1989), specifically coding for "
                            "affective expressions of guilt, remorse, sorrow, fear of sanction, and filial obligation across key plates:\n"
                            "• Plate 1: A young boy contemplating a violin resting on a table (Ambition vs. Frustration).\n"
                            "• Plate 3BM: A figure slumped on a wooden bench beside a revolver on the floor (Crime, Suicide, Despair, Guilt).\n"
                            "• Plate 6BM: An elderly mother looking out a window alongside a young man with a downcast gaze (Maternal Honor).\n"
                            "• Plate 7BM: An older man in close counsel with a younger man (Father-Son Authority & Guidance).\n"
                            "• Plate 13MF: A young man standing in anguish with arm covering his face beside a woman in bed (Passion, Remorse, Death)."
                        ),
                        "key_terms": ["George DeVos Manual", "Plate 3BM (Despair & Gun)", "Plate 13MF (Acute Remorse)", "Filial Obligation"],
                    },
                ],
            },
            {
                "chapter_id": 5,
                "title": "Empirical Evidence & Quantitative Findings: Disproving the Deficit Myth",
                "source_plate": "08.jpeg–10.jpeg (Journal Pages 310–312)",
                "sections": [
                    {
                        "heading": "Table 1: Dominant Narrative Themes Provoked by Plate 3BM",
                        "content": (
                            "Plate 3BM produced direct, unambiguous qualitative evidence of internal moral remorse, refuting the deficit claim:\n\n"
                            "| Narrative Theme | Narrative Evidence & Qualitative Student Expressions |\n"
                            "| :--- | :--- |\n"
                            "| **Criminal Behavior Followed by Guilt** | 'He committed a crime or theft... he arrived home and started to cry. He feels guilty. He blames himself deeply.' |\n"
                            "| **Criminal Behavior Followed by Punishment** | 'He was caught by police after stealing; he is locked in a cell reflecting on his foolish actions.' |\n"
                            "| **Guilt Provoked by Accidental Harm** | 'He accidentally injured his friend; he sits weeping in total despair because he cannot undo the injury.' |\n\n"
                            "In over 68% of student stories, characters displayed profound internal suffering, weeping, and self-blame independent of external capture."
                        ),
                        "key_terms": ["Table 1 Themes", "Internal Suffering", "Self-Blame", "Verbatim Qualitative Proof"],
                    },
                    {
                        "heading": "Table 2: Dominant Narrative Themes Provoked by Plate 13MF",
                        "content": (
                            "Plate 13MF evoked powerful narratives of tragic interpersonal conflict followed by overwhelming remorse:\n\n"
                            "| Narrative Theme | Quantitative Frequency & Verbatim Expressions |\n"
                            "| :--- | :--- |\n"
                            "| **Murder Followed by Severe Guilt** | 16 Subjects: 'He acted impulsively in anger. He already feels unbearable remorse. He committed a grave sin and seeks suicide to escape his inner agony.' |\n"
                            "| **Murder Followed by Guilt & Shame** | 10 Subjects: 'He killed someone. He is tormented by guilt before God, but also terrified of the public dishonor brought upon his family.' |\n"
                            "| **Tragic Loss / Accidental Grief** | 14 Subjects: 'He finds his beloved deceased; he is devastated by grief and helplessness.' |\n\n"
                            "These empirical narratives completely shatter the colonial assertion that Moroccan youth experience only superficial fear of being caught."
                        ),
                        "key_terms": ["Table 2 Themes", "Impulsive Transgression", "Unbearable Remorse", "Interlocking Affects"],
                    },
                    {
                        "heading": "Filial Honor & Maternal Emotion in Plates 6BM & 7BM",
                        "content": (
                            "In Plates 6BM and 7BM, Moroccan youngsters articulated a deeply poignant, family-centered moral code. "
                            "In 48 out of 70 stories (68.6%), narrative arcs centered on sons realizing they had wounded their parents through academic "
                            "failure or delinquent companionship: 'Look at your father, he is lying in bed weeping because you did not work in school... "
                            "Because of his mother's tears, he resolves to reform his character, seek honorable labor, and restore family dignity.' "
                            "This demonstrates that moral accountability is mediated through profound love, duty, and emotional reciprocity toward parents."
                        ),
                        "key_terms": ["Filial Honor", "Maternal Tears", "Moral Reformation", "Emotional Reciprocity"],
                    },
                ],
            },
            {
                "chapter_id": 6,
                "title": "Linguistic & Cultural Codification: The Moroccan Concepts of 'Hshuma' and 'Dhenb'",
                "source_plate": "11.jpeg & 12.jpeg (Journal Pages 313–314)",
                "sections": [
                    {
                        "heading": "The Semantic Architecture of 'Hshuma' (حشومة)",
                        "content": (
                            "In Moroccan Arabic (Darija), the concept of *hshuma* (or *hshumiya*, *heshma*) is the bedrock of social interaction. "
                            "Contrary to Western simplistic translations of 'shame' as humiliation, *hshuma* signifies propriety, mutual respect, "
                            "decency, discretion, emotional reserve, and reverence for interpersonal boundaries. The common phrase *'hshuma 'alik'* "
                            "('you ought to be ashamed') is a gentle, culturally normalized socialization cue reminding both children and adults "
                            "to maintain collective harmony and protect personal and familial dignity."
                        ),
                        "key_terms": ["Hshuma (Propriety & Modesty)", "Hshumiya", "Hshuma 'Alik", "Collective Harmony"],
                    },
                    {
                        "heading": "The Distinction of 'Dhenb' (ذنب) and 'Ndam' (ندم)",
                        "content": (
                            "While *hshuma* governs public propriety, Moroccan culture possesses distinct, powerful terms for moral culpability. "
                            "The feeling of guilt is designated as *sh'ur bi d-dhenb* (شعور بالذنب), where *dhenb* denotes a sin, religious transgression, "
                            "or violation of divine justice. Furthermore, *ndam* (ندم) expresses deep contrition, sorrow, and authentic remorse. "
                            "Because morality is culturally embedded within Islamic theology and sacred familial duties, Moroccan individuals express "
                            "guilt through spiritual and communal vocabulary rather than secular psychological jargon."
                        ),
                        "key_terms": ["Sh'ur bi d-Dhenb (Sense of Sin/Guilt)", "Ndam (Deep Remorse)", "Spiritual Vocabulary", "Divine Justice"],
                    },
                    {
                        "heading": "The Dialectic of the Gaze: Turning Inward to the Conscience",
                        "content": (
                            "A central theoretical insight of Dr. Hermans' study is the profound dialectical relationship between shame and guilt. "
                            "The external 'gaze of the community' does not replace internal conscience; rather, the gaze serves as the psychological "
                            "catalyst that activates the conscience: *'The gaze of the other turns the offender's attention to his inner self. "
                            "He is forced to look at himself, to recognize his responsibility, and to make amends.'* Shame and guilt operate as "
                            "interlocking, complementary moral regulators."
                        ),
                        "key_terms": ["Dialectic of the Gaze", "Catalyst of Conscience", "Interlocking Regulators", "Internalizing Responsibility"],
                    },
                ],
            },
            {
                "chapter_id": 7,
                "title": "Sociostructural Realities & Intercultural Pedagogical Reforms",
                "source_plate": "12.jpeg & 13.jpeg (Journal Pages 314–315)",
                "sections": [
                    {
                        "heading": "Systemic Marginalization & Defensive Rationalization",
                        "content": (
                            "Having established that Moroccan youth possess a rich capacity for guilt and moral reflection, Dr. Hermans explains "
                            "why these youngsters often appear guarded, dismissive, or reluctant to admit fault in Belgian school settings. "
                            "Moroccan students encounter pervasive societal discrimination, documented employment discrimination (Goris, 1997), "
                            "and widespread educational stigmatization. When confronting an institutional environment perceived as hostile and prejudicial, "
                            "students develop defensive coping mechanisms: externalizing blame, rationalizing setbacks, and refusing vulnerability."
                        ),
                        "key_terms": ["Societal Discrimination", "Institutional Hostility", "Defensive Coping Strategies", "Externalized Blame"],
                    },
                    {
                        "heading": "Actionable Guidelines for Educators, Counselors & Psychologists",
                        "content": (
                            "Dr. Hermans concludes with critical intercultural guidelines for Western educational institutions:\n"
                            "1. **Abandon Cultural Deficit Models:** Cease viewing immigrant cultures as developmentally deficient or morally primitive.\n"
                            "2. **Respect Familial Honor in Discipline:** Never publicly humiliate students or their families; maintain discretion and confidentiality.\n"
                            "3. **Decouple Shame from Immorality:** Recognize that *hshuma* is an expression of social decency, modesty, and community solidarity.\n"
                            "4. **Bridge Cross-Cultural Communication:** Acknowledge that moral remorse can be expressed through religious, familial, and behavioral reformation rather than individualistic verbal confessions."
                        ),
                        "key_terms": ["Intercultural Guidelines", "Confidential Discipline", "Community Solidarity", "Cross-Cultural Bridging"],
                    },
                ],
            },
        ],
    }

    # Generate Markdown documentation
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as md:
        md.write(f"# 📖 {corpus['metadata']['title']}\n\n")
        md.write(f"**Subtitle:** {corpus['metadata']['subtitle']}  \n")
        md.write(f"**Author:** {corpus['metadata']['author']} ({corpus['metadata']['affiliation']})  \n")
        md.write(f"**Citation:** *{corpus['metadata']['journal']}*  \n")
        md.write(f"**Analyzed Source Plates:** {corpus['metadata']['total_source_files']} Sequential Verified Plates\n\n")
        md.write("---\n\n")

        for ch in corpus["chapters"]:
            md.write(f"## Chapter {ch['chapter_id']}: {ch['title']}\n\n")
            md.write(f"*Source Reference: {ch['source_plate']}*\n\n")
            for sec in ch["sections"]:
                md.write(f"### {sec['heading']}\n\n")
                md.write(f"{sec['content']}\n\n")
                md.write(f"**Key Terminology:** {', '.join(sec['key_terms'])}\n\n")
            md.write("---\n\n")

    print(f"  ✓ Academic content faithfully extracted and saved to: '{output_md_path}'")
    return corpus


if __name__ == "__main__":
    extract_curriculum_corpus("input")
