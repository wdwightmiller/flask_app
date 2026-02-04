from app import app, db, Faculty

# Your faculty data
faculty_data = [
    ["W. McDowell Anderson", "813-390-2929", "wanders2@usf.edu"],
    ["Arthur Andrews", "813-986-5425", "arthur.andrews@va.gov"],
    ["Michael Burke", "941-799-1635", "michael.burke5@va.gov"],
    ["Karel Calero", "786-253-3075", "karel.calero@va.gov"],
    ["Humayun Lodhi", "573-819-0531", "humayun.lodhi@va.gov"],
    ["Ana Negron", "813-992-0177", "ana.negron@va.gov"],
    ["Vanessa Ohleyer", "727-482-6800", "vanessa.ohleyer@va.gov"],
    ["Kevin Patel", "903-278-0764", "kevin.patel2@va.gov"],
    ["Daniel Schwartz", "813-503-5147", "daniel.schwartz3@va.gov"],
    ["Rakesh Shah", "813-390-7798", "rakesh.shah@va.gov"],
    ["Benjamin Sudolcan", "608-320-6580", "benjamin.sudolcan@va.gov"],
    ["Jeffrey Timby", "757-615-2193", "jeffrey.timby@va.gov"],
    ["Thomas Truncale", "813-340-7626", "thomas.truncale@va.gov"],
    ["Jennifer Cox", "813-380-3568", "Jennifer.Cox@moffitt.org"],
    ["Jaskaran Sethi", "312-973-0126", "Jaskaran.Sethi@moffitt.org"],
    ["Eduardo Celis", "313-676-0377", "Eduardo.Celis@moffitt.org"],
    ["Sisir Akkineni", "703-981-5453", "akkinenis@usf.edu"],
    ["Endri Ceka", "775-200-2538", "ceka@usf.edu"],
    ["Jason Cummings", "321-288-1575", "jasoncummings@usf.edu"],
    ["Adiac Espinosa Hernandez", "656-231-9393", "adiace@usf.edu"],
    ["Alberto Goizueta", "386-362-9304", "agoizueta@usf.edu"],
    ["Jose David Herazo-Maya", "412-616-1070", "jherazomaya@usf.edu"],
    ["Charles Hunley", "407-927-7955", "charleshunley@usf.edu"],
    ["Brenda Juan", "412-616-1071", "brendajuan@usf.edu"],
    ["Anita Magoon", "813-545-0030", "amagoon@usf.edu"],
    ["Daniel Mathew", "404-754-5529", "danielmathew@usf.edu"],
    ["Dwight Miller", "540-292-6008", "millerw5@usf.edu"],
    ["Ishna Poojary", "201-232-2999", "ipoojaryhohman@usf.edu"],
    ["Jason Prater", "251-622-3341", "jprater2@usf.edu"],
    ["Raheel Qureshi", "631-786-5478", "muhammadraheelq@usf.edu"],
    ["Ricardo Jaramillo Restrepo", "215-964-7399", "ricardo@usf.edu"],
    ["Adam Schwartz", "561-906-3101", "ajschwar@usf.edu"],
    ["Ronaldo Sevilla", "507-993-8845", "ronaldos@usf.edu"],
    ["Ahmed Shawkat", "610-505-5109", "shawkata@usf.edu"],
    ["Adetomiwa Shokunbi", "813-767-6845", "shokunbia@usf.edu"],
    ["Chakrapol Sriaroon", "813-997-7019", "csriaroo@usf.edu"],
    ["Israel Ugalde", "305-710-6560", "icugalde@usf.edu"],
    ["Askin Uysal", "917-543-4308", "askinuysal@usf.edu"],
    ["Marsha Antoine", "407-587-5401", "mhantoin@usf.edu"],
    ["Christopher Chew", "860-371-4590", "cchew@usf.edu"],
    ["Nhi Luu", "813-944-9121", "nhiluu@usf.edu"],
    ["Bianca Dominguez", "813-833-0058", "bmdominguez@usf.edu"],
    ["Shiwani Kamanth", "727-247-8789", "shiwanikamath@usf.edu"],
    ["Nicole Haghshenas", "217-417-5155", "nhaghshenas@usf.edu"],
]

# Import them
with app.app_context():
    for row in faculty_data:
        faculty = Faculty(
            name=row[0],
            phone_number=row[1],
            email=row[2]
        )
        db.session.add(faculty)
    db.session.commit()
    print(f"Successfully added {len(faculty_data)} faculty members!")