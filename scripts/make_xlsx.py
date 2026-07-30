#!/usr/bin/env python3
"""Build proper .xlsx files (with named Tables) from the JSON datasets.

The SharePoint 'From Excel' path is far more reliable with a real Excel Table
than with raw CSV (which often fails with 'Could not obtain a WAC access token').
Outputs:
  data/month-of-connection.xlsx      (table: tblNudges)
  data/four-pillars/by-nudge.xlsx    (table: tblFourPillars)
"""
import json, os, datetime
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write_xlsx(records, cols, out_path, table_name, date_cols=()):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(cols)
    for r in records:
        row = []
        for c in cols:
            v = r.get(c, "")
            if c in date_cols and v:
                try:
                    v = datetime.date.fromisoformat(v)
                except ValueError:
                    pass
            row.append(v)
        ws.append(row)
    last_col = openpyxl.utils.get_column_letter(len(cols))
    ref = f"A1:{last_col}{len(records) + 1}"
    table = Table(displayName=table_name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(table)
    # widen a couple of columns for readability
    for i, c in enumerate(cols, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = min(
            max(12, len(c) + 2), 60)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)
    print("Wrote", os.path.relpath(out_path, ROOT), f"({len(records)} rows)")


def main():
    moc = json.load(open(os.path.join(ROOT, "data", "month-of-connection.json"), encoding="utf-8"))
    moc_cols = ["Day", "RevealDate", "DateLabel", "Weekday", "WeekArc",
                "ChallengeEN", "ChallengeAR", "WhyItMatters", "TomorrowTeaser",
                "SocialCaption", "SourceRef", "Status", "SentDateTime", "RunID"]
    write_xlsx(moc, moc_cols,
               os.path.join(ROOT, "data", "month-of-connection.xlsx"),
               "tblNudges", date_cols=("RevealDate",))

    fp = json.load(open(os.path.join(ROOT, "data", "four-pillars", "by-nudge.json"), encoding="utf-8"))
    fp_cols = ["Day", "RevealDate", "DateLabel", "Weekday", "WeekArc",
               "DailyThemeEN", "DailyThemeAR", "Pillar", "PillarEN", "PillarAR",
               "PillarEmoji", "PillarOrder", "SlotTime", "NudgeEN", "NudgeAR",
               "SourceRef", "Status", "SentDateTime", "RunID"]
    write_xlsx(fp, fp_cols,
               os.path.join(ROOT, "data", "four-pillars", "by-nudge.xlsx"),
               "tblFourPillars", date_cols=("RevealDate",))


if __name__ == "__main__":
    main()
