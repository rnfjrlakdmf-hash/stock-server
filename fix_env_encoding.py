import os

env_path = 'backend/.env'

if os.path.exists(env_path):
    try:
        with open(env_path, 'rb') as f:
            content = f.read()
        
        # Check for UTF-16 LE BOM (FF FE)
        if content.startswith(b'\xff\xfe'):
            print("Detected UTF-16 LE BOM. Converting to UTF-8...")
            decoded = content.decode('utf-16')
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(decoded)
            print("Converted successfully.")
        elif content.startswith(b'\xfe\xff'):
            print("Detected UTF-16 BE BOM. Converting to UTF-8...")
            decoded = content.decode('utf-16-be')
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(decoded)
            print("Converted successfully.")
        else:
            print("No UTF-16 BOM detected. Trying to decode as ISO-8859-1 and save as UTF-8 just in case, or skipping if already UTF-8 valid.")
            try:
                content.decode('utf-8')
                print("File is already valid UTF-8.")
            except UnicodeDecodeError:
                print("File is not UTF-8. Converting from cp949/euc-kr (common in KR Windows)...")
                try:
                    decoded = content.decode('cp949')
                    with open(env_path, 'w', encoding='utf-8') as f:
                        f.write(decoded)
                    print("Converted from CP949 to UTF-8.")
                except:
                    print("Could not determine encoding.")

    except Exception as e:
        print(f"Error: {e}")
else:
    print(".env not found")
