from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

output = "/home/kali/FUTURE_CS_01/report/FUTURE_CS_01_Vulnerability_Assessment_Report.pdf"

doc = SimpleDocTemplate(
    output,
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=18 * mm,
    bottomMargin=18 * mm,
)

styles = getSampleStyleSheet()

title = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=20,
    leading=24,
    spaceAfter=12,
)

heading = ParagraphStyle(
    "HeadingCustom",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=7,
)

subheading = ParagraphStyle(
    "SubHeadingCustom",
    parent=styles["Heading3"],
    fontSize=11,
    leading=14,
    spaceBefore=8,
    spaceAfter=5,
)

body = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
    spaceAfter=6,
)

small = ParagraphStyle(
    "SmallCustom",
    parent=body,
    fontSize=8,
    leading=11,
)

story = []

story.append(Paragraph("Vulnerability Assessment Report", title))
story.append(Paragraph("Task 1 – Vulnerability Assessment", heading))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "<b>Target:</b> OWASP Juice Shop<br/>"
    "<b>URL:</b> http://127.0.0.1:3000<br/>"
    "<b>Environment:</b> Local authorized laboratory<br/>"
    "<b>Assessment Type:</b> Vulnerability assessment / passive analysis",
    body
))

story.append(Paragraph("1. Executive Summary", heading))
story.append(Paragraph(
    "A vulnerability assessment was performed against an OWASP Juice Shop instance "
    "running in a local authorized laboratory environment. The assessment used Nmap "
    "for network/service discovery, OWASP ZAP for passive web security analysis, and "
    "manual HTTP header and response inspection. Several security observations were "
    "identified and manually reviewed where possible.",
    body
))

story.append(Paragraph("2. Scope", heading))
story.append(Paragraph(
    "<b>Target:</b> OWASP Juice Shop<br/>"
    "<b>URL:</b> http://127.0.0.1:3000<br/>"
    "<b>Environment:</b> Local authorized laboratory<br/>"
    "<b>Assessment Type:</b> Vulnerability assessment / passive analysis",
    body
))

story.append(Paragraph("3. Tools Used", heading))
tools_table = Table([
    ["Tool", "Purpose"],
    ["Nmap", "Port and service discovery"],
    ["OWASP ZAP", "Passive web application security analysis"],
    ["cURL", "Manual HTTP response and header validation"],
    ["Browser", "Application inspection"],
], colWidths=[45*mm, 125*mm])
tools_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#D9E2F3")),
    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
]))
story.append(tools_table)

story.append(Paragraph("4. Nmap Results", heading))
story.append(Paragraph(
    "The host 127.0.0.1 was reachable and port 3000/tcp was open. "
    "Nmap did not identify the service name with confidence and reported "
    "\"ppp?\". This is treated as an unrecognized-service classification, "
    "not as confirmed PPP. The HTTP response fingerprint contained OWASP "
    "Juice Shop application content.",
    body
))

story.append(Paragraph("5. Findings Summary", heading))
findings_table = Table([
    ["ID", "Finding", "Risk", "Validation"],
    ["F01", "Content Security Policy Header Not Set", "Medium", "Manually validated"],
    ["F02", "Cross-Domain Misconfiguration", "Medium", "Manually validated"],
    ["F03", "Missing Anti-clickjacking Header", "Medium", "Endpoint-specific"],
    ["F04", "Session ID in URL Rewrite", "Medium", "Partially validated"],
    ["F05", "Private IP Disclosure", "Low", "Observed; environment-specific"],
    ["F06", "Timestamp Disclosure – Unix", "Low", "Observed; low confidence"],
    ["F07", "X-Content-Type-Options Header Missing", "Low", "Endpoint-specific"],
    ["F08", "Information Disclosure – Suspicious Comments", "Info", "Observed; low confidence"],
], colWidths=[12*mm, 63*mm, 22*mm, 73*mm])
findings_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#D9E2F3")),
    ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 7.2),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
]))
story.append(findings_table)

def finding(title_text, risk, confidence, target, observation, impact, evidence, recommendation, limitation):
    items = [
        Paragraph(title_text, heading),
        Paragraph(
            f"<b>Risk:</b> {risk}<br/>"
            f"<b>Confidence:</b> {confidence}<br/>"
            f"<b>Target:</b> {target}",
            body
        ),
        Paragraph(f"<b>Observation:</b> {observation}", body),
        Paragraph(f"<b>Impact:</b> {impact}", body),
        Paragraph(f"<b>Evidence:</b> {evidence}", body),
        Paragraph(f"<b>Recommendation:</b> {recommendation}", body),
        Paragraph(f"<b>Limitation:</b> {limitation}", body),
    ]
    story.extend(items)

story.append(Paragraph("6. Detailed Findings", heading))

finding(
    "F01 – Content Security Policy Header Not Set",
    "Medium", "High", "http://127.0.0.1:3000/",
    "The root HTTP response does not contain a Content-Security-Policy header.",
    "The absence of CSP reduces a browser-side security control that can help restrict the sources from which web content may be loaded.",
    "Manual HTTP header inspection and ZAP alert F01.",
    "Implement an appropriate Content Security Policy based on the application's required scripts, styles, images, connections, and other resources. Test the policy before enforcing it in production.",
    "The missing header alone does not prove that an XSS vulnerability exists."
)

