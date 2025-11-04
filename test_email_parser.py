from llm_parser import LLMParser

email_bodies = [
"""
TOP URGENT !!

Dear Valued Vendor,

Kindly visit the site and quote below RFQ.

 

Project: Azizi Riveira 8.

Scope: Supply and Replacement of Damaged Aluminium Brown Powder Coated Frame with Glass.

Delivery: Free Delivery at Site.

 

For location and more clarification, please contact - Mohamed Sammil, 054-5825282.

 

Sl. No.

Description

Unit

Qty

1

Supply and Replacement of Damaged Aluminium Brown Powder Coated Frame with Glass, Size: 19x64 cm - Staircase Door

LS

1

 

Kind regards,
ZAYED MADIKERI
PROCUREMENT OFFICER
PROCUREMENT DEPARTMENT

M 	+971 58 8564031	
T 	+971 4 526 5015
 	
F 	+971 4 332 9102
 	 
P.O.BOX 121385	, 	CONRAD HOTEL, 5TH FLOOR, SHEIK ZAYED ROAD	, 	DUBAI	, 
UNITED ARAB EMIRATES
AZIZIDEVELOPMENTS.COM
"""
, 

"""
Dear Sir,

  

We, CPC are tendering for the above-mentioned project with the following technical description stated hereunder: 
                                                  
Project Title                       :  Capital Catering @ Warehouse # A4, Airport Free Zone (ADAFZ) Logistics Park Abu Dhabi, UAE

Client                                       :  ADNEC

Consultant                    :  Cairn Consultancy L.L.C

Contract Type                    :  Lump-sum Price Contract    

Project Location               :   Plot # P6, Sector: Abu Dhabi International Airport, Zone: Al Matar, Abu Dhabi, UAE

Project Duration              :  180 Days

                                                                                                                      

 

Note: kindly download the documents by clicking the attached link (Dropbox) : https://www.dropbox.com/scl/fo/bpau3s8n13ay9lof9nnhx/AFYpP3ZgRUpjR253U9vGubo?rlkey=p1jajrl347kf2bgjs3c6vofzc&st=ump0buwj&dl=0   

 

In this regard, you are cordially invited to submit your price proposal for the above-mentioned subject (Mirrors) as per the attached drawing, specifications and the client's requirements on or before  18 October 2025.
  

Thanking you and looking forward to a desirable response from your end!

If you require any further clarifications please don't hesitate to contact us.

  
Enclosures: BOQ, Specs, Drawings

 

 

Best regards,

 

Shahabas Parol

Tender Department

Documentation Assistant

 

 

Description: Description: CPC Logo

 

Civil Power General Contracting L.L.C.

P.O Box : 42311

Abu Dhabi

United Arab Emirates

Tel: +971 26678812  Ext: 120

Fax: +971 26678814

Mobile: +971 52 2441731

Email: p.shahabas@cpcemirates.ae        

Web: www.cpcemirates.ae
""", 

""" 

Project

:

1462- Modon- Reem hills Development

Client

:

Mudon 

Consultant

:

ECG (Engineering Consultants Group)

Contractor

:

Western Beach Gen. Contracting

Type

:

Job in Hand

Location     

:

https://share.google/kl5sJMBGdTJVUdOgg


Good day!

 

Please provide the best prices for the below .

 

The price shall include the below but not limited to

 

 

Scope of works:

Supply and installation
 

Engineering works (material submittal , shop drawings, method statements )
Supply and installation of below
Aluminium doors and windows
Aluminium curtain walls and windows
Aluminium louver
Aluminium shed
Hinged glass panel
Aluminium Islamic pattern louver
Aluminium louver to minaret
Aluminium Handrail
Aluminium railing and balustrade

 

BOQ different sheet includes but not limited to as below .

Prototype 1 and relevant external works
Prototype 2 and relevant external works
Prototype 3 and relevant external works
Mosque MS 1 and relevant external works
Mosque MS 2 and relevant external works
Retail building and relevant external works
 

Attachments:

 

Specific Drawings : 08. Aluminum Doors & Windows

 

One drive Link:  01. Tender Document

Drawings
Vendor list
Material Cut Sheets
Specs
BOQ (Attached in the email )
 

Payment terms: TBA


Please be informed that the referenced document is deemed to be mutually explanatory and any exceptions from the above requirements should be clearly identified in your proposal offer. Failure to do so will indicate that you are fully compliant with the requirements as stated therein.

 

Please submit your offer on or before 5 days , all correspondences in respect of this tender should be addressed to the undersigned and if you need any clarification, please don’t hesitated to contact.

 

Please acknowledge receipt of the same in a return email and advise if you are interested to quote for this package or not.

 

Uzair Khalid
Acting Procurement Manager
Western Beach General Contracting

📞 +971 58 125 2969
📧 purchase2@westernbeach.ae
📍 Abu Dhabi, United Arab Emirates
🏢 P.O. Box 109069
"""]

parser = LLMParser()
for email_body in email_bodies:
    result = parser.parse_email_body(email_body)
    print(result)
