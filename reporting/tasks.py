from celery import shared_task
from reportlab.pdfgen import canvas
from django.conf import settings
from .models import Report
import os


@shared_task
def generate_report_pdf(report_id):
    """
    Task to generate PDF report for a completed Scan.
    """
    try:
        report = Report.objects.get(id=report_id)
        scan = report.scan
        vulnerabilities = scan.vulnerabilities.all()  # because of related_name='vulnerabilities'

        # Folder path
        reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
        os.makedirs(reports_dir, exist_ok=True)

        # File path
        file_path = os.path.join(reports_dir, f"scan_report_{scan.id}.pdf")

        # Start generating PDF
        c = canvas.Canvas(file_path)
        y = 800

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, f"Security Scan Report - Scan #{scan.id}")
        y -= 40

        # Scan info
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Target URL: {scan.profile.target_url}")
        y -= 20
        c.drawString(50, y, f"Scan Status: {scan.status}")
        y -= 40

        # Vulnerabilities section
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Detected Vulnerabilities:")
        y -= 30

        c.setFont("Helvetica", 11)

        if not vulnerabilities.exists():
            c.drawString(50, y, "No vulnerabilities found.")
            y -= 20
        else:
            for vul in vulnerabilities:
                if y < 100:  # Avoid writing at bottom edge
                    c.showPage()
                    y = 800
                    c.setFont("Helvetica", 11)

                c.drawString(50, y, f"- {vul.name} ({vul.severity})")
                y -= 15

                c.drawString(70, y, f"Description: {vul.description[:90]}")
                y -= 15

                c.drawString(70, y, f"Fixed: {'Yes' if vul.is_fixed else 'No'}")
                y -= 25

        c.showPage()
        c.save()

        # Save file in model
        relative_path = f"reports/scan_report_{scan.id}.pdf"
        report.file.name = relative_path
        report.status = "READY"
        report.save()

        return f"Report generated: {relative_path}"

    except Exception as e:
        report.status = "FAILED"
        report.save()
        return str(e)
