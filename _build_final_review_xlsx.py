#!/usr/bin/env python3
"""Build FXR_Starfish_Kamali_Schema_Review_Final.xlsx from the unified review + latest FXR schema."""
from __future__ import annotations

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from pathlib import Path

OUT = Path(__file__).resolve().parent / "FXR_Starfish_Kamali_Schema_Review_Final.xlsx"

NAVY = "1B365D"
BLUE = "2E75B6"
WHITE = "FFFFFF"
LIGHT = "F2F5F9"
GREEN = "C6EFCE"
GREEN_FONT = "006100"
YELLOW = "FFEB9C"
YELLOW_FONT = "9C5700"
RED = "FFC7CE"
RED_FONT = "9C0006"
GRAY = "D9D9D9"
GRAY_FONT = "595959"
ORANGE = "FCE4D6"
ORANGE_FONT = "C65911"
PURPLE = "E2D5F1"
PURPLE_FONT = "5B2C6F"

THIN = Border(
    left=Side(style="thin", color="B0B8C1"),
    right=Side(style="thin", color="B0B8C1"),
    top=Side(style="thin", color="B0B8C1"),
    bottom=Side(style="thin", color="B0B8C1"),
)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="top", horizontal="center")


def fill(hex_color: str) -> PatternFill:
    return PatternFill("solid", fgColor=hex_color)


def header_font() -> Font:
    return Font(name="Calibri", bold=True, color=WHITE, size=11)


def body_font(bold=False, color="1A1A1A", size=10) -> Font:
    return Font(name="Calibri", bold=bold, color=color, size=size)


VERDICT_STYLE = {
    "TRUE — matches FXR schema": (GREEN, GREEN_FONT),
    "PARTIAL — direction right, schema gap": (YELLOW, YELLOW_FONT),
    "WRONG / outdated vs FXR docs": (RED, RED_FONT),
    "CANNOT VERIFY — FX9600/firmware": (GRAY, GRAY_FONT),
    "MISSING KAMALI": (ORANGE, ORANGE_FONT),
}

BUCKET_STYLE = {
    "A — Docs now (FXR)": (GREEN, GREEN_FONT),
    "B — Keep FXR-only until confirmed": (YELLOW, YELLOW_FONT),
    "C — Blocked on FX9600 firmware": (ORANGE, ORANGE_FONT),
    "D — Need Kamali remainder": (PURPLE, PURPLE_FONT),
}


def style_header(ws, row: int, cols: int):
    for col in range(1, cols + 1):
        cell = ws.cell(row, col)
        cell.fill = fill(NAVY)
        cell.font = header_font()
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = THIN
    ws.row_dimensions[row].height = 36
    ws.freeze_panes = f"A{row + 1}"
    ws.auto_filter.ref = f"A{row}:{get_column_letter(cols)}{ws.max_row}"


def write_rows(ws, headers, rows, widths, start_row=1):
    for i, h in enumerate(headers, 1):
        ws.cell(start_row, i, h)
    for r_i, row in enumerate(rows, start_row + 1):
        ws.row_dimensions[r_i].height = 78
        zebra = r_i % 2 == 0
        for c_i, val in enumerate(row, 1):
            cell = ws.cell(r_i, c_i, val)
            cell.font = body_font()
            cell.alignment = WRAP
            cell.border = THIN
            if zebra:
                cell.fill = fill(LIGHT)
            header = headers[c_i - 1]
            if header in (
                "Kamali vs latest FXR schema",
                "Kamali coverage",
            ) or (header == "Verdict" and val in VERDICT_STYLE):
                key = val if val in VERDICT_STYLE else None
                if key:
                    bg, fg = VERDICT_STYLE[key]
                    cell.fill = fill(bg)
                    cell.font = body_font(bold=True, color=fg)
                    cell.alignment = CENTER
            if header == "Bucket" and val in BUCKET_STYLE:
                bg, fg = BUCKET_STYLE[val]
                cell.fill = fill(bg)
                cell.font = body_font(bold=True, color=fg)
                cell.alignment = CENTER
            if header in ("Priority", "Owner"):
                cell.alignment = CENTER
    style_header(ws, start_row, len(headers))
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{start_row}:{get_column_letter(len(headers))}{start_row + len(rows)}"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.print_title_rows = f"{start_row}:{start_row}"
    ws.sheet_view.showGridLines = False


