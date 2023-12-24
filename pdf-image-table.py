import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

### Convert Pdf as separate jpg files ###
pdf=st.file_uploader("Upload File:")
if pdf is not None:
    current_directory = os.getcwd()
    image_files = [f for f in os.listdir(current_directory) if f.endswith(".jpg")]
    if not any(f.endswith(".jpg") for f in image_files):
            pages = convert_from_path(pdf.name, 500)
            for num,page in enumerate(pages):
                page.save(pdf.name.split(".")[0] +" Page "+str(num+1)+".jpg","JPEG")
    else:
        pages = convert_from_path(pdf.name, 500)
        images=[]
        for i in range(len(pages)):
            pages=pdf.name.split(".")[0]+' Page '+ str(i+1)+'.jpg'
            images.append(pages)

        #### Page Selection for data extraction ######
        pages=st.selectbox('Select an image: ',images)
        image_path = pages
        invoice_image = Image.open(image_path)
        st.image(invoice_image)


        # # Perform OCR on the image
        text = pytesseract.image_to_string(invoice_image)
        lines = text.split('\n')


        ### Data Extraction with Specific Columns Names with slicing####
        for i, line in enumerate(lines):
            if line.startswith('SERVICE'):
                index_service=lines.index(line)
                key = line.split()
                elements_to_keep = ['SERVICE', 'CODE', 'DESCRIPTION', 'QUANTITY', 'AMOUNT(S$)']
                key = [element for element in key if element in elements_to_keep]
                key = [' '.join(key[:2])] + key[2:]
                index=lines.index(line)

            if line.startswith("Subtotal"):
                index1=lines.index(line)
                selected_table=lines[index+3:index1]

            if line.startswith("Tax Invoice Number"):
                Tax=lines.index(line)
        selected_table_key=lines[Tax:index]
        list=[]        
        for input_string in selected_table_key:
            split_list = input_string.split(':')
            if len(split_list)>1:
                list.append(split_list)

        data_dict = {key: value for key, value in list}
        json_string_key_value = {"Key_Values": data_dict}
        # st.write(json_string_key_value)

        list=[]        
        for input_string in selected_table:
            if input_string!="":
                split_list = input_string.split()
                description = ' '.join(split_list[1:-2])
                result_list = [split_list[0], description,split_list[-2], split_list[-1]]
                list.append(result_list)
        

        result_dicts = [dict(zip(key, values)) for values in list]

        l=[]
        for result_dict in result_dicts:
            l.append(result_dict)

        json_string_table = {"Table": l}
        json_string_key_value.update(json_string_table)

        
        st.write(json_string_key_value)







