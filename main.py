import random
import pandas as pd
import xlsxwriter

from creators import fill_worksheet, create_wrapped_tabular
from matches import create_matches


def create_xlsx(names, n_first_poules, n_second_poules, filename):
    workbook = xlsxwriter.Workbook(f"{filename}.xlsx")
    worksheet = workbook.add_worksheet()
    first_poules = create_matches(names=names, n_poules=n_first_poules)
    poule_winner_cells, max_row = fill_worksheet(workbook, worksheet, first_poules)
    if n_second_poules > 0:
        name_refs = [f"={cell_name}" for cell_name in poule_winner_cells.values()]
        second_poules = create_matches(names=name_refs, n_poules=n_second_poules)
        fill_worksheet(workbook, worksheet, second_poules, row_offset=max_row+4, poule_id_offset=101)
    workbook.close()

def create_csv(names, n_first_poules, n_second_poules, filename):
    first_poules = create_matches(names=names, n_poules=n_first_poules)
    first_table = create_wrapped_tabular(first_poules)

    if n_second_poules > 0:
        winners = [f"Win of {i+1}" for i in range(len(first_poules))]
        second_poules = create_matches(names=winners, n_poules=n_second_poules)

        second_table = create_wrapped_tabular(second_poules)
        table = [f + s for f, s in zip(first_table, second_table)]
    else:
        table = first_table

    d = {i:c for i,c in enumerate(table)}
    df = pd.DataFrame.from_dict(d)
    df.to_csv(f"{filename}.csv", index=False, header=False)


def main():
    names = [f"name_{i}" for i in range(23)]
    # names = [str(s).strip() for s in open("c:/projects/names.txt").readlines()]
    random.shuffle(names)

    n_first_poules = 6
    n_second_poules = 2
    create_csv(names, n_first_poules, n_second_poules, "c:/projects/schema")
    create_xlsx(names, n_first_poules, n_second_poules, "c:/projects/schema")

if __name__ == "__main__":
    main()