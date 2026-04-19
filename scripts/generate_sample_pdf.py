from fpdf import FPDF
import os

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Advanced Autonomous Systems Report", ln=True, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="""This report discusses the safety protocols and moral frameworks implemented in the Model X-1 planetary rovers. 

The rovers are governed by the 'Harmony Directives,' a set of three rules designed to protect both the equipment and the environment being explored:

1. Environmental Preservation: Rovers must not permanently alter the terrain unless scientifically necessary.
2. Signal Integrity: Data transmission must be prioritized over physical movement in hazardous conditions.
3. Energy Efficiency: All systems must transition to low-power hibernations during solar eclipses.

The X-1 rovers utilize a unique LIDAR-array combined with thermal imaging to map subsurface lava tubes, which are potential sites for future human habitats.""")

    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "rover_report.pdf")
    pdf.output(output_path)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_sample_pdf()
