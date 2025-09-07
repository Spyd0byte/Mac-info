import requests
import socket
import time
import sys
from colorama import Fore, Style, init
import threading
import json
import random

# Initialize colorama
init()

class MACLookupTool:
    def __init__(self):
        self.api_key = "at_Xnz7nUZ6gQjL0Qk9z4p5C5I1B3p9A"  # Free tier API key for macaddress.io
        self.running = False
        
    def clear_screen(self):
        """Clear the terminal screen"""
        print("\033[H\033[J", end="")
    
    def animate_text(self, text: str, delay: float = 0.03, color=Fore.CYAN):
        """Animate text printing with a typewriter effect"""
        for char in text:
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def spinning_cursor(self):
        """Display a spinning cursor during operations"""
        while self.running:
            for cursor in ['|', '/', '-', '\\']:
                if not self.running:
                    break
                sys.stdout.write(Fore.YELLOW + '\r' + cursor + ' Processing ')
                sys.stdout.flush()
                time.sleep(0.1)
    
    def print_banner(self):
        """Print the animated banner"""
        banner_lines = [
            " ███╗░░░███╗░█████╗░░█████╗░  ██╗███╗░░██╗███████╗░█████╗░",
            " ████╗░████║██╔══██╗██╔══██╗  ██║████╗░██║██╔════╝██╔══██╗",
            " ██╔████╔██║███████║██║░░╚═╝  ██║██╔██╗██║█████╗░░██║░░██║",
            " ██║╚██╔╝██║██╔══██║██║░░██╗  ██║██║╚████║██╔══╝░░██║░░██║",
            " ██║░╚═╝░██║██║░░██║╚█████╔╝  ██║██║░╚███║██║░░░░░╚█████╔╝",
            " ╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚════╝░  ╚═╝╚═╝░░╚══╝╚═╝░░░░░░╚════╝░"
        ]
        
        credit = "------------ [+] MAC ADDRESS LOOKUP TOOL ----------------"
        
        self.clear_screen()
        print(Fore.CYAN + Style.BRIGHT)
        
        for line in banner_lines:
            self.animate_text(line, 0.01, Fore.CYAN)
        
        print(Fore.LIGHTCYAN_EX + "")
        self.animate_text(credit, 0.02, Fore.LIGHTMAGENTA_EX)
        print("\n")
    
    def check_internet(self):
        """Check internet connection with animation"""
        self.running = True
        spinner_thread = threading.Thread(target=self.spinning_cursor)
        spinner_thread.daemon = True
        spinner_thread.start()
        
        try:
            # Try to connect to a reliable server
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            self.running = False
            time.sleep(0.2)  # Allow spinner to stop
            print(Fore.LIGHTGREEN_EX + "\r# Internet Connection: Active" + " " * 20)
            return True
        except OSError:
            self.running = False
            time.sleep(0.2)  # Allow spinner to stop
            print(Fore.LIGHTRED_EX + "\r!! No Internet Connection !!" + " " * 20)
            return False
    
    def decode_animation(self, text: str, label: str):
        """Display a decoding animation for text"""
        print(Fore.LIGHTYELLOW_EX + f"{label}: ", end="")
        
        # Display random characters before showing the actual text
        chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        decoded = ""
        
        for i in range(len(text)):
            for _ in range(5):
                temp = decoded + ''.join(random.choice(chars) for _ in range(len(text) - i))
                print('\r' + Fore.LIGHTYELLOW_EX + f"{label}: " + temp, end='', flush=True)
                time.sleep(0.03)
            decoded += text[i]
            print('\r' + Fore.LIGHTYELLOW_EX + f"{label}: " + decoded, end='', flush=True)
        
        print()  # New line after decoding
    
    def lookup_mac(self, mac: str):
        """Look up MAC address information using macaddress.io API"""
        # Clean the MAC address input
        mac = mac.strip().replace(':', '').replace('-', '').replace('.', '').upper()
        
        if len(mac) < 6:
            print(Fore.RED + "Invalid MAC address format")
            return False
            
        # Use the first 6 characters (OUI) for the lookup
        mac_oui = mac[:6]
        
        self.running = True
        spinner_thread = threading.Thread(target=self.spinning_cursor)
        spinner_thread.daemon = True
        spinner_thread.start()
        
        try:
            # Use macaddress.io API
            url = f"https://api.macaddress.io/v1?apiKey={self.api_key}&output=json&search={mac_oui}"
            response = requests.get(url, timeout=10)
            self.running = False
            time.sleep(0.2)  # Allow spinner to stop
            
            if response.status_code == 200:
                data = response.json()
                
                # Display results with decode animation
                print(Fore.LIGHTCYAN_EX + "\r" + " " * 50)  # Clear spinner
                print(Fore.LIGHTGREEN_EX + "\nMAC Address Information:")
                print(Fore.LIGHTGREEN_EX + "─" * 40)
                
                if 'vendorDetails' in data:
                    vendor = data['vendorDetails']
                    self.decode_animation(vendor.get('companyName', 'Unknown'), "Company")
                    self.decode_animation(vendor.get('countryCode', 'Unknown'), "Country Code")
                
                if 'blockDetails' in data:
                    block = data['blockDetails']
                    self.decode_animation(block.get('borderLeft', 'Unknown'), "Block Start")
                    self.decode_animation(block.get('borderRight', 'Unknown'), "Block End")
                    self.decode_animation(block.get('blockSize', 'Unknown'), "Block Size")
                
                if 'macAddressDetails' in data:
                    details = data['macAddressDetails']
                    self.decode_animation(details.get('transmissionType', 'Unknown'), "Transmission Type")
                    self.decode_animation(details.get('administrationType', 'Unknown'), "Administration Type")
                
                return True
            else:
                print(Fore.LIGHTRED_EX + f"\rAPI Error! Status Code: {response.status_code}" + " " * 20)
                print(Fore.LIGHTRED_EX + f"Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.running = False
            time.sleep(0.2)  # Allow spinner to stop
            print(Fore.LIGHTRED_EX + f"\rRequest Error: {str(e)}" + " " * 20)
            return False
        except json.JSONDecodeError as e:
            self.running = False
            time.sleep(0.2)  # Allow spinner to stop
            print(Fore.LIGHTRED_EX + f"\rJSON Parse Error: {str(e)}" + " " * 20)
            return False
    
    def run(self):
        """Run the main application"""
        self.print_banner()
        
        # Check internet connection
        if not self.check_internet():
            print(Fore.LIGHTRED_EX + "\nExiting in 10 seconds...")
            for i in range(10, 0, -1):
                print(f"\r{i}...", end="", flush=True)
                time.sleep(1)
            return
        
        # Main loop
        while True:
            print(Fore.LIGHTBLUE_EX + "")
            mac = input("Enter MAC address (or 'quit' to exit): ").strip()
            
            if mac.lower() in ['quit', 'exit', 'q']:
                break
                
            if not mac:
                continue
                
            self.lookup_mac(mac)
            print()  # Add spacing between lookups
        
        print(Fore.LIGHTGREEN_EX + "\nThank you for using MAC Lookup Tool!")
        time.sleep(1)

# Run the application
if __name__ == "__main__":
    try:
        app = MACLookupTool()
        app.run()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nProgram interrupted. Exiting...")
        time.sleep(1)