  tx_type = self.type_var.get()
        try:
            amount = float(self.amount_var.get())
        except Exception:
            messagebox.showerror("Invalid amount", "Please provide a numeric amount.")
            return
