A Parking lot system. Developed by Eliram Shemesh on January, 2022.

Specifications:

- The algorithm is powered by OCR Space API - which is able to detect text from images.
- Public transportation vehicles cannot enter the parking lot (their license plates always end with 6 or G).
- Military and law enforcement vehicles are also prohibited (these can be identified by an inclusion of the
letter “L” or “M”)
- Plate numbers which have no letters at all, cannot enter.
- All other vehicles with a license plate are allowed to enter the parking lot.

Instructions:

1. Make sure to download all content from the Github project.
2. Install the latest version of python on your machine.
3. Install the latest version of MySQL on your machine.
4. Create a valid connection to MySQL and login.
5. Create a scheme and call it - "parking_lot"
6. Create a table inside the scheme you created and call it "incoming_vehicles"
7. Create 4 fields inside the table - id(int)(enable - primary key, not NULL, auto increment and generated params),
 plate_number(LONGTEXT), access_granted(BOOLEAN) and timestamp(DATETIME).
8. Sign up OCR to get an API key - https://ocr.space/ocrapi
9. Edit the python file - "config.py" with a text edit app and update the username and password for MySQL.
Also change the api_key to the one you got by email after registration. In addition,
 change to the language in the config file to the relevant language is going to be scanned. Save and close the file.
languages available:
Arabic=ara
Bulgarian=bul
Chinese(Simplified)=chs
Chinese(Traditional)=cht
Croatian = hrv
Czech = cze
Danish = dan
Dutch = dut
English = eng
Finnish = fin
French = fre
German = ger
Greek = gre
Hungarian = hun
Korean = kor
Italian = ita
Japanese = jpn
Polish = pol
Portuguese = por
Russian = rus
Slovenian = slv
Spanish = spa
Swedish = swe
Turkish = tur

10. Locate your image inside the folder and name it - "plate_image", PDF, GIF, PNG, JPG, TIF and BMP are supported.
11. Execute the program by double clicking the "license_plate.py" file.

Notes:
- Image examples for negative and positive expected results can be found in the project's folder.
positive.jpg and negative.png
- All data is stored in the configured database and can be filtered and ordered by date or by any other parameter.
- There is a log file named - "logfile.log" in the project's folder
- For troubleshooting please contact Eliram Shemesh by email - eliram.sh@mooncative.com