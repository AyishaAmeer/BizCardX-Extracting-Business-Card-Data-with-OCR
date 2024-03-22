import mysql.connector
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re


st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR",
                   layout="wide",
                   page_icon='🗃️',
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This OCR app is created by *Ayisha*!"""})
st.markdown("<h1 style='text-align: center; color: Blue;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)

#hide the streamlit main and footer
hide_default_format = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_default_format, unsafe_allow_html=True)

def app_background():
    st.markdown(f""" <style>.stApp {{
                            background: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDMRBHN44YW9gdwovyoDsLnXUbxUdb1BBaRg&usqp=CAU");
                            background-size: cover}}
                         </style>""", unsafe_allow_html=True)

app_background()

selected = option_menu("Main Icons", ["Home","Upload & Extract","Modify"],
                       icons=["house","upload","gear"],

                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "25px", "text-align": "centre", "margin": "0px", "--hover-color": "#AB63FA", "transition": "color 0.3s ease, background-color 0.3s ease"},
                               "icon": {"font-size": "25px"},
                               "container" : {"max-width": "6000px", "padding": "10px", "border-radius": "5px"},
                               "nav-link-selected": {"background-color": "#AB63FA", "color": "black"}})

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

#connection to mysql
config={"user":"root",
        "password":"Aspnas@2020",
        "host":"127.0.0.1",
        "database":"bizcarddb",
        "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

create_query=''' CREATE TABLE IF NOT EXISTS card_data
                 (
                  company_name varchar(50),
                  card_holder varchar(50),
                  designation varchar(50),
                  mobile_number varchar(50),
                  email varchar(50),
                  website varchar(50),
                  area varchar(100),
                  city varchar(100),
                  state varchar(50),
                  pin_code varchar(50)
                  
                  )'''
cursor.execute(create_query)
#connection.commit()

if selected == "Home":
        st.markdown("## :green[**Technologies Used :**] :rainbow[Python,easy OCR, Streamlit, SQL, Pandas]")
        st.markdown("## :green[**Overview of this project:**]") 
        st.markdown("## :orange[**Design the user interface:**] :violet[Create a simple and intuitive user interface using Streamlit that guides users through the process of uploading the businesscard image and extracting its information using widgets like fileuploader, buttons, and text boxes to make the interface more interactive.]")
        st.markdown("## :orange[**Implemention of image processing and OCR:**] :violet[Use easyOCR to extract the relevant information from the uploaded business card image. Here using image processing techniques like resizing, cropping, and thresholding to enhance the image quality.]")
        st.markdown("## :orange[**Display of extracted information:**] :violet[Once the information has been extracted, displaying in clean and organized manner in the Streamlit GUI using widgets like tables, text boxes, and labels to present the information.]")
        st.markdown("## :orange[**Implemention of database integration:**] :violet[Use a database management system likeSQLite or MySQL to store the extracted information along with the uploadedbusiness card image. You can use SQL queries to create tables, insert data,and retrieve data from the database, Update the data and Allow the user todelete the data through the streamlit UI]")
# Create the 'uploaded_cards' directory if it does not exist
if not os.path.exists("uploaded_cards"):
    os.makedirs("uploaded_cards")

# UPLOAD AND EXTRACT MENU
if selected == "Upload & Extract":
    st.subheader(":orange[Upload a Business Card]")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:

        def save_card(uploaded_card):
            with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())


        save_card(uploaded_card)
        
        def image_preview(image, res):
            for (bbox, text, prob) in res:
                # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Processing image Please wait ..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))
        #easy OCR
        saved_img = os.getcwd()+ "\\" + "uploaded_cards"+ "\\"+ uploaded_card.name
        result = reader.readtext(saved_img,detail = 0,paragraph=False)

        def binary_img(file_path):
            with open(file_path, 'rb') as file:
                binaryData = file.read()
            return binaryData


        data = {"company_name": [],
                "card_holder": [],
                "designation": [],
                "mobile_number": [],
                "email": [],
                "website": [],
                "area": [],
                "city": [],
                "state": [],
                "pin_code": [],
                #"image": binary_img(saved_img)
                }

        def get_data(res):
            for ind, i in enumerate(res):
                if "www " in i.lower() or "www." in i.lower():  # Website with 'www'
                    data["website"].append(i)
                elif "WWW" in i:  # In case the website is in the next elements of the 'res' list
                    website = res[ind + 1] + "." + res[ind + 2]
                    data["website"].append(website)
                elif '@' in i:
                    data["email"].append(i)
                # To get MOBILE NUMBER
                pattern=r'\d{3}-\d{3}-\d{4}'
                if re.findall(pattern, i):
                    data["mobile_number"].append(i)
                elif re.findall('-',i):
                    data['mobile_number'].append(i)
                    
                        
                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["company_name"].append(i)
                    if data["company_name"]==['St ,']:
                        data["company_name"].pop(0)
                        data['company_name'].append(res[-4]+res[-2])

                # To get Card Holder Name
                elif ind == 0:
                    data["card_holder"].append(i)
                #To get designation
                elif ind == 1:
                    data["designation"].append(i)

                #To get area
                if re.findall('^[0-9].+, [a-zA-Z]',i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-z]+',i):
                    data["area"].append(i)
                #To get city name
                match1 = re.findall('.+St , ([a-zA-Z]+).+',i)
                match2 = re.findall('.+St,,([a-zA-Z]+).+',i)
                match3 = re.findall('^[E].*',i)
                
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])
                
                #To get state name
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["state"].append(i.split()[-1])
                if len(data["state"]) == 2:
                    data["state"].pop(0)

                #To get Pincode
                if len(i) >= 6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["pin_code"].append(i[10:])
        get_data(result)

        #Creating a dataframe and storing in DB
        def create_df(data):
            df = pd.DataFrame.from_dict(data, orient='index')
            return df.T
        
        if len(data["mobile_number"]) == 2:
            data['mobile_number']=[' & '.join(data['mobile_number'])]
        match4 = []
        if len(data['city'])==0:
            data["city"].append(res[2][-2][13:21])
        with col1:
            st.write(data)
        df = create_df(data)
        st.success("### Data Extracted ")
        st.write(df)

        if st.button("Upload to Database"):
            for i,row in df.iterrows():
                # here %S means string values
                sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code)
                                         values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values=(row["company_name"],
                        row["card_holder"],
                        row["designation"],
                        row["mobile_number"],
                        row["email"],
                        row["website"],
                        row["area"],
                        row["city"],
                        row["state"],
                        row["pin_code"])
                cursor.execute(sql, values)
                connection.commit()
            st.success("#### Uploaded to database successfully!")

if selected == "Modify":
    col1,col2,col3 = st.columns([2,3,1])
    col2.title(":blue[Delete Or Update The Data Here]")
    column1,column2 = st.columns(2,gap='large')
    try :
        with column1:
            cursor.execute("Select card_holder FROM card_data")
            result = cursor.fetchall()
            #st.write(result)
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
        st.subheader(":orange[Modify Card Details Here:]")    
        selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
        st.markdown("#### Update or modify any data below")
        cursor.execute("select * from card_data where card_holder=%s",(selected_card,))
            
            
        result = cursor.fetchone()
        # DISPLAYING ALL THE INFORMATIONS
        company_name = st.text_input("Company_Name", result[0])
        card_holder = st.text_input("Card_Holder", result[1])
        designation = st.text_input("Designation", result[2])
        mobile_number = st.text_input("Mobile_Number", result[3])
        email = st.text_input("Email", result[4])
        website = st.text_input("Website", result[5])
        area = st.text_input("Area", result[6])
        city = st.text_input("City", result[7])
        state = st.text_input("State", result[8])
        pin_code = st.text_input("Pin_Code", result[9])

        if st.button("Commit changes to DB"):
            # Update the information for the selected business card in the database
            Update_query="""UPDATE card_data SET company_name=%s,card_holder= %s,designation=%s,mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                        WHERE card_holder=%s"""
            values=(company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code,
            selected_card)
            
            cursor.execute(Update_query,values)
            connection.commit()
            #cursor.fetchall()
            
            if st.success("Information updated in database successfully."):
                st.balloons()

        with column1:
            cursor.execute("SELECT card_holder FROM card_data")
            result = cursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            st.subheader(":orange[Delete Card here:]")
            selected_card = st.selectbox("Select a card holder name to Delete", business_cards.keys())
            
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Proceed to delete this card?")

            if st.button("Yes Delete Business Card"):
                cursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
                connection.commit()
                st.success("Business card information deleted from database.")
        with column2:
            st.image('https://www.guidingtech.com/wp-content/uploads/remove-remembered-credit-cards-from-iPhone_4d470f76dc99e18ad75087b1b8410ea9.png')
    except:
        st.warning("There is no data available in the database")

    if st.button("View updated data"):
        cursor.execute(
            "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(cursor.fetchall(),
                                  columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
                                           "Website", "Area", "City", "State", "Pin_Code"])
        st.write(updated_df)        
