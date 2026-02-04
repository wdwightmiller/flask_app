from app import app, db, Fellow

# Your fellows data
fellows_data = [
    ["Montaser Alrjoob", "848-466-9195", "malrjoob@usf.edu"],
    ["George Boghdadi", "813-731-4953", "boghdadig@usf.edu"],
    ["Francine Lucero", "201-960-4247", "flucero@usf.edu"],
    ["Brienne Petcher", "321-749-7977", "riddleb@usf.edu"],
    ["Ammar Rasul", "551-666-2520", "ammarrasul@usf.edu"],
    ["Natasha Santosh", "(612) 817-3711", "nsantosh@usf.edu"],
    ["Ross Huff", "(309) 313-3424", "huff210@usf.edu"],
    ["Lisa Hayes", "(772) 618-3223", "lpressendo@usf.edu"],
    ["Harry Monestime", "(407) 967-0321", "harry10@usf.edu"],
    ["Julie Giurintano", "(813) 892-0519", "jgiurintano@usf.edu"],
    ["Mathew Thomas", "(912) 246-4625", "Tam32@usf.edu"],
    ["Jorden Smith", "228-343-5520", "jordensmith@usf.edu"],
    ["Michael DesRosiers", "813-952-7351", "mdesrosiers@usf.edu"],
    ["Huda Asif", "203-500-8766", "hasif@usf.edu"],
    ["Jennifer Pharr", "401-954-1841", "jenniferpharr@usf.edu"],
    ["Alaa Alabdul Razzaq", "312-522-6884", "alabdulrazzaq@usf.edu"],
    ["Brian Soto", "305-297-3194", "bsoto43@usf.edu"],
]

# Import them
with app.app_context():
    for row in fellows_data:
        fellow = Fellow(
            name=row[0],
            phone_number=row[1],
            email=row[2]
        )
        db.session.add(fellow)
    db.session.commit()
    print(f"Successfully added {len(fellows_data)} fellows!")