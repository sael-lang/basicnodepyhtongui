#  Install the necessary packages using conda:
# conda install requests
# conda install tk
#python filename.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests

class SchoolManagementApp:
    def __init__(self, root): # You can choose a different theme (e.g., "blue", "equilux", "radiance", etc.)
        
        self.label = ttk.Label(root, text="School ID:")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.school_id_entry = ttk.Entry(root)
        self.school_id_entry.grid(row=0, column=1, padx=10, pady=10)

        self.get_button = ttk.Button(root, text="Get School by ID", command=self.get_school)
        self.get_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.get_all_button = ttk.Button(root, text="Get All Schools", command=self.get_all_schools)
        self.get_all_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.post_button = ttk.Button(root, text="Post School", command=self.post_school)
        self.post_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.edit_button = ttk.Button(root, text="Edit School", command=self.edit_school)
        self.edit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.delete_button = ttk.Button(root, text="Delete School", command=self.delete_school)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Table to display results
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "City", "State", "Country", "Organization"))
        self.tree.grid(row=6, column=0, columnspan=2, pady=10)

        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="Name")
        self.tree.heading("#2", text="City")
        self.tree.heading("#3", text="State")
        self.tree.heading("#4", text="Country")
        self.tree.heading("#5", text="Organization")

        self.tree.column("#0", stretch=tk.NO, width=50)
        self.tree.column("#1", stretch=tk.NO, width=150)
        self.tree.column("#2", stretch=tk.NO, width=100)
        self.tree.column("#3", stretch=tk.NO, width=100)
        self.tree.column("#4", stretch=tk.NO, width=100)
        self.tree.column("#5", stretch=tk.NO, width=150)    
    def get_school(self):
        school_id = self.school_id_entry.get()
        if not school_id:
            messagebox.showerror("Error", "Please enter a School ID")
            return

        try:
            response = requests.get(f'http://localhost:3000/api/schools/{school_id}')
            school_data = response.json()
            messagebox.showinfo("School Data", f"Name: {school_data['name']}\nAddress: {school_data['address']}\nOrganization: {school_data['organization']}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {e}")

    def get_all_schools(self):
        try:
            response = requests.get('http://localhost:3000/api/schools')
            schools_data = response.json()

            # Clear previous data in the table
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new data into the table
            for school in schools_data:
                self.tree.insert("", tk.END, values=(
                    school['_id'],
                    school['name'],
                    school['address']['city'],
                    school['address']['state'],
                    school['address']['country'],
                    school['organization']['name']
                ))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {e}")


    def post_school(self):
        name = simpledialog.askstring("Input", "Enter School Name:")
        city = simpledialog.askstring("Input", "Enter City:")
        state = simpledialog.askstring("Input", "Enter State:")
        country = simpledialog.askstring("Input", "Enter Country:")
        org_name = simpledialog.askstring("Input", "Enter Organization Name:")
        org_type = simpledialog.askstring("Input", "Enter Organization Type:")

        if not name or not city or not state or not country or not org_name or not org_type:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        data = {
            "name": name,
            "address": {
                "city": city,
                "state": state,
                "country": country
            },
            "organization": {
                "name": org_name,
                "type": org_type
            }
        }

        try:
            response = requests.post('http://localhost:3000/api/schools', json=data)
            if response.status_code == 201:
                messagebox.showinfo("Success", "School posted successfully.")
            else:
                messagebox.showerror("Error", f"Failed to post school. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to post school: {e}")

    def edit_school(self):
        school_id = self.school_id_entry.get()
        if not school_id:
            messagebox.showerror("Error", "Please enter a School ID")
            return

        name = simpledialog.askstring("Input", "Enter School Name:")
        city = simpledialog.askstring("Input", "Enter City:")
        state = simpledialog.askstring("Input", "Enter State:")
        country = simpledialog.askstring("Input", "Enter Country:")
        org_name = simpledialog.askstring("Input", "Enter Organization Name:")
        org_type = simpledialog.askstring("Input", "Enter Organization Type:")

        if not name or not city or not state or not country or not org_name or not org_type:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        data = {
            "name": name,
            "address": {
                "city": city,
                "state": state,
                "country": country
            },
            "organization": {
                "name": org_name,
                "type": org_type
            }
        }

        try:
            response = requests.put(f'http://localhost:3000/api/schools/{school_id}', json=data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "School updated successfully.")
            elif response.status_code == 201:
                messagebox.showinfo("Success", "New school created successfully.")
            else:
                messagebox.showerror("Error", f"Failed to update school. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to update school: {e}")

    def delete_school(self):
        school_id = self.school_id_entry.get()
        if not school_id:
            messagebox.showerror("Error", "Please enter a School ID")
            return

        try:
            response = requests.delete(f'http://localhost:3000/api/schools/{school_id}')
            if response.status_code == 204:
                messagebox.showinfo("Success", "School deleted successfully.")
            else:
                messagebox.showerror("Error", f"Failed to delete school. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to delete school: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementApp(root)
    root.mainloop()
