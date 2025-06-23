import tkinter as tk
from tkinter import messagebox
import socket
import whois
import requests

# Whois Lookup
def do_whois():
    domain = entry.get()
    try:
        w = whois.whois(domain)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, str(w))
    except Exception as e:
        messagebox.showerror("Error", f"Whois lookup failed: {e}")

# DNS Lookup
def do_dns():
    domain = entry.get()
    try:
        ip = socket.gethostbyname(domain)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"IP Address: {ip}")
    except Exception as e:
        messagebox.showerror("Error", f"DNS lookup failed: {e}")

# Subdomain Enumeration
def do_subdomains():
    domain = entry.get()
    subdomains = ['www', 'mail', 'ftp', 'dev', 'test', 'api']
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Subdomain Scan for {domain}:\n\n")
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            output_box.insert(tk.END, f"[+] {subdomain} -> {ip}\n")
        except socket.gaierror:
            output_box.insert(tk.END, f"[-] {subdomain} -> Not found\n")

# IP Geolocation
def do_geolocation():
    domain = entry.get()
    try:
        response = requests.get(f"http://ip-api.com/json/{domain}").json()
        if response['status'] == 'success':
            output = (
                f"Country: {response['country']}\n"
                f"City: {response['city']}\n"
                f"ISP: {response['isp']}\n"
                f"Lat/Lon: {response['lat']}, {response['lon']}"
            )
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, output)
        else:
            output_box.insert(tk.END, "Could not find location info.")
    except Exception as e:
        messagebox.showerror("Error", f"Geolocation failed: {e}")

# HTTP Header Analysis
def do_headers():
    domain = entry.get()
    if not domain.startswith("http"):
        domain = "http://" + domain
    try:
        response = requests.head(domain, timeout=5)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Headers for {domain}:\n\n")
        for key, value in response.headers.items():
            output_box.insert(tk.END, f"{key}: {value}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Header fetch failed: {e}")

def do_port_scan():
    target = entry.get()
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443]
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Port scanning {target}...\n\n")
    try:
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)  # Short timeout
            result = sock.connect_ex((target, port))
            if result == 0:
                output_box.insert(tk.END, f"Port {port}: OPEN\n")
            else:
                output_box.insert(tk.END, f"Port {port}: CLOSED\n")
            sock.close()
    except Exception as e:
        messagebox.showerror("Error", f"Port scan failed: {e}")

# GUI
app = tk.Tk()
app.title("Recon Tool")
app.geometry("700x500")
app.configure(bg="black")

# Define fonts and colors
font_style = ("Consolas", 12)
button_font = ("Consolas", 10, "bold")
green = "#00FF00"
dark_gray = "#121212"

# Label with green text
label = tk.Label(app, text="Enter Domain or IP:", fg=green, bg="black", font=font_style)
label.pack(pady=5)

# Entry box with black bg and green text
entry = tk.Entry(app, width=60, fg=green, bg=dark_gray, insertbackground=green, font=font_style)
entry.pack(pady=5)

button_frame = tk.Frame(app, bg="black")
button_frame.pack(pady=5)


# Button styling function
left_frame = tk.Frame(button_frame, bg="black")
left_frame.grid(row=0, column=0, padx=10)

right_frame = tk.Frame(button_frame, bg="black")
right_frame.grid(row=0, column=1, padx=10)

# Left column buttons
tk.Button(left_frame, text="Whois Lookup", command=do_whois, fg=green, bg=dark_gray, activebackground="black",
          activeforeground=green, relief="flat", font=button_font, width=20).pack(pady=3)
tk.Button(left_frame, text="DNS Lookup", command=do_dns, fg=green, bg=dark_gray, activebackground="black",
          activeforeground=green, relief="flat", font=button_font, width=20).pack(pady=3)
tk.Button(left_frame, text="Subdomain Enum", command=do_subdomains, fg=green, bg=dark_gray, activebackground="black",
          activeforeground=green, relief="flat", font=button_font, width=20).pack(pady=3)

# Right column buttons
tk.Button(right_frame, text="IP Geolocation", command=do_geolocation, fg=green, bg=dark_gray, activebackground="black",
          activeforeground=green, relief="flat", font=button_font, width=20).pack(pady=3)
tk.Button(right_frame, text="HTTP Headers", command=do_headers, fg=green, bg=dark_gray, activebackground="black",
          activeforeground=green, relief="flat", font=button_font, width=20).pack(pady=3)
tk.Button(right_frame, text="Port Scan", command=do_port_scan, fg=green, bg=dark_gray, activebackground="black",
          activeforeground=green, relief="flat", font=button_font, width=20).pack(pady=3)

# Output text box with black bg and green text, monospace font
output_box = tk.Text(app, height=20, width=85, bg="black", fg=green, insertbackground=green, font=font_style)
output_box.pack(pady=10)

app.mainloop()