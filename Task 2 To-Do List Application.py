import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List Manager")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        # Data storage
        self.tasks = []
        self.task_id = 0
        self.editing_task_id = None
        self.data_file = "tasks.json"
        
        # Style configuration
        self.setup_styles()
        
        # Load existing tasks
        self.load_tasks()
        
        # Create UI
        self.create_widgets()
        self.update_task_list()
        
        # Bind events
        self.bind_events()
        
        # Auto-save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        """Configure modern styling using ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 9))

    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📝 To-Do List Manager", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.task_input = ttk.Entry(input_frame, font=('Arial', 10))
        self.task_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.add_button = ttk.Button(input_frame, text="➕ Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1)
        
        # Task list section
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for better task display
        columns = ('Status', 'Task', 'Created', 'Priority')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.task_tree.heading('Status', text='Status')
        self.task_tree.heading('Task', text='Task')
        self.task_tree.heading('Created', text='Created')
        self.task_tree.heading('Priority', text='Priority')
        
        self.task_tree.column('Status', width=80, minwidth=80)
        self.task_tree.column('Task', width=300, minwidth=200)
        self.task_tree.column('Created', width=100, minwidth=100)
        self.task_tree.column('Priority', width=80, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.task_tree.xview)
        self.task_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid scrollbars and treeview
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Priority selection
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(priority_frame, text="Priority:").grid(row=0, column=0, padx=(0, 5))
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var, 
                                    values=["High", "Medium", "Low"], state="readonly", width=10)
        priority_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        buttons = [
            ("✏️ Edit", self.edit_task),
            ("🗑️ Delete", self.delete_task),
            ("✓ Toggle Complete", self.toggle_complete_task),
            ("🧹 Clear Completed", self.clear_completed),
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=5, pady=5)
            button_frame.columnconfigure(i, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                  relief=tk.SUNKEN, style='Status.TLabel')
        self.status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.update_status()

    def bind_events(self):
        """Bind keyboard and mouse events"""
        self.task_input.bind('<Return>', lambda e: self.add_task())
        self.task_input.bind('<Control-a>', lambda e: self.task_input.select_range(0, tk.END))
        self.task_tree.bind('<Double-1>', lambda e: self.edit_task())
        self.task_tree.bind('<Delete>', lambda e: self.delete_task())
        self.task_tree.bind('<space>', lambda e: self.toggle_complete_task())

    def add_task(self):
        """Add a new task with validation"""
        task_text = self.task_input.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task description.")
            self.task_input.focus()
            return
        
        if len(task_text) > 200:
            messagebox.showwarning("Warning", "Task description is too long (max 200 characters).")
            return
        
        # Create new task
        new_task = {
            'id': self.task_id,
            'text': task_text,
            'completed': False,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'priority': self.priority_var.get()
        }
        
        self.tasks.append(new_task)
        self.task_id += 1
        
        self.update_task_list()
        self.task_input.delete(0, tk.END)
        self.task_input.focus()
        self.update_status()
        
        # Auto-save
        self.save_tasks()

    def edit_task(self):
        """Edit selected task in a popup window"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        
        # Find the task
        item = selection[0]
        task_id = int(self.task_tree.item(item)['values'][0])  # Hidden ID in first column
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        
        if not task:
            messagebox.showerror("Error", "Task not found.")
            return
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x200")
        edit_window.resizable(False, False)
        edit_window.grab_set()  # Make it modal
        
        # Center the window
        edit_window.transient(self.root)
        
        frame = ttk.Frame(edit_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Edit Task:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        edit_entry = tk.Text(frame, height=4, width=40, wrap=tk.WORD, font=('Arial', 10))
        edit_entry.pack(pady=(5, 10), fill=tk.BOTH, expand=True)
        edit_entry.insert(tk.END, task['text'])
        edit_entry.focus()
        
        # Priority selection in edit window
        priority_frame = ttk.Frame(frame)
        priority_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(priority_frame, text="Priority:").pack(side=tk.LEFT)
        edit_priority_var = tk.StringVar(value=task['priority'])
        priority_combo = ttk.Combobox(priority_frame, textvariable=edit_priority_var,
                                    values=["High", "Medium", "Low"], state="readonly")
        priority_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        def save_edit():
            new_text = edit_entry.get(1.0, tk.END).strip()
            if not new_text:
                messagebox.showwarning("Warning", "Task description cannot be empty.")
                return
            
            if len(new_text) > 200:
                messagebox.showwarning("Warning", "Task description is too long (max 200 characters).")
                return
            
            # Update task
            task['text'] = new_text
            task['priority'] = edit_priority_var.get()
            
            self.update_task_list()
            self.save_tasks()
            edit_window.destroy()
        
        def cancel_edit():
            edit_window.destroy()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Save", command=save_edit).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side=tk.RIGHT)
        
        # Bind Enter and Escape keys
        edit_window.bind('<Control-Return>', lambda e: save_edit())
        edit_window.bind('<Escape>', lambda e: cancel_edit())

    def delete_task(self):
        """Delete selected tasks with confirmation"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select task(s) to delete.")
            return
        
        if len(selection) == 1:
            message = "Are you sure you want to delete this task?"
        else:
            message = f"Are you sure you want to delete {len(selection)} tasks?"
        
        if messagebox.askyesno("Confirm Delete", message):
            # Get task IDs to delete
            task_ids = []
            for item in selection:
                values = self.task_tree.item(item)['values']
                if values:  # Make sure values exist
                    task_id = int(values[0]) if values[0] else None
                    if task_id is not None:
                        task_ids.append(task_id)
            
            # Remove tasks
            self.tasks = [task for task in self.tasks if task['id'] not in task_ids]
            
            self.update_task_list()
            self.update_status()
            self.save_tasks()

    def toggle_complete_task(self):
        """Toggle completion status of selected tasks"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select task(s) to toggle completion.")
            return
        
        # Toggle completion for all selected tasks
        for item in selection:
            values = self.task_tree.item(item)['values']
            if values:
                task_id = int(values[0])
                task = next((t for t in self.tasks if t['id'] == task_id), None)
                if task:
                    task['completed'] = not task['completed']
        
        self.update_task_list()
        self.update_status()
        self.save_tasks()

    def clear_completed(self):
        """Remove all completed tasks"""
        completed_count = sum(1 for task in self.tasks if task['completed'])
        
        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear.")
            return
        
        if messagebox.askyesno("Confirm Clear", 
                             f"Are you sure you want to remove {completed_count} completed task(s)?"):
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.update_task_list()
            self.update_status()
            self.save_tasks()

    def update_task_list(self):
        """Update the task display with sorting and formatting"""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Sort tasks: incomplete first, then by priority, then by creation time
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        sorted_tasks = sorted(self.tasks, 
                            key=lambda x: (x['completed'], 
                                         priority_order.get(x['priority'], 1), 
                                         x['created']))
        
        # Add tasks to treeview
        for task in sorted_tasks:
            status = "✓ Done" if task['completed'] else "⏳ Pending"
            
            # Format date
            try:
                created_date = datetime.strptime(task['created'], '%Y-%m-%d %H:%M')
                date_str = created_date.strftime('%m/%d/%y')
            except:
                date_str = task.get('created', 'Unknown')
            
            # Priority emoji
            priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(task['priority'], '🟡')
            priority_text = f"{priority_emoji} {task['priority']}"
            
            item_id = self.task_tree.insert('', tk.END, values=(
                task['id'],  # Hidden ID for reference
                status,
                task['text'],
                date_str,
                priority_text
            ))
            
            # Apply different styling for completed tasks
            if task['completed']:
                self.task_tree.item(item_id, tags=('completed',))
        
        # Configure tags for styling
        self.task_tree.tag_configure('completed', foreground='gray', font=('Arial', 9, 'italic'))

    def update_status(self):
        """Update status bar with task statistics"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        status_text = f"Total: {total} | Pending: {pending} | Completed: {completed}"
        self.status_var.set(status_text)

    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.task_id = data.get('next_id', 0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            self.tasks = []
            self.task_id = 0

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': self.tasks,
                'next_id': self.task_id,
                'saved_at': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")

    def on_closing(self):
        """Handle application closing"""
        self.save_tasks()
        self.root.destroy()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()