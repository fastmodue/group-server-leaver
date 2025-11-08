#made by fastmodue :D

import requests
import time
import sys
import random
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.RED}
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║            DISCORD SERVER/GROUP LEAVER                ║
    ║                  AGENT SOLUTION                       ║
    ║                                                       ║
    ╔═══════════════════════════════════════════════════════╗
{Style.RESET_ALL}
    """
    print(banner)

def get_headers(token):
    return {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

def get_user_id(token):
    """Get the current user's ID"""
    headers = get_headers(token)
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code == 200:
        return response.json()['id']
    return None

def get_guilds(token):
    """Fetch all servers (guilds) the user is in"""
    headers = get_headers(token)
    response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print(f"{Fore.RED}[ERROR] Invalid token! Please check your token and try again.")
        sys.exit(1)
    else:
        print(f"{Fore.RED}[ERROR] Failed to fetch servers: {response.status_code}")
        return []

def get_dms(token):
    """Fetch all DM channels/groups"""
    headers = get_headers(token)
    response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
    
    if response.status_code == 200:
        # filter
        all_channels = response.json()
        return [ch for ch in all_channels if ch.get('type') == 3]
    else:
        print(f"{Fore.RED}[ERROR] Failed to fetch DMs: {response.status_code}")
        return []

def leave_guild(token, guild_id):
    """Leave a server and return (success, status_code, error_message, is_owner)"""
    headers = get_headers(token)
    response = requests.delete(
        f'https://discord.com/api/v9/users/@me/guilds/{guild_id}', 
        headers=headers
    )
    
    if response.status_code == 204:
        return (True, 204, None, False)
    else:
        # errors
        try:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
            error_code = error_data.get('code', 0)
            
            # look for errors
            # turn invalid guild into owned server error :D
            if error_code == 10004 or 'Invalid Guild' in error_msg:
                return (False, response.status_code, error_msg, True)
        except:
            error_msg = 'Unknown error'
        
        return (False, response.status_code, error_msg, False)

def leave_group(token, channel_id):
    """Leave a group DM and return (success, status_code, error_message)"""
    headers = get_headers(token)
    response = requests.delete(
        f'https://discord.com/api/v9/channels/{channel_id}', 
        headers=headers
    )
    
    if response.status_code in [200, 204]:
        return (True, response.status_code, None)
    else:
        # error msgs
        try:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
        except:
            error_msg = 'Unknown error'
        
        return (False, response.status_code, error_msg)

def progress_bar(current, total, bar_length=40):
    """Display a progress bar"""
    percent = current / total
    filled = int(bar_length * percent)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f'\r{Fore.GREEN}[Progress] {bar} {current}/{total}', end='', flush=True)

def get_error_description(status_code):
    """Get human-readable description of HTTP status codes"""
    error_codes = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found (Server may be deleted)",
        429: "Rate Limited",
        500: "Discord Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable"
    }
    return error_codes.get(status_code, f"Error {status_code}")

def smart_delay(base_delay=0.5, variance=0.3):
    """Add a random delay to avoid rate limits"""
    delay = base_delay + random.uniform(0, variance)
    time.sleep(delay)

def handle_rate_limit(retry_after=30):
    """Handle rate limiting with countdown"""
    print(f"\n{Fore.YELLOW}[RATE LIMITED] Waiting {retry_after} seconds...")
    for remaining in range(retry_after, 0, -1):
        print(f"\r{Fore.YELLOW}[Resuming in {remaining}s...]", end='', flush=True)
        time.sleep(1)
    print(f"\r{Fore.GREEN}[Resuming operations...]")

