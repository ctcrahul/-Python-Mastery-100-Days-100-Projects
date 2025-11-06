                                                        Day = 49

                                                  Social Media Scraper
"""
Social Media Scraper UI (Twitter/X and Instagram)
- Twitter/X scraping via snscrape (public tweets)
- Instagram scraping via instaloader (public posts)
- Tkinter GUI with table preview and CSV/JSON export

Limits & behavior:
- Only public content. Does NOT bypass authentication.
- Lightweight rate limiting for politeness.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import pandas as pd
import platform
import os
import json

# External libs (snscrape, instaloader)
# If not installed, instruct user in the GUI.
try:
    import snscrape.modules.twitter as sntwitter
except Exception:
    sntwitter = None

try:
    import instaloader
except Exception:
    instaloader = None

# ---------------------------
# Scraping helper functions
# ---------------------------

def scrape_twitter_by_user(username: str, limit: int = 100):
    """
    Uses snscrape to fetch public tweets from a username.
    Returns a list of dicts.
    """
    if sntwitter is None:
        raise ImportError("snscrape is not installed. pip install snscrape")
    results = []
    query = f"from:{username}"
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "platform": "twitter",
            "id": tweet.id,
            "date": tweet.date.isoformat(),
            "username": tweet.user.username,
            "display_name": tweet.user.displayname,
            "content": tweet.content,
            "replyCount": tweet.replyCount,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount,
            "quoteCount": getattr(tweet, "quoteCount", None),
            "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        })
    return results

def scrape_twitter_by_hashtag(hashtag: str, limit: int = 100):
    if sntwitter is None:
        raise ImportError("snscrape is not installed. pip install snscrape")
    results = []
    query = f"#{hashtag}"
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "platform": "twitter",
            "id": tweet.id,
            "date": tweet.date.isoformat(),
            "username": tweet.user.username,
            "display_name": tweet.user.displayname,
            "content": tweet.content,
            "replyCount": tweet.replyCount,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount,
            "quoteCount": getattr(tweet, "quoteCount", None),
            "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        })
    return results

def scrape_instagram_by_user(username: str, limit: int = 50):
    """
    Uses instaloader to fetch recent public posts from a username.
    Returns a list of dicts. Requires 'instaloader' installed.
    """
    if instaloader is None:
        raise ImportError("instaloader is not installed. pip install instaloader")
    L = instaloader.Instaloader(download_pictures=False, download_videos=False,
                                download_video_thumbnails=False, save_metadata=False,
                                compress_json=False, dirname_pattern=".")
    results = []
    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except Exception as e:
        raise RuntimeError(f"Unable to load Instagram profile: {e}")

    count = 0
    for post in profile.get_posts():
        if count >= limit:
            break
        caption = post.caption or ""
        results.append({
            "platform": "instagram",
            "id": post.shortcode,
            "date": post.date_utc.isoformat(),
            "username": profile.username,
            "display_name": profile.full_name,
            "content": caption,
            "likes": getattr(post, "likes", None),
            "comments": getattr(post, "comments", None),
            "url": f"https://www.instagram.com/p/{post.shortcode}/"
        })
        count += 1
        # polite pause
        time.sleep(0.2)
    return results

# ---------------------------
# Tkinter UI
# ---------------------------

class SocialScraperUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Scraper — Twitter & Instagram (public only)")
        self.root.geometry("1000x650")

        self.data = []  # collected items
        self._build_ui()

    def _build_ui(self):
        top = tk.Frame(self.root, padx=12, pady=8)
        top.pack(fill="x")

        # Platform selection
        tk.Label(top, text="Platform:").grid(row=0, column=0, sticky="w")
        self.platform_var = tk.StringVar(value="twitter_user")
        platform_menu = ttk.Combobox(top, textvariable=self.platform_var, width=26, state="readonly")
        platform_menu["values"] = [
            "twitter_user", "twitter_hashtag", "instagram_user"
        ]
        platform_menu.grid(row=0, column=1, padx=6)

        # Target input
        tk.Label(top, text="Target (username or hashtag):").grid(row=0, column=2, sticky="w", padx=(12,0))
        self.target_entry = tk.Entry(top, width=35)
        self.target_entry.grid(row=0, column=3, padx=6)

        # Limit input
        tk.Label(top, text="Limit:").grid(row=0, column=4, sticky="w", padx=(12,0))
        self.limit_var = tk.IntVar(value=50)
        tk.Entry(top, textvariable=self.limit_var, width=6).grid(row=0, column=5, padx=6)

        # Controls
        self.scrape_btn = tk.Button(top, text="Start Scrape", command=self.start_scrape, bg="#2b7a78", fg="white")
        self.scrape_btn.grid(row=0, column=6, padx=8)
        self.clear_btn = tk.Button(top, text="Clear Results", command=self.clear_results)
        self.clear_btn.grid(row=0, column=7, padx=4)

        # Status
        self.status_var = tk.StringVar(value="Idle")
        tk.Label(top, textvariable=self.status_var, fg="#555").grid(row=1, column=0, columnspan=8, sticky="w", pady=(8,0))

        # Middle: Treeview showing results
        mid = tk.Frame(self.root)
        mid.pack(fill="both", expand=True, padx=12, pady=8)

        cols = ("platform", "date", "username", "content", "url")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            # give content a bit more width
            width = 180 if c == "content" else 120
            self.tree.column(c, width=width, anchor="w")
        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(mid, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.pack(side="top", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Bottom: export and preview
        bottom = tk.Frame(self.root, pady=8)
        bottom.pack(fill="x", padx=12)

        tk.Button(bottom, text="Export CSV", command=self.export_csv).pack(side="left", padx=6)
        tk.Button(bottom, text="Export JSON", command=self.export_json).pack(side="left", padx=6)
        tk.Button(bottom, text="Open Output Folder", command=self.open_output_dir).pack(side="left", padx=6)

        tk.Button(bottom, text="Show Selected Details", command=self.show_selected).pack(side="right", padx=6)

        # default output folder
        self.output_dir = os.path.join(os.getcwd(), "scraper_outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    # --------- Actions ----------
    def start_scrape(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Input", "Enter a username or hashtag.")
            return

        platform_choice = self.platform_var.get()
        limit = int(self.limit_var.get() or 50)
        self.scrape_btn.config(state="disabled")
        self.status_var.set("Scraping... (this runs in background)")

        # run scraper in a thread so UI stays responsive
        t = threading.Thread(target=self._scrape_worker, args=(platform_choice, target, limit), daemon=True)
        t.start()

    def _scrape_worker(self, platform_choice, target, limit):
        try:
            items = []
            if platform_choice == "twitter_user":
                # if user provided with @, strip it
                username = target.lstrip("@")
                items = scrape_twitter_by_user(username, limit=limit)
            elif platform_choice == "twitter_hashtag":
                hashtag = target.lstrip("#")
                items = scrape_twitter_by_hashtag(hashtag, limit=limit)
            elif platform_choice == "instagram_user":
                username = target.lstrip("@")
                items = scrape_instagram_by_user(username, limit=limit)
            else:
                raise ValueError("Unknown platform choice.")

            # small polite pause
            time.sleep(0.2)
            self._on_scrape_complete(items)
        except Exception as exc:
            self._on_scrape_error(exc)

    def _on_scrape_complete(self, items):
        # Update data & UI on main thread
        def _update():
            self.data = items
            self._refresh_treeview()
            self.status_var.set(f"Done. {len(items)} items collected.")
            self.scrape_btn.config(state="normal")
        self.root.after(0, _update)

    def _on_scrape_error(self, exc):
        def _err():
            self.status_var.set("Error during scrape.")
            messagebox.showerror("Scrape error", str(exc))
            self.scrape_btn.config(state="normal")
        self.root.after(0, _err)

    def _refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.data:
            # truncate content for preview
            content_preview = (item.get("content") or "")[:200].replace("\n"," ")
            self.tree.insert("", "end", values=(item.get("platform"), item.get("date"), item.get("username"), content_preview, item.get("url")))

    def clear_results(self):
        if messagebox.askyesno("Clear", "Clear current results?"):
            self.data = []
            self._refresh_treeview()
            self.status_var.set("Cleared results.")

    def export_csv(self):
        if not self.data:
            messagebox.showinfo("No data", "No items to export.")
            return
        df = pd.DataFrame(self.data)
        default_path = os.path.join(self.output_dir, f"scrape_{int(time.time())}.csv")
        path = filedialog.asksaveasfilename(initialfile=os.path.basename(default_path), defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"CSV saved: {path}")

    def export_json(self):
        if not self.data:
            messagebox.showinfo("No data", "No items to export.")
            return
        default_path = os.path.join(self.output_dir, f"scrape_{int(time.time())}.json")
        path = filedialog.asksaveasfilename(initialfile=os.path.basename(default_path), defaultextension=".json", filetypes=[("JSON files","*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Saved", f"JSON saved: {path}")

    def show_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Select a row first.")
            return
        idx = self.tree.index(sel[0])
        item = self.data[idx]
        text = json.dumps(item, indent=2, ensure_ascii=False)
        # show in a simple popup with a scrollable Text
        top = tk.Toplevel(self.root)
        top.title("Item details")
        txt = tk.Text(top, wrap="word", width=100, height=30)
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", text)
        txt.config(state="disabled")

    def open_output_dir(self):
        if platform.system() == "Windows":
            os.startfile(self.output_dir)
        elif platform.system() == "Darwin":
            os.system(f"open {self.output_dir}")
        else:
            os.system(f"xdg-open {self.output_dir}")

# ---------------------------
# Run the app
# ---------------------------

def main():
    root = tk.Tk()
    app = SocialScraperUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

############################################################################################################################################################################
                                                       Thanks for visting keep supporting
############################################################################################################################################################################



      idx = self.tree.index(sel[0])
        item = self.data[idx]
        text = json.dumps(item, indent=2, ensure_ascii=False)
        # show in a simple popup with a scrollable Text
        top = tk.Toplevel(self.root)
        top.title("Item details")
        txt = tk.Text(top, wrap="word", width=100, height=30)
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", text)
        txt.config(state="disabled")

        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Saved", f"JSON saved: {path}")

    def export_csv(self):
        if not self.data:
            messagebox.showinfo("No data", "No items to export.")
            retur
          

def main():
  
    def export_json(self):
        if not self.data:
            messagebox.showinfo("No data", "No items to export.")
            return
        default_path = os.path.join(self.output_dir, f"scrape_{int(time.time())}.json")
        path = filedialog.asksaveasfilename(initialfile=os.path.basename(default_path), defaultextension=".json", filetypes=[("JSON files","*.json")])
        if not path:
          
      def show_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Select a row first.")
            return
    root = tk.Tk()
    app = SocialScraperUI(root)
    root.mainloop()

        df = pd.DataFrame(self.data)
        default_path = os.path.join(self.output_dir, f"scrape_{int(time.time())}.csv")
        path = filedialog.asksaveasfilename(initialfile=os.path.basename(default_path), defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"CSV saved: {path}")


if __name__ == "__main__":
    main()



    def open_output_dir(self):
        if platform.system() == "Windows":
            os.startfile(self.output_dir)
        elif platform.system() == "Darwin":
            os.system(f"open {self.output_dir}")
        else:
            os.system(f"xdg-open {self.output_dir}")