def howto(wb):
    ws = wb.active
    ws.title = "How to read this"
    ws.sheet_view.showGridLines = False
    ws["A1"] = "FXR vs Starfish unified review — final working sheet"
    ws["A1"].font = Font(name="Calibri", bold=True, size=18, color=NAVY)
    ws.merge_cells("A1:B1")
    ws["A2"] = (
        "Purpose: decide what is true in the latest FXR REST schema, what Kamali got right, "
        "and what still needs firmware confirmation on FX9600. This is not a firmware lab report."
    )
    ws["A2"].alignment = WRAP
    ws["A2"].font = body_font(size=11)
    ws.merge_cells("A2:B2")
    ws.row_dimensions[2].height = 48

    legend = [
        ("Column / sheet", "Meaning"),
        (
            "Kamali vs latest FXR schema",
            "Checked against rest/RestDeveloperfile.yaml and rest/operation_descriptions/*.md (FXR60/FXR90 only).",
        ),
        ("TRUE — matches FXR schema", "Kamali’s FXR claim matches the current published FXR API docs."),
        ("PARTIAL — direction right, schema gap", "Kamali is right about product behaviour, but our YAML/examples are not fully aligned yet."),
        ("WRONG / outdated vs FXR docs", "Kamali’s wording does not match the latest FXR docs (often too broad, or mixing two endpoints)."),
        ("CANNOT VERIFY — FX9600/firmware", "Claim is about FX9600 / Vulcan. This repo cannot prove it."),
        ("MISSING KAMALI", "Kamali’s pasted review did not include this row (field rows 17–28; endpoint row 32 truncated)."),
        ("Bucket A — Docs now (FXR)", "Safe FXR documentation work. No FX9600 firmware wait."),
        ("Bucket B — Keep FXR-only until confirmed", "Leave as FXR60/90 (or FXR60 Premium / FXR90) until FX9600 REST is proven."),
        ("Bucket C — Blocked on FX9600 firmware", "Do not mark common until REST mapping + firmware version are confirmed."),
        ("Bucket D — Need Kamali remainder", "Do not close the row until Kamali’s missing comment is restored."),
        ("Sources", "Unified_FXR_Starfish_Review.xlsx + latest FXR OpenAPI (openapi 3.1.0). Built 2026-09-16."),
        ("Do not treat as", "A single merged Starfish+FXR OpenAPI. Common vs FXR-only vs FX9600-only tags still apply."),
    ]
    for i, (a, b) in enumerate(legend, 4):
        ws.cell(i, 1, a).font = body_font(bold=True)
        ws.cell(i, 2, b).alignment = WRAP
        ws.cell(i, 1).border = THIN
        ws.cell(i, 2).border = THIN
        ws.row_dimensions[i].height = 36
        if a.startswith("TRUE"):
            ws.cell(i, 1).fill = fill(GREEN)
        elif a.startswith("PARTIAL"):
            ws.cell(i, 1).fill = fill(YELLOW)
        elif a.startswith("WRONG"):
            ws.cell(i, 1).fill = fill(RED)
        elif a.startswith("CANNOT"):
            ws.cell(i, 1).fill = fill(GRAY)
        elif a.startswith("MISSING"):
            ws.cell(i, 1).fill = fill(ORANGE)
        elif a.startswith("Bucket A"):
            ws.cell(i, 1).fill = fill(GREEN)
        elif a.startswith("Bucket B"):
            ws.cell(i, 1).fill = fill(YELLOW)
        elif a.startswith("Bucket C"):
            ws.cell(i, 1).fill = fill(ORANGE)
        elif a.startswith("Bucket D"):
            ws.cell(i, 1).fill = fill(PURPLE)
        elif i == 4:
            ws.cell(i, 1).fill = fill(NAVY)
            ws.cell(i, 1).font = header_font()
            ws.cell(i, 2).fill = fill(NAVY)
            ws.cell(i, 2).font = header_font()
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 110

    ws["A19"] = "Sheets in this workbook"
    ws["A19"].font = Font(name="Calibri", bold=True, size=14, color=NAVY)
    sheets = [
        ("01 Summary", "Counts and recommended work order."),
        ("02 Endpoint review", "32 endpoint rows: Kamali vs latest FXR schema."),
        ("03 Field review", "28 field rows: Kamali vs latest FXR schema."),
        ("04 FXR schema gaps", "Concrete FXR doc/schema fixes that do not wait on FX9600."),
    ]
    for i, (a, b) in enumerate(sheets, 20):
        ws.cell(i, 1, a).font = body_font(bold=True, color=BLUE)
        ws.cell(i, 2, b)
        ws.cell(i, 1).border = THIN
        ws.cell(i, 2).border = THIN
    ws.row_dimensions[1].height = 28


ENDPOINT_HEADERS = [
    "Row",
    "Method",
    "Endpoint",
    "Original category",
    "Kamali comment",
    "Starfish comment",
    "Kamali vs latest FXR schema",
    "What latest FXR schema / docs say",
    "Evidence (file)",
    "Bucket",
    "Priority",
    "Owner",
    "Recommended next action",
    "Final decision / FW version (fill in)",
]