def main():
    print_banner()
    
    print(f"{Fore.YELLOW}What would you like to leave?")
    print("[1] Discord Groups (DMs)")
    print("[2] Discord Servers")
    print("[3] Both\n")
    
    choice = input(f"{Fore.CYAN}Enter your choice (1/2/3): ").strip()
    
    if choice not in ['1', '2', '3']:
        print(f"{Fore.RED}[ERROR] Invalid choice!")
        return
    
    token = input(f"\n{Fore.CYAN}Enter your Discord token: ").strip()
    
    if not token:
        print(f"{Fore.RED}[ERROR] Token cannot be empty!")
        return
    
    keep_ids = input(f"\n{Fore.CYAN}[OPTIONAL] Any server/group IDs to KEEP?\n(Format: id1,id2,id3 or press Enter to leave ALL): ").strip()
    keep_list = [id.strip() for id in keep_ids.split(',') if id.strip()] if keep_ids else []
    
    print(f"\n{Fore.YELLOW}[Scanning...]")
    
    user_id = get_user_id(token)
    if not user_id:
        print(f"{Fore.RED}[ERROR] Could not fetch user information!")
        return
    
    
    guilds = []
    groups = []
    
    if choice in ['2', '3']:
        guilds = get_guilds(token)
    if choice in ['1', '3']:
        groups = get_dms(token)
   
    if keep_list:
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════╗")
        print(f"{Fore.CYAN}║        SERVERS/GROUPS TO KEEP:        ║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
        
        found_keeps = []
        not_found = []
        
        for keep_id in keep_list:
            # check in guilds
            guild_match = next((g for g in guilds if g['id'] == keep_id), None)
            if guild_match:
                found_keeps.append(f"🛡️  {guild_match['name']} (Server)")
                continue
            
            # check in groups
            group_match = next((g for g in groups if g['id'] == keep_id), None)
            if group_match:
                group_name = group_match.get('name', 'Unnamed Group')
                found_keeps.append(f"💬 {group_name} (Group)")
                continue
            
            # not found!
            not_found.append(keep_id)
        
        if found_keeps:
            for item in found_keeps:
                print(f"{Fore.GREEN}  {item}")
        
        if not_found:
            print(f"\n{Fore.RED}  ⚠️  Warning: These IDs were not found:")
            for nf_id in not_found:
                print(f"{Fore.RED}     {nf_id}")
        
        print(f"\n{Fore.YELLOW}Total keeping: {len(found_keeps)} | Not found: {len(not_found)}")
        
        confirm = input(f"\n{Fore.CYAN}Proceed with these settings? (y/n): ").strip().lower()
        if confirm != 'y':
            print(f"{Fore.RED}[Cancelled by user]")
            return
        print()
    else:
        print(f"\n{Fore.RED}⚠️  WARNING: You will leave ALL servers/groups!")
        confirm = input(f"{Fore.CYAN}Are you sure? (y/n): ").strip().lower()
        if confirm != 'y':
            print(f"{Fore.RED}[Cancelled by user]")
            return
        print()
    
    left_count = 0
    kept_count = 0
    owned_count = 0
    failed_count = 0
    
    # servers
    if choice in ['2', '3']:
        print(f"{Fore.GREEN}[Found {len(guilds)} servers]")
        
        if guilds:
            print(f"\n{Fore.YELLOW}[Leaving servers...]")
            print(f"{Fore.YELLOW}[Using 0.5-0.8s delay between requests]\n")
            
            for i, guild in enumerate(guilds):
                guild_id = guild['id']
                guild_name = guild['name']
                owner_id = guild.get('owner_id')
                
                # check for owner
                if owner_id == user_id:
                    print(f"{Fore.RED}[SKIPPED] Can't leave owned server: {guild_name}")
                    owned_count += 1
                elif guild_id in keep_list:
                    print(f"{Fore.CYAN}[KEPT] {guild_name} (ID: {guild_id})")
                    kept_count += 1
                else:
                    max_retries = 3
                    retry_count = 0
                    
                    while retry_count < max_retries:
                        success, status_code, error_msg, is_owner = leave_guild(token, guild_id)
                        
                        if success:
                            left_count += 1
                            print(f"{Fore.GREEN}[LEFT] {guild_name}")
                            smart_delay(0.5, 0.3)  
                            break
                        elif is_owner:
                            print(f"{Fore.RED}[SKIPPED] Can't leave owned server: {guild_name}")
                            owned_count += 1
                            break
                        elif status_code == 429:
                            # rate limit
                            retry_count += 1
                            if retry_count < max_retries:
                                print(f"{Fore.YELLOW}[RATE LIMITED] {guild_name} - Retry {retry_count}/{max_retries}")
                                handle_rate_limit(30)
                            else:
                                print(f"{Fore.RED}[FAILED] {guild_name} - Too many rate limits")
                                failed_count += 1
                        else:
                            # some other error
                            error_desc = get_error_description(status_code)
                            print(f"{Fore.RED}[FAILED] {guild_name} - {error_desc}: {error_msg}")
                            failed_count += 1
                            break
                
                progress_bar(i + 1, len(guilds))
            
            print("\n")
    
    # groups
    if choice in ['1', '3']:
        groups = get_dms(token)
        print(f"\n{Fore.GREEN}[Found {len(groups)} groups]")
        
        if groups:
            print(f"\n{Fore.YELLOW}[Leaving groups...]\n")
            
            for i, group in enumerate(groups):
                channel_id = group['id']
                group_name = group.get('name', 'Unnamed Group')
                
                if channel_id in keep_list:
                    print(f"{Fore.CYAN}[KEPT] {group_name} (ID: {channel_id})")
                    kept_count += 1
                else:
                    success, status_code, error_msg = leave_group(token, channel_id)
                    
                    if success:
                        left_count += 1
                        print(f"{Fore.GREEN}[LEFT] {group_name}")
                        smart_delay(0.3, 0.2)  
                    else:
                        error_desc = get_error_description(status_code)
                        print(f"{Fore.RED}[FAILED] {group_name} - {error_desc}: {error_msg}")
                        failed_count += 1
                
                progress_bar(i + 1, len(groups))
            
            print("\n")
    
    print(f"\n{Fore.GREEN}╔═══════════════════════════════════════╗")
    print(f"{Fore.GREEN}║          OPERATION COMPLETE!          ║")
    print(f"{Fore.GREEN}╠═══════════════════════════════════════╣")
    print(f"{Fore.GREEN}║  Left:   {left_count:<2}                           ║")
    print(f"{Fore.GREEN}║  Kept:   {kept_count:<2}                           ║")
    print(f"{Fore.GREEN}║  Owned:  {owned_count:<2} (skipped)                ║")
    print(f"{Fore.GREEN}║  Failed: {failed_count:<2}                           ║")
    print(f"{Fore.GREEN}╚═══════════════════════════════════════╝")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[Cancelled by user]")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] {str(e)}")
        sys.exit(1)
