# Python libraries
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
    #pdf.write(5, f"Environmental Analytics for Lisbon Report")
    pdf.ln(10)
    #pdf.write(5, f"Report")
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'Time period selected: {initial_date} to {final_date}')
    pdf.ln(5)

def content_report(config: dict, initial_date:str, final_date:str):
    
    # create pdf object
    pdf = FPDF()

    pdfname = config["fname_report"]
    

    ''' First Page '''
    pdf.add_page()
    pdf.image(f'{IMG}/banner.png', 0, 0, WIDTH)
    title (initial_date, final_date, pdf)
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'Temperature map:')
    pdf.image(f'{PLOTS}/temperature.png', 5, 90, WIDTH-20)


    ''' Second Page '''
    pdf.add_page()
    pdf.image(f'{IMG}/banner.png', 0, 0, WIDTH)

    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'Noise map:')
    pdf.image(f'{PLOTS}/noise.png', 5, 90, WIDTH-20)


    ''' Third Page '''
    pdf.add_page()
    pdf.image(f'{IMG}/banner.png', 0, 0, WIDTH)
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'Humidity map:')
    pdf.image(f'{PLOTS}/humidity.png', 5, 90, WIDTH-20)

    pdf.output(pdfname)

def main(config_file: str):

    config = e.read_config(config_file)

    content_report(config) 

if __name__ == '__main__':
  
    main(config_file)
    e.info("REPORT FINISHED!!")