ENDPOINT_ROWS = [
    [
        1, "GET", "/cloud/bleConfig", "FXR 60/90 only",
        "supported only in fxr90/60",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Present. Applies To: FXR60 / FXR90. Path in schema is /cloud/bleConfig (not /cloud/ble-config).",
        "RestDeveloperfile.yaml → /cloud/bleConfig; getBleConfig.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FXR60/90-only. Use approved path spelling /cloud/bleConfig.",
        "",
    ],
    [
        2, "PUT", "/cloud/bleConfig", "FXR 60/90 only",
        "supported only in fxr90/60",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Present. Applies To: FXR60 / FXR90.",
        "RestDeveloperfile.yaml → /cloud/bleConfig; setBleConfig.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FXR60/90-only.",
        "",
    ],
    [
        3, "GET", "/cloud/caCertificates", "FXR 60/90 only",
        "not supported in fx9600 (local rest mapping missing, mqtt available)",
        "FX9600 supports this (undocumented)",
        "CANNOT VERIFY — FX9600/firmware",
        "Endpoint IS in FXR schema (Applies To FXR60 / FXR90). Kamali is talking about FX9600 local REST, not FXR. MQTT on FX9600 does not prove local REST.",
        "getCACertificates.md; RestDeveloperfile.yaml → /cloud/caCertificates",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Do not mark common. Confirm FX9600 local REST mapping + firmware version. Keep FXR documented as FXR60/90.",
        "",
    ],
    [
        4, "DELETE", "/cloud/caCertificates", "FXR 60/90 only",
        "not supported in fx9600 (local rest mapping missing, mqtt available)",
        "FX9600 supports this (undocumented)",
        "CANNOT VERIFY — FX9600/firmware",
        "FXR DELETE exists (name in JSON body; GET returns .crt suffix that must be stripped). FX9600 REST unconfirmed.",
        "delCACertificate.md; RestDeveloperfile.yaml DELETE /cloud/caCertificates",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Same as row 3. Confirm local REST on FX9600 before classifying as common.",
        "",
    ],
    [
        5, "PUT", "/cloud/caCertificates", "FXR 60/90 only",
        "not supported in fx9600 (local rest mapping missing, mqtt available)",
        "FX9600 supports this (undocumented)",
        "CANNOT VERIFY — FX9600/firmware",
        "FXR PUT exists (name + PEM content in body for REST and MQTT).",
        "setInstallCACertificate.md",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Same as row 3.",
        "",
    ],
    [
        6, "GET", "/cloud/eSimConfig", "FXR 60/90 only",
        "supported only in fxr90/60",
        "Firmware confirms FX9600 does not support it.",
        "WRONG / outdated vs FXR docs",
        "Latest FXR docs say FXR90 only. Not FXR60. Kamali is too broad.",
        "getEsimConfig.md → Applies To: FXR90",
        "B — Keep FXR-only until confirmed", "P1", "Docs",
        "Correct unified docs to FXR90-only (already in latest descriptions). Do not say FXR60.",
        "",
    ],
    [
        7, "PUT", "/cloud/eSimConfig", "FXR 60/90 only",
        "supported only in fxr90/60",
        "Firmware confirms FX9600 does not support it.",
        "WRONG / outdated vs FXR docs",
        "Latest FXR docs say FXR90 only.",
        "setEsimConfig.md → Applies To: FXR90",
        "B — Keep FXR-only until confirmed", "P1", "Docs",
        "Keep FXR90-only.",
        "",
    ],
    [
        8, "GET", "/cloud/impinjGen2X", "FXR 60/90 only",
        "supported only in fxr90/60",
        "FX9600 supports this (undocumented)",
        "CANNOT VERIFY — FX9600/firmware",
        "Dedicated GET /cloud/impinjGen2X exists on FXR (Applies To FXR60 / FXR90). Gen2X fields on /start or /status do not prove this endpoint on FX9600.",
        "getImpinjGen2X.md; RestDeveloperfile.yaml → /cloud/impinjGen2X",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Confirm FX9600 REST path exists. Keep FXR documented separately from start/status Gen2X flags.",
        "",
    ],
    [
        9, "PUT", "/cloud/impinjGen2X", "FXR 60/90 only",
        "supported only in fxr90/60",
        "FX9600 supports this (undocumented)",
        "CANNOT VERIFY — FX9600/firmware",
        "Dedicated PUT exists on FXR.",
        "setImpinjGen2X.md",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Same as row 8.",
        "",
    ],
    [
        10, "GET", "/cloud/localRestLogin", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (undocumented)",
        "CANNOT VERIFY — FX9600/firmware",
        "FXR has GET /cloud/localRestLogin. Both reviewers agree FX9600 has it undocumented — that is a Starfish doc gap, not an FXR schema issue.",
        "localRestLogin.md; RestDeveloperfile.yaml",
        "C — Blocked on FX9600 firmware", "P2", "Docs",
        "Add FX9600 documentation if firmware confirms. FXR docs already include it as FXR60/90.",
        "",
    ],
    [
        11, "GET", "/cloud/logs/RcLog", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented) plus parameterized /cloud/logs/{logType}",
        "TRUE — matches FXR schema",
        "Concrete path GET /cloud/logs/RcLog exists in FXR. FXR does NOT use /cloud/logs/{logType}.",
        "RestDeveloperfile.yaml → /cloud/logs/RcLog",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Document FXR as concrete log paths. Reconcile FX9600 parameterized vs concrete docs separately.",
        "",
    ],
    [
        12, "GET", "/cloud/logs/RgErrorLog", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented)",
        "TRUE — matches FXR schema",
        "Present in FXR schema.",
        "RestDeveloperfile.yaml → /cloud/logs/RgErrorLog",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Same as row 11.",
        "",
    ],
    [
        13, "GET", "/cloud/logs/RgWarningLog", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented)",
        "TRUE — matches FXR schema",
        "Present in FXR schema.",
        "RestDeveloperfile.yaml → /cloud/logs/RgWarningLog",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Same as row 11.",
        "",
    ],
    [
        14, "DELETE", "/cloud/logs/radioPacketLog", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented)",
        "TRUE — matches FXR schema",
        "Present in FXR schema.",
        "RestDeveloperfile.yaml → DELETE /cloud/logs/radioPacketLog",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Same as row 11.",
        "",
    ],
    [
        15, "GET", "/cloud/logs/radioPacketLog", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented)",
        "TRUE — matches FXR schema",
        "Present in FXR schema.",
        "RestDeveloperfile.yaml → GET /cloud/logs/radioPacketLog",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Same as row 11.",
        "",
    ],
    [
        16, "DELETE", "/cloud/logs/syslog", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented)",
        "TRUE — matches FXR schema",
        "Present in FXR schema.",
        "RestDeveloperfile.yaml → DELETE /cloud/logs/syslog",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Same as row 11.",
        "",
    ],
    [
        17, "GET", "/cloud/logs/syslog", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented)",
        "TRUE — matches FXR schema",
        "Present. This is syslog CONTENT, not GET /cloud/logs (log levels).",
        "getLogsSyslog.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep concrete syslog path. Do not merge with GET /cloud/logs.",
        "",
    ],
    [
        18, "GET", "/cloud/networkInterfaces", "FXR 60/90 only",
        "not supported in fx9600",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Present. Applies To: FXR60 / FXR90. Both reviewers agree FX9600 does not have it.",
        "getNetworkinterfaces.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FXR60/90-only.",
        "",
    ],
    [
        19, "PUT", "/cloud/pass-through", "FXR 60/90 only",
        "supported in fx9600 undocumented",
        "FX9600 supports this (documented)",
        "CANNOT VERIFY — FX9600/firmware",
        "FXR has PUT /cloud/pass-through. Reviewers disagree only on whether FX9600 docs already exist.",
        "setPassthru.md",
        "C — Blocked on FX9600 firmware", "P2", "Docs",
        "Verify existing FX9600 docs before adding a duplicate. FXR already documented.",
        "",
    ],
    [
        20, "GET", "/cloud/preSelection", "FXR 60/90 only",
        "supported only in fxr90/60",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Present. GET returns enabled/disabled string; PUT uses boolean.",
        "getPreSelection.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FXR60/90-only.",
        "",
    ],
    [
        21, "PUT", "/cloud/preSelection", "FXR 60/90 only",
        "supported only in fxr90/60",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Present.",
        "setPreSelection.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FXR60/90-only.",
        "",
    ],
    [
        22, "GET", "/cloud/readPoints", "FXR 60/90 only",
        "not supported in fx9600 (local rest mapping missing, mqtt available)",
        "FX9600 supports this internally (undocumented); API not exposed outside",
        "CANNOT VERIFY — FX9600/firmware",
        "FXR public REST endpoint exists (Applies To FXR60 / FXR90). Internal/MQTT on FX9600 is not public REST.",
        "getReadpoints.md",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Do not list as public FX9600 local REST. Keep FXR documented.",
        "",
    ],
    [
        23, "GET", "/cloud/readerLocation", "FXR 60/90 only",
        "supported in fxr90/60 (does not explicitly deny FX9600)",
        "Firmware confirms FX9600 does not support it.",
        "CANNOT VERIFY — FX9600/firmware",
        "FXR endpoint exists. Kamali confirms FXR but does not explicitly exclude FX9600. Starfish says FX9600 no.",
        "RestDeveloperfile.yaml → /cloud/readerLocation",
        "C — Blocked on FX9600 firmware", "P2", "Firmware",
        "Ask Kamali to explicitly confirm FX9600 exclusion. Until then keep FXR-only per Starfish.",
        "",
    ],
    [
        24, "PUT", "/cloud/region", "FXR 60/90 only",
        "supported in fxr90/60.",
        "FX9600 supports this (undocumented); implementation in progress",
        "CANNOT VERIFY — FX9600/firmware",
        "FXR PUT /cloud/region exists. Starfish says FX9600 support AND implementation in progress — needs firmware version.",
        "setRegion.md",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Confirm whether FX9600 implementation is released. Keep FXR documented as FXR60/90.",
        "",
    ],
    [
        25, "GET", "/cloud/stack-led", "FXR 60/90 only",
        "supported only in fxr60",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Latest FXR docs: FXR60 Premium only (not other FXR60 variants; FXR90 has no stack light). Kamali is right that it is not FXR90; we are stricter than 'all FXR60'.",
        "getStackled.md → Applies To: FXR60 Premium",
        "A — Docs now (FXR)", "P1", "Docs",
        "Mark FXR60 Premium only in any unified catalog. Already done in latest FXR descriptions.",
        "",
    ],
    [
        26, "PUT", "/cloud/stack-led", "FXR 60/90 only",
        "supported only in fxr60",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Same as GET: FXR60 Premium only.",
        "setStackled.md",
        "A — Docs now (FXR)", "P1", "Docs",
        "Same as row 25.",
        "",
    ],
    [
        27, "PUT", "/cloud/updatePassword", "FXR 60/90 only",
        "not supported in fx9600",
        "firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Present. Applies To: FXR60 / FXR90. Both agree FX9600 does not support it.",
        "updatePassword.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FXR60/90-only.",
        "",
    ],
    [
        28, "GET", "/cloud/wifiNetworks", "FXR 60/90 only",
        "not supported in fx9600",
        "Firmware confirms FX9600 does not support it.",
        "TRUE — matches FXR schema",
        "Present. Applies To: FXR60 / FXR90.",
        "getAvailablewifinetworks.md",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FXR60/90-only. Path in schema is /cloud/wifiNetworks.",
        "",
    ],
    [
        29, "DELETE", "/cloud/logs/{logType}", "FX9600 only",
        "I don’t think this is a valid command",
        "Confirm if FXR supports this, or firmware confirms FXR does not",
        "TRUE — matches FXR schema",
        "FXR schema has NO parameterized /cloud/logs/{logType}. FXR uses concrete paths (syslog, radioPacketLog). {logType} is a placeholder, not a second API.",
        "RestDeveloperfile.yaml paths under /cloud/logs/*",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Confirm FX9600 DELETE allowed logType values. Do not add {logType} to FXR OpenAPI.",
        "",
    ],
    [
        30, "GET", "/cloud/logs/{logType}", "FX9600 only",
        "is this the same as /cloud/logs (GET and PUT)? supported by all platforms",
        "Confirm FXR support",
        "WRONG / outdated vs FXR docs",
        "Not the same. GET /cloud/logs = log LEVELS / radioPacketLog setting. GET /cloud/logs/syslog = syslog content. FXR does not expose {logType}.",
        "getLogs.md vs getLogsSyslog.md",
        "C — Blocked on FX9600 firmware", "P1", "Docs + Firmware",
        "Keep the two FXR endpoints separate. Confirm FX9600 parameterized GET independently.",
        "",
    ],
    [
        31, "GET", "/cloud/nameAndDescription", "FX9600 only",
        "currently not supported in fxr90/60",
        "Confirm if FXR supports this",
        "TRUE — matches FXR schema",
        "Path is not in RestDeveloperfile.yaml. Kamali is correct for FXR.",
        "No matching path in RestDeveloperfile.yaml",
        "B — Keep FXR-only until confirmed", "P2", "Docs",
        "Keep FX9600-only. Do not add to FXR OpenAPI.",
        "",
    ],
    [
        32, "PUT", "/cloud/nameAndDescription", "FX9600 only",
        "cu (truncated — incomplete source)",
        "Confirm if FXR supports this",
        "MISSING KAMALI",
        "GET absence does not prove PUT absence, but FXR schema has neither GET nor PUT.",
        "No matching path in RestDeveloperfile.yaml",
        "D — Need Kamali remainder", "P2", "Kamali",
        "Request remainder of Kamali comment. Until then keep FX9600-only; do not infer PUT from GET.",
        "",
    ],
]

