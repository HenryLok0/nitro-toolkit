#!/usr/bin/env python3
"""
Discord Gift Link Checker
Check Discord gift card link validity
"""

import requests
import time
import re
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import random

class DiscordGiftChecker:
    def __init__(self, delay: float = 1.0, timeout: int = 10, max_workers: int = 5, use_proxy: bool = False, proxy_file: str = "data/proxies.txt"):
        """
        Initialize Discord gift card checker
        
        Args:
            delay: Delay between requests (seconds)
            timeout: Request timeout (seconds)
            max_workers: Maximum concurrent workers
            use_proxy: Whether to use proxies
            proxy_file: Path to proxy list file
        """
        self.delay = delay
        self.timeout = timeout
        self.max_workers = max_workers
        self.use_proxy = use_proxy
        self.proxy_file = proxy_file
        self.session = requests.Session()
        self.results = {'valid': [], 'invalid': [], 'ratelimited': [], 'error': [], 'unknown': []}
        # 你可以根據需要初始化 proxy pool 等
    def extract_gift_codes(self, text: str) -> list:
        """Extract Discord gift codes from text"""
        import re
        pattern = r'discord\.gift/([A-Za-z0-9]+)'
        matches = re.findall(pattern, text)
        return matches

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

    # ...existing code...
    
    def check_gift_code(self, code: str) -> Tuple[str, str]:
        """
        Check single gift card code
        
        Args:
            code: Gift card code
            
        Returns:
            (code, status) tuple
        """
        url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"
        proxy = self._get_random_proxy()
        try:
            response = self.session.get(url, timeout=self.timeout, proxies=proxy)
            if response.status_code == 200:
                data = response.json()
                # If gift information is returned, it means it's valid
                if 'uses' in data or 'max_uses' in data:
                    return code, 'valid'
                else:
                    return code, 'unknown'
            elif response.status_code == 404:
                return code, 'invalid'
            elif response.status_code == 429:
                return code, 'ratelimited'
            elif response.status_code == 401 or response.status_code == 403:
                return code, 'unauthorized'
            else:
                return code, f'error_{response.status_code}'
        except requests.exceptions.Timeout:
            return code, 'timeout'
        except requests.exceptions.RequestException as e:
            return code, f'error_{str(e)}'
        except Exception as e:
            return code, f'unknown_error_{str(e)}'
    
    def check_codes_batch(self, codes: List[str], use_threading: bool = True) -> Dict:
        """
        Batch check gift card codes
        
        Args:
            codes: List of gift card codes
            use_threading: Whether to use multi-threading
            
        Returns:
            Check result dictionary
        """
        print(f"Starting to check {len(codes)} gift card codes...")
        
        if use_threading and len(codes) > 1:
            return self._check_codes_threaded(codes)
        else:
            return self._check_codes_sequential(codes)
    
    def _check_codes_sequential(self, codes: List[str]) -> Dict:
        """Sequential code checking"""
        for i, code in enumerate(codes, 1):
            print(f"Check progress: {i}/{len(codes)} - {code}")
            
            code, status = self.check_gift_code(code)
            self._categorize_result(code, status)
            
            # Add delay to avoid rate limiting
            if i < len(codes):
                time.sleep(self.delay)
        
        return self.results
    
    def _check_codes_threaded(self, codes: List[str]) -> Dict:
        """Multi-threaded code checking"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_code = {
                executor.submit(self.check_gift_code, code): code 
                for code in codes
            }
            
            completed = 0
            for future in as_completed(future_to_code):
                completed += 1
                code, status = future.result()
                self._categorize_result(code, status)
                
                print(f"Check progress: {completed}/{len(codes)} - {code} -> {status}")
                
                # Add small delay in multi-threaded environment
                time.sleep(self.delay / self.max_workers)
        
        return self.results
    
    def _categorize_result(self, code: str, status: str):
        """Categorize results into corresponding categories"""
        if status == 'valid':
            self.results['valid'].append(code)
        elif status == 'invalid':
            self.results['invalid'].append(code)
        elif status == 'ratelimited':
            self.results['ratelimited'].append(code)
        elif status.startswith('error_'):
            self.results['error'].append(code)
        else:
            self.results['unknown'].append(code)

    def save_results(self, filename: str = None):
        """Save results to result folder"""
        # Ensure result folder exists
        os.makedirs('./result', exist_ok=True)

        # 決定儲存檔名
        save_filename = filename
        if save_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_filename = f"./result/discord_gift_check_results_{timestamp}.json"
        else:
            # If user specified filename, ensure it's in result folder
            if not save_filename.startswith('./result/'):
                save_filename = f"./result/{save_filename}"

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

        with open(save_filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {save_filename}")

def main():
    # ...existing code...
    parser = argparse.ArgumentParser(
        description='Discord Gift Link Checker',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\nAll options:\n\n'
        --gen-proxies           Download fresh proxies to data/proxies.txt and exit\n'
        --input, -i             Input file path (containing gift card links)\n'
        --delay, -d             Request delay (seconds, default: 1.0)\n'
        --timeout, -t           Request timeout (seconds, default: 10)\n'
        --workers, -w           Max concurrent workers (default: 5)\n'
        --no-threading          Disable multi-threading\n'
        --output, -o            Output filename\n'
        --use-proxy             Enable proxy mode (load proxies from data/proxies.txt)\n'
        --proxy-file            Proxy list file path (default: data/proxies.txt)\n'
        '''
    )
    parser.add_argument('--gen-proxies', action='store_true', help='Download fresh proxies to data/proxies.txt and exit')
    parser.add_argument('--input', '-i', help='Input file path (containing gift card links)')
    parser.add_argument('--delay', '-d', type=float, default=1.0, help='Request delay (seconds, default: 1.0)')
    parser.add_argument('--timeout', '-t', type=int, default=10, help='Request timeout (seconds, default: 10)')
    parser.add_argument('--workers', '-w', type=int, default=5, help='Max concurrent workers (default: 5)')
    parser.add_argument('--no-threading', action='store_true', help='Disable multi-threading')
    parser.add_argument('--output', '-o', help='Output filename')
    parser.add_argument('--use-proxy', action='store_true', help='Enable proxy mode (load proxies from data/proxies.txt)')
    parser.add_argument('--proxy-file', type=str, default='data/proxies.txt', help='Proxy list file path (default: data/proxies.txt)')

    args = parser.parse_args()

    if args.gen_proxies:
        download_and_save_proxies(args.proxy_file)
        return

    # Initialize checker
    checker = DiscordGiftChecker(
        delay=args.delay,
        timeout=args.timeout,
        max_workers=args.workers,
        use_proxy=args.use_proxy,
        proxy_file=args.proxy_file
    )
    
    # Get input text
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found {args.input}")
            sys.exit(1)
    else:
        print("Please enter text containing Discord gift card links (press Ctrl+D or Ctrl+Z to finish):")
        input_text = sys.stdin.read()
    
    # Extract gift card codes
    codes = checker.extract_gift_codes(input_text)    
    if not codes:
        print("No Discord gift card links found")
        sys.exit(1)    
    print(f"Found {len(codes)} gift card codes")
    
    # Check codes
    use_threading = not args.no_threading
    checker.check_codes_batch(codes, use_threading=use_threading)
    
    # Show results
    checker.print_results()
    
    # Save results
    checker.save_results(args.output)

if __name__ == "__main__":
    main()
