from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors


def generate_resume_pdf(person, emails, socials, skills, experience, projects, certifications, education):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Enhanced Custom Styles with Times New Roman
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=3,
        alignment=TA_CENTER,
        fontName='Times-Bold'
    )
    
    role_style = ParagraphStyle(
        'RoleStyle',
        parent=styles['Normal'],
        fontSize=13,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Times-Roman'
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#5d6d7e'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Times-Roman'
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=5,
        spaceBefore=8,
        fontName='Times-Bold'
    )
    
    normal_style = ParagraphStyle(
        'NormalContent',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=3,
        alignment=TA_JUSTIFY,
        fontName='Times-Roman'
    )
    
    bold_style = ParagraphStyle(
        'BoldContent',
        parent=normal_style,
        fontName='Times-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=normal_style,
        leftIndent=15,
        bulletIndent=8,
        spaceAfter=2
    )
    
    def add_section_divider():
        """Add a horizontal line between sections"""
        story.append(Spacer(1, 5))
        story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#34495e')))
        story.append(Spacer(1, 5))
    
    # Header Section
    story.append(Paragraph(person.get('name', 'Your Name').upper(), name_style))
    story.append(Paragraph(person.get('role', 'Your Role'), role_style))
    
    # Contact Information with actual links
    contact_parts = []
    if person.get('phone'):
        contact_parts.append(f"Phone: {person['phone']}")
    if emails:
        contact_parts.append(f"Email: {emails[0].get('email', '')}")
    if socials.get('linkedin'):
        contact_parts.append(f"LinkedIn: {socials['linkedin']}")
    if socials.get('github'):
        contact_parts.append(f"GitHub: {socials['github']}")
    
    if contact_parts:
        contact_text = " | ".join(contact_parts)
        story.append(Paragraph(contact_text, contact_style))
    
    # Professional Summary
    if person.get('summary'):
        add_section_divider()
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        story.append(Paragraph(person['summary'], normal_style))
    
    # Technical Skills
    if skills:
        add_section_divider()
        story.append(Paragraph("TECHNICAL SKILLS", section_style))
        for cat in skills:
            skill_names = [s['name'] for s in cat.get('skills', [])]
            if skill_names:
                # Create skill text without HTML tags
                skill_text = f"{cat['name']}: {', '.join(skill_names)}"
                # Use Paragraph with proper bold formatting
                story.append(Paragraph(f"<b>{cat['name']}:</b> {', '.join(skill_names)}", normal_style))
    
    # Work Experience
    if experience:
        add_section_divider()
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
        for exp in experience:
            # Job title and company with date alignment
            title_company = f"{exp['role']}"
            if exp.get('company'):
                title_company += f" | {exp['company']}"
            
            date_range = ""
            if exp.get('start_year'):
                date_range = f"{exp['start_year']} - {exp.get('end_year', 'Present')}"
            
            if date_range:
                # Create table data without HTML tags in the data
                table_data = [[title_company, date_range]]
                table = Table(table_data, colWidths=[4.5*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, 0), 'Times-Bold'),
                    ('FONTNAME', (1, 0), (1, 0), 'Times-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1a1a1a')),
                    ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#5d6d7e')),
                ]))
                story.append(table)
            else:
                story.append(Paragraph(f"<b>{title_company}</b>", bold_style))
            
            # Duration (if different from date range)
            if exp.get('duration') and exp.get('duration') != date_range:
                story.append(Paragraph(f"Duration: {exp['duration']}", normal_style))
            
            # Responsibilities
            for resp in exp.get('responsibilities', []):
                story.append(Paragraph(f"• {resp['description']}", bullet_style))
            
            # Technologies
            if exp.get('technologies'):
                tech_names = [t['name'] for t in exp['technologies']]
                tech_text = f"Technologies: {', '.join(tech_names)}"
                story.append(Paragraph(tech_text, normal_style))
            
            story.append(Spacer(1, 6))
    
    # Projects
    if projects:
        add_section_divider()
        story.append(Paragraph("KEY PROJECTS", section_style))
        for proj in projects:
            proj_title = proj['title']
            if proj.get('category'):
                proj_title += f" | {proj['category']}"
            story.append(Paragraph(f"<b>{proj_title}</b>", bold_style))
            
            if proj.get('description'):
                story.append(Paragraph(proj['description'], normal_style))
            
            if proj.get('tools'):
                tool_names = [t['name'] for t in proj['tools']]
                tech_text = f"Technologies: {', '.join(tool_names)}"
                story.append(Paragraph(tech_text, normal_style))
            
            if proj.get('metrics'):
                for metric in proj['metrics']:
                    metric_text = f"• {metric['metric_name']}: {metric['value']}"
                    story.append(Paragraph(metric_text, bullet_style))
            
            # Links with actual URLs
            links = []
            if proj.get('github_url'):
                links.append(f"GitHub: {proj['github_url']}")
            if proj.get('demo_url'):
                links.append(f"Demo: {proj['demo_url']}")
            if links:
                story.append(Paragraph(' | '.join(links), normal_style))
            
            story.append(Spacer(1, 6))
    
    # Education
    if education:
        add_section_divider()
        story.append(Paragraph("EDUCATION", section_style))
        for edu in sorted(education, key=lambda x: x.get('sort_order', 99)):
            # Degree and institution with year alignment
            edu_text = edu['degree']
            if edu.get('institution'):
                edu_text += f" | {edu['institution']}"
            
            year_text = ""
            if edu.get('year'):
                year_text = edu['year']
            
            if year_text:
                table_data = [[edu_text, year_text]]
                table = Table(table_data, colWidths=[4.5*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, 0), 'Times-Bold'),
                    ('FONTNAME', (1, 0), (1, 0), 'Times-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1a1a1a')),
                    ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#5d6d7e')),
                ]))
                story.append(table)
            else:
                story.append(Paragraph(f"<b>{edu_text}</b>", bold_style))
            
            # Location and status
            details = []
            if edu.get('place'):
                details.append(edu['place'])
            if edu.get('status'):
                details.append(edu['status'])
            if details:
                story.append(Paragraph(' | '.join(details), normal_style))
            
            story.append(Spacer(1, 4))
    
    # Certifications (NO TIME PERIOD)
    if certifications:
        add_section_divider()
        story.append(Paragraph("CERTIFICATIONS", section_style))
        for cert in certifications:
            # Certification name and platform (NO DURATION)
            cert_text = cert['name']
            if cert.get('platform'):
                cert_text += f" | {cert['platform']}"
            
            story.append(Paragraph(f"<b>{cert_text}</b>", bold_style))
            
            # Topics
            if cert.get('topics'):
                topics_list = [t['topic'] for t in cert['topics']]
                if topics_list:
                    topics_text = f"Topics: {', '.join(topics_list)}"
                    story.append(Paragraph(topics_text, normal_style))
            
            story.append(Spacer(1, 4))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