FIELD_HEADERS = [
    "Row",
    "Method",
    "Endpoint",
    "Side",
    "Original field status",
    "Kamali comment (summary)",
    "Starfish comment (summary)",
    "Kamali vs latest FXR schema",
    "What latest FXR schema / docs say",
    "Evidence (file)",
    "Bucket",
    "Priority",
    "Owner",
    "Recommended next action",
    "Final decision / FW version (fill in)",
]

FIELD_ROWS = [
    [
        1, "GET", "/cloud/app-led", "RESPONSE", "DIFF",
        "Both Starfish and Vulcan return status. No change needed if schema is updated.",
        "Incorrect in documentation. Fix: same as Vulcan.",
        "TRUE — matches FXR schema",
        "GET response already has status enum DEFAULT / NON_DEFAULT.",
        "RestDeveloperfile.yaml /cloud/app-led GET; getAppled.md",
        "A — Docs now (FXR)", "P2", "Docs",
        "FXR already has status. Check Starfish schema if still missing.",
        "",
    ],
    [
        2, "PUT", "/cloud/app-led", "REQUEST", "DIFF",
        "If color, flash, seconds are in JSON body the command works on Starfish. May need schema update.",
        "Parameters intended to be in the body.",
        "TRUE — matches FXR schema",
        "FXR PUT body requires color, flash, seconds. No query parameters in schema.",
        "RestDeveloperfile.yaml /cloud/app-led PUT",
        "A — Docs now (FXR)", "P2", "Docs",
        "Document JSON body as the FXR contract. Confirm Starfish query-param compatibility separately.",
        "",
    ],
    [
        3, "PUT", "/cloud/apps/{appname}/autostart", "REQUEST", "DIFF",
        "appname is not required in payload; works when removed; needs schema update.",
        "No changes required (MQTT uses appname key).",
        "PARTIAL — direction right, schema gap",
        "Prose says appname is MQTT-only; REST uses path. Schema still lists optional body appname and examples still send it.",
        "RestDeveloperfile.yaml /cloud/apps/{appname}/autostart",
        "A — Docs now (FXR)", "P1", "Docs",
        "Remove body appname from REST schema/examples; keep path {appname}; keep MQTT appname.",
        "",
    ],
    [
        4, "PUT", "/cloud/apps/{appname}/start", "REQUEST", "DIFF",
        "appname not required in payload; needs schema update.",
        "No changes required.",
        "PARTIAL — direction right, schema gap",
        "Same pattern: path required, body appname still in schema/examples.",
        "RestDeveloperfile.yaml /cloud/apps/{appname}/start",
        "A — Docs now (FXR)", "P1", "Docs",
        "Remove redundant REST body appname.",
        "",
    ],
    [
        5, "PUT", "/cloud/apps/{appname}/stop", "REQUEST", "DIFF",
        "appname not required in payload; needs schema update.",
        "No changes required.",
        "PARTIAL — direction right, schema gap",
        "Same as start.",
        "RestDeveloperfile.yaml /cloud/apps/{appname}/stop",
        "A — Docs now (FXR)", "P1", "Docs",
        "Remove redundant REST body appname.",
        "",
    ],
    [
        6, "PUT", "/cloud/apps/{appname}/uninstall", "REQUEST", "DIFF",
        "appname not required in payload; needs schema update.",
        "No changes required.",
        "PARTIAL — direction right, schema gap",
        "Same as start.",
        "RestDeveloperfile.yaml /cloud/apps/{appname}/uninstall",
        "A — Docs now (FXR)", "P1", "Docs",
        "Remove redundant REST body appname.",
        "",
    ],
    [
        7, "GET", "/cloud/certificates", "RESPONSE", "DIFF",
        "Both readers return array of objects. May need Starfish schema update.",
        "Response must be an array of certificate objects.",
        "TRUE — matches FXR schema",
        "FXR GET /cloud/certificates schema is type: array of certificate objects.",
        "RestDeveloperfile.yaml /cloud/certificates GET; getCertificates.md",
        "A — Docs now (FXR)", "P2", "Docs",
        "FXR already correct. Update Starfish schema if it still shows a single object.",
        "",
    ],
    [
        8, "DELETE", "/cloud/certificates/{certname}", "REQUEST", "DIFF",
        "Command accepts JSON body on both readers; may need schema update.",
        "9600 supports certname as path and as body. No changes required.",
        "PARTIAL — direction right, schema gap",
        "FXR DELETE uses path {certname} plus JSON body field type (client|app). Starfish talked about certname, not type — do not mix those fields.",
        "RestDeveloperfile.yaml DELETE /cloud/certificates/{certname}",
        "A — Docs now (FXR)", "P2", "Docs",
        "Keep FXR body type + path certname. Verify Starfish body vs query without inferring optional fields.",
        "",
    ],
    [
        9, "PUT", "/cloud/network", "REQUEST", "DIFF",
        "Vulcan supports ethernet/wifi/bluetooth and WAN. Hardware differs; payload will differ.",
        "FX9600 wrongly documented; only flat hostname/ip/gateway/mask/dns/dhcp/mac; ETH/MLAN not implemented like Vulcan.",
        "TRUE — matches FXR schema",
        "FXR uses nested per-interface payload (eth0, mlan0, bnep0, wan0, uap0). That matches Kamali’s “hardware differs” point. FX9600 flat payload cannot be copied into FXR schema.",
        "RestDeveloperfile.yaml PUT /cloud/network; updateNetwork.md",
        "B — Keep FXR-only until confirmed", "P1", "Docs",
        "Document FXR nested interfaces and FX9600 flat payload separately. Do not document planned FX9600 ETH/MLAN as released.",
        "",
    ],
    [
        10, "PUT", "/cloud/stop", "REQUEST", "DIFF",
        "BLE added on Vulcan so scanType field added. Needed.",
        "FX9600 does not accept payload for stop.",
        "TRUE — matches FXR schema",
        "FXR PUT /cloud/stop has optional scanType [ble, rfid]. Omit/{} stops RFID only.",
        "RestDeveloperfile.yaml /cloud/stop; stopInventory.md",
        "A — Docs now (FXR)", "P2", "Docs",
        "Keep FXR scanType. Document FX9600 stop with no body.",
        "",
    ],
    [
        11, "PUT", "/cloud/apps/install", "REQUEST", "PARTIAL",
        "Retry/backoff added for Resonate; will be supported Q3 / needed from Q4 (two quarters given).",
        "FX9600 has backoff policy to support Resonate. No changes required.",
        "WRONG / outdated vs FXR docs",
        "Current FXR docs: retry/timeout/sync-async install options are NOT supported on FXR60/FXR90. Schema has url, filename, authenticationType, headers, cert fields — no retry/backoff.",
        "setInstalluserapp.md; RestDeveloperfile.yaml /cloud/apps/install",
        "C — Blocked on FX9600 firmware", "P1", "Firmware",
        "Keep FXR schema without retry. Confirm Q3 vs Q4 and firmware version before adding fields. Treat as future, not current FXR.",
        "",
    ],
    [
        12, "PUT", "/cloud/apps/{appname}/pass-through", "REQUEST", "PARTIAL",
        "Code supports both object and string; needs schema update.",
        "No changes required.",
        "PARTIAL — direction right, schema gap",
        "FXR schema documents command as object {message} only. No string|object oneOf.",
        "RestDeveloperfile.yaml /cloud/apps/{appname}/pass-through; setReqtouserapp.md",
        "A — Docs now (FXR)", "P1", "Docs",
        "If firmware confirms both forms on FXR, add string|object union. Confirm Starfish object support separately.",
        "",
    ],
    [
        13, "PUT", "/cloud/cloudConfig", "REQUEST", "PARTIAL",
        "enableLocalRest is not needed — remove from schema. dataAck needed. Other Starfish fields should match.",
        "FX9600 requires firmware changes to match FX90.",
        "PARTIAL — direction right, schema gap",
        "Prose already: Local REST is always enabled and not configurable. YAML still contains enableLocalRest. dataAck is present under additionalOptions.",
        "setImportcloudconfig.md; RestDeveloperfile.yaml endpointConfig",
        "A — Docs now (FXR)", "P1", "Docs",
        "Remove enableLocalRest from FXR schema/examples. Keep dataAck. Do not assume full Starfish field parity without a field list.",
        "",
    ],
    [
        14, "GET", "/cloud/config", "RESPONSE", "PARTIAL",
        "Same enableLocalRest / dataAck / xml / GPIO-LED notes as cloudConfig.",
        "No changes required.",
        "PARTIAL — direction right, schema gap",
        "Starfish “no change” is not proof the FXR schema is complete. Follow Kamali on enableLocalRest removal and dataAck.",
        "setConfigMqtt.md / GET config schema in RestDeveloperfile.yaml",
        "A — Docs now (FXR)", "P1", "Docs",
        "Expand FXR xml/GPIO-LED if firmware returns them. Remove enableLocalRest. Keep dataAck.",
        "",
    ],
    [
        15, "PUT", "/cloud/config", "REQUEST", "PARTIAL",
        "All fields supported in Starfish are supported in Vulcan; may need schema update.",
        "No changes required.",
        "PARTIAL — direction right, schema gap",
        "Too vague to mark TRUE. GPI event names vs 4 ports: port count does not prove every event name exists.",
        "RestDeveloperfile.yaml managementEventConfig",
        "D — Need Kamali remainder", "P2", "Docs + Firmware",
        "Get a field-level list (xml, GPI debounce, GPI 3/4 events). Do not bulk-copy Starfish fields.",
        "",
    ],
    [
        16, "GET", "/cloud/gpi", "RESPONSE", "PARTIAL",
        "FXR90 has 4 GPI pins; FX7500 has 2; FX9600 has 4. Hardware difference. Schema may need update. (truncated)",
        "Response is same as FX90. No changes required.",
        "TRUE — matches FXR schema",
        "FXR GET /cloud/gpi requires pins 1–4 (HIGH/LOW). Matches Kamali for FXR90/FX9600 pin count. Do not apply FX7500’s 2 pins to FX9600. Comment truncated.",
        "RestDeveloperfile.yaml /cloud/gpi; getGPIStatus.md",
        "D — Need Kamali remainder", "P2", "Kamali",
        "Obtain remainder of Kamali comment. Confirm FXR60 GPI count separately if needed.",
        "",
    ],
    [
        17, "GET", "/cloud/mode", "RESPONSE", "PARTIAL",
        "Not provided in the pasted Kamali review.",
        "Document is matching firmware. No changes required.",
        "MISSING KAMALI",
        "Cannot validate wordCounter, inventoryProtocol, beams, tagMetaData vs Starfish without Kamali.",
        "getMode.md",
        "D — Need Kamali remainder", "P1", "Kamali",
        "Obtain Kamali row 17. Do not discard differences as schema noise.",
        "",
    ],
    [
        18, "PUT", "/cloud/mode", "REQUEST", "PARTIAL",
        "Not provided.",
        "FX9600 response same as FX90; ATR7000 has Directionality. No changes required. (comment is about response, row is request)",
        "MISSING KAMALI",
        "Starfish mixed request vs response. DIRECTIONALITY/beams must not be copied onto FXR without confirmation.",
        "setMode.md",
        "D — Need Kamali remainder", "P1", "Kamali",
        "Obtain Kamali PUT /cloud/mode review. Separate ATR7000 directionality from FX9600.",
        "",
    ],
    [
        19, "GET", "/cloud/network", "REQUEST", "PARTIAL",
        "Not provided.",
        "FX9600 matches FX90. No changes required.",
        "MISSING KAMALI",
        "FXR GET accepts optional JSON body {interface: eth0|mlan0|bnep0|wan0|uap0|all}. Omit body = all interfaces.",
        "RestDeveloperfile.yaml GET /cloud/network; getNetwork.md",
        "D — Need Kamali remainder", "P2", "Kamali",
        "Confirm whether FX9600 uses query, body, or no parameter. Do not assume location.",
        "",
    ],
    [
        20, "PUT", "/cloud/network", "RESPONSE", "PARTIAL",
        "Not provided. Row label says PUT but issue files describe GET responses.",
        "FX9600 does not support BLE. No changes required.",
        "MISSING KAMALI",
        "Original method likely wrong (GET not PUT). FXR extras include bnep0, wan0, uap0. BLE absence does not resolve WAN/hotspot wrapping.",
        "getNetwork.md",
        "D — Need Kamali remainder", "P2", "Kamali",
        "Fix method to GET if that is the intent. Verify every interface variant with Kamali.",
        "",
    ],
    [
        21, "PUT", "/cloud/ntpServer", "REQUEST", "PARTIAL",
        "Not provided.",
        "FX9600 has only field server. No changes required.",
        "MISSING KAMALI",
        "FXR schema documents server / server1 / server2 variants. Starfish single-server contract is a platform difference if true.",
        "updateNtpServer.md",
        "D — Need Kamali remainder", "P2", "Kamali",
        "Confirm FXR server vs server1/server2 with Kamali. Keep FX9600 as server-only until proven otherwise.",
        "",
    ],
    [
        22, "PUT", "/cloud/os", "REQUEST", "PARTIAL",
        "Not provided.",
        "FX9600 has backoff policy for Resonate. No changes required.",
        "MISSING KAMALI",
        "FXR set_os docs: protocol from URL scheme; HTTPS retry/timeout not supported on FXR60/FXR90. Do not auto-apply row 11 timing.",
        "setOs.md",
        "D — Need Kamali remainder", "P2", "Kamali + Firmware",
        "Preserve Starfish retry/backoff as FX9600. Confirm FXR OS fields with Kamali.",
        "",
    ],
    [
        23, "GET", "/cloud/readerCapabilities", "RESPONSE", "PARTIAL",
        "Not provided.",
        "FX9600 document matches firmware. No changes required.",
        "MISSING KAMALI",
        "Reported diffs (apiSupported.versions shape, appLEDColors case, antenna enum, WAN/SIM) must not be dismissed as noise.",
        "getReadercapabilities.md",
        "D — Need Kamali remainder", "P1", "Kamali",
        "Obtain Kamali review. Document model applicability, not a single merged capabilities object.",
        "",
    ],
    [
        24, "GET", "/cloud/region", "RESPONSE", "PARTIAL",
        "Not provided.",
        "FX9600 document matching firmware. No changes required.",
        "MISSING KAMALI",
        "FXR samples include FrequencyHopping and country. Confirm which fields are FXR-only.",
        "getRegion.md",
        "D — Need Kamali remainder", "P2", "Kamali",
        "Retain Starfish schema pending paired review.",
        "",
    ],
    [
        25, "PUT", "/cloud/start", "REQUEST", "PARTIAL",
        "Not provided.",
        "FX9600 has applyImpinjGen2X in payload and does not have scanType. Docs need update. Also says no changes required (internal conflict).",
        "MISSING KAMALI",
        "FXR start has both scanType and applyImpinjGen2X. BLE scanType cannot combine with applyImpinjGen2X. Starfish should add applyImpinjGen2X and must not add scanType.",
        "RestDeveloperfile.yaml /cloud/start; startInventory.md",
        "D — Need Kamali remainder", "P1", "Kamali + Docs",
        "Obtain Kamali row 25. For Starfish: add applyImpinjGen2X; do not add scanType. Dedicated /cloud/impinjGen2X is a separate question (endpoint rows 8–9).",
        "",
    ],
    [
        26, "GET", "/cloud/status", "RESPONSE", "PARTIAL",
        "Not provided.",
        "FX9600 reports impinjGen2X in status but not ble. Documentation needs update.",
        "MISSING KAMALI",
        "Comment resolves only Gen2X/BLE. Other diffs (update progress, ntp, radioActivitiy spelling, enums) still open.",
        "getStatus.md",
        "D — Need Kamali remainder", "P1", "Kamali",
        "Add Starfish impinjGen2X status; exclude ble. Verify remaining fields with Kamali.",
        "",
    ],
    [
        27, "GET", "/cloud/supportedStandardList", "REQUEST", "PARTIAL",
        "Not provided. No api_field_details file.",
        "FX9600 document matching firmware. No changes required.",
        "MISSING KAMALI",
        "region is listed as shared; parameter location not confirmed.",
        "getSupportedstandardlist.md",
        "D — Need Kamali remainder", "P3", "Kamali",
        "Clarify region parameter location and why status was PARTIAL.",
        "",
    ],
    [
        28, "GET", "/cloud/supportedStandardList", "RESPONSE", "PARTIAL",
        "Not provided. No api_field_details file.",
        "FX9600 document matching firmware. No changes required.",
        "MISSING KAMALI",
        "Reported FXR channeldata / isChannelSelectable vs Starfish channelData.",
        "getSupportedstandardlist.md",
        "D — Need Kamali remainder", "P3", "Kamali",
        "Confirm FXR key spelling vs Starfish channelData.",
        "",
    ],
]

