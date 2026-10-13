# split lecture markdown into numbered units, keeping source metadata with each one
import re
from pathlib import Path


# read one lecture and return numbered units, followed by an intro entry
def chunk_markdown(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    valid_headings = [
        "Definition",
        "Example",
        "Proposition",
        "Corollary",
        "Exercise",
        "Theorem",
        "Lemma",
        "Remark",
    ]

    # stem is just the filename w/o .md
    # 'lecture-03-subspaces' -> ['lecture', '03', 'subspaces'] -> 3
    lecture_number = int(path.stem.split("-")[1])

    sections = []
    current_index = -1  # no unit to attach text to yet
    current_heading = ""
    unit_type = ""
    intro_text = ""
    collecting_intro = False

    # pull apart headings like '## Proposition 3.4 — Subspace test (pp. 2–3)'
    # we want: type, number, title, first page, last page
    # pp? handles both p. and pp.; the last page is optional
    heading_pattern = (
        r"## (\w+) (\d+\.\d+) — (.+) "
        r"\(pp?\. (\d+)(?:[–-](\d+))?\)"
    )

    # splitlines drops the newlines, so add them back when collecting text
    for line in content.splitlines():
        if line.startswith("# Lecture"):
            collecting_intro = True

        elif line.startswith("#"):
            # done with the actual lecture; skip source checks and everything after it
            if line.strip() == "## Source checks":
                break

            current_heading = line
            heading_words = line.split()
            unit_type = heading_words[1] if len(heading_words) > 1 else ""

            # an intro heading doesn't mean the intro is over
            # keep it if we're still collecting intro text
            # otherwise skip it; the invalid type also stops its body
            # from getting attached to the previous unit
            if unit_type not in valid_headings:
                if collecting_intro:
                    intro_text += line + "\n"
                continue

            collecting_intro = False

            # check the whole heading matches, then pull out the pieces
            match = re.fullmatch(heading_pattern, line.strip())
            if match is None:
                raise ValueError(f"{path.name}: malformed unit heading: {line}")

            unit_type, section, title, first_page, last_page = match.groups()

            # if there is only one page, last_page came back as None
            first_page = int(first_page)
            last_page = int(last_page) if last_page else first_page

            if last_page < first_page:
                raise ValueError(f"{path.name}: reversed page range: {line}")
            if int(section.split(".")[0]) != lecture_number:
                raise ValueError(f"{path.name}: unit belongs to another lecture: {line}")

            # +1 because range stops before the end: pages 2–3 -> [2, 3]
            pages = list(range(first_page, last_page + 1))
            if first_page == last_page:
                page_label = f"p. {first_page}"
            else:
                page_label = f"pp. {first_page}–{last_page}"

            context_prefix = (
                f"MATH 235 | Lecture {lecture_number} | "
                f"{unit_type} {section}: {title} | {page_label}"
            )

            # use lecture + unit number so editing text doesn't change the id
            # :02d just adds a leading zero: 3 -> '03'
            chunk_id = f"lecture-{lecture_number:02d}-unit-{section}"

            current_index += 1
            sections.append(
                {
                    "lecture": lecture_number,
                    "heading": current_heading,
                    "type": unit_type,
                    "section": section,
                    "title": title,
                    "pages": pages,
                    "source_file": path.name,
                    "id": chunk_id,
                    "context_prefix": context_prefix,
                    "text": "",
                }
            )

        elif current_index >= 0 and unit_type in valid_headings:
            # keep collecting text for the current unit
            sections[current_index]["text"] += line + "\n"

        elif collecting_intro:
            intro_text += line + "\n"

    # keep the intro around since some units depend on its assumptions
    # text is still just the body; we haven't added the prefix or intro to it
    for chunk in sections:
        chunk["lecture_intro"] = intro_text

    # put the intro at the end, separate from the numbered units
    # skip type='intro' when we only want numbered chunks
    sections.append(
        {
            "lecture": lecture_number,
            "heading": "intro",
            "type": "intro",
            "section": "intro",
            "source_file": path.name,
            "id": f"lecture-{lecture_number:02d}-intro",
            "text": intro_text,
        }
    )

    return sections


# read lectures in order and return summaries plus chunks
def chunk_files() -> tuple[list[dict], list[dict]]:
    path = Path(__file__).resolve().parents[2] / "lectures"
    files = list(path.glob("lecture-*.md"))
    files.sort()  # 01, 02, etc. means sorting puts the lectures in order

    chunked_files = []
    summary = []

    for file_num, file in enumerate(files):
        chunked_file = chunk_markdown(file)
        unit_count = 0
        empty_chunks = 0

        for chunk in chunked_file:
            # an empty intro is fine; only check the actual units
            if chunk["type"] == "intro":
                continue

            unit_count += 1
            if not chunk["text"].strip():
                empty_chunks += 1

        summary.append(
            {
                "file_name": file.name,
                "file_num": file_num,  # position in the list, starts at 0
                "chunk_count": unit_count,
                "empty_chunks": empty_chunks,
            }
        )
        chunked_files.append(
            {
                "file_name": file.name,
                "data": chunked_file,
            }
        )

    return summary, chunked_files


# add the text we'll actually embed/search. Leave the original body alone
def add_search_text(
    chunked_file: list[dict],
    assumptions: dict[str, str] | None = None,
    global_assumptions: str = "",
) -> list[dict]:
    assumptions = assumptions or {}
    for chunk in chunked_file:
        if chunk["type"] == "intro":
            continue

        # don't dump the whole intro in here; use the assumptions we checked
        shared_context = assumptions.get(chunk["id"], "")
        chunk["assumptions"] = shared_context
        parts = [chunk["context_prefix"], global_assumptions, shared_context, chunk["text"]]
        chunk["search_text"] = "\n\n".join(part.strip() for part in parts if part.strip())
    return chunked_file


# only run this if we execute the file, not if we import it elsewhere
if __name__ == "__main__":
    summary, chunked_files = chunk_files()
    for lecture_summary in summary:
        print(lecture_summary["file_name"], " empty chunks: ", lecture_summary["empty_chunks"])
