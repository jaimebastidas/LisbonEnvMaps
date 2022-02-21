# Python libraries
from turtle import width
from fpdf import FPDF
from datetime import datetime, timedelta
import os
#from retriving_data import querydata, interpolation, plots
import etl as e

WIDTH = 210
HEIGHT = 297
IMG = "data/static"
PLOTS = "data/plots"



def title(initial_date:str, final_date:str, pdf):
    # Unicode is not yet supported in the py3k version; use windows-1252 standard font
    pdf.set_font('Arial', 'B', 24)  
    pdf.ln(20)
    pdf.cell(200, 7, f"Environmental Analytics for Lisbon", 0, 1, "C" )
    
    pdf.ln(20)
    
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'Time period selected: {initial_date} to {final_date}')
    
def paragraph(pdf, initial_date:str, final_date:str, var:str):

    text = f"""The image below shows the behavoiur of {var} in the time period selected, from  {initial_date} to {final_date}.
            \nEach column is a day in the time period and shows the aveage of the values for the total sensors""" 

    pdf.set_font('Arial', '', 10)
   
    pdf.multi_cell(200, 5, text, 0, 1, "L" )


def content_report(pdfname: str, initial_date:str, final_date:str):

    var = ['temperature', 'noise', 'humidity']
    Paragraph = f"""The image below shows the behavoiur of {var[0]} in the time period selected, from  {initial_date} to {final_date}.
            \nEach column is a day in the time period and shows the aveage of the values for the total sensors"""
    
    # create pdf object
    pdf = FPDF()


    ''' First Page '''
    pdf.add_page()
    pdf.image(f'{IMG}/banner.png', 0, 0, WIDTH)
    title (initial_date, final_date, pdf)
    pdf.ln(10)
    pdf.set_font('Arial', '', 14)
    pdf.cell(200, 10, f"Temperature map:", 0, 1, "C" )
    
    pdf.image(f'{PLOTS}/temperature.png', w = 190 )
    
    paragraph(pdf, initial_date, final_date, var='temperature')
    
    pdf.image(f'{PLOTS}/temp_ts.png', WIDTH/8, 210, h = 70)

    ''' Second Page '''
    pdf.add_page()
    pdf.image(f'{IMG}/banner.png', 0, 0, WIDTH)
    pdf.ln(50)
    pdf.set_font('Arial', '', 14)
    pdf.cell(200, 10, f"Noise map:", 0, 1, "C" )
    
    pdf.image(f'{PLOTS}/noise.png', w = 190 )
    
    paragraph(pdf, initial_date, final_date, var='noise')
    
    pdf.image(f'{PLOTS}/noise_ts.png', WIDTH/8, 210, h = 70)


    ''' Third Page '''
    pdf.add_page()
    pdf.image(f'{IMG}/banner.png', 0, 0, WIDTH)
    pdf.ln(50)
    pdf.set_font('Arial', '', 14)
    pdf.cell(200, 10, f"Humidity map:", 0, 1, "C" )
    
    pdf.image(f'{PLOTS}/humidity.png', w = 190 )
    paragraph(pdf, initial_date, final_date, var='humidity')
    pdf.image(f'{PLOTS}/hum_ts.png', WIDTH/8, 210, h = 70)

    pdf.output(pdfname)

    e.info("REPORT FINISHED!!")

def main():


    content_report() 

if __name__ == '__main__':
    
    main()
