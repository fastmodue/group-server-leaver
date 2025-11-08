#made by fastmodue :D

import requests
import time
import sys
import random

def print_banner():
    banner = """
\033[91m
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║            DISCORD SERVER/GROUP LEAVER                ║
    ║                  AGENT SOLUTION                       ║
    ║                                                       ║
    ╔═══════════════════════════════════════════════════════╗
\033[0m
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
        print("\033[91m[ERROR] Invalid token! Please check your token and try again.\033[0m")
        sys.exit(1)
    else:
        print(f"\033[91m[ERROR] Failed to fetch servers: {response.status_code}\033[0m")
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
        print(f"\033[91m[ERROR] Failed to fetch DMs: {response.status_code}\033[0m")
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
    print(f'\r\033[92m[Progress] {bar} {current}/{total}\033[0m', end='', flush=True)

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
    print(f"\n\033[93m[RATE LIMITED] Waiting {retry_after} seconds...\033[0m")
    for remaining in range(retry_after, 0, -1):
        print(f"\r\033[93m[Resuming in {remaining}s...]\033[0m", end='', flush=True)
        time.sleep(1)
    print("\r\033[92m[Resuming operations...]\033[0m")

def main():
    print_banner()
    
    print("\033[93mWhat would you like to leave?\033[0m")
    print("[1] Discord Groups (DMs)")
    print("[2] Discord Servers")
    print("[3] Both\n")
    
    choice = input("\033[96mEnter your choice (1/2/3): \033[0m").strip()
    
    if choice not in ['1', '2', '3']:
        print("\033[91m[ERROR] Invalid choice!\033[0m")
        return
    
    token = input("\n\033[96mEnter your Discord token: \033[0m").strip()
    
    if not token:
        print("\033[91m[ERROR] Token cannot be empty!\033[0m")
        return
    
    keep_ids = input("\n\033[96m[OPTIONAL] Any server/group IDs to KEEP?\n(Format: id1,id2,id3 or press Enter to leave ALL): \033[0m").strip()
    keep_list = [id.strip() for id in keep_ids.split(',') if id.strip()] if keep_ids else []
    
    print("\n\033[93m[Scanning...]\033[0m")
    
    user_id = get_user_id(token)
    if not user_id:
        print("\033[91m[ERROR] Could not fetch user information!\033[0m")
        return
    
    
    guilds = []
    groups = []
    
    if choice in ['2', '3']:
        guilds = get_guilds(token)
    if choice in ['1', '3']:
        groups = get_dms(token)
   
    if keep_list:
        print(f"\n\033[96m╔═══════════════════════════════════════╗\033[0m")
        print(f"\033[96m║        SERVERS/GROUPS TO KEEP:        ║\033[0m")
        print(f"\033[96m╚═══════════════════════════════════════╝\033[0m")
        
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
                print(f"\033[92m  {item}\033[0m")
        
        if not_found:
            print(f"\n\033[91m  ⚠️  Warning: These IDs were not found:\033[0m")
            for nf_id in not_found:
                print(f"\033[91m     {nf_id}\033[0m")
        
        print(f"\n\033[93mTotal keeping: {len(found_keeps)} | Not found: {len(not_found)}\033[0m")
        
        confirm = input("\n\033[96mProceed with these settings? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[91m[Cancelled by user]\033[0m")
            return
        print()
    else:
        print("\n\033[91m⚠️  WARNING: You will leave ALL servers/groups!\033[0m")
        confirm = input("\033[96mAre you sure? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[91m[Cancelled by user]\033[0m")
            return
        print()
    
    left_count = 0
    kept_count = 0
    owned_count = 0
    failed_count = 0
    
    # servers
    if choice in ['2', '3']:
        print(f"\033[92m[Found {len(guilds)} servers]\033[0m")
        
        if guilds:
            print("\n\033[93m[Leaving servers...]\033[0m")
            print("\033[93m[Using 0.5-0.8s delay between requests]\033[0m\n")
            
            for i, guild in enumerate(guilds):
                guild_id = guild['id']
                guild_name = guild['name']
                owner_id = guild.get('owner_id')
                
                # check for owner
                if owner_id == user_id:
                    print(f"\033[91m[SKIPPED] Can't leave owned server: {guild_name}\033[0m")
                    owned_count += 1
                elif guild_id in keep_list:
                    print(f"\033[96m[KEPT] {guild_name} (ID: {guild_id})\033[0m")
                    kept_count += 1
                else:
                    max_retries = 3
                    retry_count = 0
                    
                    while retry_count < max_retries:
                        success, status_code, error_msg, is_owner = leave_guild(token, guild_id)
                        
                        if success:
                            left_count += 1
                            print(f"\033[92m[LEFT] {guild_name}\033[0m")
                            smart_delay(0.5, 0.3)  
                            break
                        elif is_owner:
                            print(f"\033[91m[SKIPPED] Can't leave owned server: {guild_name}\033[0m")
                            owned_count += 1
                            break
                        elif status_code == 429:
                            # rate limit
                            retry_count += 1
                            if retry_count < max_retries:
                                print(f"\033[93m[RATE LIMITED] {guild_name} - Retry {retry_count}/{max_retries}\033[0m")
                                handle_rate_limit(30)
                            else:
                                print(f"\033[91m[FAILED] {guild_name} - Too many rate limits\033[0m")
                                failed_count += 1
                        else:
                            # some other error
                            error_desc = get_error_description(status_code)
                            print(f"\033[91m[FAILED] {guild_name} - {error_desc}: {error_msg}\033[0m")
                            failed_count += 1
                            break
                
                progress_bar(i + 1, len(guilds))
            
            print("\n")
    
    # groups
    if choice in ['1', '3']:
        groups = get_dms(token)
        print(f"\n\033[92m[Found {len(groups)} groups]\033[0m")
        
        if groups:
            print("\n\033[93m[Leaving groups...]\033[0m\n")
            
            for i, group in enumerate(groups):
                channel_id = group['id']
                group_name = group.get('name', 'Unnamed Group')
                
                if channel_id in keep_list:
                    print(f"\033[96m[KEPT] {group_name} (ID: {channel_id})\033[0m")
                    kept_count += 1
                else:
                    success, status_code, error_msg = leave_group(token, channel_id)
                    
                    if success:
                        left_count += 1
                        print(f"\033[92m[LEFT] {group_name}\033[0m")
                        smart_delay(0.3, 0.2)  
                    else:
                        error_desc = get_error_description(status_code)
                        print(f"\033[91m[FAILED] {group_name} - {error_desc}: {error_msg}\033[0m")
                        failed_count += 1
                
                progress_bar(i + 1, len(groups))
            
            print("\n")
    
    print(f"\n\033[92m╔═══════════════════════════════════════╗\033[0m")
    print(f"\033[92m║          OPERATION COMPLETE!          ║\033[0m")
    print(f"\033[92m╠═══════════════════════════════════════╣\033[0m")
    print(f"\033[92m║  Left:   {left_count:<2}                           ║\033[0m")
    print(f"\033[92m║  Kept:   {kept_count:<2}                           ║\033[0m")
    print(f"\033[92m║  Owned:  {owned_count:<2} (skipped)                ║\033[0m")
    print(f"\033[92m║  Failed: {failed_count:<2}                           ║\033[0m")
    print(f"\033[92m╚═══════════════════════════════════════╝\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m[Cancelled by user]\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[ERROR] {str(e)}\033[0m")
        sys.exit(1)