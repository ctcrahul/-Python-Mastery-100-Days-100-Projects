"""                                            Day = 47
                                        
                                            PDF Merger Tool
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import subprocess
import platform

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Tool")
        self.root.geometry("700x450")
        self.pdf_files = []

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="PDF Merger Tool", font=("Helvetica", 16))
        self.title_label.pack(pady=12)

        # Instructions
        self.instruction_label = tk.Label(self.root, text="Select PDFs to merge in the desired order. The list shows full paths to avoid confusion.", font=("Helvetica", 11))
        self.instruction_label.pack(pady=6)

        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=8)

        # Add PDFs Button
        self.add_button = tk.Button(btn_frame, text="Add PDFs", font=("Helvetica", 11), command=self.add_pdfs)
        self.add_button.grid(row=0, column=0, padx=6)

        # Remove Selected
        self.remove_button = tk.Button(btn_frame, text="Remove Selected", font=("Helvetica", 11), command=self.remove_selected)
        self.remove_button.grid(row=0, column=1, padx=6)

        # Clear List
        self.clear_button = tk.Button(btn_frame, text="Clear List", font=("Helvetica", 11), command=self.clear_list)
        self.clear_button.grid(row=0, column=2, padx=6)

        # Listbox to display selected PDFs with a scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, height=12, width=95, selectmode=tk.SINGLE, font=("Helvetica", 10), yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # Merge Button
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=8)

        self.merge_button = tk.Button(action_frame, text="Merge PDFs", font=("Helvetica", 12), command=self.merge_pdfs)
        self.merge_button.grid(row=0, column=0, padx=8)

        self.open_folder_button = tk.Button(action_frame, text="Open Output Folder", font=("Helvetica", 11), command=self.open_output_folder, state=tk.DISABLED)
        self.open_folder_button.grid(row=0, column=1, padx=8)

        # Label to show last output file path
        self.output_label = tk.Label(self.root, text="", font=("Helvetica", 10), fg="green")
        self.output_label.pack(pady=6)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
        if files:
            # preserve order and avoid duplicates
            for f in files:
                if f not in self.pdf_files:
                    self.pdf_files.append(f)
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, pdf in enumerate(self.pdf_files, start=1):
            display = f"{idx}. {pdf}"  # indexed + full path
            self.listbox.insert(tk.END, display)

    def remove_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "No item selected to remove.")
            return
        index = sel[0]
        removed = self.pdf_files.pop(index)
        self.update_listbox()

    def clear_list(self):
        if not self.pdf_files:
            return
        if messagebox.askyesno("Confirm", "Clear all selected files?"):
            self.pdf_files.clear()
            self.update_listbox()
            self.output_label.config(text="")
            self.open_folder_button.config(state=tk.DISABLED)

    def validate_files(self):
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

        output_file = filedialog.asksaveasfilename(title="Save merged PDF as...", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file:
            return

        try:
            merger = PdfMerger()
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_file)
            merger.close()

            # Show success and keep app open
            self.output_label.config(text=f"Merged: {output_file}")
            messagebox.showinfo("Success", f"PDFs merged successfully into:\n{os.path.basename(output_file)}")

            # Enable Open Output Folder button and open merged PDF
            self.last_output = output_file
            self.open_folder_button.config(state=tk.NORMAL)

            # Open the merged PDF with default viewer
            try:
                if platform.system() == "Windows":
                    os.startfile(output_file)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(["open", output_file])
                else:  # Linux variants
                    subprocess.Popen(["xdg-open", output_file])
            except Exception:
                # fallback to subprocess with shell
                subprocess.Popen([output_file], shell=True)

            # Do NOT quit the app; keep the selected files so user can merge again or manage them
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while merging: {str(e)}")

    def open_output_folder(self):
        if not hasattr(self, "last_output") or not self.last_output:
            messagebox.showinfo("Info", "No merged file available yet.")
            return
        folder = os.path.dirname(self.last_output)
        try:
            if platform.system() == "Windows":
                os.startfile(folder)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open folder: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()

#############################################################################################################################################################################
                                                               Thanks for visting keep supporting us
#############################################################################################################################################################################



import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import subprocess
import platform


