# BizCardX-Extracting-Business-Card-Data-with-OCR

Introduction:
In this streamlit web app you can upload an image of a business card and extract relevant information from it using easyOCR. You can view, modify or delete the extracted data in this app. 
This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, 
each with its own business card image and extracted information.

Technologies used for this project:  OCR , Streamlit,  SQL , Data Extraction.

Installation of required packages:
There is a need to install Python, Streamlit, easyOCR, and a database management system like SQLite or MySQL.

Design for the purpose of user interface: 
Create a simple and intuitive user interface using Streamlit that guides users through the process of uploading the business
card image and extracting its information and can use widgets like fileuploader, buttons, and text boxes to make the interface more interactive.

Implementation of the image processing and OCR:
Use easyOCR to extract the relevant information from the uploaded business card image and can use
image processing techniques like resizing, cropping, and thresholding to enhance the image quality before passing it to the OCR engine.

Displaying the extracted information: 
Once the information has been extracted, display that in a clean and organized manner in the Streamlit GUI and using
widgets like tables, text boxes, and labels to present the information.

Implementation of database integration: Using a database management system like MySQL to store the extracted information along with the uploaded
business card image using SQL queries to create tables, insert data, and retrieve data from the database, Update the data and also allowing the user to
delete the data through the streamlit UI.

Result:
The result of the project would be a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR.
The extracted information would include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin
code. The extracted information would then be displayed in the application's graphical user interface (GUI).
The application would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able
to store multiple entries, each with its own business card image and extracted information.
The final application would have a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its
information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button.

Conclusion:
The project would require skills in image processing, OCR, GUI development, and database management. It would also require careful design and planning of the
application architecture to ensure that it is scalable, maintainable, and extensible.
Overall, the result of the project would be a useful tool for businesses and individuals who need to manage business card information efficiently.




