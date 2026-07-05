import os
import re
import base64
import json
import requests
from typing import List, Dict, Optional
import time

class DiscordBotExtractor:
    def __init__(self, filename: str = "tokensbot.txt"):
        self.filename = filename
        self.tokens = []
        self.bots_data = []
        
    def read_tokens_file(self) -> List[str]:
        try:
            if not os.path.exists(self.filename):
                print(f"File {self.filename} not found!")
                return []
            
            with open(self.filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            token_pattern = r'[A-Za-z0-9-_]{24,28}\.[A-Za-z0-9-_]{6,7}\.[A-Za-z0-9-_]{27,38}'
            tokens = re.findall(token_pattern, content)
            
            self.tokens = list(set([t.strip() for t in tokens if t.strip()]))
            
            print(f"Found {len(self.tokens)} tokens in file")
            return self.tokens
            
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    def extract_bot_id_from_token(self, token: str) -> Optional[str]:
        try:
            token_parts = token.split('.')
            if len(token_parts) >= 1:
                encoded_id = token_parts[0]
                padding = len(encoded_id) % 4
                if padding:
                    encoded_id += '=' * (4 - padding)
                
                decoded = base64.b64decode(encoded_id)
                decoded_str = decoded.decode('utf-8', errors='ignore')
                
                id_match = re.search(r'\d+', decoded_str)
                if id_match:
                    return id_match.group()
        except:
            pass
        return None
    
    def get_bot_info_from_api(self, bot_id: str, token: str) -> Dict:
        try:
            headers = {
                'Authorization': f'Bot {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f'https://discord.com/api/v10/users/{bot_id}',
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': bot_id,
                    'username': data.get('username', 'Unknown'),
                    'discriminator': data.get('discriminator', '0000'),
                    'global_name': data.get('global_name', ''),
                    'avatar': data.get('avatar', ''),
                    'bot': data.get('bot', True)
                }
            else:
                return self.get_bot_info_from_token(bot_id)
                
        except Exception as e:
            return self.get_bot_info_from_token(bot_id)
    
    def get_bot_info_from_token(self, bot_id: str) -> Dict:
        return {
            'id': bot_id,
            'username': f'bot_{bot_id[:6]}',
            'discriminator': '0000',
            'global_name': '',
            'bot': True,
            'status': 'offline (API error)'
        }
    
    def extract_all_bots(self, use_api: bool = True) -> List[Dict]:
        if not self.tokens:
            print("No tokens to extract")
            return []
        
        print("\nExtracting bot information...")
        print("-" * 50)
        
        for i, token in enumerate(self.tokens, 1):
            try:
                bot_id = self.extract_bot_id_from_token(token)
                
                if bot_id:
                    print(f"[{i}/{len(self.tokens)}] Processing bot: {bot_id}")
                    
                    if use_api:
                        bot_info = self.get_bot_info_from_api(bot_id, token)
                    else:
                        bot_info = {'id': bot_id, 'username': f'bot_{bot_id[:6]}'}
                    
                    bot_username = bot_info.get('username', 'Unknown')
                    
                    self.bots_data.append({
                        'token': token,
                        'id': bot_id,
                        'username': bot_username,
                        'full_info': bot_info
                    })
                    
                    print(f"   ID: {bot_id}")
                    print(f"   Username: {bot_username}")
                    print(f"   Token: {token[:30]}...")
                    print("-" * 30)
                    
                else:
                    print(f"[{i}/{len(self.tokens)}] Failed to extract ID from token")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error processing token: {e}")
                continue
        
        print(f"\nExtracted {len(self.bots_data)} bots successfully")
        return self.bots_data
    
    def display_in_console(self):
        if not self.bots_data:
            print("No data to display")
            return
        
        print("\n" + "=" * 70)
        print("Bot Extraction Results:")
        print("=" * 70)
        
        for bot in self.bots_data:
            print(f"{bot['token']} - {bot['id']} - {bot['username']}")
        
        print("=" * 70)
        print(f"Total: {len(self.bots_data)} bots")
        print("=" * 70)
    
    def save_to_file(self, output_file: str = "bots_output.txt"):
        if not self.bots_data:
            print("No data to save")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for bot in self.bots_data:
                    line = f"{bot['token']}:{bot['id']}:{bot['username']}\n"
                    f.write(line)
            
            print(f"Saved results to {output_file}")
            
            print("\nFile content:")
            print("-" * 50)
            with open(output_file, 'r', encoding='utf-8') as f:
                print(f.read())
                
        except Exception as e:
            print(f"Error saving file: {e}")
    
    def save_to_json(self, output_file: str = "bots_data.json"):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'total_bots': len(self.bots_data),
                    'bots': self.bots_data
                }, f, indent=2, ensure_ascii=False)
            print(f"Saved full details to {output_file}")
        except Exception as e:
            print(f"Error saving JSON: {e}")
    
    def run(self, use_api: bool = True):
        print("Starting bot information extraction...")
        print("=" * 50)
        
        tokens = self.read_tokens_file()
        
        if not tokens:
            print("No valid tokens found")
            return
        
        bots = self.extract_all_bots(use_api)
        
        if bots:
            self.display_in_console()
            self.save_to_file("bots_output.txt")
            self.save_to_json("bots_data.json")
            
            print("\nProcess completed successfully!")
            print(f"Saved files: bots_output.txt, bots_data.json")
        else:
            print("No bots extracted")

def main():
    extractor = DiscordBotExtractor("tokensbot.txt")
    extractor.run(use_api=True)

if __name__ == "__main__":
    main()
