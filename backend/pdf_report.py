import os

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch


class PDFReport:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name="SectionHeading",
            parent=self.styles["Heading2"],
            spaceBefore=14,
            spaceAfter=6,
        ))

    def generate(
        self,
        filename,
        parsed_result,
        warnings,
        complexity,
        explanation,
        language="python",
        bugs=None,
        security_issues=None,
        ai_review=None,
    ):
        os.makedirs("reports", exist_ok=True)

        safe_name = "".join(c for c in filename if c.isalnum() or c in "._-")
        pdf_path = f"reports/{safe_name}.pdf"

        doc = SimpleDocTemplate(pdf_path, topMargin=0.6 * inch, bottomMargin=0.6 * inch)
        story = []

        story.append(Paragraph("AI Code Review Report", self.styles["Title"]))
        story.append(Spacer(1, 8))

        story.append(Paragraph(f"<b>File:</b> {filename}", self.styles["BodyText"]))
        story.append(Paragraph(f"<b>Language:</b> {language.capitalize()}", self.styles["BodyText"]))
        story.append(Paragraph(f"<b>Functions:</b> {len(parsed_result.get('functions', []))}", self.styles["BodyText"]))
        story.append(Paragraph(f"<b>Classes:</b> {len(parsed_result.get('classes', []))}", self.styles["BodyText"]))
        story.append(Paragraph(f"<b>Imports:</b> {len(parsed_result.get('imports', []))}", self.styles["BodyText"]))
        story.append(Paragraph(f"<b>Static Warnings:</b> {len(warnings)}", self.styles["BodyText"]))
        story.append(Paragraph(f"<b>Time Complexity:</b> {complexity['complexity']}", self.styles["BodyText"]))
        story.append(Paragraph(f"<b>Reason:</b> {complexity['reason']}", self.styles["BodyText"]))

        self._add_list_section(story, "⚠ Static Code Review Warnings", warnings)
        self._add_list_section(story, "🐞 Detected Bugs", bugs or [])

        if security_issues:
            story.append(Paragraph("🔒 Security Issues", self.styles["SectionHeading"]))
            items = [
                ListItem(Paragraph(
                    f"[{issue['severity']}] Line {issue['line']} — {issue['type']}: {issue['message']}",
                    self.styles["BodyText"],
                ))
                for issue in security_issues
            ]
            story.append(ListFlowable(items, bulletType="bullet"))
        else:
            story.append(Paragraph("🔒 Security Issues", self.styles["SectionHeading"]))
            story.append(Paragraph("No security issues detected.", self.styles["BodyText"]))

        story.append(Paragraph("🤖 Code Summary", self.styles["SectionHeading"]))
        for line in explanation.replace("#", "").split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), self.styles["BodyText"]))

        if ai_review and ai_review.get("available"):
            story.append(Paragraph("🤖 AI Review (Groq)", self.styles["SectionHeading"]))
            for key, label in [
                ("bugs", "Bugs"), ("code_smells", "Code Smells"),
                ("security_issues", "Security Issues"),
                ("performance_suggestions", "Performance Suggestions"),
                ("improvements", "Improvements"),
            ]:
                values = ai_review.get(key) or []
                if values:
                    story.append(Paragraph(f"<b>{label}</b>", self.styles["BodyText"]))
                    story.append(ListFlowable(
                        [ListItem(Paragraph(str(v), self.styles["BodyText"])) for v in values],
                        bulletType="bullet",
                    ))

        doc.build(story)

        return pdf_path

    def _add_list_section(self, story, title, items):
        story.append(Paragraph(title, self.styles["SectionHeading"]))
        if items:
            story.append(ListFlowable(
                [ListItem(Paragraph(str(i), self.styles["BodyText"])) for i in items],
                bulletType="bullet",
            ))
        else:
            story.append(Paragraph("None found. 🎉", self.styles["BodyText"]))
