import flet as ft
import requests
import os
import shutil

# To build for android, replace this URL with your production backend URL
BACKEND_URL = "http://127.0.0.1:8000/generate-subtitles/"

def main(page: ft.Page):
    page.title = "Video Subtitle Generator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    selected_file_path = ft.Text(value="No file selected", color="red")
    language_input = ft.TextField(label="Language Code (Optional, e.g., en, es)", width=300)
    status_text = ft.Text(value="", color="blue")
    progress_ring = ft.ProgressRing(visible=False)

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    selected_file = None

    srt_result = ""

    def on_file_selected(e):
        nonlocal selected_file
        if e.files and len(e.files) > 0:
            selected_file = e.files[0]
            selected_file_path.value = selected_file.name
            selected_file_path.color = "green"
        else:
            selected_file = None
            selected_file_path.value = "No file selected"
            selected_file_path.color = "red"
        page.update()

    def on_upload_result(e: ft.FilePickerUploadEvent):
        if e.progress == 1.0:
            status_text.value = "Upload complete. Processing on server..."
            page.update()
            
            # For this to work smoothly without OOMing the device, we upload using file_picker.upload.
            # To actually get the subtitles back, we must make sure our backend knows which file to process, 
            # and we need an endpoint to download it. 
            # BUT because we just want the simple 1-endpoint behavior:
            # For demonstration, we simulate fetching the file path locally if it exists, or just explain.
            pass

    file_picker.on_result = on_file_selected
    file_picker.on_upload = on_upload_result

    def generate_subtitles(e):
        if not selected_file:
            status_text.value = "Please select a video file first!"
            status_text.color = "red"
            page.update()
            return

        status_text.value = "Uploading and processing... This may take a while."
        status_text.color = "blue"
        progress_ring.visible = True
        page.update()

        try:
            # We use selected_file.path because we are running on desktop/device where path is accessible
            # Note: For strict Android 11+ scoped storage, reading file.path might fail, and we should use file_picker.upload().
            # For this simple port, let's read the file using standard open, since Flet `with_data=True` crashes on large files.
            # When building for Android, further permissions/handling might be needed for Scoped Storage.
            with open(selected_file.path, "rb") as f:
                files = {"file": (selected_file.name, f)}
                data = {}
                if language_input.value:
                    data["language"] = language_input.value

                response = requests.post(BACKEND_URL, files=files, data=data)

            if response.status_code == 200:
                nonlocal srt_result
                srt_result = response.text
                status_text.value = "Success! Subtitles Generated."
                status_text.color = "green"
                save_button.visible = True
            else:
                status_text.value = f"Error: {response.text}"
                status_text.color = "red"
        except Exception as ex:
            status_text.value = f"Failed to connect or process: {ex}"
            status_text.color = "red"

        progress_ring.visible = False
        page.update()

    def on_save_result(e):
        if e.path and srt_result:
            with open(e.path, "w", encoding="utf-8") as f:
                f.write(srt_result)
            status_text.value = f"Subtitles saved to {e.path}"
            status_text.color = "green"
            page.update()

    save_file_picker = ft.FilePicker(on_result=on_save_result)
    page.overlay.append(save_file_picker)

    def save_subtitles(e):
        default_name = f"{os.path.splitext(selected_file.name)[0]}_subtitles.srt" if selected_file else "subtitles.srt"
        save_file_picker.save_file(
            file_name=default_name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["srt"]
        )

    select_button = ft.ElevatedButton(
        "Select Video File",
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    generate_button = ft.ElevatedButton(
        "Generate Subtitles",
        icon=ft.icons.SUBTITLES,
        on_click=generate_subtitles
    )

    save_button = ft.ElevatedButton(
        "Save Subtitles",
        icon=ft.icons.SAVE,
        on_click=save_subtitles,
        visible=False
    )

    page.add(
        ft.Icon(ft.icons.VIDEO_FILE, size=80),
        ft.Text("Subtitle Generator", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        select_button,
        selected_file_path,
        language_input,
        generate_button,
        progress_ring,
        status_text,
        save_button
    )

ft.app(target=main)
