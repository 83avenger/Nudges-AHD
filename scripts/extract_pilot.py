#!/usr/bin/env python3
"""Extract the Month of Connection 21-day pilot from the AHD workbook into
CSV + JSON for the automation. Single source of truth, traceable to the
workbook Dr. Dania / Fahad provided.

Usage: python3 scripts/extract_pilot.py /path/to/AHD_...August2026.xlsx
"""
import sys, csv, json, re
import openpyxl

SRC = sys.argv[1] if len(sys.argv) > 1 else "source/AHD_Wellbing365_Month_of_Connection_August2026.xlsx"
SHEET = "August Connection – 21 Days"
YEAR = 2026
MONTHS = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,
          "aug":8,"sep":9,"oct":10,"nov":11,"dec":12}


def iso_date(datestr):
    # e.g. "3 Aug" -> 2026-08-03
    m = re.match(r"\s*(\d{1,2})\s+([A-Za-z]{3})", str(datestr))
    if not m:
        return ""
    day = int(m.group(1))
    mon = MONTHS[m.group(2).lower()[:3]]
    return f"{YEAR:04d}-{mon:02d}-{day:02d}"


def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb[SHEET]
    rows = list(ws.iter_rows(values_only=True))
    # header row is index 2 (0-based): Day, Date, Weekday, Week Arc, EN, AR, ...
    header_idx = next(i for i, r in enumerate(rows) if r and r[0] == "Day")
    data = []
    for r in rows[header_idx + 1:]:
        if r[0] is None or not str(r[0]).strip().isdigit():
            continue
        day = int(r[0])
        rec = {
            "Day": day,
            "RevealDate": iso_date(r[1]),
            "DateLabel": (r[1] or "").strip(),
            "Weekday": (r[2] or "").strip(),
            "WeekArc": (r[3] or "").strip(),
            "ChallengeEN": (r[4] or "").strip(),
            "ChallengeAR": (r[5] or "").strip(),
            "WhyItMatters": (r[6] or "").strip(),
            "TomorrowTeaser": (r[7] or "").strip(),
            "SocialCaption": (r[8] or "").strip(),
            "SourceRef": (r[9] or "").strip(),
            "Status": "Scheduled",
            "SentDateTime": "",
            "RunID": "",
        }
        data.append(rec)

    assert len(data) == 21, f"Expected 21 challenges, got {len(data)}"
    assert all(d["RevealDate"] for d in data), "A row is missing a reveal date"
    assert all(d["ChallengeAR"] for d in data), "A row is missing Arabic text"

    cols = ["Day","RevealDate","DateLabel","Weekday","WeekArc","ChallengeEN",
            "ChallengeAR","WhyItMatters","TomorrowTeaser","SocialCaption",
            "SourceRef","Status","SentDateTime","RunID"]

    with open("data/month-of-connection.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for d in data:
            w.writerow(d)

    with open("data/month-of-connection.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(data)} challenges to data/month-of-connection.csv and .json")
    print("Reveal dates:", data[0]["RevealDate"], "->", data[-1]["RevealDate"])


if __name__ == "__main__":
    main()
