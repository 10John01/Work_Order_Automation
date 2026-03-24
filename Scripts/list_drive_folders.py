from authenticate_google import authenticate

def list_drive_folders():
    """Lists folders in Google Drive using Service Account authentication."""
    auth_result = authenticate()
    if not auth_result or len(auth_result) < 2:
        print("❌ ERROR: Google Drive authentication failed!")
        return

    drive_service = auth_result[0]  # Ensure authentication returns the correct Drive API object

    try:
        results = drive_service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name, parents)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        folders = results.get("files", [])
        if not folders:
            print("❌ No folders found in Google Drive!")
        else:
            print("✅ Google Drive Folders:")
            for folder in folders:
                print(f"📂 {folder['name']} - ID: {folder['id']} - Parent: {folder.get('parents', 'None')}")

    except Exception as e:
        print(f"❌ ERROR: Google Drive API call failed: {e}")

if __name__ == "__main__":
    list_drive_folders()
