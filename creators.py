from xlsxwriter.utility import xl_rowcol_to_cell
from poule import Poule


def create_wrapped_tabular(poules) -> list[list[str]]:
    n_columns = 3
    table = [[] for _ in range(n_columns * 5)]
    max_rows = -1
    for p in range(len(poules)):
        col = p % n_columns
        row = p // n_columns
        m = poules[p].get_matches()
        id = f"{poules[p]._index + 1}"
        table[col * 5].extend([id] + [n[0] for n in m] + [""])
        table[(col * 5) + 1].extend([""] + [n[1] for n in m] + [""])
        table[(col * 5) + 2].extend([""] + ["<winner>" for n in m] + [""])
        table[(col * 5) + 3].extend([""] + ["<score>" for n in m] + [""])
        table[(col * 5) + 4].extend([""] + ["" for n in m] + [""])
        if len(table[col * 5]) > max_rows:
            max_rows = len(table[col * 5])

    # Add padding
    table = [c + ([""] * (max(max_rows - len(c), 0) + 1)) for c in table]
    return table


def write_poule_header(workbook, worksheet, r, c, poule: Poule, poule_id_offset):
    bold = workbook.add_format({"bold": True})
    bold_italic = workbook.add_format({"bold": True, "italic": True})
    poule_id = f"{poule._index + poule_id_offset}"
    worksheet.write(r, c, f"poule: {poule_id}", bold)
    worksheet.write(r, c + 1, "team 1", bold)
    worksheet.write(r, c + 2, "team 2", bold)
    worksheet.write(r, c + 3, "score 1", bold)
    worksheet.write(r, c + 4, "score 2", bold)
    worksheet.write(r, c + 5, "amount", bold_italic)
    worksheet.write(r, c + 6, "winner", bold_italic)

def write_poule_row(workbook, worksheet, r, c, match):
    italic = workbook.add_format({"italic": True})
    empty = xl_rowcol_to_cell(r, c)
    worksheet.write(r, c + 1, match[0])
    worksheet.write(r, c + 2, match[1])
    team1_cell = xl_rowcol_to_cell(r, c + 1)
    team2_cell = xl_rowcol_to_cell(r, c + 2)
    worksheet.write(r, c + 3, 0)
    worksheet.write(r, c + 4, 0)
    score1_cell = xl_rowcol_to_cell(r, c + 3)
    score2_cell = xl_rowcol_to_cell(r, c + 4)
    first_if = f"IF({score1_cell}-{score2_cell}>0, {team1_cell}, {team2_cell})"
    second_if = f"IF({score1_cell} + {score2_cell} > 0, {first_if}, {empty})"
    amount_formula = f"ABS({score1_cell} - {score2_cell})"
    worksheet.write_formula(r, c + 5, amount_formula, italic)
    worksheet.write_formula(r, c + 6, second_if, italic)

def fill_worksheet(workbook, worksheet, poules, row_offset=0, poule_id_offset=1):
    bold = workbook.add_format({"bold": True})
    poule_winner_cells = {}
    max_row = 0
    for p_idx in range(len(poules)):
        cpp = 8 # cols per poule
        write_poule_header(workbook, worksheet, row_offset, p_idx * cpp, poules[p_idx], poule_id_offset)
        matches = poules[p_idx].get_matches()

        # winner cell
        winner_row = len(matches)+row_offset+1
        poule_winner_cells[p_idx] = xl_rowcol_to_cell(winner_row, (p_idx * cpp) + 6)
        worksheet.write(poule_winner_cells[p_idx], f"who won {poules[p_idx]._index + poule_id_offset}?")
        # worksheet.write(winner_row, p_idx * cpp, "winner", bold)
        if max_row < winner_row:
            max_row = winner_row

        # individual matches
        for m_idx in range(len(matches)):
            write_poule_row(workbook, worksheet, row_offset+m_idx+1, p_idx * cpp, matches[m_idx])
    return poule_winner_cells, max_row