SUMMARY_HEADERS = [
    "Item",
    "Count",
    "What it means",
    "Do this next",
]

GAPS_HEADERS = [
    "#",
    "Area",
    "Kamali claim",
    "Current FXR schema / docs",
    "Fix in FXR repo?",
    "Suggested change",
    "Priority",
]


def summary_rows():
    ep_v = {}
    for r in ENDPOINT_ROWS:
        ep_v[r[6]] = ep_v.get(r[6], 0) + 1
    fl_v = {}
    for r in FIELD_ROWS:
        fl_v[r[7]] = fl_v.get(r[7], 0) + 1
    ep_b = {}
    for r in ENDPOINT_ROWS:
        ep_b[r[9]] = ep_b.get(r[9], 0) + 1
    fl_b = {}
    for r in FIELD_ROWS:
        fl_b[r[9]] = fl_b.get(r[9], 0) + 1

    rows = [
        ["Endpoint rows", 32, "All original unified endpoint rows.", "Use sheet 02."],
        ["Field rows", 28, "All original unified field rows.", "Use sheet 03."],
        ["", "", "", ""],
        ["ENDPOINT — TRUE vs FXR schema", ep_v.get("TRUE — matches FXR schema", 0), "Kamali’s FXR-side statement matches latest OpenAPI/docs.", "Safe to treat as settled for FXR."],
        ["ENDPOINT — PARTIAL", ep_v.get("PARTIAL — direction right, schema gap", 0), "Direction right but docs/schema incomplete.", "See schema gaps sheet."],
        ["ENDPOINT — WRONG / outdated", ep_v.get("WRONG / outdated vs FXR docs", 0), "Kamali wording does not match latest FXR docs.", "Correct unified catalog (eSim FXR90-only; logs/{logType} ≠ /cloud/logs)."],
        ["ENDPOINT — cannot verify (FX9600)", ep_v.get("CANNOT VERIFY — FX9600/firmware", 0), "About FX9600 REST/MQTT, not this repo.", "Firmware must confirm before marking common."],
        ["ENDPOINT — missing Kamali", ep_v.get("MISSING KAMALI", 0), "Row 32 truncated at “cu”.", "Ask Kamali to complete PUT nameAndDescription."],
        ["", "", "", ""],
        ["FIELD — TRUE vs FXR schema", fl_v.get("TRUE — matches FXR schema", 0), "Already reflected in latest FXR schema.", "Usually Starfish-side follow-up only."],
        ["FIELD — PARTIAL (FXR schema gap)", fl_v.get("PARTIAL — direction right, schema gap", 0), "Kamali right; FXR YAML/examples still lag.", "Do Bucket A docs work."],
        ["FIELD — WRONG / outdated", fl_v.get("WRONG / outdated vs FXR docs", 0), "Install retry/backoff is future, not current FXR.", "Do not add retry fields to FXR now."],
        ["FIELD — missing Kamali (rows 17–28)", fl_v.get("MISSING KAMALI", 0), "Pasted Kamali review stopped before these rows.", "Block close-out until Kamali supplies them."],
        ["", "", "", ""],
        ["Recommended work order 1", "", "Correct FXR catalog facts already known.", "eSim = FXR90 only; stack-led = FXR60 Premium; logs paths are concrete; no nameAndDescription; no {logType}."],
        ["Recommended work order 2", "", "FXR schema cleanup that matches Kamali and does not need FX9600.", "Remove REST body appname; strip enableLocalRest; keep dataAck; consider pass-through string|object."],
        ["Recommended work order 3", "", "Do not unify yet.", "CA certs, Gen2X REST endpoints, region PUT, readPoints on FX9600."],
        ["Recommended work order 4", "", "Unblock field rows 17–28.", "Get Kamali’s remainder, especially mode, start, status, capabilities."],
    ]
    return rows


