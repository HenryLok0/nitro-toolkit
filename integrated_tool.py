#!/usr/bin/env python3
"""
Discord Nitro Generator + Checker Integrated Tool
Automatically generate Discord Nitro codes and check their validity
"""

from time import localtime, strftime, sleep
from colorama import Fore, init
import requests
import random
import string
import os
import json
from datetime import datetime
from typing import List, Dict, Tuple
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize colorama
init(autoreset=True)

class IntegratedDiscordTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Proxy settings
        self.prox_api = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        self.prox = []
        
        # Results
        self.results = {
            'valid': [],
            'invalid': [],
            'ratelimited': [],
            'error': [],
            'unknown': []
        }
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Print application banner"""
        self.clear_screen()
        print(Fore.CYAN + """
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗██║     ██╗ 
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║   ██║  ██║   
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║   ██║  ╚██╗ ██╔╝ 
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║████████╗   ██║   ╚████╔╝
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═══════╝   ╚═╝    ╚═══╝

        """ + Fore.YELLOW + "Discord Nitro Generator & Checker v2.0")
        print(Fore.WHITE + "=" * 60)
    
    def load_proxies(self):
        """Load proxy list from GitHub"""
        try:
            print(Fore.YELLOW + "Loading proxy list...")
            response = requests.get(self.prox_api, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().split('\n')
                self.prox = [{'http': f'http://{proxy}', 'https': f'http://{proxy}'} 
                           for proxy in proxies if proxy.strip()]
                print(Fore.GREEN + f"Loaded {len(self.prox)} proxies")
                return True
            else:
                print(Fore.RED + "Failed to load proxy list")
                return False
        except Exception as e:
            print(Fore.RED + f"Error loading proxies: {str(e)}")
            return False
    
    def generate_codes(self, amount: int, code_type: str = "boost") -> List[str]:
        """
        Generate Discord Nitro codes
        
        Args:
            amount: Number of codes to generate
            code_type: Type of code ("boost" or "classic")
            
        Returns:
            List of generated codes
        """
        codes = []
        print(Fore.CYAN + f"Generating {amount} {code_type} codes...")
        
        for i in range(amount):
            if code_type.lower() == "boost":
                # Discord Nitro Boost format (16 characters)
                code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            else:
                # Discord Nitro Classic format (16 characters)  
                code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            
            codes.append(code)
            
            # Progress display
            if (i + 1) % 50 == 0 or i == amount - 1:
                print(Fore.YELLOW + f"Generated: {i + 1}/{amount}")
        
        print(Fore.GREEN + f"Successfully generated {len(codes)} codes")
        return codes
    
    def check_gift_code(self, code: str, use_proxy: bool = False) -> Tuple[str, str]:
        """
        Check single gift code validity
        
        Args:
            code: Gift code to check
            use_proxy: Whether to use proxy
            
        Returns:
            (code, status) tuple
        """
        url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"
        
        try:
            # Select random proxy if enabled
            proxy = None
            if use_proxy and self.prox:
                proxy = random.choice(self.prox)
            
            response = self.session.get(url, timeout=10, proxies=proxy)
            
            if response.status_code == 200:
                data = response.json()
                if 'uses' in data or 'max_uses' in data:
                    return code, 'valid'
                else:
                    return code, 'unknown'
            elif response.status_code == 404:
                return code, 'invalid'
            elif response.status_code == 429:
                return code, 'ratelimited'
            elif response.status_code in [401, 403]:
                return code, 'unauthorized'
            else:
                return code, f'error_{response.status_code}'
                
        except requests.exceptions.Timeout:
            return code, 'timeout'
        except requests.exceptions.RequestException as e:
            return code, f'error_{str(e)}'
        except Exception as e:
            return code, f'unknown_error_{str(e)}'
    
    def check_codes_batch(self, codes: List[str], use_proxy: bool = False, 
                         speed_mode: str = "balanced", max_workers: int = 5) -> Dict:
        """
        Batch check gift codes
        
        Args:
            codes: List of codes to check
            use_proxy: Whether to use proxy
            speed_mode: Speed mode ("fast", "balanced", "safe")
            max_workers: Maximum concurrent workers
            
        Returns:
            Check results dictionary
        """
        print(Fore.CYAN + f"Starting batch check of {len(codes)} codes...")
        print(Fore.YELLOW + f"Speed mode: {speed_mode}")
        
        # Configure delays based on speed mode
        if speed_mode == "fast":
            base_delay = 0.1
            max_workers = min(max_workers, 10)
        elif speed_mode == "safe":
            base_delay = 3.0
            max_workers = min(max_workers, 2)
        else:  # balanced
            base_delay = 1.0
            max_workers = min(max_workers, 5)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_code = {
                executor.submit(self.check_gift_code, code, use_proxy): code 
                for code in codes
            }
            
            completed = 0
            for future in as_completed(future_to_code):
                completed += 1
                code, status = future.result()
                self._categorize_result(code, status)
                
                # Status display with colors
                if status == 'valid':
                    print(Fore.GREEN + f"[{completed}/{len(codes)}] {code} -> VALID!")
                elif status == 'invalid':
                    print(Fore.RED + f"[{completed}/{len(codes)}] {code} -> Invalid")
                elif status == 'ratelimited':
                    print(Fore.YELLOW + f"[{completed}/{len(codes)}] {code} -> Rate Limited")
                else:
                    print(Fore.CYAN + f"[{completed}/{len(codes)}] {code} -> {status}")
                
                # Dynamic delay adjustment
                if status == 'ratelimited':
                    sleep(base_delay * 2)  # Longer delay for rate limited
                elif status.startswith('error'):
                    sleep(base_delay * 1.5)  # Medium delay for errors
                else:
                    sleep(base_delay)  # Normal delay
        
        return self.results
    
    def _categorize_result(self, code: str, status: str):
        """Categorize result into appropriate category"""
        if status == 'valid':
            self.results['valid'].append(code)
        elif status == 'invalid':
            self.results['invalid'].append(code)
        elif status == 'ratelimited':
            self.results['ratelimited'].append(code)
        elif status.startswith('error') or status == 'timeout' or status == 'unauthorized':
            self.results['error'].append({'code': code, 'status': status})
        else:
            self.results['unknown'].append({'code': code, 'status': status})
    
    def recheck_ratelimited_codes(self, use_proxy: bool = False) -> Dict:
        """
        Recheck rate limited codes with longer delays
        
        Args:
            use_proxy: Whether to use proxy
            
        Returns:
            Updated results dictionary
        """
        if not self.results['ratelimited']:
            print(Fore.YELLOW + "No rate limited codes to recheck")
            return self.results
        
        print(Fore.CYAN + f"Rechecking {len(self.results['ratelimited'])} rate limited codes...")
        
        # Move rate limited codes to temporary list
        codes_to_recheck = self.results['ratelimited'].copy()
        self.results['ratelimited'].clear()
        
        # Recheck with longer delays
        for i, code in enumerate(codes_to_recheck, 1):
            print(Fore.YELLOW + f"Rechecking [{i}/{len(codes_to_recheck)}]: {code}")
            
            code, status = self.check_gift_code(code, use_proxy)
            self._categorize_result(code, status)
            
            # Status display
            if status == 'valid':
                print(Fore.GREEN + f"  -> VALID!")
            elif status == 'invalid':
                print(Fore.RED + f"  -> Invalid")
            elif status == 'ratelimited':
                print(Fore.YELLOW + f"  -> Still Rate Limited")
            else:
                print(Fore.CYAN + f"  -> {status}")
            
            # Longer delay between rechecks
            if i < len(codes_to_recheck):
                sleep(5.0)
        
        return self.results
    
    def print_results(self):
        """Print detailed results"""
        print("" + Fore.WHITE + "=" * 60)
        print(Fore.CYAN + "CHECK RESULTS SUMMARY")
        print(Fore.WHITE + "=" * 60)
        
        print(Fore.GREEN + f"Valid: {len(self.results['valid'])}")
        print(Fore.RED + f"Invalid: {len(self.results['invalid'])}")
        print(Fore.YELLOW + f"Rate Limited: {len(self.results['ratelimited'])}")
        print(Fore.CYAN + f"Errors: {len(self.results['error'])}")
        print(Fore.MAGENTA + f"Unknown: {len(self.results['unknown'])}")
        
        # Show valid codes prominently
        if self.results['valid']:
            print("" + Fore.GREEN + "VALID GIFT CODES:")
            for code in self.results['valid']:
                print(Fore.GREEN + f"  https://discord.gift/{code}")
        
        # Show rate limited codes
        if self.results['ratelimited']:
            print("" + Fore.YELLOW + "RATE LIMITED CODES (retry recommended):")
            for code in self.results['ratelimited']:
                print(Fore.YELLOW + f"  https://discord.gift/{code}")
    
    def save_results(self, filename: str = None):
        """Save results to JSON file in result folder"""
        # Ensure result folder exists
        os.makedirs('./result', exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"./result/discord_integrated_results_{timestamp}.json"
        else:
            if not filename.startswith('./result/'):
                filename = f"./result/{filename}"
        
        # Prepare data to save
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_checked': sum(len(v) if isinstance(v, list) else len(v) for v in self.results.values()),
                'valid': len(self.results['valid']),
                'invalid': len(self.results['invalid']),
                'ratelimited': len(self.results['ratelimited']),
                'error': len(self.results['error']),
                'unknown': len(self.results['unknown'])
            },
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(Fore.GREEN + f"Results saved to: {filename}")
    
    def main_menu(self):
        """Main application menu"""
        while True:
            self.print_banner()
            
            print(Fore.WHITE + "Select Discord Nitro code type:")
            print(Fore.CYAN + "1. Discord Nitro Boost")
            print(Fore.CYAN + "2. Discord Nitro Classic")
            print(Fore.RED + "3. Exit")
            
            choice = input(Fore.WHITE + "Enter choice (1-3): ").strip()
            
            if choice == '1':
                code_type = "boost"
                break
            elif choice == '2':
                code_type = "classic"
                break
            elif choice == '3':
                print(Fore.YELLOW + "Goodbye!")
                sys.exit(0)
            else:
                print(Fore.RED + "Invalid choice. Please select 1, 2, or 3.")
                input(Fore.WHITE + "Press Enter to continue...")
                continue
        
        # Proxy settings
        print(Fore.WHITE + "Proxy Configuration:")
        print(Fore.CYAN + "1. Use proxies (recommended - avoids IP blocking)")
        print(Fore.CYAN + "2. Don't use proxies (faster but higher risk)")
        
        proxy_choice = input(Fore.WHITE + "Enter choice (1-2): ").strip()
        use_proxy = proxy_choice == '1'
        
        if use_proxy:
            if not self.load_proxies():
                print(Fore.RED + "Failed to load proxies. Continuing without proxies.")
                use_proxy = False
        
        # Speed mode selection
        print(Fore.WHITE + "Speed mode:")
        print(Fore.GREEN + "1. Fast (0.1s delay, higher rate limit risk)")
        print(Fore.YELLOW + "2. Balanced (1s delay, recommended)")
        print(Fore.RED + "3. Safe (3s delay, lowest rate limit risk)")
        
        speed_choice = input(Fore.WHITE + "Enter choice (1-3): ").strip()
        speed_modes = {'1': 'fast', '2': 'balanced', '3': 'safe'}
        speed_mode = speed_modes.get(speed_choice, 'balanced')
        
        # Number of codes to generate
        while True:
            try:
                amount = int(input(Fore.WHITE + "Enter number of codes to generate: "))
                if amount > 0:
                    break
                else:
                    print(Fore.RED + "Please enter a positive number.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")
        
        # Generate codes
        codes = self.generate_codes(amount, code_type)
        
        # Ask if user wants to check codes
        print(Fore.WHITE + "Do you want to check the generated codes?")
        print(Fore.CYAN + "1. Yes, check all codes")
        print(Fore.CYAN + "2. No, just save codes to file")
        
        check_choice = input(Fore.WHITE + "Enter choice (1-2): ").strip()
        
        if check_choice == '1':
            # Check codes
            self.check_codes_batch(codes, use_proxy, speed_mode)
            
            # Show results
            self.print_results()
            
            # Ask about rechecking rate limited codes
            if self.results['ratelimited']:
                print(Fore.WHITE + f"Found {len(self.results['ratelimited'])} rate limited codes.")
                recheck = input(Fore.YELLOW + "Do you want to recheck them? (y/n): ").strip().lower()
                if recheck == 'y':
                    self.recheck_ratelimited_codes(use_proxy)
                    self.print_results()
            
            # Save results
            self.save_results()
        else:
            # Just save generated codes
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs('./result', exist_ok=True)
            filename = f"./result/discord_codes_{code_type}_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                for code in codes:
                    f.write(f"https://discord.gift/{code}")
            
            print(Fore.GREEN + f"Codes saved to: {filename}")
        
        input(Fore.WHITE + "Press Enter to exit...")

def main():
    """Main function"""
    tool = IntegratedDiscordTool()
    try:
        tool.main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "Operation cancelled by user.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
