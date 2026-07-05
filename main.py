import os, re, base64, json, requests, time
from typing import List, Dict, Optional

class Colors:
    G = '\033[92m'
    R = '\033[91m'
    B = '\033[94m'
    M = '\033[95m'
    Y = '\033[93m'
    C = '\033[96m'
    RESET = '\033[0m'

class DiscordBotExtractor:
    def __init__(self, filename: str = "tokensbot.txt"):
        self.filename = filename
        self.tokens = []
        self.bots_data = []
        
    def read_tokens_file(self) -> List[str]:
        try:
            if not os.path.exists(self.filename):
                print(f"{Colors.R}File not found!{Colors.RESET}")
                return []
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
            token_pattern = r'[A-Za-z0-9-_]{24,28}\.[A-Za-z0-9-_]{6,7}\.[A-Za-z0-9-_]{27,38}'
            self.tokens = list(set(re.findall(token_pattern, content)))
            print(f"{Colors.G}Found {len(self.tokens)} tokens{Colors.RESET}")
            return self.tokens
        except Exception as e:
            print(f"{Colors.R}Error: {e}{Colors.RESET}")
            return []
    
    def extract_bot_id_from_token(self, token: str) -> Optional[str]:
        try:
            encoded = token.split('.')[0]
            padding = len(encoded) % 4
            if padding: encoded += '=' * (4 - padding)
            decoded = base64.b64decode(encoded).decode('utf-8', errors='ignore')
            match = re.search(r'\d+', decoded)
            return match.group() if match else None
        except:
            return None
    
    def get_bot_info_from_api(self, bot_id: str, token: str) -> Dict:
        try:
            r = requests.get(f'https://discord.com/api/v10/users/{bot_id}', 
                           headers={'Authorization': f'Bot {token}'}, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return {'username': data.get('username', 'Unknown'), 'discriminator': data.get('discriminator', '0000')}
            return {'username': f'bot_{bot_id[:6]}', 'discriminator': '0000'}
        except:
            return {'username': f'bot_{bot_id[:6]}', 'discriminator': '0000'}
    
    def extract_all_bots(self, use_api: bool = True) -> List[Dict]:
        if not self.tokens:
            print(f"{Colors.R}No tokens{Colors.RESET}")
            return []
        print(f"{Colors.Y}Extracting...{Colors.RESET}")
        for i, token in enumerate(self.tokens, 1):
            try:
                bot_id = self.extract_bot_id_from_token(token)
                if bot_id:
                    info = self.get_bot_info_from_api(bot_id, token) if use_api else {'username': f'bot_{bot_id[:6]}', 'discriminator': '0000'}
                    self.bots_data.append({'token': token, 'id': bot_id, 'username': info['username'], 'discriminator': info['discriminator']})
                    print(f"{Colors.G}{i}/{len(self.tokens)} {Colors.C}Token: {token[:30]}... {Colors.B}ID: {bot_id} {Colors.M}Bot: {info['username']}#{info['discriminator']}{Colors.RESET}")
                time.sleep(0.5)
            except Exception as e:
                print(f"{Colors.R}Error: {e}{Colors.RESET}")
        print(f"{Colors.G}Extracted {len(self.bots_data)} bots{Colors.RESET}")
        return self.bots_data
    
    def save_to_file(self, output_file: str = "output.txt"):
        if not self.bots_data:
            print(f"{Colors.R}No data{Colors.RESET}")
            return
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for bot in self.bots_data:
                    f.write(f"{bot['token']}:{bot['id']}:{bot['username']}#{bot['discriminator']}\n")
            print(f"{Colors.Y}Saved to {output_file}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.R}Error: {e}{Colors.RESET}")
    
    def run(self, use_api: bool = True):
        print(f"{Colors.C}TokenBotExtractor{Colors.RESET}")
        if self.read_tokens_file():
            self.extract_all_bots(use_api)
            if self.bots_data:
                self.save_to_file("output.txt")
                print(f"{Colors.G}Done!{Colors.RESET}")

def main():
    DiscordBotExtractor("tokensbot.txt").run(use_api=True)

if __name__ == "__main__":
    main()