GAPS_ROWS = [
    [1, "eSIM scope", "supported only in fxr90/60", "Docs already FXR90 only.", "No (already fixed in descriptions)", "If any overview still says FXR60/90, change to FXR90.", "P1"],
    [2, "Stack LED scope", "supported only in fxr60", "Docs: FXR60 Premium only.", "No (already fixed)", "Use FXR60 Premium in any unified catalog — not FXR60/90.", "P1"],
    [3, "User app REST body appname", "appname not required in REST payload", "Schema still has optional appname + examples include it.", "Yes", "start / stop / autostart / uninstall: drop body appname from REST schema and examples; keep path; keep MQTT.", "P1"],
    [4, "enableLocalRest", "Remove from schema; not needed on Vulcan", "Prose says not configurable; YAML still has the property and examples.", "Yes", "Remove enableLocalRest from cloudConfig/config schema and examples. Keep dataAck.", "P1"],
    [5, "Pass-through command type", "object or string", "command is object {message} only.", "Yes, if firmware confirms", "Add oneOf string | object after FXR lab confirmation.", "P1"],
    [6, "App LED GET status", "Both return status", "Already in schema.", "No", "Starfish schema may still need the array/status fix.", "P2"],
    [7, "Certificates GET", "Array of objects", "Already type: array.", "No", "Fix Starfish if still a single object.", "P2"],
    [8, "stop scanType", "Needed because BLE exists on Vulcan", "Already on FXR /cloud/stop.", "No", "Document FX9600 stop with empty/no body.", "P2"],
    [9, "Install retry/backoff", "Coming Q3/Q4", "Explicitly not supported on FXR60/FXR90 today.", "No — not now", "Do not add retry fields until a firmware version is named. Resolve Q3 vs Q4 conflict.", "P1"],
    [10, "GET /cloud/logs vs {logType}", "Are they the same?", "No. /cloud/logs = levels; /cloud/logs/syslog = content. No {logType} path.", "No", "Keep endpoints separate in unified docs.", "P1"],
    [11, "nameAndDescription", "Not supported on FXR", "Not in RestDeveloperfile.yaml.", "No", "Keep FX9600-only.", "P2"],
    [12, "CA / Gen2X / region / readPoints on FX9600", "Local REST missing or FXR-only", "All exist on FXR.", "No until firmware", "Do not mark common. Need FX9600 REST mapping + version.", "P1"],
]