finding(
    "F02 – Cross-Domain Misconfiguration",
    "Medium", "Medium", "/polyfills.js",
    "The response contains Access-Control-Allow-Origin: *.",
    "A wildcard CORS policy permits cross-origin access to the resource. The security impact depends on what resources or data are exposed and whether credentials or sensitive information are involved.",
    "Manual HTTP response inspection and ZAP alert F02.",
    "Restrict allowed origins to trusted origins where cross-origin access is required. Avoid wildcard CORS policies for sensitive resources.",
    "The wildcard header alone does not prove that sensitive data can be accessed cross-origin."
)

finding(
    "F03 – Missing Anti-clickjacking Header",
    "Medium", "Medium", "Endpoint identified by ZAP",
    "ZAP identified an application response without the expected anti-clickjacking protection. The root response contains X-Frame-Options: SAMEORIGIN.",
    "Responses lacking appropriate framing restrictions may be more exposed to clickjacking attacks when they can be embedded by an untrusted origin.",
    "ZAP alert F03 and manual review of the root response.",
    "Apply consistent anti-clickjacking protection to applicable application responses, using appropriate X-Frame-Options and/or CSP frame-ancestors controls.",
    "This finding is endpoint-specific and should not be described as a site-wide absence of X-Frame-Options."
)

finding(
    "F04 – Session ID in URL Rewrite",
    "Medium", "High", "Socket.IO polling endpoint",
    "The Socket.IO handshake response contains a sid value.",
    "Session identifiers require appropriate protection to prevent unauthorized reuse.",
    "ZAP alert F04 and manual inspection of the Socket.IO response.",
    "Use secure session-management mechanisms and avoid exposing sensitive session identifiers through URLs where applicable.",
    "The captured evidence shows the sid in the response body, not in the request URL. URL exposure has not been confirmed."
)

finding(
    "F05 – Private IP Disclosure",
    "Low", "Medium", "/rest/admin/application-configuration",
    "ZAP identified the private address 192.168.99.100:3000 in the response.",
    "Internal network information can provide additional environmental information to an attacker.",
    "ZAP alert F05.",
    "Avoid exposing internal infrastructure addresses in client-facing responses unless required.",
    "The assessment was performed against a local OWASP Juice Shop laboratory environment, so this observation is environment-specific."
)

finding(
    "F06 – Timestamp Disclosure – Unix",
    "Low", "Low", "Endpoint identified by ZAP",
    "ZAP identified the Unix timestamp 1666666667.",
    "The available evidence does not establish a meaningful security impact.",
    "ZAP alert F06.",
    "Review whether timestamps exposed to clients are necessary and avoid exposing sensitive internal timing information where unnecessary.",
    "This finding remains low-confidence and does not demonstrate a significant vulnerability by itself."
)

finding(
    "F07 – X-Content-Type-Options Header Missing",
    "Low", "Medium", "Endpoint identified by ZAP",
    "The root response contains X-Content-Type-Options: nosniff, while the inspected Socket.IO response does not contain the header.",
    "Missing MIME-sniffing protection on applicable responses can reduce browser-side security hardening.",
    "ZAP alert F07 and manual HTTP header inspection.",
    "Configure X-Content-Type-Options: nosniff consistently on applicable HTTP responses.",
    "This is an endpoint-specific observation and should not be described as a site-wide absence of the header."
)

finding(
    "F08 – Information Disclosure – Suspicious Comments",
    "Informational", "Low", "/main.js",
    "ZAP identified the term \"query\" as a potentially interesting source-code/comment reference.",
    "No sensitive information disclosure was established from the available evidence.",
    "ZAP alert F08.",
    "Review production JavaScript for unnecessary comments, debugging information, or sensitive implementation details before deployment.",
    "The available evidence does not demonstrate sensitive information disclosure."
)

story.append(Paragraph("7. Informational Scanner Observation", heading))
story.append(Paragraph(
    "<b>F09 – Modern Web Application</b><br/>"
    "ZAP identified the application as a modern web application. "
    "This is an informational scanner observation and is not treated as a vulnerability.",
    body
))

story.append(Paragraph("8. Overall Recommendations", heading))
recommendations = [
    "Implement and test an appropriate Content Security Policy.",
    "Restrict CORS to trusted origins where required.",
    "Apply anti-clickjacking protection consistently to applicable responses.",
    "Review session-management and session-identifier exposure.",
    "Remove unnecessary internal infrastructure information from client-facing responses.",
    "Apply security headers consistently across applicable endpoints.",
    "Review production JavaScript for unnecessary comments or debugging information.",
]
for i, item in enumerate(recommendations, 1):
    story.append(Paragraph(f"{i}. {item}", body))

story.append(Paragraph("9. Evidence", heading))
story.append(Paragraph(
    "Supporting evidence is stored in the project repository under "
    "evidence/zap/, evidence/F01_manual_validation.txt through "
    "evidence/F08_manual_validation.txt, the HTTP response evidence files, "
    "evidence/nmap_summary.txt, and scans/nmap_scan.txt.",
    body
))

story.append(Paragraph("10. Assessment Limitation", heading))
story.append(Paragraph(
    "This assessment was conducted against a locally hosted OWASP Juice Shop "
    "instance for authorized laboratory practice. The findings should not be "
    "represented as findings from a public production website or as evidence "
    "of vulnerabilities in an unrelated live system.",
    body
))

doc.build(story)

print(f"PDF created: {output}")
