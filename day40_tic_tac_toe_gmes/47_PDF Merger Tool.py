"""                                            Day = 47
                                        
                                            PDF Merger Tool
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Tool")
        self.root.geometry("600x400")
        self.pdf_files = []
        
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="PDF Merger Tool", font=("Helvetica", 16))
        self.title_label.pack(pady=20)

        # Instructions
        self.instruction_label = tk.Label(self.root, text="Select PDFs to merge in the desired order.", font=("Helvetica", 12))
        self.instruction_label.pack(pady=10)

        # Add PDFs Button
        self.add_button = tk.Button(self.root, text="Add PDFs", font=("Helvetica", 12), command=self.add_pdfs)
        self.add_button.pack(pady=10)

        # Listbox to display selected PDFs
        self.listbox = tk.Listbox(self.root, height=10, width=50, selectmode=tk.SINGLE, font=("Helvetica", 12))
        self.listbox.pack(pady=20)

        # Merge Button
        self.merge_button = tk.Button(self.root, text="Merge PDFs", font=("Helvetica", 12), command=self.merge_pdfs)
        self.merge_button.pack(pady=10)

    def add_pdfs(self):
        # Open file dialog to select PDFs
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            # Add selected files to the list
            self.pdf_files.extend(files)
            self.update_listbox()

    def update_listbox(self):
        # Clear current listbox and show updated list of PDFs
        self.listbox.delete(0, tk.END)
        for pdf in self.pdf_files:
            self.listbox.insert(tk.END, os.path.basename(pdf))

    def validate_files(self):
        # Check if all selected PDFs exist
        for pdf in self.pdf_files:
            if not os.path.exists(pdf):
                messagebox.showerror("Error", f"File {os.path.basename(pdf)} does not exist!")
                return False
        return True

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("Error", "No PDFs selected!")
            return
        
        if not self.validate_files():
            return

        # Output file name input box
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_file:
            try:
                # Create PDF Merger object and merge files
                merger = PdfMerger()
                for pdf in self.pdf_files:
                    merger.append(pdf)
                merger.write(output_file)
                merger.close()

                messagebox.showinfo("Success", f"PDFs merged successfully into {os.path.basename(output_file)}")
                self.pdf_files.clear()  # Clear the list after merge
                self.update_listbox()   # Update the listbox
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()


#############################################################################################################################################################################
                                                               Thanks for visting keep supporting us
#############################################################################################################################################################################
