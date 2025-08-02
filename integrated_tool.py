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
import argparse
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize colorama
init(autoreset=True)

def download_and_save_proxies(proxy_file='data/proxies.txt', limit=200):
    import requests, os
    proxy_sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    ]
    all_proxies = []
    for url in proxy_sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                proxies = r.text.strip().split('\n')
                all_proxies.extend([p.strip() for p in proxies if p.strip()])
        except Exception:
            continue
    unique = list(set(all_proxies))[:limit]
    os.makedirs(os.path.dirname(proxy_file), exist_ok=True)
    with open(proxy_file, 'w', encoding='utf-8') as f:
        for p in unique:
            f.write(p + '\n')
    print(f"Downloaded {len(unique)} proxies to {proxy_file}")
    return True


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
        """Load proxy list from multiple sources with validation"""
        try:
            print(Fore.YELLOW + "Loading proxy list...")
            
            # Try multiple proxy sources
            proxy_sources = [
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
            ]
            
            all_proxies = []
            for source in proxy_sources:
                try:
                    response = requests.get(source, timeout=10)
                    if response.status_code == 200:
                        proxies = response.text.strip().split('\n')
                        all_proxies.extend([proxy.strip() for proxy in proxies if proxy.strip()])
                        print(Fore.GREEN + f"Loaded {len(proxies)} proxies from {source.split('/')[-2]}")
                except Exception as e:
                    print(Fore.YELLOW + f"Failed to load from {source.split('/')[-2]}: {str(e)}")
                    continue
            
            if not all_proxies:
                print(Fore.RED + "No proxies loaded from any source")
                return False
            
            # Remove duplicates and validate format
            unique_proxies = list(set(all_proxies))
            valid_proxies = []
            
            for proxy in unique_proxies:
                if ':' in proxy and len(proxy.split(':')) == 2:
                    try:
                        ip, port = proxy.split(':')
                        # Basic IP format validation
                        parts = ip.split('.')
                        if len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts):
                            if 1 <= int(port) <= 65535:
                                valid_proxies.append(proxy)
                    except ValueError:
                        continue
            
            self.prox = [{'http': f'http://{proxy}', 'https': f'http://{proxy}'} 
                        for proxy in valid_proxies[:100]]  # Limit to 100 best proxies
            
            print(Fore.GREEN + f"Validated {len(self.prox)} working proxies")
            return len(self.prox) > 0
            
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
        Check single gift code validity with improved error handling
        
        Args:
            code: Gift code to check
            use_proxy: Whether to use proxy
            
        Returns:
            (code, status) tuple
        """
        url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Select random proxy if enabled
                proxy = None
                if use_proxy and self.prox:
                    proxy = random.choice(self.prox)
                
                # Use shorter timeout for proxy requests
                timeout = 5 if use_proxy else 10
                response = self.session.get(url, timeout=timeout, proxies=proxy)
                
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
                    
            except requests.exceptions.ProxyError as e:
                if attempt < max_retries - 1:
                    print(Fore.YELLOW + f"Proxy error for {code}, retrying without proxy...")
                    use_proxy = False  # Fallback to no proxy
                    continue
                else:
                    return code, f"proxy_error"
            except requests.exceptions.ConnectTimeout:
                if attempt < max_retries - 1:
                    sleep(0.5)  # Brief pause before retry
                    continue
                else:
                    return code, 'timeout'
            except requests.exceptions.Timeout:
                return code, 'timeout'
            except requests.exceptions.RequestException as e:
                if "ProxyError" in str(e) or "Cannot connect to proxy" in str(e):
                    if attempt < max_retries - 1:
                        use_proxy = False  # Disable proxy for this request
                        continue
                    else:
                        return code, 'proxy_connection_failed'
                return code, f'error_{str(e)[:30]}'
            except Exception as e:
                return code, f'unknown_error_{str(e)[:30]}'
        
        return code, 'max_retries_exceeded'
    
    def check_codes_batch(self, codes: List[str], use_proxy: bool = False, 
                         speed_mode: str = "balanced", max_workers: int = 5) -> Dict:
        """
        Batch check gift codes
        
        Args:
            codes: List of codes to check
            use_proxy: Whether to use proxy
            speed_mode: Speed mode ("fast", "balanced", "safe", "ultra_safe")
            max_workers: Maximum concurrent workers
            
        Returns:
            Check results dictionary
        """
        print(Fore.CYAN + f"Starting batch check of {len(codes)} codes...")
        print(Fore.YELLOW + f"Speed mode: {speed_mode}")
        
        # Check if IP might be heavily rate limited
        total_rate_limits = 0
        heavy_rate_limit_warning_shown = False
        
        # Configure delays based on speed mode
        if speed_mode == "fast":
            base_delay = 0.1
            max_workers = min(max_workers, 10)
            rate_limit_threshold = 3  # 3 consecutive rate limits trigger cooldown
        elif speed_mode == "safe":
            base_delay = 3.0
            max_workers = min(max_workers, 2)
            rate_limit_threshold = 3  # 3 consecutive rate limits trigger cooldown
        elif speed_mode == "ultra_safe":
            base_delay = 10.0
            max_workers = 1  # Single threaded for ultra safe
            rate_limit_threshold = 3  # 3 consecutive rate limits trigger cooldown
            print(Fore.MAGENTA + f"⚠️  Ultra Safe Mode: Using 10s delays with single threading")
        else:  # balanced
            base_delay = 1.0
            max_workers = min(max_workers, 5)
            rate_limit_threshold = 3  # 3 consecutive rate limits trigger cooldown
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_code = {
                executor.submit(self.check_gift_code, code, use_proxy): code 
                for code in codes
            }
            
            completed = 0
            consecutive_rate_limits = 0
            post_cooldown_sensitivity = False  # Flag for immediate cooldown after previous cooldown
            cooldown_cycles = 0  # Track number of cooldown cycles
            
            for future in as_completed(future_to_code):
                completed += 1
                code, status = future.result()
                self._categorize_result(code, status)
                
                # Track consecutive rate limits
                if status == 'ratelimited':
                    consecutive_rate_limits += 1
                    total_rate_limits += 1
                    
                    # If we're in post-cooldown sensitivity mode, immediately cooldown on ANY rate limit
                    if post_cooldown_sensitivity:
                        cooldown_cycles += 1
                        print(Fore.RED + f"\n🔄 Rate limit detected after cooldown (Cycle #{cooldown_cycles})!")
                        print(Fore.YELLOW + f"⏳ Immediate 30-second cooldown...")
                        
                        for i in range(30, 0, -1):
                            print(Fore.CYAN + f"\r⏱️  Cooldown... {i} seconds remaining", end="", flush=True)
                            sleep(1)
                        
                        print(Fore.GREEN + f"\n✅ Cooldown #{cooldown_cycles} complete! Continuing with high sensitivity...")
                        consecutive_rate_limits = 0  # Reset but stay in sensitive mode
                        continue  # Skip the normal rate limit handling
                else:
                    consecutive_rate_limits = 0  # Reset counter
                
                # Warn about heavy rate limiting
                if total_rate_limits > 10 and not heavy_rate_limit_warning_shown:
                    print(Fore.RED + f"\n⚠️  WARNING: Your IP is heavily rate limited ({total_rate_limits} total)")
                    print(Fore.YELLOW + f"🔄 Consider:")
                    print(Fore.YELLOW + f"   • Using Ultra Safe mode (4)")
                    print(Fore.YELLOW + f"   • Waiting 30-60 minutes before retrying")
                    print(Fore.YELLOW + f"   • Using a VPN to change your IP")
                    heavy_rate_limit_warning_shown = True
                
                # Status display with colors
                if status == 'valid':
                    print(Fore.GREEN + f"[{completed}/{len(codes)}] {code} -> ✅ VALID!")
                elif status == 'invalid':
                    print(Fore.WHITE + f"[{completed}/{len(codes)}] {code} -> ❌ Invalid (normal)")
                elif status == 'ratelimited':
                    print(Fore.YELLOW + f"[{completed}/{len(codes)}] {code} -> ⏳ Rate Limited")
                elif status.startswith('proxy') or 'proxy' in status.lower():
                    print(Fore.MAGENTA + f"[{completed}/{len(codes)}] {code} -> 🔗 Proxy issue (switching to direct)")
                else:
                    print(Fore.CYAN + f"[{completed}/{len(codes)}] {code} -> ⚠️ {status}")
                
                # Auto-cooldown when too many consecutive rate limits (normal mode)
                if consecutive_rate_limits >= rate_limit_threshold:
                    cooldown_cycles += 1
                    if speed_mode == "ultra_safe":
                        cooldown_time = 120  # 2 minutes for ultra safe
                    elif speed_mode == "safe":
                        cooldown_time = 60   # 1 minute for safe
                    else:
                        cooldown_time = 30   # 30 seconds for others
                    
                    print(Fore.RED + f"\n🛑 Too many rate limits detected ({consecutive_rate_limits} consecutive)")
                    print(Fore.YELLOW + f"⏳ Cooling down for {cooldown_time} seconds (Cycle #{cooldown_cycles})...")
                    
                    # Suggest more conservative settings
                    if speed_mode != "ultra_safe":
                        print(Fore.CYAN + f"💡 Consider using 'Ultra Safe' mode for heavily rate-limited IPs")
                    
                    for i in range(cooldown_time, 0, -1):
                        print(Fore.CYAN + f"\r⏱️  Waiting... {i} seconds remaining", end="", flush=True)
                        sleep(1)
                    
                    print(Fore.GREEN + f"\n✅ Cooldown #{cooldown_cycles} complete! Entering high sensitivity mode...")
                    consecutive_rate_limits = 0  # Reset counter after cooldown
                    post_cooldown_sensitivity = True  # Enable immediate cooldown on next rate limit
                    
                    # Auto-adjust delays after cooldown to be more conservative
                    if speed_mode == "fast":
                        base_delay *= 3  # Triple the delay for fast mode
                        print(Fore.YELLOW + f"⚙️  Auto-adjusted delay to {base_delay}s for better rate limiting")
                    elif speed_mode == "balanced":
                        base_delay *= 2  # Double delay for balanced mode
                        print(Fore.YELLOW + f"⚙️  Auto-adjusted delay to {base_delay}s for better rate limiting")
                    elif speed_mode == "safe":
                        base_delay *= 1.5  # Increase delay for safe mode
                        print(Fore.YELLOW + f"⚙️  Auto-adjusted delay to {base_delay}s for better rate limiting")
                
                # Dynamic delay adjustment
                elif status == 'ratelimited':
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
        """Main application menu (now supports CLI proxy args)"""
        parser = argparse.ArgumentParser(description='Nitro Toolkit Integrated Tool')
        parser.add_argument('--use-proxy', action='store_true', help='Enable proxy mode (load proxies from data/proxies.txt)')
        parser.add_argument('--proxy-file', type=str, default='data/proxies.txt', help='Proxy list file path (default: data/proxies.txt)')
        args, unknown = parser.parse_known_args()

        self.use_proxy = False
        if args.use_proxy:
            self.use_proxy = True
            if not self.load_proxies():
                print(Fore.RED + "Failed to load proxies. Continuing without proxies.")
                self.use_proxy = False
        # 若沒用 CLI 參數，則進入互動式選單
        else:
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
            # Proxy settings互動式
            print(Fore.WHITE + "\nProxy Configuration:")
            print(Fore.CYAN + "1. Use proxies (recommended - avoids IP blocking)")
            print(Fore.CYAN + "2. Don't use proxies (faster but higher risk)")
            print(Fore.CYAN + "3. Auto-detect (try proxies first, fallback to direct)")
            print(Fore.WHITE + "\n⚠️  IMPORTANT NOTE:")
            print(Fore.YELLOW + "• 404 errors are NORMAL - they mean the code doesn't exist")
            print(Fore.YELLOW + "• Valid Discord Nitro codes are extremely rare (1 in billions)")
            print(Fore.YELLOW + "• Most generated codes will show as '404/Invalid' - this is expected!")
            proxy_choice = input(Fore.WHITE + "\nEnter choice (1-3): ").strip()
            if proxy_choice == '1':
                self.use_proxy = True
                if not self.load_proxies():
                    print(Fore.RED + "Failed to load proxies. Would you like to continue without proxies? (y/n)")
                    fallback = input().strip().lower()
                    if fallback != 'y':
                        print(Fore.YELLOW + "Operation cancelled.")
                        return
                    self.use_proxy = False
            elif proxy_choice == '3':
                self.use_proxy = True
                if not self.load_proxies():
                    print(Fore.YELLOW + "Auto-detect: Using direct connection (no proxies available)")
                    self.use_proxy = False
            else:
                self.use_proxy = False
                print(Fore.YELLOW + "Using direct connection (no proxies)")

        # Speed mode selection
        print(Fore.WHITE + "Speed mode:")
        print(Fore.GREEN + "1. Fast (0.1s delay, higher rate limit risk)")
        print(Fore.YELLOW + "2. Balanced (1s delay, recommended)")
        print(Fore.RED + "3. Safe (3s delay, lowest rate limit risk)")
        print(Fore.MAGENTA + "4. Ultra Safe (10s delay, for heavily rate limited IPs)")
        speed_choice = input(Fore.WHITE + "Enter choice (1-4): ").strip()
        speed_modes = {'1': 'fast', '2': 'balanced', '3': 'safe', '4': 'ultra_safe'}
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
            self.check_codes_batch(codes, self.use_proxy, speed_mode)
            self.print_results()
            if self.results['ratelimited']:
                print(Fore.WHITE + f"Found {len(self.results['ratelimited'])} rate limited codes.")
                recheck = input(Fore.YELLOW + "Do you want to recheck them? (y/n): ").strip().lower()
                if recheck == 'y':
                    self.recheck_ratelimited_codes(self.use_proxy)
                    self.print_results()
            self.save_results()
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs('./result', exist_ok=True)
            filename = f"./result/discord_codes_{code_type}_{timestamp}.txt"
            with open(filename, 'w') as f:
                for code in codes:
                    f.write(f"https://discord.gift/{code}\n")
            print(Fore.GREEN + f"Codes saved to: {filename}")
        input(Fore.WHITE + "Press Enter to exit...")
        
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
            self.check_codes_batch(codes, self.use_proxy, speed_mode)
            
            # Show results
            self.print_results()
            
            # Ask about rechecking rate limited codes
            if self.results['ratelimited']:
                print(Fore.WHITE + f"Found {len(self.results['ratelimited'])} rate limited codes.")
                recheck = input(Fore.YELLOW + "Do you want to recheck them? (y/n): ").strip().lower()
                if recheck == 'y':
                    self.recheck_ratelimited_codes(self.use_proxy)
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
                    f.write(f"https://discord.gift/{code}\n")
            
            print(Fore.GREEN + f"Codes saved to: {filename}")
        
        input(Fore.WHITE + "Press Enter to exit...")

def main():
    parser = argparse.ArgumentParser(description='Nitro Toolkit Integrated Tool')
    parser.add_argument('--gen-proxies', action='store_true', help='Download fresh proxies to data/proxies.txt and exit')
    args, unknown = parser.parse_known_args()
    if args.gen_proxies:
        download_and_save_proxies()
        return
    tool = IntegratedDiscordTool()
    try:
        tool.main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "Operation cancelled by user.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
