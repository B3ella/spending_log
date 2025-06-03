from dataclasses import dataclass
from os import listdir

base_dir = "/home/bella/General/4 - Archive/Diary/"

@dataclass
class Spent:
    name: str
    price: float

@dataclass
class Daily_note:
    day: int
    month: int
    year: int
    date: str

def main():
    all_files = get_files()
    daily_notes = list(map(convert_file_to_daily_note, all_files))
    get_available_months(daily_notes)
    may_notes = filter_by_month(daily_notes, 3)
    spending_lines = []
    for note in may_notes:
        spending_lines += get_spending_log(note.date).split('\n')
    spents = 0
    for line in spending_lines:
        spents += convert_string_to_spent(line).price
    print(spents)


def get_files():
    addrs = base_dir
    files = listdir(addrs)
    return files


def convert_file_to_daily_note(file_name):
    date = file_name[:-3]
    year = int(file_name[:4])
    month = int(file_name[5:7])
    day = int(file_name[8:10])
    return Daily_note(day, month, year, date)


def get_available_months(daily_notes):
    available_months = set([])
    for note in daily_notes:
        month = (note.month, note.year)
        available_months.add(month)
    return list(available_months)


def filter_by_month(daily_notes, month):
    return [note for note in daily_notes if note.month == month]


def get_spending_log(date):
    addrs = base_dir + date + ".md"
    with open(addrs) as file:
        search_pattern = "## Spending log"
        file_content = file.read()

        start = file_content.find(search_pattern) + len(search_pattern)
        end = file_content.find("##", start)

        spending_log = file_content[start:end].strip()
        return spending_log


def convert_string_to_spent(spending_line):
    spending_line = spending_line.strip()
    first_space = spending_line.find(" ")
    if not spending_line:
        return Spent("", 0)

    price_str = spending_line[0:first_space].replace(",", '.')
    price = float(price_str)

    name = spending_line[first_space+1:]
    return Spent(name, price)


if __name__ == "__main__":
    main()
