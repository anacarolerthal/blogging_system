import tkinter as tk

class BlogView:
    def __init__():
        view = tk.Tk()
        view.mainloop()
        
    def show_all_posts(self, posts):
        for post in posts:
            print(f"Title: {post[1]}")
            print(f"Content: {post[2]}")
            print("=" * 30)