def main():
    wb = Workbook()
    howto(wb)

    ws = wb.create_sheet("01 Summary")
    write_rows(
        ws,
        SUMMARY_HEADERS,
        summary_rows(),
        [42, 12, 72, 78],
    )
    ws.row_dimensions[1].height = 32
    for r in range(2, ws.max_row + 1):
        if ws.cell(r, 1).value in (None, ""):
            ws.row_dimensions[r].height = 10
        else:
            ws.row_dimensions[r].height = 48

    ws = wb.create_sheet("02 Endpoint review")
    write_rows(
        ws,
        ENDPOINT_HEADERS,
        ENDPOINT_ROWS,
        [6, 10, 32, 16, 42, 42, 34, 48, 40, 32, 10, 16, 48, 28],
    )

    ws = wb.create_sheet("03 Field review")
    write_rows(
        ws,
        FIELD_HEADERS,
        FIELD_ROWS,
        [6, 10, 36, 12, 14, 42, 42, 34, 48, 40, 32, 10, 16, 48, 28],
    )

    ws = wb.create_sheet("04 FXR schema gaps")
    write_rows(
        ws,
        GAPS_HEADERS,
        GAPS_ROWS,
        [6, 28, 40, 48, 28, 62, 10],
    )
    for r in range(2, ws.max_row + 1):
        ws.row_dimensions[r].height = 52

    # Freeze + print
    for name in wb.sheetnames:
        wb[name].print_options.horizontalCentered = True

    wb.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
