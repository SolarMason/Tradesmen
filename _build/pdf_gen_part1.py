"""
NEPA-PRO Tradesmen — Generate all 9 onboarding/customer PDFs.

Each function builds ONE distinct document with a clear, non-overlapping purpose:

WORKER (1099 subcontractor onboarding):
  NPSA-001  Subcontractor Master Agreement
  NPSA-002  W-9 Tax Information Form
  NPSA-003  Background Check & MVR Authorization (FCRA)
  NPSA-004  Direct Deposit Authorization
  NPSA-005  Credentials & Insurance Verification
  NPSA-006  Field Operations & Safety Acknowledgment

CUSTOMER (booking protections):
  NPCS-001  Customer Service Agreement & Terms
  NPCS-002  Jobsite Safety Attestation
  NPCS-003  Liability Waiver & Indemnification

Output: /home/claude/tradesmen-nepa-pro/docs/pdfs/*.pdf
"""

import sys, os
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_brand import (
    BrandedDoc, get_styles, doc_title_block, signature_block,
    callout_box, fillable_field, numbered_clause, section_divider,
    submission_instructions,
    NAVY, ORANGE, GREY_BG, GREY_BORDER, GREY_TEXT,
)

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'pdfs')
os.makedirs(OUT_DIR, exist_ok=True)


