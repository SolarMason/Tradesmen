"""
NEPA-PRO Tradesmen — Generate PDFs 4-9 (the rest of the packet).
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


# ============================================================
# NPSA-004  DIRECT DEPOSIT AUTHORIZATION
# ============================================================
def build_npsa_004():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPSA-004-Direct-Deposit-Authorization.pdf')
    doc = BrandedDoc(fname,
        doc_title='Direct Deposit Authorization',
        doc_code='NPSA-004', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Direct Deposit (ACH) Authorization',
        'Authorization for NEPA-PRO LLC to deposit subcontractor compensation directly into the bank '
        'account identified below by Automated Clearing House (ACH) transfer.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Captures banking information and the subcontractor\'s ACH '
        'authorization for payment of compensation. This document does not address tax reporting (NPSA-002), '
        'compensation rates or schedule (which are governed by NPSA-001 § 5), or any other onboarding matter.',
        styles))
    s.append(Spacer(1, 14))

    # ----- Subcontractor identification -----
    s.append(Paragraph('Subcontractor Identification', styles['h2']))
    fields_id = [
        ('Full legal name', 4.5),
        ('Business / DBA name (if any)', 4.5),
        ('Email address (for ACH remittance notices)', 4.5),
        ('Mobile phone', 4.5),
    ]
    for label, w in fields_id:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    # ----- Banking information -----
    s.append(Spacer(1, 8))
    s.append(Paragraph('Bank Account Information', styles['h2']))

    fields_bank = [
        ('Receiving bank name', 4.5),
        ('Bank branch city / state', 4.5),
        ('Bank routing number (9 digits)', 3.0),
        ('Bank account number', 4.0),
    ]
    for label, w in fields_bank:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 6))
    s.append(Paragraph('<b>Account type</b> (mark one):', styles['body']))
    s.append(Paragraph('☐ Checking &nbsp;&nbsp;&nbsp; ☐ Savings &nbsp;&nbsp;&nbsp; ☐ Business checking', styles['body']))
    s.append(Spacer(1, 12))

    # ----- Voided check -----
    s.append(callout_box(
        '<b>Voided check or bank letter required.</b> You must attach <b>one</b> of the following with this '
        'authorization, so the routing and account numbers can be verified independently of what you write '
        'above: (a) a printed image of a <b>voided</b> check from the account; or (b) a letter on the bank\'s '
        'letterhead, signed by a bank representative, confirming the account holder\'s name, routing number, '
        'and account number. Deposit slips are <b>not</b> acceptable.',
        styles))
    s.append(Spacer(1, 12))

    # ----- Authorization -----
    s.append(Paragraph('ACH Authorization', styles['h2']))
    s.append(Paragraph(
        'I authorize NEPA-PRO LLC ("the Company") to initiate ACH credit entries to the account identified '
        'above for purposes of paying compensation owed to me as a subcontractor on the NEPA-PRO Tradesmen '
        'platform. I further authorize the Company, and the depository financial institution named above, '
        'to initiate <b>ACH debit entries to recover any deposit credited to me in error</b>, in accordance '
        'with the rules of the National Automated Clearing House Association (Nacha).',
        styles['body']))

    s.append(Paragraph(
        'This authorization remains in full force and effect until the Company has received written '
        'notification from me of its termination — by email to <b>service@nepa-pro.com</b> with the subject '
        '"Direct Deposit Termination" — in such time and manner as to afford the Company and the depository '
        'institution a reasonable opportunity to act on it (typically <b>five (5) business days</b>). I am '
        'responsible for keeping the Company informed of any change to my banking information.',
        styles['body']))

    s.append(Paragraph(
        'I represent that I am the sole or joint owner of the account identified above and that I have '
        'authority to initiate this authorization.',
        styles['body']))

    s.append(Spacer(1, 12))
    s.append(callout_box(
        '<b>Liability and error correction.</b> The Company\'s sole obligation under this authorization is '
        'to issue ACH credit entries for amounts properly owed. If a deposit is misrouted or rejected '
        'because of inaccurate information you provided, you remain responsible for reconciling the '
        'transaction with your bank. If a deposit is issued in error or in excess of what is owed, you '
        'authorize the Company to recover the overpayment via ACH debit, set-off against future payments, '
        'or any other lawful means.',
        styles))

    s.append(Spacer(1, 14))
    s.append(submission_instructions(styles))
    s.append(Spacer(1, 12))

    s += signature_block('Account Holder', ['Signature', 'Printed Name', 'Date'], styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# ============================================================
# NPSA-005  CREDENTIALS & INSURANCE VERIFICATION
# ============================================================
def build_npsa_005():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPSA-005-Credentials-Insurance-Verification.pdf')
    doc = BrandedDoc(fname,
        doc_title='Credentials & Insurance Verification',
        doc_code='NPSA-005', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Credentials & Insurance Verification',
        'Documentation of trade licenses, professional certifications, and current commercial insurance '
        'coverage. Required before any job dispatch and on every policy renewal.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Captures evidence of the credentials and insurance the '
        'Subcontractor must maintain under <b>NPSA-001 § 6</b>. This document is the operational record of '
        'compliance — it does not modify the underlying obligations in NPSA-001, address banking (NPSA-004), '
        'or address jobsite conduct (NPSA-006).',
        styles))
    s.append(Spacer(1, 12))

    # ----- Identity -----
    s.append(Paragraph('Section 1 — Subcontractor Identity', styles['h2']))
    fields_id = [
        ('Full legal name', 4.5),
        ('Business name (if any)', 4.5),
        ('Primary trade(s) — list all', 4.5),
        ('Years of professional experience in primary trade', 2.5),
    ]
    for label, w in fields_id:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    # ----- Trade Licenses -----
    s.append(Spacer(1, 8))
    s.append(Paragraph('Section 2 — Active Trade License(s)', styles['h2']))
    s.append(Paragraph(
        'List every active trade or professional license held. Attach a clear photocopy or PDF of each '
        'license. Examples: PA Master Electrician License, PA Home Improvement Contractor (HIC) Registration, '
        'Master Plumber municipal registration, EPA 608 universal certification, ASME welding certification, '
        'crane operator NCCCO card, OSHA-30 wallet card.',
        styles['body']))
    s.append(Spacer(1, 4))

    license_tbl = Table([
        ['#', 'License / cert type', 'Issuing authority', 'License #', 'State', 'Expires'],
        ['1', '____________________', '__________________', '____________', '____', '__/__/____'],
        ['2', '____________________', '__________________', '____________', '____', '__/__/____'],
        ['3', '____________________', '__________________', '____________', '____', '__/__/____'],
        ['4', '____________________', '__________________', '____________', '____', '__/__/____'],
    ], colWidths=[0.3*inch, 1.7*inch, 1.6*inch, 1.2*inch, 0.5*inch, 1.0*inch])
    license_tbl.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#0a1628')),
        ('TEXTCOLOR', (0,0), (-1,0), HexColor('#ffffff')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#d4d7dc')),
    ]))
    s.append(license_tbl)
    s.append(Spacer(1, 12))

    # ----- Specialty certifications -----
    s.append(Paragraph('Section 3 — Specialty Certifications', styles['h2']))
    s.append(Paragraph(
        'Mark all that apply, and provide proof. Add expiration dates where applicable.',
        styles['body']))

    certs = [
        '☐ OSHA 10-hour Construction &nbsp;&nbsp;&nbsp; Issued: __/__/____',
        '☐ OSHA 30-hour Construction &nbsp;&nbsp;&nbsp; Issued: __/__/____',
        '☐ EPA 608 (refrigerant) &nbsp;&nbsp;&nbsp; Type: ____ &nbsp;&nbsp; Issued: __/__/____',
        '☐ EPA 609 (MVAC) &nbsp;&nbsp;&nbsp; Issued: __/__/____',
        '☐ Welding certification (AWS / ASME) &nbsp;&nbsp;&nbsp; Process: ________ &nbsp;&nbsp; Issued: __/__/____',
        '☐ NCCCO crane operator &nbsp;&nbsp;&nbsp; Class: ________ &nbsp;&nbsp; Expires: __/__/____',
        '☐ Aerial / scissor lift (OSHA 1926.453) &nbsp;&nbsp;&nbsp; Expires: __/__/____',
        '☐ Forklift / powered industrial truck &nbsp;&nbsp;&nbsp; Expires: __/__/____',
        '☐ Confined space entry &nbsp;&nbsp;&nbsp; Expires: __/__/____',
        '☐ NFPA 70E arc flash &nbsp;&nbsp;&nbsp; Expires: __/__/____',
        '☐ First aid / CPR / AED &nbsp;&nbsp;&nbsp; Expires: __/__/____',
        '☐ Other: ______________________________________________________________',
    ]
    for c in certs:
        s.append(Paragraph(c, styles['body']))
    s.append(Spacer(1, 10))

    s.append(PageBreak())

    # ----- Insurance -----
    s.append(Paragraph('Section 4 — Commercial Insurance', styles['h2']))
    s.append(Paragraph(
        'Per <b>NPSA-001 § 6</b>, the Subcontractor must maintain Commercial General Liability (CGL), '
        'Workers Compensation (per PA law), and Commercial Auto coverage. Provide carrier and policy data '
        'below, and attach a current Certificate of Insurance (COI) listing NEPA-PRO LLC as a certificate '
        'holder and additional insured on the CGL.',
        styles['body']))
    s.append(Spacer(1, 6))

    ins_tbl = Table([
        ['Coverage', 'Carrier', 'Policy #', 'Limit per occ.', 'Aggregate', 'Effective', 'Expires'],
        ['CGL',           '__________', '__________', '__________', '__________', '__/__/__', '__/__/__'],
        ['Workers Comp',  '__________', '__________', '__________', '__________', '__/__/__', '__/__/__'],
        ['Commercial Auto','__________', '__________', '__________', '__________', '__/__/__', '__/__/__'],
        ['Excess / Umbrella','__________', '__________', '__________', '__________', '__/__/__', '__/__/__'],
    ], colWidths=[1.0*inch, 1.0*inch, 1.0*inch, 0.95*inch, 0.95*inch, 0.7*inch, 0.7*inch])
    ins_tbl.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#0a1628')),
        ('TEXTCOLOR', (0,0), (-1,0), HexColor('#ffffff')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#d4d7dc')),
    ]))
    s.append(ins_tbl)
    s.append(Spacer(1, 10))

    s.append(callout_box(
        '<b>Workers Comp exemption (sole proprietors).</b> If you are a sole proprietor with no employees '
        'and you have lawfully elected exemption from PA workers compensation, mark "EXEMPT" in the WC '
        'carrier field above and attach (i) the PA Department of Labor & Industry exemption '
        'acknowledgment, and (ii) proof of occupational accident insurance of not less than '
        '$250,000 per occurrence.',
        styles))
    s.append(Spacer(1, 12))

    # ----- Vehicle (when driving to jobsite) -----
    s.append(Paragraph('Section 5 — Work Vehicle (if applicable)', styles['h2']))
    fields_v = [
        ('Year / Make / Model', 4.5),
        ('License plate / state', 3.0),
        ('VIN', 4.0),
        ('Driver license # / state / expiration', 4.5),
    ]
    for label, w in fields_v:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 10))

    # ----- Acknowledgment -----
    s.append(Paragraph('Section 6 — Acknowledgments', styles['h2']))
    acks = [
        '<b>(a)</b> I certify that the information above is true, complete, and correct as of the date of '
        'signing.',
        '<b>(b)</b> I will <b>notify NEPA-PRO LLC within seven (7) calendar days</b> if any license is '
        'suspended, revoked, allowed to lapse, or has its scope materially changed; if any insurance policy '
        'is non-renewed, canceled, or has its limits reduced; or if my driver license status changes.',
        '<b>(c)</b> I authorize NEPA-PRO LLC to verify any of the credentials, certifications, or insurance '
        'policies listed above with the issuing authority or carrier directly.',
        '<b>(d)</b> I understand that lapse of any required license or insurance coverage <b>immediately '
        'suspends</b> my eligibility for new engagements until cured, and may be grounds for termination of '
        'NPSA-001.',
    ]
    for a in acks:
        s.append(Paragraph(a, styles['body']))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 12))
    s.append(submission_instructions(styles))
    s.append(Spacer(1, 12))

    s += signature_block('Subcontractor', ['Signature', 'Printed Name', 'Date'], styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# ============================================================
# NPSA-006  FIELD OPERATIONS & SAFETY ACKNOWLEDGMENT
# ============================================================
def build_npsa_006():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPSA-006-Field-Operations-Safety.pdf')
    doc = BrandedDoc(fname,
        doc_title='Field Operations & Safety Acknowledgment',
        doc_code='NPSA-006', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Field Operations & Safety Acknowledgment',
        'Operational expectations on Customer jobsites — PPE, OSHA compliance, conduct, drug-free policy, '
        'incident reporting, and quality standards.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Establishes the day-to-day field operations expected of every '
        'subcontractor on a Customer site. This document is incorporated into NPSA-001 § 9 by reference. '
        'It does not address insurance requirements (NPSA-005), the legal relationship between the Parties '
        '(NPSA-001), or background screening (NPSA-003).',
        styles))
    s.append(Spacer(1, 12))

    s += numbered_clause(1, 'Independent Responsibility for Safety',
        'You are an independent contractor. You are solely responsible for the safe means and methods of '
        'your work, for compliance with applicable Occupational Safety and Health Administration (OSHA) '
        'standards, and for any required training (including, where applicable, OSHA-10 or OSHA-30 '
        'construction). NEPA-PRO LLC does not direct your work product or means and is not your safety '
        'employer.',
        styles)

    s += numbered_clause(2, 'Personal Protective Equipment (PPE) — Minimum',
        'You shall arrive on every Customer site with, at minimum:<br/>'
        '<b>•</b> ANSI Z89.1 Type I or II hard hat (when working below others or in any active construction zone)<br/>'
        '<b>•</b> ANSI Z87.1 safety glasses<br/>'
        '<b>•</b> ASTM F2413 or equivalent safety-toe work boots<br/>'
        '<b>•</b> ANSI Class 2 hi-visibility vest or shirt when within 15 feet of any roadway or '
        'mechanized equipment<br/>'
        '<b>•</b> Cut-resistant gloves and hearing protection appropriate to the task<br/><br/>'
        'Trade-specific PPE — arc-flash gear, fall-arrest, respirators, welding hoods/leathers, '
        'lockout/tagout devices — is your responsibility per task. If a task requires PPE you do not have, '
        'stop work and notify NEPA-PRO immediately. Do not proceed without proper protection.',
        styles)

    s += numbered_clause(3, 'Drug-Free and Alcohol-Free While Dispatched',
        'You shall not consume, possess, or be under the influence of alcohol, recreational marijuana, or '
        'any controlled substance — including substances lawful in Pennsylvania for non-medical use — '
        'during the period from dispatch to the close of your engagement. Lawful prescription medication '
        'that does not impair your ability to work safely is permitted; medication that carries impairment '
        'warnings requires you to stop work. Reporting to a Customer site under the influence is grounds '
        'for immediate termination of NPSA-001 and forfeiture of compensation for the engagement.',
        styles)

    s += numbered_clause(4, 'Conduct on Customer Property',
        '<b>(a) Professional conduct.</b> You shall be polite and respectful to the Customer, the '
        'Customer\'s family or employees, the Customer\'s neighbors, and any other tradespeople on site. '
        'No profanity directed at others, no harassment, no discriminatory conduct.<br/><br/>'
        '<b>(b) Property care.</b> Cover floors and surfaces appropriately to protect from damage. Use '
        'drop cloths, runners, or shoe covers in finished spaces. Clean up at the end of each engagement; '
        'remove your own debris and packaging.<br/><br/>'
        '<b>(c) Smoking.</b> No smoking, vaping, or chewing tobacco inside any structure or in the '
        'Customer\'s vehicles. Outdoor smoking is permitted only in clearly-disposed manner, away from '
        'flammable materials, and only if the Customer has not designated the property smoke-free.<br/><br/>'
        '<b>(d) Photography.</b> Do not photograph any Customer\'s personal property, family members, or '
        'sensitive areas of the home or business beyond what is needed to document your own work. Any '
        'work-progress photos are considered Confidential Information under NPSA-001 § 8.<br/><br/>'
        '<b>(e) Communications.</b> Do not give the Customer your personal contact information, business '
        'card, or any social-media handle while on the engagement; route follow-up through NEPA-PRO. This '
        'protects you and supports the non-circumvention provisions in NPSA-001.',
        styles)

    s.append(PageBreak())

    s += numbered_clause(5, 'Hazard Recognition and Stop-Work Authority',
        '<b>(a)</b> If you arrive at a site and observe any of the following, you have <b>stop-work '
        'authority</b> and shall not begin: live unmarked utilities in a digging area; visible asbestos, '
        'lead, or mold not previously disclosed; structural conditions that pose imminent collapse risk; '
        'obvious aggressive animals; missing OSHA-required fall protection above 6 feet; or any other '
        'condition you reasonably believe creates a serious risk of injury.<br/><br/>'
        '<b>(b)</b> Notify the Customer\'s on-site point of contact and call NEPA-PRO dispatch immediately '
        'at <b>570-677-7971</b>. Document the condition with photos. You will be paid the booked block for '
        'the engagement even if you stand down.',
        styles)

    s += numbered_clause(6, 'Incident, Injury, and Near-Miss Reporting',
        'Any of the following must be reported to NEPA-PRO LLC <b>within 24 hours</b>, in writing to '
        'service@nepa-pro.com, with photos where possible:<br/>'
        '<b>•</b> Any injury to you, the Customer, the Customer\'s family or employees, or any third party<br/>'
        '<b>•</b> Any property damage, however minor — including dings to walls, scratches to floors, or '
        'damaged finishes<br/>'
        '<b>•</b> Any near-miss event<br/>'
        '<b>•</b> Any vehicle accident while in transit to or from the engagement<br/>'
        '<b>•</b> Any contact with law enforcement related to the engagement<br/>'
        '<b>•</b> Any verbal or written threat made by or against you on the Customer site<br/><br/>'
        'Failure to timely report an incident is itself grounds for termination, separately from the '
        'underlying conduct.',
        styles)

    s += numbered_clause(7, 'Quality Standards',
        '<b>(a) Workmanship.</b> All work shall meet or exceed the prevailing industry standard for the '
        'trade and tier (apprentice, journeyman, master/foreman) booked. Master/foreman engagements include '
        'an obligation to leave finished work to a callable inspection-ready condition where applicable.<br/><br/>'
        '<b>(b) Documentation.</b> Take "before" and "after" photos of your work area for every engagement, '
        'and submit them with your completion report. This protects you in the event of any later '
        'Customer dispute.<br/><br/>'
        '<b>(c) Customer feedback.</b> Customer ratings and unresolved complaints affect your eligibility '
        'for future engagements. Repeated 1- or 2-star ratings, or a single substantiated complaint of '
        'theft, dishonesty, or unsafe behavior, are grounds for immediate suspension.',
        styles)

    s += numbered_clause(8, 'Tools and Equipment Responsibility',
        'You provide your own hand tools, standard PPE, and (where applicable) basic power tools and '
        'consumables for your trade. Specialty equipment — lifts, generators, line trucks, large '
        'compressors, welder/plasma units, forklifts, cranes — is the Customer\'s responsibility unless '
        'a separate written addendum says otherwise. Borrowed Customer tools or equipment shall not be '
        'used unless the Customer affirmatively offers them and you have personal training on the item.',
        styles)

    s += numbered_clause(9, 'Subcontracting and Substitution',
        'You may not assign or sub-contract an accepted engagement to another tradesperson without '
        'NEPA-PRO\'s prior written approval. The vetted person who accepted the engagement must be the '
        'person on the Customer\'s site.',
        styles)

    s += numbered_clause(10, 'Acknowledgment',
        'I have read and understand each of the field operations and safety expectations above. I agree '
        'to follow them on every NEPA-PRO Tradesmen engagement. I understand that violation of any item '
        'in this document may result in suspension or termination of my Subcontractor Master Agreement '
        '(NPSA-001) and may forfeit compensation for the affected engagement.',
        styles)

    s.append(Spacer(1, 14))
    s.append(submission_instructions(styles))
    s.append(Spacer(1, 12))

    s += signature_block('Subcontractor', ['Signature', 'Printed Name', 'Date'], styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# ============================================================
# NPCS-001  CUSTOMER SERVICE AGREEMENT & TERMS
# ============================================================
def build_npcs_001():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPCS-001-Customer-Service-Agreement.pdf')
    doc = BrandedDoc(fname,
        doc_title='Customer Service Agreement & Terms',
        doc_code='NPCS-001', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Customer Service Agreement & Terms',
        'The terms under which NEPA-PRO LLC dispatches independent contractor tradespeople to your jobsite. '
        'Accepted by your booking, and confirmable in writing.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Establishes the booking relationship between you (the Customer) '
        'and NEPA-PRO LLC — service description, scope, exclusions, payment terms, cancellation, customer '
        'obligations, and the limits of NEPA-PRO\'s undertaking. Jobsite safety conditions are addressed '
        'separately in <b>NPCS-002</b>; indemnification and liability limits are addressed in <b>NPCS-003</b>.',
        styles))
    s.append(Spacer(1, 10))

    s += numbered_clause(1, 'Parties; Acceptance',
        '<b>(a) Parties.</b> This Customer Service Agreement (the "<b>Agreement</b>") is between '
        '<b>NEPA-PRO LLC</b> ("<b>NEPA-PRO</b>") and the booking customer identified at Stripe checkout or '
        'in the signature block of this document (the "<b>Customer</b>").<br/><br/>'
        '<b>(b) Acceptance.</b> The Customer is deemed to have read and accepted this Agreement upon the '
        'earlier of: (i) submitting payment for any booking through tradesmen.nepa-pro.com or any other '
        'NEPA-PRO checkout endpoint; or (ii) signing this Agreement. Each subsequent booking by the same '
        'Customer is governed by the version of this Agreement in effect at the time of that booking.',
        styles)

    s += numbered_clause(2, 'Service Description',
        '<b>(a) What we are.</b> NEPA-PRO operates an on-demand skilled trade labor platform that matches '
        'vetted independent tradespeople with customers in Northeast Pennsylvania who require labor on a '
        'per-engagement basis (half-day, full day, or weekly blocks).<br/><br/>'
        '<b>(b) What we are not.</b> NEPA-PRO is <b>not</b>: a general contractor for the Customer\'s '
        'project; the engineer, architect, or designer of the Customer\'s project; the employer of the '
        'tradesperson dispatched to the Customer\'s site; the seller of any material installed at the '
        'Customer\'s site (unless explicitly so in writing); or the Customer\'s licensed trade contractor '
        'where Pennsylvania law requires the Customer to hold a separate contract with a licensed '
        'professional.<br/><br/>'
        '<b>(c) Independent contractor disclosure.</b> Every tradesperson dispatched is an independent '
        '1099 subcontractor of NEPA-PRO, vetted under the Subcontractor Master Agreement (NPSA-001) and '
        'related onboarding documents. The tradesperson controls the means and methods of work within the '
        'booked scope. The Customer does not direct the tradesperson\'s work product beyond the scope.',
        styles)

    s += numbered_clause(3, 'Scope of Services Included',
        'For each accepted booking, NEPA-PRO will: (a) match a tradesperson with the booked trade and '
        'skill tier (apprentice, journeyman, or master/foreman); (b) confirm the engagement with the '
        'Customer by phone within one business hour of payment; (c) dispatch the tradesperson to the '
        'shipping address provided at checkout (the "<b>Jobsite</b>") for the booked duration; and '
        '(d) provide the Customer post-engagement with a completion report and any required compliance '
        'documentation we have on file.',
        styles)

    s += numbered_clause(4, 'Scope EXCLUSIONS',
        '<b>The following are not included in any booking unless expressly added in a written addendum '
        'signed by NEPA-PRO and the Customer:</b><br/>'
        '<b>•</b> Engineering, architectural design, or stamped construction drawings<br/>'
        '<b>•</b> Permit applications, code-compliance certifications, or interface with authorities '
        'having jurisdiction (the "<b>AHJ</b>") beyond simple inspections incidental to the booked work<br/>'
        '<b>•</b> Construction materials, fixtures, equipment, or consumables<br/>'
        '<b>•</b> Specialty equipment beyond the tradesperson\'s standard hand tools and PPE — e.g., aerial '
        'lifts, forklifts, generators, line trucks, cranes, large compressors, welder/plasma rigs<br/>'
        '<b>•</b> Project management, scheduling of other trades, or general-contractor responsibilities<br/>'
        '<b>•</b> Removal, abatement, or remediation of asbestos, lead paint, mold, biological hazards, '
        'or other regulated hazardous materials — these require specially-licensed contractors<br/>'
        '<b>•</b> Warranty on workmanship beyond the warranty in <b>Section 9</b> of this Agreement<br/>'
        '<b>•</b> 24/7 emergency dispatch outside posted dispatch hours<br/>'
        '<b>•</b> Any service in any geography outside the NEPA service area unless mobilization is '
        'separately quoted and accepted',
        styles)

    s.append(PageBreak())

    s += numbered_clause(5, 'Payment Terms',
        '<b>(a) Payment up front.</b> Each booking is paid in full at checkout via Stripe. Card, Apple Pay, '
        'and Google Pay are accepted. Promotional codes are honored as posted at checkout.<br/><br/>'
        '<b>(b) Overtime.</b> Hours beyond the booked block, or any overtime worked at the Customer\'s '
        'request, bill at <b>1.5×</b> the rate posted for the booked tier and trade after eight (8) hours '
        'in a calendar day or forty (40) in a calendar week. Sundays and federally-recognized holidays bill '
        'at <b>2.0×</b>. Overtime is invoiced after engagement on the same payment instrument unless the '
        'Customer requests a different method.<br/><br/>'
        '<b>(c) Material cost pass-through.</b> If NEPA-PRO procures any material at the Customer\'s '
        'request, the Customer is invoiced at NEPA-PRO\'s cost <b>plus 12% handling</b>, with documented '
        'receipts attached. No procurement happens without the Customer\'s written approval.<br/><br/>'
        '<b>(d) Late payment.</b> Any post-engagement invoice not paid within fourteen (14) days bears '
        'interest at <b>1.5% per month</b> (or the maximum rate permitted by Pennsylvania law if lower). '
        'NEPA-PRO may also suspend the Customer\'s ability to book new engagements until past-due amounts '
        'are paid.',
        styles)

    s += numbered_clause(6, 'Cancellation and Rescheduling',
        '<b>(a) 24+ hours before dispatch.</b> Full refund or fee-free reschedule.<br/>'
        '<b>(b) Inside 24 hours, half-day or full-day bookings.</b> Non-refundable. The Customer receives '
        'a credit equal to the booking amount, valid for ninety (90) days against any future booking.<br/>'
        '<b>(c) Weekly bookings.</b> May be paused mid-week with at least 12 hours\' notice; remaining '
        'days roll forward up to thirty (30) days from the original start date.<br/>'
        '<b>(d) NEPA-PRO cancellation.</b> If NEPA-PRO is unable to dispatch a confirmed booking due to '
        'tradesperson illness, equipment failure, or other reason within NEPA-PRO\'s control, the Customer '
        'will be offered a same-week reschedule, a substitute tradesperson, or a full refund — '
        'Customer\'s choice.',
        styles)

    s += numbered_clause(7, 'Customer Obligations',
        'For each booking, the Customer shall: (a) provide the Jobsite address accurately at checkout; '
        '(b) provide an accurate written description of the project scope through the checkout custom '
        'fields; (c) make the Jobsite reasonably ready for skilled work, including basic access, lighting, '
        'and the safety conditions covered in <b>NPCS-002 (Jobsite Safety Attestation)</b>; (d) provide a '
        'site contact reachable by phone during the engagement; and (e) make payment available before '
        'dispatch.',
        styles)

    s += numbered_clause(8, 'Disclaimers',
        '<b>(a) AS-IS labor delivery.</b> NEPA-PRO and the dispatched tradesperson deliver skilled labor '
        'at the booked tier. NEPA-PRO does not warrant that the labor will achieve any particular outcome '
        'on the Customer\'s project. The Customer is solely responsible for evaluating whether the work '
        'product meets the Customer\'s needs and for accepting or rejecting the work upon completion.<br/><br/>'
        '<b>(b) No warranty of fitness for a particular purpose.</b> EXCEPT FOR THE LIMITED WARRANTY IN '
        'SECTION 9, NEPA-PRO DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED '
        'WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.<br/><br/>'
        '<b>(c) Permit and inspection responsibility.</b> The Customer is responsible for any permits, '
        'inspections, or AHJ approvals their project requires under Pennsylvania law and applicable '
        'municipal code, unless explicitly added to the booking in writing.',
        styles)

    s += numbered_clause(9, 'Limited Workmanship Warranty',
        'NEPA-PRO warrants that the labor performed under each booking will be free from material '
        'workmanship defects for <b>thirty (30) days</b> after the engagement\'s completion date. The '
        'Customer\'s sole and exclusive remedy under this warranty is, at NEPA-PRO\'s election, '
        '(a) re-performance of the defective portion of the work, or (b) refund of the labor cost for the '
        'defective portion. To make a warranty claim, the Customer shall notify NEPA-PRO in writing at '
        'service@nepa-pro.com within the warranty period, with photos of the defect.',
        styles)

    s += numbered_clause(10, 'Force Majeure',
        'Neither party is liable for delay or failure to perform due to causes beyond reasonable control '
        'and without the party\'s fault, including acts of God; severe weather (snow, ice, lightning); '
        'fires; floods; civil unrest; epidemic; governmental action; or third-party utility outage. The '
        'affected party shall give prompt notice and the parties shall reschedule in good faith.',
        styles)

    s += numbered_clause(11, 'Independent Documents',
        'This Agreement is read together with <b>NPCS-002 (Jobsite Safety Attestation)</b> and '
        '<b>NPCS-003 (Liability Waiver & Indemnification)</b>. Each customer-facing document covers a '
        'distinct subject; in the event of any apparent conflict, NPCS-001 controls the booking '
        'relationship, NPCS-002 controls jobsite safety conditions, and NPCS-003 controls allocation of '
        'liability and indemnification.',
        styles)

    s += numbered_clause(12, 'Governing Law; Venue',
        'This Agreement is governed by the laws of the Commonwealth of Pennsylvania, without regard to '
        'its conflict-of-laws principles. Any action shall be brought exclusively in the state or federal '
        'courts of Lackawanna County, Pennsylvania, and each party consents to personal jurisdiction there. '
        'Before filing suit, the parties shall first attempt good-faith mediation in Scranton, PA.',
        styles)

    s.append(Spacer(1, 14))
    s.append(callout_box(
        '<b>Acceptance via Stripe checkout.</b> Submitting payment through tradesmen.nepa-pro.com '
        'constitutes acceptance of this Agreement. Customers who require a wet-signature copy for their '
        'records may sign below; this is optional and does not change the legal effect of acceptance via '
        'checkout.',
        styles))
    s.append(Spacer(1, 12))

    s += signature_block('Customer (optional wet signature)',
        ['Signature', 'Printed Name', 'Title (if entity)', 'Entity name (if any)', 'Date'],
        styles)
    s += signature_block('NEPA-PRO LLC',
        ['Signature', 'Printed Name', 'Title', 'Date'],
        styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# ============================================================
# NPCS-002  JOBSITE SAFETY ATTESTATION
# ============================================================
def build_npcs_002():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPCS-002-Jobsite-Safety-Attestation.pdf')
    doc = BrandedDoc(fname,
        doc_title='Jobsite Safety Attestation',
        doc_code='NPCS-002', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Jobsite Safety Attestation',
        'Customer\'s pre-dispatch certification that the Jobsite is reasonably safe for skilled trade work, '
        'and disclosure of any conditions a dispatched tradesperson should know before arrival.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Captures the Customer\'s factual representations about the '
        'Jobsite — utility marking, hazardous materials, access, and any known hazards — so the dispatched '
        'tradesperson is informed and protected. This document does not modify the booking terms in '
        '<b>NPCS-001</b> or the indemnification in <b>NPCS-003</b>; it is the factual record those '
        'documents rely on.',
        styles))
    s.append(Spacer(1, 12))

    # Jobsite identification
    s.append(Paragraph('Section 1 — Jobsite & Booking', styles['h2']))
    s_fields = [
        ('Customer / entity name', 4.5),
        ('Jobsite street address', 4.5),
        ('City / state / ZIP', 4.5),
        ('Booking reference (Stripe receipt # or trade & date)', 4.5),
        ('On-site point of contact (name / cell)', 4.5),
        ('Scheduled dispatch date / time', 4.5),
    ]
    for label, w in s_fields:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    # Section 2 — utility marking
    s.append(Spacer(1, 10))
    s.append(Paragraph('Section 2 — Underground Utility Marking', styles['h2']))
    s.append(Paragraph(
        '<b>Pennsylvania law requires any party who excavates or demolishes to notify Pennsylvania One '
        'Call (call 811 or visit pa1call.org) at least three (3) business days before any digging.</b> '
        'If the booked work involves any excavation, trenching, post-hole, anchoring, drilling into '
        'exterior walls, or pulling underground service, the Customer must complete this section.',
        styles['body']))
    s.append(Spacer(1, 6))

    s.append(Paragraph('Will the booked work involve any digging, excavation, or anchoring into the ground?',
        styles['body']))
    s.append(Paragraph('☐ No — proceed to Section 3 &nbsp;&nbsp;&nbsp; ☐ Yes — complete below', styles['body']))
    s.append(Spacer(1, 6))

    util_fields = [
        ('PA One Call ticket number', 3.5),
        ('Date ticket filed (3 biz days before work)', 3.0),
        ('Date markings completed on site', 3.0),
        ('Marker color legend confirmed?  ☐ Yes  ☐ No', 4.0),
    ]
    for label, w in util_fields:
        s.append(fillable_field(label, width=w, styles=styles))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 4))
    s.append(callout_box(
        '<b>Marker color legend.</b> Red = electric · Yellow = gas/oil · Orange = communications · '
        'Blue = water · Green = sewer · Purple = reclaimed water/irrigation · White = proposed excavation · '
        'Pink = surveying.',
        styles))

    s.append(PageBreak())

    # Section 3 — Hazardous materials disclosure
    s.append(Paragraph('Section 3 — Hazardous Materials Disclosure', styles['h2']))
    s.append(Paragraph(
        'The Customer affirmatively discloses any of the following <b>known or suspected</b> on the '
        'Jobsite. NEPA-PRO subcontractors are not licensed for hazardous-material remediation; if any '
        'are present, the booked work must avoid those areas, or the booking must be re-scoped.',
        styles['body']))
    s.append(Spacer(1, 4))

    haz_items = [
        '☐ Asbestos suspected (typical indicators: pre-1980 construction, vermiculite insulation, 9×9 floor '
        'tiles, popcorn ceilings) — Disclosure: ____________________________________________',
        '☐ Lead paint suspected (typical indicator: pre-1978 housing) — Disclosure: ___________',
        '☐ Mold visible — Location: _______________________________________________________',
        '☐ Mold odor without visible growth — Description: ___________________________________',
        '☐ PCB-containing equipment (e.g., older transformers, ballasts) — Location: __________',
        '☐ Underground oil tank — Location: ________________________________________________',
        '☐ Known sewer / septic backup — Description: _______________________________________',
        '☐ Known structural deficiency / soft floor / failing beam — Location: ________________',
        '☐ Animal infestation (rodents, bats, wasps, etc.) — Description: ____________________',
        '☐ Other hazard: __________________________________________________________________',
        '☐ <b>None of the above is known to the Customer.</b>',
    ]
    for it in haz_items:
        s.append(Paragraph(it, styles['body']))
    s.append(Spacer(1, 6))

    # Section 4 — Access, lighting, services
    s.append(Paragraph('Section 4 — Access and Site Conditions', styles['h2']))
    access_items = [
        '<b>Site access.</b> Tradesperson can reach the work area without entering an active home '
        'office, sleeping area of an unrelated occupant, or any locked space without a designated POC: '
        '☐ Yes &nbsp; ☐ No (explain): ____________________________________________________',
        '<b>Lighting.</b> Adequate natural or artificial lighting is available in the work area: '
        '☐ Yes &nbsp; ☐ No (work zone is dark — please describe): ____________________________',
        '<b>Bathroom access.</b> Tradesperson has access to a bathroom or alternate facility: '
        '☐ Yes &nbsp; ☐ No',
        '<b>Running water available on site:</b> ☐ Yes &nbsp; ☐ No (off-grid)',
        '<b>Pets.</b> Any animals on the property: ☐ No &nbsp; ☐ Yes — will be secured: ______________',
        '<b>Live electrical hazards beyond the booked scope</b> (e.g., a panel that has not been de-'
        'energized, exposed conductors): ☐ None known &nbsp; ☐ Yes (describe): _________________',
        '<b>Active gas / pressurized lines beyond scope:</b> ☐ None known &nbsp; ☐ Yes (describe): _____',
        '<b>Other on-site contractors</b> working at same time: ☐ No &nbsp; ☐ Yes (which trades): _______',
        '<b>Live security cameras / monitoring</b> on the property: ☐ No &nbsp; ☐ Yes',
        '<b>Anyone authorized to be present</b> who is not the Customer: ___________________________',
    ]
    for it in access_items:
        s.append(Paragraph(it, styles['body']))
        s.append(Spacer(1, 3))

    s.append(PageBreak())

    # Section 5 — Customer attestation
    s.append(Paragraph('Section 5 — Customer Attestation', styles['h2']))
    attest_items = [
        '<b>(a)</b> The information above is true, complete, and correct to the best of the Customer\'s '
        'knowledge as of the date signed.',
        '<b>(b)</b> The Customer accepts that NEPA-PRO and the dispatched tradesperson will rely on these '
        'representations in deciding whether to proceed with the engagement and how to perform the work.',
        '<b>(c)</b> If any condition listed above changes between the date this attestation is signed and '
        'the date of dispatch, the Customer will <b>notify NEPA-PRO immediately</b> at 570-677-7971 or '
        'service@nepa-pro.com.',
        '<b>(d)</b> The Customer acknowledges that the tradesperson has stop-work authority under '
        '<b>NPSA-006 § 5</b> and may decline to perform any portion of the booked work that, in the '
        'tradesperson\'s reasonable judgment, exceeds safe field conditions. <b>The Customer remains '
        'responsible for the booked block in such case.</b>',
        '<b>(e)</b> The Customer acknowledges that hazardous-material conditions disclosed in '
        '<b>Section 3</b> may require the booked scope to be modified or rescheduled, and that NEPA-PRO '
        'may pause the engagement to work this out without penalty to NEPA-PRO.',
    ]
    for a in attest_items:
        s.append(Paragraph(a, styles['body']))
        s.append(Spacer(1, 4))

    s.append(Spacer(1, 14))
    s.append(submission_instructions(styles, recipient_role='customer dispatch'))
    s.append(Spacer(1, 12))

    s += signature_block('Customer', ['Signature', 'Printed Name', 'Date'], styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


# ============================================================
# NPCS-003  LIABILITY WAIVER & INDEMNIFICATION
# ============================================================
def build_npcs_003():
    styles = get_styles()
    fname = os.path.join(OUT_DIR, 'NPCS-003-Liability-Waiver-Indemnification.pdf')
    doc = BrandedDoc(fname,
        doc_title='Liability Waiver & Indemnification',
        doc_code='NPCS-003', doc_version='1.0')
    s = []

    s += doc_title_block(
        'Liability Waiver & Indemnification',
        'Allocation of risk between the Customer, NEPA-PRO LLC, and the dispatched tradesperson — '
        'including the limit of NEPA-PRO\'s liability, exclusion of consequential damages, customer '
        'indemnification, and dispute-resolution mechanics.',
        styles)

    s.append(callout_box(
        '<b>Purpose of this document:</b> Allocates legal risk for the booking — what NEPA-PRO is and '
        'is not liable for, the customer\'s indemnification obligation in narrow circumstances, the cap '
        'on NEPA-PRO\'s exposure, and dispute mechanics. This document does not establish booking terms '
        '(<b>NPCS-001</b>) or capture jobsite-condition representations (<b>NPCS-002</b>); both of those '
        'are independent and necessary references.',
        styles))
    s.append(Spacer(1, 10))

    s += numbered_clause(1, 'Definitions',
        '<b>(a)</b> "<b>Customer</b>" — the booking party identified at Stripe checkout or in the signature '
        'block.<br/>'
        '<b>(b)</b> "<b>NEPA-PRO Parties</b>" — NEPA-PRO LLC, its members, officers, employees, agents, '
        'insurers, and dispatched tradespeople (each of whom is an independent 1099 subcontractor under '
        'NPSA-001).<br/>'
        '<b>(c)</b> "<b>Engagement</b>" — a single accepted booking dispatched to a Jobsite.<br/>'
        '<b>(d)</b> "<b>Booking Amount</b>" — the dollar amount paid by the Customer for the Engagement, '
        'exclusive of any later overtime invoice.',
        styles)

    s += numbered_clause(2, 'Customer Indemnification',
        'The Customer shall defend, indemnify, and hold harmless the NEPA-PRO Parties from and against '
        'any and all claims, demands, losses, costs, fines, penalties, judgments, settlements, and '
        'expenses (including reasonable attorneys\' fees) arising out of or related to:<br/><br/>'
        '<b>(a)</b> Any condition on the Jobsite that was not disclosed by the Customer in the Jobsite '
        'Safety Attestation (NPCS-002), or that was disclosed inaccurately, including undisclosed '
        'hazardous materials, unmarked utilities, structural conditions, or biological hazards;<br/><br/>'
        '<b>(b)</b> Any work performed at the Customer\'s specific direction beyond the booked scope, '
        'including any direction the dispatched tradesperson reasonably understood as a Customer '
        'instruction;<br/><br/>'
        '<b>(c)</b> Acts or omissions of any third party present on the Jobsite — including the '
        'Customer\'s employees, family members, guests, neighbors, other contractors, or animals — that '
        'cause injury, death, or property damage;<br/><br/>'
        '<b>(d)</b> Any claim brought by a third party against the NEPA-PRO Parties premised on the '
        'condition of the Jobsite or the Customer\'s use of the labor delivered.',
        styles)

    s += numbered_clause(3, 'Limitation of Liability',
        '<b>(a) Cap.</b> The aggregate liability of the NEPA-PRO Parties for any and all claims arising '
        'out of or relating to an Engagement — whether sounding in contract, tort, negligence, breach of '
        'warranty, statute, or otherwise — is <b>limited to the Booking Amount paid for that Engagement</b>. '
        'Where multiple Engagements are at issue, the cap is applied separately for each Engagement.<br/><br/>'
        '<b>(b) No consequential damages.</b> THE NEPA-PRO PARTIES SHALL NOT BE LIABLE FOR ANY INDIRECT, '
        'INCIDENTAL, CONSEQUENTIAL, SPECIAL, EXEMPLARY, OR PUNITIVE DAMAGES, INCLUDING WITHOUT LIMITATION '
        'LOST PROFITS, LOST PRODUCTIVITY, PROJECT DELAY DAMAGES, LOSS OF USE, OR DIMINUTION IN VALUE, '
        'EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.<br/><br/>'
        '<b>(c) Carve-outs.</b> The cap and exclusion in (a) and (b) do not apply to: (i) liability for '
        'gross negligence or willful misconduct of a NEPA-PRO Party that is established by a court of '
        'competent jurisdiction; (ii) bodily injury claims to the extent covered by NEPA-PRO\'s commercial '
        'general liability insurance; or (iii) any liability that cannot lawfully be limited under '
        'Pennsylvania law.<br/><br/>'
        '<b>(d) Allocation.</b> The Customer expressly acknowledges that the cap and exclusion are an '
        'essential allocation of risk that is reflected in the pricing of the Engagement and that the '
        'Engagement would not be offered at the posted rate without them.',
        styles)

    s += numbered_clause(4, 'Property Damage on the Jobsite',
        '<b>(a)</b> NEPA-PRO and the dispatched tradesperson are liable for property damage on the '
        'Jobsite caused by their <b>gross negligence or willful misconduct</b>, subject to the cap in '
        'Section 3.<br/><br/>'
        '<b>(b)</b> Ordinary wear-and-tear of the Jobsite incidental to the booked work — including dust, '
        'minor scuffs from drop cloths, and necessary marks from layout — is not "damage" for purposes of '
        'this Section.<br/><br/>'
        '<b>(c)</b> Damage caused by a pre-existing condition (e.g., a wall that fails when a fixture is '
        'removed because the wall was already failing), or by undisclosed Jobsite conditions per Section 2, '
        'is the Customer\'s responsibility.',
        styles)

    s += numbered_clause(5, 'Notice of Claim',
        '<b>(a) Time.</b> The Customer shall give written notice of any claim against the NEPA-PRO Parties '
        'within <b>thirty (30) days</b> of the event giving rise to the claim. A claim not noticed within '
        'this period is waived.<br/><br/>'
        '<b>(b) Form.</b> Notice shall be sent to <b>service@nepa-pro.com</b> and copied to '
        '14012 Orchard Drive, Clarks Summit, PA 18411, with: a description of the event; the date and '
        'time; photographic evidence; identification of the dispatched tradesperson and Engagement; and '
        'a statement of the relief sought.<br/><br/>'
        '<b>(c) Cooperation.</b> The Customer shall cooperate in good faith with NEPA-PRO\'s investigation, '
        'including making the Jobsite available for inspection, providing copies of any third-party reports, '
        'and not destroying physical evidence.',
        styles)

    s.append(PageBreak())

    s += numbered_clause(6, 'Mediation; Arbitration; Jury Waiver',
        '<b>(a) Mediation first.</b> The parties shall attempt in good faith to resolve any dispute through '
        'non-binding mediation administered by a mutually agreed neutral mediator in Scranton, PA, before '
        'commencing formal proceedings. The parties shall share the mediator\'s fee equally and bear their '
        'own costs.<br/><br/>'
        '<b>(b) Binding arbitration option.</b> If mediation does not resolve the dispute within ninety '
        '(90) days, either party may elect — by written notice to the other — to submit the dispute to '
        '<b>binding arbitration</b> administered by the American Arbitration Association under its '
        'Commercial Arbitration Rules, seated in Scranton, Pennsylvania, before a single arbitrator '
        'mutually selected. Judgment on the arbitrator\'s award may be entered in any court of competent '
        'jurisdiction.<br/><br/>'
        '<b>(c) Court alternative.</b> If neither party elects arbitration under (b), any unresolved '
        'dispute shall be brought exclusively in the state or federal courts of <b>Lackawanna County, '
        'Pennsylvania</b>, and each party consents to personal jurisdiction there.<br/><br/>'
        '<b>(d) Jury Trial Waiver.</b> EACH PARTY KNOWINGLY, VOLUNTARILY, AND INTENTIONALLY WAIVES THE '
        'RIGHT TO A JURY TRIAL ON ANY DISPUTE ARISING OUT OF OR RELATED TO THIS DOCUMENT, NPCS-001, OR '
        'NPCS-002.<br/><br/>'
        '<b>(e) Class action waiver.</b> Each party agrees that any claim shall be brought in the '
        'party\'s individual capacity and not as a plaintiff or class member in any purported class, '
        'representative, or consolidated proceeding.',
        styles)

    s += numbered_clause(7, 'Insurance Subrogation',
        'To the maximum extent permitted by their respective insurance policies, the Customer and '
        'NEPA-PRO each waive any right of subrogation their insurers may have against the other party '
        'for losses to the extent covered by insurance the waiving party carries. Each party is '
        'responsible for ensuring its own insurance permits this waiver.',
        styles)

    s += numbered_clause(8, 'Governing Law',
        'This Liability Waiver & Indemnification is governed by the laws of the Commonwealth of '
        'Pennsylvania, without regard to its conflict-of-laws principles. The federal Arbitration Act '
        'governs the enforceability of Section 6.',
        styles)

    s += numbered_clause(9, 'Severability; Survival',
        'If any provision of this document is held unenforceable, it shall be enforced to the maximum '
        'extent permitted by law and the remaining provisions shall remain in full force and effect. '
        'The provisions of this document survive completion or termination of the Engagement.',
        styles)

    s.append(Spacer(1, 14))
    s.append(callout_box(
        '<b>Read carefully before signing.</b> This document limits the Customer\'s ability to recover '
        'damages from NEPA-PRO and the dispatched tradesperson, and waives the Customer\'s right to a '
        'jury trial. Customers may consult counsel before signing. Acceptance via Stripe checkout under '
        'NPCS-001 incorporates this document by reference.',
        styles))
    s.append(Spacer(1, 12))

    s += signature_block('Customer', ['Signature', 'Printed Name', 'Title (if entity)', 'Date'], styles)
    s += signature_block('NEPA-PRO LLC', ['Signature', 'Printed Name', 'Title', 'Date'], styles)

    doc.build(s)
    print(f'  ✓ {os.path.basename(fname)}')


if __name__ == '__main__':
    print('NEPA-PRO PDF Generator — Part 2 (Worker docs 4-6 + Customer docs 7-9)')
    print('-' * 60)
    build_npsa_004()
    build_npsa_005()
    build_npsa_006()
    build_npcs_001()
    build_npcs_002()
    build_npcs_003()
    print('-' * 60)
    print('Part 2 complete.')