# ============================================================
# NPSA-001  SUBCONTRACTOR MASTER AGREEMENT
# ============================================================
def build_npsa_001():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPSA-001-Subcontractor-Master-Agreement.pdf')
    doc = BrandedDoc(fname,
        doc_title='Subcontractor Master Agreement',
        doc_code='NPSA-001', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Subcontractor Master Agreement',
        'The legal relationship between NEPA-PRO LLC and the independent contractor tradesperson named below. '
        'This is the master document — every subcontractor must execute this before any job dispatch.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Establishes the independent contractor relationship, defines how '
        'jobs are offered and accepted, sets payment terms, allocates insurance responsibility, and protects '
        'confidential customer information. This document does not address tax reporting, banking, '
        'credentials, safety conduct, or background screening — those are addressed in separate documents in '
        'the onboarding packet (NPSA-002 through NPSA-006).',
        styles))
    s.append(Spacer(1, 12))

    # --- Parties ---
    s += numbered_clause(1, 'Parties',
        'This Subcontractor Master Agreement (the "<b>Agreement</b>") is entered into between '
        '<b>NEPA-PRO LLC</b>, a Pennsylvania limited liability company with its principal place of business '
        'at 14012 Orchard Drive, Clarks Summit, PA 18411 (the "<b>Company</b>"), and the individual or '
        'business entity identified in the signature block at the end of this Agreement (the "<b>Subcontractor</b>"), '
        'each a "<b>Party</b>" and collectively the "<b>Parties</b>."',
        styles)

    s += numbered_clause(2, 'Recitals',
        'The Company operates an on-demand skilled trade labor platform under the trade name '
        '<b>NEPA-PRO Tradesmen</b>, accessible at tradesmen.nepa-pro.com, that matches verified independent '
        'tradespeople with general contractors, builders, property owners, and other end customers '
        '(each, a "<b>Customer</b>") in Northeast Pennsylvania who require skilled labor on a per-engagement basis. '
        'The Subcontractor represents that they are a skilled tradesperson operating an independent business '
        'and wish to receive job offers through the Company\'s platform. The Parties enter into this Agreement '
        'to define the terms under which job offers will be made and performed.',
        styles)

    s += numbered_clause(3, 'Independent Contractor Status',
        '<b>(a)</b> The Parties expressly intend the Subcontractor to be an <b>independent contractor</b> for '
        'all purposes — federal, state, local, and otherwise. Nothing in this Agreement creates an '
        'employer-employee relationship, partnership, joint venture, or agency between the Parties.<br/><br/>'
        '<b>(b)</b> Without limiting subsection (a), the Subcontractor specifically acknowledges and agrees '
        'that the Subcontractor: (i) is not entitled to any employee benefits from the Company, including but '
        'not limited to health insurance, paid time off, retirement contributions, unemployment insurance, or '
        'workers compensation coverage from the Company; (ii) is solely responsible for their own federal, '
        'state, and local income taxes, self-employment tax, and any other applicable taxes on amounts paid '
        'by the Company; (iii) controls the means, methods, and details of the work performed, subject only '
        'to the scope of work agreed for each individual engagement; (iv) may decline any job offer for any '
        'reason without penalty; (v) may perform work for other customers or platforms during the term of '
        'this Agreement; and (vi) provides their own tools, work vehicle, hand tools, and standard PPE '
        'except where specifically agreed otherwise in writing for a particular engagement.<br/><br/>'
        '<b>(c)</b> The Company will issue an IRS Form 1099-NEC (or successor form) for any calendar year in '
        'which payments to the Subcontractor exceed the applicable IRS reporting threshold.',
        styles)

    s += numbered_clause(4, 'How Engagements Work',
        '<b>(a) Job Offers.</b> When a Customer books labor through the Company\'s platform that matches the '
        'Subcontractor\'s trade, skill tier, and availability, the Company may offer the engagement to the '
        'Subcontractor by phone, text, email, or platform notification. <br/><br/>'
        '<b>(b) Acceptance.</b> No engagement is created until the Subcontractor affirmatively accepts the '
        'specific offer. Each accepted engagement creates a separate, per-job obligation incorporating the '
        'terms of this Agreement.<br/><br/>'
        '<b>(c) No Guarantee of Work.</b> Nothing in this Agreement guarantees the Subcontractor any minimum '
        'number of engagements, hours, or compensation. The Company makes no representation that any '
        'particular volume of Customer demand will be available.<br/><br/>'
        '<b>(d) Scope of Work.</b> Each accepted engagement is performed within the scope described in the '
        'Customer\'s booking, the Customer\'s pre-dispatch communications, and any reasonable on-site '
        'direction from the Customer that is consistent with the booked tier and trade. Work that materially '
        'exceeds the booked scope must be documented and re-booked.',
        styles)

    s.append(PageBreak())

    s += numbered_clause(5, 'Compensation and Payment',
        '<b>(a) Hourly Rates.</b> The Subcontractor will be paid the per-hour rate published on the Company\'s '
        'rate schedule for the Subcontractor\'s tier and trade, less the Company\'s platform fee. Rates may be '
        'updated by the Company on 30 days\' written notice; updated rates apply only to engagements accepted '
        'after the effective date.<br/><br/>'
        '<b>(b) Payment Schedule.</b> The Company will pay the Subcontractor for completed engagements via '
        'ACH direct deposit on a <b>weekly cycle</b>. Payments are issued no later than the second business '
        'day after the close of the prior week\'s engagements, conditional on the Subcontractor\'s submission '
        'of completion confirmation and any required job documentation.<br/><br/>'
        '<b>(c) Overtime.</b> Hours worked in excess of eight (8) in a calendar day or forty (40) in a '
        'calendar week, on a single Customer engagement, are billed to the Customer at 1.5× and paid to the '
        'Subcontractor at 1.5× of the Subcontractor\'s base hourly rate. Sundays and recognized holidays '
        'are billed and paid at 2.0×.<br/><br/>'
        '<b>(d) Materials and Reimbursable Expenses.</b> Materials, equipment beyond the Subcontractor\'s '
        'standard hand tools, and travel beyond a fifty-mile radius from Scranton, PA require pre-approval '
        'and a separate written addendum to be reimbursable.',
        styles)

    s += numbered_clause(6, 'Subcontractor\'s Insurance Requirements',
        '<b>The Subcontractor shall maintain, at the Subcontractor\'s sole expense, the following insurance '
        'in force throughout the term of this Agreement:</b><br/><br/>'
        '<b>(a) Commercial General Liability (CGL):</b> not less than <b>$1,000,000 per occurrence</b> and '
        '<b>$2,000,000 aggregate</b>, written on an occurrence form, naming NEPA-PRO LLC as an additional '
        'insured on a primary and non-contributory basis with respect to the Subcontractor\'s operations '
        'under this Agreement.<br/><br/>'
        '<b>(b) Workers Compensation:</b> as required by Pennsylvania law for the Subcontractor\'s business '
        'structure. If the Subcontractor is a sole proprietor with no employees and elects to be exempt under '
        'applicable law, the Subcontractor shall complete a separate written exemption acknowledgment, and '
        'shall procure and maintain occupational accident coverage of not less than $250,000 per occurrence.<br/><br/>'
        '<b>(c) Commercial Auto Liability:</b> not less than $300,000 combined single limit, covering any '
        'vehicle the Subcontractor uses for travel to or from a job site or for transport of tools, equipment, '
        'or materials.<br/><br/>'
        '<b>(d) Certificate of Insurance.</b> The Subcontractor shall provide the Company with a current '
        'Certificate of Insurance ("<b>COI</b>") evidencing each policy above, before any job dispatch and '
        'on each policy renewal. The COI shall list NEPA-PRO LLC as a certificate holder, and the CGL '
        'endorsement page shall be attached. Lapse, cancellation, or material reduction of any required '
        'coverage immediately suspends the Subcontractor\'s eligibility for new engagements until cured.',
        styles)

    s += numbered_clause(7, 'Indemnification',
        '<b>(a) By Subcontractor.</b> The Subcontractor shall defend, indemnify, and hold harmless the '
        'Company, its members, officers, employees, contractors, and Customers from and against any and all '
        'claims, damages, losses, fines, penalties, judgments, settlements, and expenses (including '
        'reasonable attorneys\' fees) arising out of or relating to: (i) the Subcontractor\'s acts, omissions, '
        'or negligence in performing engagements; (ii) the Subcontractor\'s breach of this Agreement; '
        '(iii) bodily injury or death of the Subcontractor or the Subcontractor\'s employees; (iv) damage to '
        'property caused by the Subcontractor; or (v) the Subcontractor\'s misclassification claim, '
        'tax-withholding claim, or any other claim premised on an alleged employer-employee relationship.<br/><br/>'
        '<b>(b) By Company.</b> The Company shall defend, indemnify, and hold harmless the Subcontractor '
        'from and against claims arising solely from the Company\'s gross negligence or willful misconduct '
        'in operating the platform, dispatching engagements, or processing Customer payments.<br/><br/>'
        '<b>(c) The indemnification obligations in this Section survive termination of this Agreement.</b>',
        styles)

    s.append(PageBreak())

    s += numbered_clause(8, 'Confidentiality and Non-Solicitation',
        '<b>(a) Confidential Information.</b> The Subcontractor shall not disclose, copy, or use, except as '
        'necessary to perform engagements, any non-public information learned through the Company or any '
        'Customer, including Customer identities, project details, addresses, pricing, business processes, '
        'or contact information ("<b>Confidential Information</b>").<br/><br/>'
        '<b>(b) Non-Solicitation.</b> For the term of this Agreement and for <b>twelve (12) months</b> after '
        'its termination, the Subcontractor shall not directly solicit, contract with, or perform paid trade '
        'work for any Customer the Subcontractor was introduced to through the Company\'s platform, except '
        'through the Company. This restriction is limited to direct circumvention; it does not prevent the '
        'Subcontractor from working for any Customer the Subcontractor independently knew prior to '
        'introduction or who independently engages the Subcontractor without referencing the Company.<br/><br/>'
        '<b>(c) Reasonableness.</b> The Subcontractor acknowledges that the restrictions in this Section are '
        'reasonable in scope, duration, and geography given the nature of the platform business. If any '
        'restriction is held unenforceable, it shall be enforced to the maximum extent permitted by law.',
        styles)

    s += numbered_clause(9, 'Quality, Conduct, and Site Behavior',
        'The Subcontractor agrees that all engagement performance is subject to the standards in the '
        '<b>Field Operations & Safety Acknowledgment (NPSA-006)</b>, which is incorporated by reference. '
        'Repeated Customer complaints, no-shows, safety violations, or substandard workmanship are grounds '
        'for immediate suspension or termination of this Agreement.',
        styles)

    s += numbered_clause(10, 'Term and Termination',
        '<b>(a) Term.</b> This Agreement is effective on the date of countersignature by NEPA-PRO LLC and '
        'continues until terminated.<br/><br/>'
        '<b>(b) Termination for Convenience.</b> Either Party may terminate this Agreement for any reason '
        'on <b>seven (7) days</b> written notice. Pending engagements already accepted are honored unless '
        'either Party gives notice of termination based on cause.<br/><br/>'
        '<b>(c) Termination for Cause.</b> The Company may terminate this Agreement and any pending '
        'engagements <b>immediately</b> upon: (i) the Subcontractor\'s breach of any insurance requirement; '
        '(ii) any safety violation, theft, or material misconduct on a Customer site; (iii) the lapse, '
        'suspension, or revocation of any required trade license; (iv) any positive controlled-substance '
        'test result while on a Customer site; or (v) the Subcontractor\'s breach of confidentiality or '
        'non-solicitation obligations.<br/><br/>'
        '<b>(d) Survival.</b> Sections 3 (Independent Contractor Status), 7 (Indemnification), '
        '8 (Confidentiality and Non-Solicitation), 11 (Dispute Resolution), and any provision that by its '
        'nature should survive, survive termination.',
        styles)

    s += numbered_clause(11, 'Dispute Resolution and Governing Law',
        '<b>(a) Governing Law.</b> This Agreement is governed by the laws of the Commonwealth of Pennsylvania, '
        'without regard to its conflict-of-laws principles.<br/><br/>'
        '<b>(b) Venue.</b> Any action that must be brought in court shall be brought exclusively in the '
        'state or federal courts located in Lackawanna County, Pennsylvania, and each Party consents to '
        'personal jurisdiction there.<br/><br/>'
        '<b>(c) Mediation Required First.</b> Before either Party may file suit, the Parties shall attempt '
        'in good faith to resolve any dispute through non-binding mediation administered by a mutually '
        'agreed mediator in Scranton, Pennsylvania, with each Party bearing its own costs and an equal share '
        'of the mediator\'s fee.<br/><br/>'
        '<b>(d) Jury Trial Waiver.</b> EACH PARTY KNOWINGLY, VOLUNTARILY, AND INTENTIONALLY WAIVES THE RIGHT '
        'TO A JURY TRIAL ON ANY DISPUTE ARISING OUT OF OR RELATING TO THIS AGREEMENT.',
        styles)

    s += numbered_clause(12, 'General Provisions',
        '<b>(a) Entire Agreement.</b> This Agreement, together with the documents NPSA-002 through NPSA-006 '
        'in the onboarding packet, constitutes the entire agreement between the Parties on its subject '
        'matter and supersedes all prior discussions and writings.<br/><br/>'
        '<b>(b) Amendment.</b> This Agreement may only be amended by a writing signed by both Parties. '
        'Rate-schedule updates under Section 5(a) are not amendments to this Agreement.<br/><br/>'
        '<b>(c) Assignment.</b> The Subcontractor may not assign this Agreement without the Company\'s prior '
        'written consent. The Company may assign this Agreement to any successor entity.<br/><br/>'
        '<b>(d) Severability.</b> If any provision is held unenforceable, the remainder of the Agreement '
        'remains in full force and effect.<br/><br/>'
        '<b>(e) Notices.</b> Notices to the Company shall be sent to service@nepa-pro.com and to '
        '14012 Orchard Drive, Clarks Summit, PA 18411. Notices to the Subcontractor shall be sent to the '
        'address and email on file.',
        styles)

    # Submission instructions + signature blocks
    s.append(Spacer(1, 14))
    s.append(submission_instructions(styles, recipient_role='subcontractor onboarding'))
    s.append(Spacer(1, 16))

    s.append(Paragraph(
        '<b>By signing below, each Party acknowledges that they have read this Agreement, understand it, '
        'and agree to be bound by it.</b>',
        styles['body']))
    s.append(Spacer(1, 6))

    s += signature_block('Subcontractor (Independent Tradesperson)',
        ['Signature', 'Printed Name', 'Business Entity (if any)', 'Title', 'Date'],
        styles)
    s += signature_block('NEPA-PRO LLC (Company)',
        ['Signature', 'Printed Name', 'Title', 'Date'],
        styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# ============================================================
# NPSA-002  W-9 TAX INFORMATION FORM
# ============================================================
def build_npsa_002():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPSA-002-W9-Tax-Information.pdf')
    doc = BrandedDoc(fname,
        doc_title='W-9 Tax Information Form',
        doc_code='NPSA-002', doc_version='1.0')
    s = []

    s += doc_title_block(
        'W-9 Tax Information Form',
        'Substitute IRS Form W-9 — Request for Taxpayer Identification Number and Certification, collected '
        'by NEPA-PRO LLC for IRS Form 1099-NEC reporting.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Collects the federal taxpayer identification information NEPA-PRO '
        'LLC needs to issue an annual IRS Form 1099-NEC. This document does not address the legal '
        'relationship between the parties (NPSA-001), banking instructions for payment (NPSA-004), or any '
        'other onboarding matter.',
        styles))
    s.append(Spacer(1, 14))

    s.append(Paragraph(
        '<b>Section 1 — Identification</b>',
        styles['h2']))

    fields_1 = [
        ('Full legal name (as shown on tax return)', 4.5),
        ('Business / "doing-business-as" name (if different)', 4.5),
        ('Mailing address (street, city, state, ZIP)', 4.5),
    ]
    for label, w in fields_1:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 10))
    s.append(Paragraph(
        '<b>Section 2 — Federal Tax Classification</b><br/>'
        '<font size="9">Mark exactly one box.</font>',
        styles['h2']))

    classification = [
        '☐  Individual / Sole proprietor / Single-member LLC (disregarded entity)',
        '☐  C Corporation',
        '☐  S Corporation',
        '☐  Partnership',
        '☐  Limited Liability Company (multi-member) — Tax classification: ____ (C / S / P)',
        '☐  Other: _______________________________________________________',
    ]
    for c in classification:
        s.append(Paragraph(c, styles['body']))
    s.append(Spacer(1, 6))

    s.append(callout_box(
        '<b>Exempt payee code (if any):</b> ____________ &nbsp;&nbsp;&nbsp; '
        '<b>FATCA exemption code (if any):</b> ____________<br/>'
        '<font size="8">Most independent trade subcontractors will leave both blank. Refer to the IRS '
        'Instructions for Form W-9 if uncertain.</font>',
        styles))

    s.append(Spacer(1, 12))
    s.append(Paragraph(
        '<b>Section 3 — Taxpayer Identification Number (TIN)</b><br/>'
        '<font size="9">Enter ONE — either your Social Security Number (SSN) for individuals/sole proprietors, '
        'or your Employer Identification Number (EIN) for entities. Do not enter both.</font>',
        styles['h2']))

    tin_table = Table([
        [Paragraph('<b>Social Security Number (SSN):</b>', styles['body']),
         Paragraph('______ — ______ — __________', styles['body'])],
        [Paragraph('<b>Employer Identification Number (EIN):</b>', styles['body']),
         Paragraph('______ — _______________', styles['body'])],
    ], colWidths=[2.5*inch, 4.4*inch])
    tin_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    s.append(tin_table)

    s.append(Spacer(1, 14))

    s.append(Paragraph(
        '<b>Section 4 — Certification</b>',
        styles['h2']))

    s.append(Paragraph(
        '<b>Under penalties of perjury, I certify that:</b>',
        styles['body']))

    cert_items = [
        '<b>1.</b> The number shown on this form is my correct taxpayer identification number (or I am '
        'waiting for a number to be issued to me); and',
        '<b>2.</b> I am not subject to backup withholding because: (a) I am exempt from backup withholding; '
        'or (b) I have not been notified by the Internal Revenue Service that I am subject to backup '
        'withholding as a result of a failure to report all interest or dividends; or (c) the IRS has '
        'notified me that I am no longer subject to backup withholding; and',
        '<b>3.</b> I am a U.S. citizen or other U.S. person (as defined by the IRS); and',
        '<b>4.</b> The FATCA code(s) entered on this form (if any) indicating that I am exempt from FATCA '
        'reporting is correct.',
    ]
    for it in cert_items:
        s.append(Paragraph(it, styles['body']))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 6))
    s.append(callout_box(
        '<b>Backup withholding notice.</b> If you have been notified by the IRS that you are currently '
        'subject to backup withholding because you failed to report all interest and dividends on your tax '
        'return, you must cross out item 2 above before signing.',
        styles))

    s.append(Spacer(1, 14))
    s.append(submission_instructions(styles))
    s.append(Spacer(1, 12))

    s += signature_block('Subcontractor (U.S. Person)',
        ['Signature', 'Printed Name', 'Date'],
        styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# ============================================================
# NPSA-003  BACKGROUND CHECK & MVR AUTHORIZATION (FCRA)
# ============================================================
def build_npsa_003():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPSA-003-Background-Check-MVR-Authorization.pdf')
    doc = BrandedDoc(fname,
        doc_title='Background Check & MVR Authorization (FCRA)',
        doc_code='NPSA-003', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Background Check & MVR Authorization',
        'Standalone disclosure and authorization to obtain consumer reports under the Fair Credit Reporting '
        'Act (FCRA) and applicable Pennsylvania law.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Provides FCRA-required disclosure and obtains your written '
        'authorization for NEPA-PRO LLC to obtain a consumer report (criminal history, motor vehicle record, '
        'and prior employment / professional reference verification) <b>solely</b> for purposes of subcontractor '
        'vetting on the NEPA-PRO Tradesmen platform. Federal law requires this authorization to be a '
        '<b>standalone document</b>, separate from any other agreement. Do not sign other documents at the '
        'same time as this one.',
        styles))
    s.append(Spacer(1, 12))

    s.append(Paragraph('Disclosure Regarding Consumer Reports', styles['h2']))

    s.append(Paragraph(
        'In connection with your application to be onboarded as an independent tradesperson on the '
        'NEPA-PRO Tradesmen platform operated by NEPA-PRO LLC ("<b>the Company</b>"), the Company may obtain '
        'a "<b>consumer report</b>" and/or an "<b>investigative consumer report</b>" about you, as those terms '
        'are defined under the federal Fair Credit Reporting Act, 15 U.S.C. § 1681 et seq. ("<b>FCRA</b>"). '
        'Reports may be obtained at any time during your relationship with the Company, in connection with '
        'continued vetting and platform eligibility.',
        styles['body']))

    s.append(Paragraph(
        '<b>Scope of report.</b> The report may include the following information, to the extent permitted '
        'by applicable law:',
        styles['body']))

    scope_items = [
        '• Criminal history (county, state, and federal records, including pending charges and convictions);',
        '• Motor vehicle record and driver license status, including violations, suspensions, and accident history;',
        '• Identity verification, including Social Security Number trace and address history;',
        '• Sex offender registry checks;',
        '• Trade license and professional certification verification (PA and other states as applicable);',
        '• Prior employment, prior subcontractor engagements, and professional references for the past seven (7) years;',
        '• Public-record litigation involving you in your professional capacity.',
    ]
    for it in scope_items:
        s.append(Paragraph(it, styles['body']))
    s.append(Spacer(1, 8))

    s.append(callout_box(
        '<b>Source of report.</b> The Company may obtain the report directly or through a third-party '
        'consumer reporting agency. Upon written request, the Company will provide the name, address, and '
        'telephone number of the consumer reporting agency that prepared the report and a complete and '
        'accurate disclosure of the nature and scope of the investigation conducted.',
        styles))

    s.append(Spacer(1, 12))
    s.append(Paragraph('A Summary of Your Rights Under the FCRA', styles['h2']))

    rights_items = [
        '<b>Right to know.</b> You have the right to know what is in your file. You may request and obtain '
        'all information about you in the files of any consumer reporting agency, generally for free.',
        '<b>Right to dispute.</b> If you believe information in your file is inaccurate or incomplete, you '
        'may dispute it with the consumer reporting agency, which must investigate (usually within '
        'thirty (30) days) and correct or delete inaccurate, incomplete, or unverifiable information.',
        '<b>Adverse action notice.</b> If the Company takes adverse action against you (denies your '
        'application or terminates your eligibility) based in whole or in part on information from a consumer '
        'report, you must be told this orally, in writing, or electronically, given the name, address, and '
        'telephone number of the agency that supplied the report, and provided a copy of your rights.',
        '<b>Right to limit use.</b> Consumer reporting agencies may not give out information about you to '
        'your employer or prospective employer (or principal under FCRA-equivalent rules) without your '
        'written consent.',
        '<b>Right to seek damages.</b> If a consumer reporting agency, or a user or furnisher of consumer '
        'report information, violates the FCRA, you may be able to sue in state or federal court.',
        '<b>Identity-theft and victims of military service.</b> Identity-theft victims and active duty '
        'military personnel have additional rights. For more information, visit '
        '<font color="#ff6b35">www.consumerfinance.gov/learnmore</font> or call (855) 411-2372.',
    ]
    for it in rights_items:
        s.append(Paragraph(it, styles['body']))
    s.append(Spacer(1, 8))

    s.append(PageBreak())

    s.append(Paragraph('Authorization', styles['h2']))

    s.append(Paragraph(
        'I have read the Disclosure above and the Summary of Rights. I voluntarily authorize NEPA-PRO LLC, '
        'and any consumer reporting agency or background investigation service it engages, to procure a '
        'consumer report and/or investigative consumer report about me, of the scope described above, for '
        'use solely in evaluating my application for onboarding to the NEPA-PRO Tradesmen platform and for '
        'continued platform eligibility throughout my relationship with the Company.<br/><br/>'
        'I authorize, without reservation, any party or agency contacted by NEPA-PRO LLC or its '
        'investigation service to provide the requested information. I understand that I may, upon written '
        'request, be informed whether a consumer report was requested, and if so, the name and address of '
        'the agency that furnished the report. I further understand that this authorization does not '
        'guarantee that any report will be obtained or that I will be onboarded.',
        styles['body']))

    s.append(Spacer(1, 12))
    s.append(Paragraph('Identifying Information', styles['h2']))

    fields = [
        ('Full legal name (first, middle, last)', 4.5),
        ('Other names used (maiden, alias, nickname)', 4.5),
        ('Date of birth (month / day / year)', 3.0),
        ('Social Security Number (last four digits acceptable on this form)', 3.0),
        ('Driver license number and issuing state', 4.5),
        ('Current address (street, city, state, ZIP)', 4.5),
        ('Prior address within last 7 years', 4.5),
        ('Email address', 4.5),
        ('Mobile phone', 4.5),
    ]
    for label, w in fields:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 14))
    s.append(submission_instructions(styles))
    s.append(Spacer(1, 12))

    s += signature_block('Applicant',
        ['Signature', 'Printed Name', 'Date'],
        styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# Continued in pdf_gen_part2.py
if __name__ == '__main__':
    print('NEPA-PRO PDF Generator — Part 1 (Worker docs 1-3)')
    print('-' * 60)
    build_npsa_001()
    build_npsa_002()
    build_npsa_003()
    print('-' * 60)
    print('Part 1 complete.')
